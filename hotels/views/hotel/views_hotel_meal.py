# from drf_spectacular.types import OpenApiTypes
# from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
# from rest_framework import viewsets
# from hotels.models.hotel.models_hotel_meal import MealPlan
# from hotels.serializers.hotel.serializers_hotel_meal import MealPlanSerializer
#
#
# @extend_schema_view(
#     list=extend_schema(
#         summary="Список типов питания в отеле",
#         description="Получение списка всех типов питания в отеле",
#         parameters=[
#             OpenApiParameter(
#                 "hotel_id",
#                 OpenApiTypes.INT,
#                 OpenApiParameter.PATH,
#                 description="ID отеля",
#             ),
#         ],
#         responses={
#             200: MealPlanSerializer(many=True),
#             400: OpenApiResponse(description="Ошибка запроса"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
#     create=extend_schema(
#         summary="Добавление типа питания в отеле",
#         description="Создание нового типа питания в отеле",
#         request=MealPlanSerializer,
#         responses={
#             201: MealPlanSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
#     retrieve=extend_schema(
#         summary="Детали типа питания в отеле",
#         description="Получение полной информации типа питания в отеле",
#         responses={
#             200: MealPlanSerializer,
#             404: OpenApiResponse(description="Тип питания в отеле не найден"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
#     update=extend_schema(
#         summary="Полное обновление типа питания в отеле",
#         description="Обновление всех полей типа питания в отеле",
#         request=MealPlanSerializer,
#         responses={
#             200: MealPlanSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Тип питания в отеле не найден"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
#     partial_update=extend_schema(
#         summary="Частичное обновление типа питания в отеле",
#         description="Обновление отдельных полей типа питания в отеле",
#         request=MealPlanSerializer,
#         responses={
#             200: MealPlanSerializer,
#             400: OpenApiResponse(description="Ошибка валидации"),
#             404: OpenApiResponse(description="Тип питания в отеле не найден"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
#     destroy=extend_schema(
#         summary="Удаление типа питания в отеле",
#         description="Полное удаление типа питания в отеле",
#         responses={
#             204: OpenApiResponse(description="Тип питания в отеле удален"),
#             404: OpenApiResponse(description="Тип питания в отеле не найден"),
#         },
#         tags=["3.1.2 Питание в отеле"],
#     ),
# )
# class MealPlanViewSet(viewsets.ModelViewSet):
#     serializer_class = MealPlanSerializer
#     pagination_class = None
#
#     def get_queryset(self):
#         hotel_id = self.kwargs.get('hotel_id')
#         return MealPlan.objects.filter(hotel_id=hotel_id)
#
#     def perform_create(self, serializer):
#         hotel_id = self.kwargs.get('hotel_id')
#         serializer.save(hotel_id=hotel_id)
