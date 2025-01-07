from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from applications.models.models_application import Application
from applications.serializers.serializers_applications import ApplicationCreateSerializer, ApplicationSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):

    queryset = Application.objects.all()

    @swagger_auto_schema(
        operation_description="Получение списка всех заявок",
        operation_summary="Список заявок",
        tags=["5. Заявки"],
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество Заявок для возврата на страницу",
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Начальный индекс, из которого возвращаются результаты",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка заявок",
                schema=ApplicationSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание новой заявки",
        operation_summary="Добавление заявки",
        request_body=ApplicationCreateSerializer,
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное создание заявки", schema=ApplicationCreateSerializer()
            ),
            400: "Ошибка запроса",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ApplicationCreateSerializer
        return ApplicationSerializer


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer

    @swagger_auto_schema(
        operation_description="Получение информации о заявке через идентификатор",
        operation_summary="Информация о заявке",
        tags=["5. Заявки"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Заявки",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о заявке",
                schema=ApplicationCreateSerializer(),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменение информации всех полей заявки через идентификатор",
        operation_summary="Полное изменение заявки",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное изменение всей заявки",
                schema=ApplicationCreateSerializer(),
            ),
            400: "Ошибка запроса",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частичное изменение информации о заявке через идентификатор",
        operation_summary="Частичное изменение информации озаявке",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное изменение части информации о заявке",
                schema=ApplicationCreateSerializer(),
            ),
            400: "Ошибка запроса",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление заявки через идентификатор",
        operation_summary="Удаление заявки",
        tags=["5. Заявки"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Заявки",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное удаление заявки", schema=ApplicationCreateSerializer()
            ),
            400: "Ошибка запроса",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
