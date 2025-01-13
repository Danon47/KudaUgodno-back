import random

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer
from users.tasks import clear_user_password, send_message


class UserListCreateView(generics.ListCreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Список пользователей",
        operation_description="Получения списка всех пользователей",
        tags=["1. Пользователи"],
        manual_parameters=[
            openapi.Parameter(
                   name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество Пользователей для возврата на страницу",
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
            description="Успешное получение списка всех пользователей",
            schema=UserSerializer(many=True)
        ),
        400: "Ошибка запроса"
    }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_summary="Добавление пользователя",
        operation_description="Создание нового пользователя",
        request_body=UserSerializer,
        tags=["1. Пользователи"],
        responses={
            200: openapi.Response(
                description="Успешное создание пользователя",
                schema=UserSerializer(),
            ),
            400: "Ошибка запроса"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save()
        random_number = random.randint(1000, 9999)
        user.set_password(str(random_number))
        user.save(update_fields=["password"])
        send_message.delay(
            "Код для подтверждения входа",
            f"Код для входа в сервис 'Куда Угодно'. {random_number}. Никому не сообщайте его! Если вы не запрашивали код, игнорируйте сообщение.",
            EMAIL_HOST_USER,
            [user.email]
        )
        clear_user_password.apply_async((user.id,), countdown=300)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Информация о пользователе",
        operation_description="Получение информации о пользователе через идентификатор",
        tags = ["1. Пользователи"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Пользователя",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о пользователе",
                schema=UserSerializer()
            ),
            400: "Ошибка запроса"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное изменение пользователя",
        operation_description="Изменение информации всех полей пользователя через идентификатор",
        tags=["1. Пользователи"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Пользователя",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное изменение всего пользователя",
                schema=UserSerializer()
            ),
            400: "Ошибка запроса"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное изменение пользователя",
        operation_description="Частичное изменение данных пользователя по идентификатору",
        tags=["1. Пользователи"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Заявки",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное частичное изменение данных пользователя",
                schema=UserSerializer()
            ),
            400: "Ошибка запроса"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление пользователя",
        operation_description="Удаление данных пользователя по идентификатору",
        tags=["1. Пользователи"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор Заявки",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное удаление данных пользователя",
            ),
            400: "Ошибка запроса"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(self, request, *args, **kwargs)
