import random
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)

from all_fixture.fixture_views import user_settings, offset, limit, entreprise, auth
from users.models import User
from users.serializers import (
    UserSerializer,
    CompanyUserSerializer,
    EmailLoginSerializer,
    VerifyCodeSerializer,
)
from users.pagination import CustomLOPagination
from config.settings import EMAIL_HOST_USER
from users.tasks import clear_user_password
from users.choices import RoleChoices


@extend_schema_view(
    list=extend_schema(
        summary="Список пользователей (обычные)",
        description="Получение списка всех обычных пользователей",
        tags=[user_settings["name"]],
        parameters=[limit, offset],
        responses={200: UserSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Создание пользователя",
        description="Создание нового пользователя с указанием email и пароля",
        tags=[user_settings["name"]],
        request=UserSerializer,
        responses={201: UserSerializer},
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для обычных пользователей."""

    queryset = User.objects.filter(role=RoleChoices.USER).order_by("-pk")
    serializer_class = UserSerializer
    pagination_class = CustomLOPagination


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
)
class CompanyUserViewSet(viewsets.ModelViewSet):
    """ViewSet для Туроператоров и Отельеров."""

    queryset = User.objects.filter(
        role__in=[RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]
    ).order_by("-pk")
    serializer_class = CompanyUserSerializer
    pagination_class = CustomLOPagination


class AuthViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """ViewSet для аутентификации по email-коду."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Запросить код для входа",
        description="Отправляет 4-значный код на email пользователя для входа в систему.",
        tags=[auth["name"]],
        request=EmailLoginSerializer,
        responses={200: OpenApiResponse(description="Код отправлен на email")},
    )
    def create(self, request, *args, **kwargs):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        code = random.randint(1000, 9999)
        user.set_password(str(code))
        user.save(update_fields=["password"])

        self.send_email(user.email, code)
        clear_user_password.apply_async((user.id,), countdown=300)

        return Response(
            {"message": "Код отправлен на email"}, status=status.HTTP_200_OK
        )

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
                       <p><strong>Никому не сообщайте этот код!</strong> Если вы не запрашивали код, просто проигнорируйте это сообщение.</p>
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
        responses={200: OpenApiResponse(description="JWT-токены получены")},
    )
    def partial_update(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)
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
