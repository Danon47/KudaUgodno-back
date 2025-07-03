from rest_framework.serializers import CharField, Serializer

from all_fixture.errors.list_error import (
    APPLICATION_HOTEL_ERROR,
    APPLICATION_TOUR_ERROR,
    FLIGHT_ERROR,
    GUEST_AUTH_ERROR,
    GUEST_ERROR,
    GUEST_USER_ERROR,
)


class MailingErrorSerializer(Serializer):
    detail = CharField()


class ApplicationHotelErrorIdSerializer(Serializer):
    detail = CharField(default=APPLICATION_HOTEL_ERROR)


class ApplicationTourErrorIdSerializer(Serializer):
    detail = CharField(default=APPLICATION_TOUR_ERROR)


class FlightErrorIdSerializer(Serializer):
    detail = CharField(default=FLIGHT_ERROR)


class GuestErrorBaseSerializer(Serializer):
    detail = CharField()


class GuestErrorIdSerializer(Serializer):
    detail = CharField(default=GUEST_ERROR)


class GuestErrorAuthSerializer(Serializer):
    detail = CharField(default=GUEST_AUTH_ERROR)


class GuestErrorUserSerializer(Serializer):
    detail = CharField(default=GUEST_USER_ERROR)
