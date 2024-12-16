from rest_framework import serializers

from applications.models import Application, Guest


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


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Application
    """

    # quantity_guests = GuestSerializer(source="guest_applications", many=True)

    class Meta:
        model = Application
        fields = (
            "pk",
            "tour",
            "email",
            "phone_number",
            "status",
            "quantity_rooms",
            "quantity_guests",
            "visa",
            "med_insurance",
            "cancellation_insurance",
            "wishes",
            "user_owner",
        )
