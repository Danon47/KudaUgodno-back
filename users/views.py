import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer
from users.tasks import clear_user_password, send_message


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD-операций над пользователями.

    Данный класс объединяет следующие действия:
      - list: получение списка пользователей;
      - retrieve: получение данных отдельного пользователя;
      - create: создание нового пользователя (с генерацией пароля и отправкой email);
      - update: полное обновление данных пользователя;
      - partial_update: частичное обновление данных пользователя;
      - destroy: удаление пользователя.

    При создании пользователя генерируется случайное 4-значное число, которое устанавливается в качестве пароля.
    Также отправляется сообщение на email пользователя с указанием кода, и запускается задача для очистки пароля через 5 минут.
    """
    queryset = User.objects.all().order_by("-pk")
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Список пользователей",
        operation_description="Получение списка всех пользователей."
    )
    def list(self, request, *args, **kwargs):
        """
        Получение списка пользователей.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получение пользователя",
        operation_description="Получение данных пользователя по его идентификатору."
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Получение данных одного пользователя.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создание пользователя",
        operation_description="Создание нового пользователя. При этом генерируется 4-значный код, который устанавливается как пароль, и отправляется на email.",
        request_body=UserSerializer
    )
    def create(self, request, *args, **kwargs):
        """
        Создание нового пользователя с дополнительной логикой:
          - генерация случайного 4-значного кода;
          - установка кода как пароля (с хэшированием через set_password);
          - отправка email с кодом подтверждения;
          - планирование задачи очистки пароля через 5 минут.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерация случайного 4-значного кода
        random_number = random.randint(1000, 9999)
        user.set_password(str(random_number))
        user.save(update_fields=["password"])

        # Отправка email с кодом подтверждения
        send_message.delay(
            "Код для подтверждения входа",
            f"Код для входа в сервис 'Куда Угодно'. {random_number}. Никому не сообщайте его! Если вы не запрашивали код, игнорируйте сообщение.",
            EMAIL_HOST_USER,
            [user.email]
        )

        # Планирование задачи очистки пароля через 5 минут (300 секунд)
        clear_user_password.apply_async((user.id,), countdown=300)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_summary="Полное обновление пользователя",
        operation_description="Полное обновление данных пользователя по его идентификатору.",
        request_body=UserSerializer
    )
    def update(self, request, *args, **kwargs):
        """
        Полное обновление данных пользователя.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление пользователя",
        operation_description="Частичное обновление данных пользователя по его идентификатору.",
        request_body=UserSerializer
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Частичное обновление данных пользователя.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление пользователя",
        operation_description="Удаление пользователя по его идентификатору."
    )
    def destroy(self, request, *args, **kwargs):
        """
        Удаление пользователя.
        """
        return super().destroy(request, *args, **kwargs)
