from rest_framework import serializers
from flights.validators.validators import ForbiddenWordValidator
from users.models import User

class AdminSerializer(serializers.ModelSerializer):
    """
    Админский сериализатор (полное представление) + ForbiddenWordValidator
    """
    class Meta:
        model = User
        fields = "__all__"
        validators = [
            # Подключаем тот же валидатор, что и в UserSerializer:
            ForbiddenWordValidator(fields=["username", "first_name", "last_name", "email", "address", "description"]),
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    "Узкий" сериализатор: только основные поля.
    """
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "avatar",
            "address",
            "description"
        )
        validators = [
            ForbiddenWordValidator(fields=["username", "first_name", "last_name", "email", "address", "description"]),
        ]
