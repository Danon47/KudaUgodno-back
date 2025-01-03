from rest_framework import serializers

from applications.models.models_application import Application
from applications.models.models_guest import Guest
from applications.serializers.serializers_guests import GuestSerializer
from hotels.models import Room
from hotels.serializers import RoomSerializer
from users.serializers import UserSerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ("user_owner",)


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Application
    """

    quantity_guests = GuestSerializer(many=True)
    quantity_rooms = RoomSerializer(many=True)
    user_owner = UserSerializer(read_only=True)

    class Meta(ApplicationCreateSerializer.Meta):
        model = Application
        fields = ApplicationCreateSerializer.Meta.fields
        read_only_fields = ("quantity_guests", "quantity_rooms", "user_owner")