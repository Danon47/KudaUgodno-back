from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Пользователя"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "user_type",
            "first_name",
            "last_name",
            "password",
            "phone_number",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_phone_number(self, value):
        """Проверка на уникальность номера телефона."""
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Этот номер телефона уже используется.")
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
