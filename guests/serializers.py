from rest_framework import serializers

from flights.validators.validators import ForbiddenWordValidator
from guests.models import Guest
from guests.validators import DateBornValidator, ValidityOfForeignPassportValidator
from users.serializers import UserSerializer


class GuestDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Guest
    """

    class Meta:
        model = Guest
        fields = (
            "pk",
            "firstname",
            "lastname",
            "surname",
            "date_born",
            "citizenship",
            "russian_passport_no",
            "international_passport_no",
            "validity_international_passport",
            "user_owner",
        )
        read_only_fields = ("user_owner",)
        validators = [
            ForbiddenWordValidator(fields=["firstname", "lastname", "surname", "citizenship"]),
            DateBornValidator(),
            ValidityOfForeignPassportValidator(),
        ]


class GuestSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Guest
    """

    user_owner = UserSerializer(read_only=True)

    class Meta:
        model = Guest
        fields = (
            "pk",
            "firstname",
            "lastname",
            "surname",
            "date_born",
            "citizenship",
            "russian_passport_no",
            "international_passport_no",
            "validity_international_passport",
            "user_owner",
        )
