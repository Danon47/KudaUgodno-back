from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets
from all_fixture.fixture_views import offset, limit, id_hotel, tags_hotel_settings
from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.serializers_hotel import (
    HotelBaseSerializer,
    HotelDetailSerializer,
    HotelListSerializer,
)


class CreatedByUserFilterMixin:
    """
    Миксин для фильтрации queryset по полю created_by.
    Если пользователь принадлежит к группе 'tur' (например, туроператоры),
    то возвращаются только записи, где created_by совпадает с текущим пользователем.
    Если пользователь принадлежит к группе 'user' или является администратором,
    возвращаются все записи.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Если пользователь администратор или суперпользователь, возвращаем все данные
        if user.is_staff or user.is_superuser:
            return qs
        # Если пользователь принадлежит к группе "user", возвращаем все данные
        if user.groups.filter(name="user").exists():
            return qs
        # Если пользователь принадлежит к группе "tur", фильтруем по созданным данным
        if user.groups.filter(name="tur").exists():
            return qs.filter(created_by=user)
        # По умолчанию можно вернуть либо пустой queryset, либо фильтрацию по created_by
        return qs.filter(created_by=user)


@extend_schema_view(
    list=extend_schema(
        summary="Список отелей",
        description="Получение списка всех отелей с пагинацией",
        parameters=[limit, offset],
        responses={
            200: HotelDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_hotel_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление отеля",
        description="Создание нового отеля",
        request=HotelBaseSerializer,
        responses={
            201: HotelBaseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[tags_hotel_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали отеля",
        description="Получение полной информации об отеле",
        parameters=[id_hotel],
        responses={
            200: HotelDetailSerializer,
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[tags_hotel_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление отеля",
        description="Обновление всех полей отеля",
        parameters=[id_hotel],
        request=HotelDetailSerializer,
        responses={
            200: HotelDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[tags_hotel_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление отеля",
        description="Полное удаление отеля",
        parameters=[id_hotel],
        responses={
            204: OpenApiResponse(description="Отель удален"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[tags_hotel_settings["name"]],
    ),
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']  # Исключаем 'patch'

    def get_serializer_class(self):
        if self.action == "create":
            return HotelBaseSerializer
        elif self.action in ["list", "retrieve"]:
            return HotelListSerializer
        else:
            return HotelDetailSerializer

    # def perform_create(self, serializer):
    #     # При создании записи устанавливаем поле created_by равным текущему пользователю
    #     serializer.save(created_by=self.request.user)
