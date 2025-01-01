from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from applications.models.models_guest import Guest
from applications.serializers.serializers_guests import GuestSerializer


class GuestListCreateView(generics.ListCreateAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех гостей",
        operation_summary="Список гостей",
        tags=["5.1. Гости в заявке"],
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество Гостей для возврата на страницу",
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Начальный индекс, из которого возвращаются результаты",
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка гостей",
                schema=GuestSerializer(many=True)
            ),
            400: "Ошибка запроса"
        })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Создание нового гостя",
        operation_summary="Добавление гостя",
        request_body=GuestSerializer,
        tags=["5.1. Гости в заявке"],
        responses={
            200: openapi.Response(
                description="Успешное создание гостя",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)



class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @swagger_auto_schema(
        operation_description="Получение информации о госте через идентификатор",
        operation_summary="Информация о госте",
        tags=["5.1. Гости в заявке"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Гостя",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о госте",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Изменение всей информации о госте через идентификатор",
        operation_summary="Полное изменение гостя",
        tags=["5.1. Гости в заявке"],
        responses={
            200: openapi.Response(
                description="Успешное изменение всей заявки",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Частичное изменение информации о госте через идентификатор",
        operation_summary="Частичное изменение информации о госте",
        tags=["5.1. Гости в заявке"],
        responses={
            200: openapi.Response(
                description="Успешное изменение части информации о госте",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Удаление гостя через идентификатор",
        operation_summary="Удаление гостя",
        tags=["5.1. Гости в заявке"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Гостя",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное удаление гостя",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


