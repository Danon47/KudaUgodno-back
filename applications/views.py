from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from applications.models import Application
from applications.serializers import ApplicationSerializer


class ApplicationListCreateView(generics.ListCreateAPIView):

    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех заявок",
        operation_summary="Список заявок",
        tags=["7. Заявки"],
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
        operation_summary="Добавление завявки",
        request_body=ApplicationSerializer,
        tags=["7. Заявки"],
        responses={
            200: openapi.Response(
                description="Успешное создание заявки",
                schema=ApplicationSerializer()
            ),
            400: "Ошибка запроса"
        })
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)