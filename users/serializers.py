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
            "first_name",
            "last_name",
            "password",
            "phone_number",
            "avatar",
        ]
        read_only_fields = ("is_staff", "is_superuser",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
