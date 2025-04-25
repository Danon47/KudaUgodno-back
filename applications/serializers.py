from rest_framework import serializers

from all_fixture.validators.validators import ForbiddenWordValidator
from applications.models import Application
from guests.serializers import GuestSerializer
from hotels.serializers.hotel.serializers_hotel import HotelListSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer
from tours.serializers import TourListSerializer


# from users.serializers import UserSerializer


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявок по турам.
    методы PUT POST PATCH.
    """

    class Meta:
        model = Application
        fields = (
            "pk",
            "tour",
            "hotel",
            "room",
            "email",
            "phone_number",
            "status",
            "quantity_guests",
            "visa",
            "med_insurance",
            "cancellation_insurance",
            "wishes",
            # "user_owner",
        )
        read_only_fields = ("status",)  # , "user_owner")
        validators = [ForbiddenWordValidator(fields=["wishes"])]


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор заявок по турам.
    методы GET.
    """

    tour = TourListSerializer()
    hotel = HotelListSerializer()
    room = RoomDetailSerializer()
    quantity_guests = GuestSerializer(many=True)
    # user_owner = UserSerializer()

    class Meta(ApplicationDetailSerializer.Meta):
        read_only_fields = (
            "tour",
            "quantity_guests",
        )  # "user_owner"
