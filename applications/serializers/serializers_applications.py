from rest_framework import serializers

from applications.models.models_application import Application
from applications.models.models_guest import Guest
from hotels.models import Room


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Application
    """

    quantity_guests = serializers.PrimaryKeyRelatedField(many=True, queryset=Guest.objects.all())
    quantity_rooms = serializers.PrimaryKeyRelatedField(many=True, queryset=Room.objects.all())

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
            "user_owner"
        )
        read_only_fields = ("user_owner", "status")