# from rest_framework.generics import (
#     ListCreateAPIView,
#     RetrieveUpdateDestroyAPIView,
# )
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema
#
#
# from flights.models import Flight
# from flights.serializers import FlightSerializer

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import viewsets

from flights.models import Flight
from flights.serializers import FlightSerializer

parameters_application = [
    OpenApiParameter(
        location=OpenApiParameter.PATH,
        name="id",
        type=int,
        description="Уникальное целочисленное значение, идентифицирующее данный Рейс",
        required=True,
    ),
]

tags_flight = ["4. Рейсы"]


@extend_schema_view(
    list=extend_schema(
        summary="Список рейсов",
        description="Получение списка всех рейсов",
        tags=tags_flight,
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество рейсов для возврата на страницу",
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
            200: FlightSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление рейса",
        description="Создание новой рейса",
        request=FlightSerializer,
        tags=tags_flight,
        responses={
            201: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о рейсе",
        description="Получение информации о рейсе через идентификатор",
        tags=tags_flight,
        parameters=parameters_application,
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление рейса",
        description="Обновление всех полей рейса",
        request=FlightSerializer,
        tags=tags_flight,
        parameters=parameters_application,
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление рейса",
        description="Обновление отдельных полей рейса",
        request=FlightSerializer,
        tags=tags_flight,
        parameters=parameters_application,
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление рейса",
        description="Полное удаление рейса",
        tags=tags_flight,
        parameters=parameters_application,
        responses={
            204: OpenApiResponse(description="Рейса удален"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer



# class FlightListCreateView(ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#
#     @swagger_auto_schema(
#         operation_description="Получение списка рейсов",
#         operation_summary="Список рейсов",
#         tags=["4. Рейс"],
#         manual_parameters=[
#             openapi.Parameter(
#                 name="limit",
#                 in_=openapi.IN_QUERY,
#                 type=openapi.TYPE_INTEGER,
#                 description="Количество рейсов для возврата на страницу",
#             ),
#             openapi.Parameter(
#                 name="offset",
#                 in_=openapi.IN_QUERY,
#                 type=openapi.TYPE_INTEGER,
#                 description="Начальный индекс, из которого возвращаются результаты",
#             ),
#         ],
#         responses={
#             200: openapi.Response(
#                 description="Успешное получение списка рейсов",
#                 schema=FlightSerializer(many=True),
#             ),
#             400: "Ошибка запроса",
#         },
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     @swagger_auto_schema(
#         operation_description="Создание рейса",
#         operation_summary="Добавление рейса",
#         request_body=FlightSerializer,
#         tags=["4. Рейс"],
#         responses={
#             201: openapi.Response(
#                 description="Успешное создание номера", schema=FlightSerializer()
#             ),
#             400: "Ошибка валидации",
#         },
#     )
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)
#
#
# class FlightDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#
#     @swagger_auto_schema(
#         operation_summary="Получение детальной информации о рейсе",
#         operation_description="Возвращает полную информацию о рейсе по его идентификатору",
#         tags=["4. Рейс"],
#         manual_parameters=[
#             openapi.Parameter(
#                 name="id",
#                 in_=openapi.IN_PATH,
#                 type=openapi.TYPE_INTEGER,
#                 description="Уникальный идентификатор рейса в базе данных",
#                 required=True,
#             )
#         ],
#         responses={
#             200: openapi.Response(
#                 description="Успешное получение информации о рейсе",
#                 schema=FlightSerializer(),
#             ),
#             404: "Рейс не найден",
#         },
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)
#
#     @swagger_auto_schema(
#         operation_summary="Полное обновление информации о рейсе",
#         operation_description="Обновляет все поля рейса",
#         tags=["4. Рейс"],
#         request_body=FlightSerializer,
#         manual_parameters=[
#             openapi.Parameter(
#                 name="id",
#                 in_=openapi.IN_PATH,
#                 type=openapi.TYPE_INTEGER,
#                 description="Уникальный идентификатор номера в базе данных",
#                 required=True,
#             )
#         ],
#         responses={
#             200: openapi.Response(
#                 description="Рейс успешно обновлен", schema=FlightSerializer()
#             ),
#             400: "Ошибка валидации",
#             404: "Рейс не найден",
#         },
#     )
#     def put(self, request, *args, **kwargs):
#         return super().put(request, *args, **kwargs)
#
#     @swagger_auto_schema(
#         operation_summary="Частичное обновление информации о рейсе",
#         operation_description="Обновляет указанные поля рейса",
#         tags=["4. Рейс"],
#         request_body=FlightSerializer,
#         manual_parameters=[
#             openapi.Parameter(
#                 name="id",
#                 in_=openapi.IN_PATH,
#                 type=openapi.TYPE_INTEGER,
#                 description="Уникальный идентификатор номера в базе данных",
#                 required=True,
#             )
#         ],
#         responses={
#             200: openapi.Response(
#                 description="Рейс успешно обновлен", schema=FlightSerializer()
#             ),
#             400: "Ошибка валидации",
#             404: "Рейс не найден",
#         },
#     )
#     def patch(self, request, *args, **kwargs):
#         return super().patch(request, *args, **kwargs)
#
#     @swagger_auto_schema(
#         operation_summary="Удаление рейса",
#         operation_description="Полное удаление рейса по его идентификатору",
#         tags=["4. Рейс"],
#         manual_parameters=[
#             openapi.Parameter(
#                 name="id",
#                 in_=openapi.IN_PATH,
#                 type=openapi.TYPE_INTEGER,
#                 description="Уникальный идентификатор рейса",
#                 required=True,
#             )
#         ],
#         responses={204: "Рейс успешно удален", 404: "Рейс не найден"},
#     )
#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)
