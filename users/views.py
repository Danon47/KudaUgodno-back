import random

from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_field,
    extend_schema_view,
)
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from all_fixture.fixture_views import auth, entreprise, entreprise_id, limit, offset, user_id, user_settings
from all_fixture.pagination import CustomLOPagination
from config.settings import EMAIL_HOST_USER
from users.choices import RoleChoices
from users.models import User
from users.permissions import IsAdminOrOwner
from users.serializers import (
    CompanyUserSerializer,
    EmailLoginSerializer,
    LogoutSerializer,
    UserSerializer,
    VerifyCodeSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список пользователей (турист)",
        description="Получение списка всех обычных пользователей",
        tags=[user_settings["name"]],
        parameters=[limit, offset],
        responses={200: UserSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Создание пользователя",
        description="Создание нового пользователя с указанием email и пароля",
        tags=[user_settings["name"]],
        request={"multipart/form-data": UserSerializer},
        responses={201: UserSerializer},
    ),
    retrieve=extend_schema(
        summary="Детальная информация о пользователе",
        description="Получение полной информации о конкретном пользователе (туристе) по ID",
        tags=[user_settings["name"]],
        parameters=[user_id],
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
    update=extend_schema(
        summary="Обновление пользователя",
        description="Полное обновление информации о пользователе (туристе) по ID",
        tags=[user_settings["name"]],
        parameters=[user_id],
        request={"multipart/form-data": UserSerializer},
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление пользователя",
        description="Удаление обычного пользователя по ID",
        tags=[user_settings["name"]],
        parameters=[user_id],
        responses={
            204: OpenApiResponse(description="Удалено"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для обычных пользователей (туристов)."""

    serializer_class = UserSerializer
    pagination_class = CustomLOPagination
    # Админ видит всех, юзер — только себя

    # Исключаем 'patch'
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return User.objects.all().order_by("-pk")
        else:
            return User.objects.filter(pk=user.pk)
        # <- никогда не будет вызван
        # return User.objects.none()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """Получение детальной информации о пользователе по ID."""
        instance = self.get_object()
        # Проверка объекта
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema_field(serializers.ImageField())
    def get_avatar(self, obj):
        """Отображает URL аватарки, если она загружена."""
        if obj.avatar:
            return obj.avatar.url
        return None

    def update(self, request, *args, **kwargs):
        """Полное обновление информации о пользователе (туристе)."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя по ID."""
        instance = self.get_object()

        # Дополнительная логика: проверка, можно ли удалять (в будущем потребуется не удалять администраторов)
        if instance.role != RoleChoices.USER:
            return Response({"error": "Удаление запрещено"}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({"message": "Пользователь удален"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary="Список компаний (Туроператоры и Отельеры)",
        description="Получение списка всех компаний (Туроператоры и Отельеры)",
        tags=[entreprise["name"]],
        parameters=[limit, offset],
        responses={200: CompanyUserSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Создание компании",
        description="Создание нового Туроператора или Отельера",
        tags=[entreprise["name"]],
        request=CompanyUserSerializer,
        responses={201: CompanyUserSerializer},
    ),
    retrieve=extend_schema(
        summary="Детальная информация о компании",
        description="Получение детальной информации о конкретной компании по ID",
        tags=[entreprise["name"]],
        parameters=[entreprise_id],
        responses={
            200: CompanyUserSerializer,
            404: OpenApiResponse(description="Компания не найдена"),
        },
    ),
    update=extend_schema(
        summary="Обновление компании",
        description="Полное обновление информации о компании по ID",
        tags=[entreprise["name"]],
        parameters=[entreprise_id],
        request=CompanyUserSerializer,
        responses={
            200: CompanyUserSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Компания не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление компании",
        description="Полное удаление компании по ID",
        tags=[entreprise["name"]],
        parameters=[entreprise_id],
        responses={
            204: OpenApiResponse(description="Компания удалена"),
            404: OpenApiResponse(description="Компания не найдена"),
        },
    ),
)
class CompanyUserViewSet(viewsets.ModelViewSet):
    """ViewSet для Туроператоров и Отельеров."""

    queryset = User.objects.filter(role__in=[RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]).order_by("-pk")
    serializer_class = CompanyUserSerializer
    pagination_class = CustomLOPagination
    # Исключаем 'patch'
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return User.objects.filter(role__in=[RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]).order_by("-pk")
        elif user.role in [RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]:
            return User.objects.filter(pk=user.pk)
        return User.objects.none()

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        """Получение детальной информации о компании по ID."""
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Полное обновление информации о компании по ID."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление компании по ID."""
        # Получение объекта для удаления
        instance = self.get_object()
        # Дополнительная логика: проверка, можно ли удалять
        if instance.role not in [RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]:
            return Response({"error": "Удаление запрещено"}, status=status.HTTP_403_FORBIDDEN)

        # Удаление объекта
        self.perform_destroy(instance)
        return Response({"message": "Удалено"}, status=status.HTTP_204_NO_CONTENT)


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ViewSet для аутентификации по email-коду (без ID пользователя)."""

    permission_classes = [AllowAny]
    serializer_class = EmailLoginSerializer

    def get_serializer_class(self):
        """Определяем сериализатор в зависимости от действия."""
        if self.action == "create":
            return EmailLoginSerializer
        elif self.action == "verify":
            return VerifyCodeSerializer
        return self.serializer_class

    @extend_schema(
        summary="Запросить код для входа",
        description="Отправляет 4-значный код на email пользователя для входа в систему.",
        tags=[auth["name"]],
        request=EmailLoginSerializer,
        responses={
            200: OpenApiResponse(
                description="Код успешно отправлен",
                examples=[
                    OpenApiExample(name="Success", value={"message": "Код отправлен на email"}, response_only=True)
                ],
            ),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        code = random.randint(1000, 9999)
        user.set_password(str(code))
        user.save(update_fields=["password"])

        self.send_email(user.email, code)

        return Response({"message": "Код отправлен на email"}, status=status.HTTP_200_OK)

    @staticmethod
    def send_email(email, code):
        """Отправка email с кодом."""
        email_message = EmailMessage(
            subject="Ваш код для входа",
            body=f"""
                <html>
                    <body>
                        <p>Код для входа в сервис <strong>'Куда Угодно'</strong>:
                        <strong style="font-size:18px;color:#007bff;">{code}</strong>.</p>
                        <p><strong>Никому не сообщайте этот код!</strong>
                        Если вы не запрашивали код, просто проигнорируйте это сообщение.</p>
                    </body>
                </html>
            """,
            from_email=EMAIL_HOST_USER,
            to=[email],
        )
        email_message.content_subtype = "html"
        email_message.send()

    @extend_schema(
        summary="Подтвердить код и получить токены",
        description="Проверка кода и выдача JWT-токенов + роль пользователя.",
        tags=[auth["name"]],
        request=VerifyCodeSerializer,
        responses={
            200: OpenApiResponse(
                description="JWT-токены успешно получены",
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={"access": "jwt_access_token", "refresh": "jwt_refresh_token", "role": "USER"},
                        response_only=True,
                    )
                ],
            ),
            400: OpenApiResponse(description="Неверный код"),
        },
    )
    @action(detail=False, methods=["post"], url_path="verify", permission_classes=[AllowAny])
    def verify(self, request):
        """Проверка кода и получение токенов."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        user = authenticate(email=email, password=str(code))
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role,
                },
                status=status.HTTP_200_OK,
            )

        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Выход из системы (Logout)",
        description="Аннулирует refresh-токен, выход из системы.",
        tags=[auth["name"]],
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(
                description="Вы успешно вышли из системы",
                examples=[
                    OpenApiExample(
                        name="Success", value={"message": "Вы успешно вышли из системы"}, response_only=True
                    )
                ],
            ),
            400: OpenApiResponse(description="Ошибка при выходе"),
        },
    )
    @action(detail=False, methods=["post"], url_path="logout", permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Выход из системы: аннулирование refresh-токена."""
        try:
            # Получаем токен из запроса
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh-токен не передан"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            # Добавляем токен в блэклист
            token.blacklist()

            return Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Проверка активности access-токена",
        description="Возвращает 200 OK, если access-токен валиден, иначе 401 Unauthorized.",
        tags=[auth["name"]],
        responses={
            200: OpenApiResponse(description="Токен действителен"),
            401: OpenApiResponse(description="Токен недействителен или отсутствует"),
        },
    )
    @action(detail=False, methods=["get"], url_path="check-token", permission_classes=[IsAuthenticated])
    def check_token(self, request):
        """Проверка активности access-токена."""
        return Response({"message": "Токен активен"}, status=status.HTTP_200_OK)
