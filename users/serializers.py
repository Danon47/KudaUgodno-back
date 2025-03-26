from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from users.choices import RoleChoices
from users.models import User
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

        # Проверяем, передан ли новый файл, если да – обновляем, иначе не трогаем старый
        if "documents" in validated_data:
            new_document = validated_data.pop("documents")
            if new_document:  # Если передан НЕ пустой файл
                instance.documents = new_document

        # Обновляем только переданные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def validate(self, data):
        """
        Валидация полей в зависимости от роли.
        """
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


class EmailLoginSerializer(serializers.Serializer):
    """Сериализатор для запроса кода на email."""

    email = serializers.EmailField(required=True)


class VerifyCodeSerializer(serializers.Serializer):
    """Сериализатор для подтверждения кода и получения токенов."""

    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
