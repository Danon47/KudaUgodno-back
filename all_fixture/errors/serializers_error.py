from rest_framework.serializers import CharField, Serializer

from all_fixture.errors.list_error import (
    APPLICATION_HOTEL_ERROR,
    APPLICATION_TOUR_ERROR,
)


class MailingErrorSerializer(Serializer):
    detail = CharField()


class ApplicationHotelErrorIdSerializer(Serializer):
    detail = CharField(default=APPLICATION_HOTEL_ERROR)


class ApplicationTourErrorIdSerializer(Serializer):
    detail = CharField(default=APPLICATION_TOUR_ERROR)
