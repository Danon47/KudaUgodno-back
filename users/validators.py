from rest_framework.exceptions import ValidationError

from users.choices import RoleChoices


class FillFieldsValidator:
    """Проверка на заполнение полей в зависимости от роли"""

    def __call__(self, value):

        if value.get("role") == RoleChoices.USER and value.get("username") or value.get("address") or value.get("description"):
                raise ValidationError("У пользователя не могут быть заполнены поля: username, address, description")
        if value.get("role") == RoleChoices.TOUR_OPERATOR and value.get("first_name") or value.get("last_name"):
                raise ValidationError("У туроператора не могут быть заполнены поля: first_name, last_name")