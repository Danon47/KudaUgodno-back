from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.serializers.hotel.serializers_hotel_photo import HotelPhotoSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список типов фотографий отеля",
        description="Получение списка всех фотографий отеля",
        parameters=[
            OpenApiParameter(
                name="hotel_id",
                type=int,
                location=OpenApiParameter.PATH,  # Параметр передается в URL
                description="ID отеля, у которого получаем список всех фотографий",
                required=True,
            ),
        ],
        responses={
            200: HotelPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.3 Фотографии в отеле"],
    ),
    create=extend_schema(
        summary="Добавление фотографий отеля",
        description="Создание новых фотографий отеля",
        parameters=[
            OpenApiParameter(
                name="hotel_id",
                type=int,
                location=OpenApiParameter.PATH,  # Параметр передается в URL
                description="ID отеля, к которому добавляется фотография",
                required=True,
            ),
        ],
        request={
            "multipart/form-data": HotelPhotoSerializer,  # Указываем формат данных
        },
        responses={
            201: HotelPhotoSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.3 Фотографии в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление фотографий отеля",
        description="Полное удаление фотографий отеля",
        parameters=[
            OpenApiParameter(
                name="hotel_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID отеля, у которого удаляется фотография",
                required=True,
            ),
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID фотографий отеля, которая удаляется",
                required=True,
            ),
        ],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=["3.1.3 Фотографии в отеле"],
    ),
)
class HotelPhotoViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = HotelPhotoSerializer
    pagination_class = None

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return HotelPhoto.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        serializer.save(hotel_id=self.kwargs['hotel_id'])
