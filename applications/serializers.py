from rest_framework import serializers

from all_fixture.validators.validators import ForbiddenWordValidator
from applications.models import ApplicationHotel, ApplicationTour
from guests.serializers import GuestSerializer
from hotels.serializers import HotelListWithPhotoSerializer
from rooms.serializers import RoomDetailSerializer
from tours.serializers import TourListSerializer


class ApplicationBaseSerializer(serializers.ModelSerializer):
    """
    Базовая сериализация для заявок
    """

    class Meta:
        fields = (
            "id",
            "email",
            "phone_number",
            "visa",
            "med_insurance",
            "cancellation_insurance",
            "wishes",
            "status",
        )
        validators = [ForbiddenWordValidator(fields=["wishes"])]


class ApplicationTourSerializer(ApplicationBaseSerializer):
    """
    Сериализация заявки тура.
    Методы PUT POST PATCH
    """

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationTour
        fields = ApplicationBaseSerializer.Meta.fields + ("tour", "quantity_guests")


class ApplicationTourListSerializer(ApplicationBaseSerializer):
    """
    Сериализация заявки тура.
    Методы GET
    """

    tour = TourListSerializer(read_only=True)
    quantity_guests = GuestSerializer(many=True, read_only=True)

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationTour
        fields = ApplicationBaseSerializer.Meta.fields + ("tour", "quantity_guests")
        read_only_fields = ("status",)


class ApplicationHotelSerializer(ApplicationBaseSerializer):
    """
    Сериализация заявки отеля.
    Методы PUT POST PATCH
    """

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationHotel
        fields = ApplicationBaseSerializer.Meta.fields + ("hotel", "room", "quantity_guests")


class ApplicationHotelListSerializer(ApplicationBaseSerializer):
    """
    Сериализация заявки отеля.
    Методы GET
    """

    hotel = HotelListWithPhotoSerializer(read_only=True)
    room = RoomDetailSerializer(read_only=True)
    quantity_guests = GuestSerializer(many=True, read_only=True)

    class Meta(ApplicationBaseSerializer.Meta):
        model = ApplicationHotel
        fields = ApplicationBaseSerializer.Meta.fields + ("hotel", "room", "quantity_guests")
        read_only_fields = ("status",)
