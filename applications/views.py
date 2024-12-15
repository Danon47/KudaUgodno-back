from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from applications.models import Application, Guest
from applications.serializers import ApplicationSerializer, GuestSerializer


class GuestListCreateView(generics.ListCreateAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех гостей",
        operation_summary="Список гостей",
        tags=["5.1. Гости в заявке"],
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

class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    @swagger_auto_schema(
        operation_description="Получение информации о госте через идентификатор",
        operation_summary="Информация о госте",
        tags=["5.1. Гости в заявке"],
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
        responses={
            200: openapi.Response(
                description="Успешное удаление гостя",
                schema=GuestSerializer()
            ),
            400: "Ошибка запроса"
        })
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ApplicationListCreateView(generics.ListCreateAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех заявок",
        operation_summary="Список заявок",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка заявок",
                schema=ApplicationSerializer(many=True)
            ),
            400: "Ошибка запроса"
        })
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание новой заявки",
        operation_summary="Добавление заявки",
        request_body=ApplicationSerializer,
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное создание заявки",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


    @swagger_auto_schema(
        operation_description="Получение информации о заявке через идентификатор",
        operation_summary="Информация о заявке",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о заявке",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Изменение информации всех полей заявки через идентификатор",
        operation_summary="Полное изменение заявки",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное изменение всей заявки",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Частичное изменение информации о заявке через идентификатор",
        operation_summary="Частичное изменение информации озаявке",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное изменение части информации о заявке",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Удаление заявки через идентификатор",
        operation_summary="Удаление заявки",
        tags=["5. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное удаление заявки",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)