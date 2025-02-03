from rest_framework import serializers

from flights.validators.validators import ForbiddenWordValidator
from users.models import User
from users.validators import FillFieldsValidator


class AdminSerializer(serializers.ModelSerializer):
    """
    Сериализатор для администратора (полное представление модели User).
    Используется, если требуется отображать все поля модели.
    """
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для пользователя.

    Отображает только основные поля модели User.
    Применяются дополнительные валидаторы:
    - ForbiddenWordValidator: запрещает использование запрещённых слов в указанных полях;
    - FillFieldsValidator: проверяет, что необходимые поля заполнены.
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
            FillFieldsValidator()
        ]
