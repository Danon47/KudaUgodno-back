from rest_framework import serializers

from flights.validators.validators import ForbiddenWordValidator
from users.models import User
from users.validators import FillFieldsValidator


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для пользователя"""

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
            FillFieldsValidator()
        ]
