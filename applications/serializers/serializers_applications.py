from rest_framework import serializers

from applications.models.models_application import Application
from applications.serializers.serializers_guests import GuestSerializer
from flights.validators.validators import ForbiddenWordValidator
from hotels.serializers import RoomBaseSerializer
from tours.serializers import TourSerializer
from users.serializers import UserSerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Application
    """

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
        validators = [
            ForbiddenWordValidator(fields=["wishes"])
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Application
    """
    tour = TourSerializer()
    quantity_guests = GuestSerializer(many=True)
    quantity_rooms = RoomBaseSerializer(many=True)
    user_owner = UserSerializer()

    class Meta(ApplicationCreateSerializer.Meta):
        model = Application
        fields = ApplicationCreateSerializer.Meta.fields
        read_only_fields = ("tour", "quantity_guests", "quantity_rooms", "user_owner")