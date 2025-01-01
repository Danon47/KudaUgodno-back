from rest_framework import serializers

from applications.models.models_guest import Guest


class GuestSerializer(serializers.ModelSerializer):
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
