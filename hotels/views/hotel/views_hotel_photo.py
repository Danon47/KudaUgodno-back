from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets
from all_fixture.fixture_views import hotel_id, hotel_id_photo, tags_hotel_photo_settings
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.serializers.hotel.serializers_hotel_photo import HotelPhotoSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список типов фотографий отеля",
        description="Получение списка всех фотографий отеля",
        parameters=[hotel_id],
        responses={
            200: HotelPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_hotel_photo_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографий отеля",
        description="Создание новых фотографий отеля",
        parameters=[hotel_id],
        request={
            "multipart/form-data": HotelPhotoSerializer,  # Указываем формат данных
        },
        responses={
            201: HotelPhotoSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[tags_hotel_photo_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографий отеля",
        description="Полное удаление фотографий отеля",
        parameters=[hotel_id, hotel_id_photo],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[tags_hotel_photo_settings["name"]],
    ),
)
class HotelPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = HotelPhotoSerializer
    pagination_class = None
    http_method_names = ["get", "post", "delete", "head", "options", "trace"]  # исключаем обновления

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        return HotelPhoto.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        serializer.save(hotel_id=self.kwargs["hotel_id"])
