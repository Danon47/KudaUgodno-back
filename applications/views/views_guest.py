from drf_spectacular.utils import extend_schema_view, OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework import viewsets

from applications.models.models_guest import Guest
from applications.serializers.serializers_guests import GuestSerializer, GuestDetailSerializer

parameters_guest = [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="id",
                type=int,
                description="Уникальное целочисленное значение, идентифицирующее данную Гостя",
                required=True,

            ),
        ]

tags_guest = ["5.1 Заявки"]

@extend_schema_view(
    list=extend_schema(
        summary="Список гостей",
        description="Получение списка всех гостей",
        tags=tags_guest,
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество Гостей для возврата на страницу",
                required=False,
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Начальный индекс для пагинации",
                required=False,
            ),
        ],
        responses={
            200: GuestSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление Гостя",
        description="Создание нового Гостя",
        request=GuestDetailSerializer,
        tags=tags_guest,
        responses={
            201: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о Госте",
        description="Получение информации о Госте через идентификатор",
        tags=tags_guest,
        parameters=parameters_guest,
        responses={
            200: GuestSerializer,
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление Гостя",
        description="Обновление всех полей Гостя",
        request=GuestDetailSerializer,
        tags=tags_guest,
        parameters=parameters_guest,
        responses={
            200: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление Гостя",
        description="Обновление отдельных полей Гостя",
        request=GuestDetailSerializer,
        tags=tags_guest,
        parameters=parameters_guest,
        responses={
            200: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление Гостя",
        description="Полное удаление Гостя",
        tags=tags_guest,
        parameters=parameters_guest,
        responses={
            204: OpenApiResponse(description="Гость удален"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
)
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GuestDetailSerializer
        return GuestSerializer

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)