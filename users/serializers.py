from rest_framework import serializers
from users.models import User
from users.choices import RoleChoices
from users.validators import ForbiddenWordValidator


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для всех пользователей."""

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "avatar", "birth_date", "role")


class UserSerializer(BaseUserSerializer):
    """Сериализатор для обычных пользователей."""
    first_name = serializers.CharField(validators=[ForbiddenWordValidator()])
    last_name = serializers.CharField(validators=[ForbiddenWordValidator()])

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields


class CompanyUserSerializer(BaseUserSerializer):
    """Сериализатор для Туроператора и Отельера."""

    company_name = serializers.CharField(required=True, validators=[ForbiddenWordValidator()])
    documents = serializers.FileField(required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("company_name", "documents")

    def validate(self, data):
        """
        Валидация полей в зависимости от роли.
        """
        role = data.get("role", RoleChoices.USER)

        if role == RoleChoices.USER:
            raise serializers.ValidationError("Обычный пользователь не может иметь company_name и documents.")

        return data


class EmailLoginSerializer(serializers.Serializer):
    """Сериализатор для запроса кода на email."""
    email = serializers.EmailField(required=True)


class VerifyCodeSerializer(serializers.Serializer):
    """Сериализатор для подтверждения кода и получения токенов."""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
