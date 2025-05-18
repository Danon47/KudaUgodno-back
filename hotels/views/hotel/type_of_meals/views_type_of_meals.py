from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import hotel_id, type_of_meal_id, type_of_meal_settings
from hotels.models.hotel.type_of_meals.models_type_of_meals import TypeOfMeal
from hotels.serializers.hotel.type_of_meals.serializers_type_of_meals import TypeOfMealSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список типов питания в определённом отеле",
        description="Получение списка всех типов питания в определённом отеле",
        parameters=[hotel_id],
        responses={
            200: TypeOfMealSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление типа питания в определённый отель",
        description="Создание нового типа питания в определённом отеле",
        parameters=[hotel_id],
        request={
            "multipart/form-data": TypeOfMealSerializer,
        },
        responses={
            201: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Получение типа питания в определённом отеле",
        description="Получение типа питания в определённом отеле",
        parameters=[hotel_id, type_of_meal_id],
        responses={
            200: TypeOfMealSerializer,
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление типа питания в определённом отеле",
        description="Обновление всех полей типа питания в определённом отеле",
        request=TypeOfMealSerializer,
        parameters=[hotel_id, type_of_meal_id],
        responses={
            200: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление типа питания в определённом отеле",
        description="Полное удаление типа питания в определённом отеле",
        parameters=[hotel_id, type_of_meal_id],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
)
class TypeOfMealViewSet(viewsets.ModelViewSet):
    serializer_class = TypeOfMealSerializer
    http_method_names = ["get", "post", "delete", "put", "head", "options", "trace"]  # исключаем обновления

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        return TypeOfMeal.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        serializer.save(hotel_id=self.kwargs["hotel_id"])
