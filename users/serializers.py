from rest_framework import serializers
from users.models import User
from users.choices import RoleChoices
from users.validators import ForbiddenWordValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения общих данных пользователя."""

    class Meta:
        model = User
        fields = (
            "id", "first_name", "last_name", "email", "phone_number", "avatar", "birth_date", "role"
        )


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями, с проверкой запрещённых слов."""

    first_name = serializers.CharField(validators=[ForbiddenWordValidator()])
    last_name = serializers.CharField(validators=[ForbiddenWordValidator()])
    company_name = serializers.CharField(validators=[ForbiddenWordValidator()], required=False)

    class Meta:
        model = User
        fields = (
            "id", "username", "first_name", "last_name", "email",
            "phone_number", "avatar", "birth_date", "role",
            "company_name", "documents"
        )

    def validate(self, data):
        """
        Валидация данных в зависимости от роли пользователя.
        """
        role = data.get("role", RoleChoices.USER)

        if role == RoleChoices.USER:
            if data.get("company_name") or data.get("documents"):
                raise serializers.ValidationError(
                    "У обычного пользователя не могут быть заполнены поля: company_name, documents.")

        elif role in [RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]:
            if not data.get("company_name"):
                raise serializers.ValidationError(
                    "Для Туроператора и Отельера поле 'Название компании' является обязательным.")
            if not data.get("documents"):
                raise serializers.ValidationError("Для Туроператора и Отельера необходимо загрузить документы.")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmailLoginSerializer(serializers.Serializer):
    """Сериализатор для запроса кода на email."""
    email = serializers.EmailField(required=True)

class VerifyCodeSerializer(serializers.Serializer):
    """Сериализатор для подтверждения кода и получения токенов."""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
