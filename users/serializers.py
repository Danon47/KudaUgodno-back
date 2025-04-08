from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from users.choices import RoleChoices
from users.models import User
from users.validators import ForbiddenWordValidator


# ───── Пользователи ───────────────────────────────────────────────────────────


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для всех пользователей."""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "avatar", "birth_date", "role")


class UserSerializer(BaseUserSerializer):
    """Сериализатор для обычных пользователей."""

    first_name = serializers.CharField(validators=[ForbiddenWordValidator()])
    last_name = serializers.CharField(validators=[ForbiddenWordValidator()])
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class CompanyUserSerializer(BaseUserSerializer):
    """Сериализатор для Туроператоров и Отельеров."""

    first_name = serializers.CharField(required=True, validators=[ForbiddenWordValidator()])
    last_name = serializers.CharField(required=True, validators=[ForbiddenWordValidator()])
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(required=True)
    company_name = serializers.CharField(required=True, validators=[ForbiddenWordValidator()])
    documents = serializers.FileField(required=False, allow_null=True)
    role = serializers.CharField(default=RoleChoices.TOUR_OPERATOR)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("company_name", "documents")

    def update(self, instance, validated_data):
        """Полное обновление объекта (PUT)."""
        if "documents" in validated_data:
            new_document = validated_data.pop("documents")
            if new_document:
                instance.documents = new_document
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        """Валидация полей в зависимости от роли."""
        role = data.get("role", RoleChoices.USER)
        if role == RoleChoices.USER:
            raise serializers.ValidationError("Обычный пользователь не может иметь company_name и documents.")
        return data


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)

    def save(self, request):
        user = super().save(request)
        user.username = user.email
        user.save()
        return user


# ───── Аутентификация ─────────────────────────────────────────────────────────


class EmailLoginSerializer(serializers.Serializer):
    """Сериализатор для запроса кода на email."""

    email = serializers.EmailField(
        help_text="Email пользователя, на который будет отправлен код для входа.",
    )


class EmailCodeResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Сообщение об успешной отправке кода.")


class VerifyCodeSerializer(serializers.Serializer):
    """Сериализатор запроса на подтверждение кода.
    Используется для передачи email и 4-значного кода из письма.
    """

    email = serializers.EmailField(help_text="Email, на который отправлен код")
    code = serializers.CharField(help_text="Код из письма")


class VerifyCodeResponseSerializer(serializers.Serializer):
    """Сериализатор успешного ответа с JWT-токенами.
    Возвращает access/refresh токены, роль пользователя и флаг регистрации.
    """

    refresh = serializers.CharField(help_text="JWT refresh-токен")
    access = serializers.CharField(help_text="JWT access-токен")
    role = serializers.CharField(help_text="Роль пользователя, например: USER, ADMIN")
    id = serializers.IntegerField(help_text="Уникальный идентификатор пользователя в базе данных")


class LogoutSerializer(serializers.Serializer):
    """Сериализатор для выхода из системы"""

    refresh = serializers.CharField(required=True)


class LogoutSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Сообщение об успешном выходе из системы.")


# ───── Общие ошибки ───────────────────────────────────────────────────────────


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Описание ошибки, если выход не удался.")


# ───── Проверка токена ────────────────────────────────────────────────────────


class CheckTokenSuccessResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Успешное подтверждение, что токен активен.")


class CheckTokenErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Описание ошибки: недействительный или отсутствующий токен.")
