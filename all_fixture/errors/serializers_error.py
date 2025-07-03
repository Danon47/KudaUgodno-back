from rest_framework.serializers import CharField, ListField, Serializer

from all_fixture.errors.list_error import (
    APPLICATION_HOTEL_ERROR,
    APPLICATION_TOUR_ERROR,
    FLIGHT_ERROR,
    GUEST_AUTH_ERROR,
    GUEST_ERROR,
    GUEST_USER_ERROR,
    HOTEL_ID_ERROR,
    INSURANCE_ERROR,
    PHOTO_ERROR,
    PHOTO_FILE_ERROR,
    ROOM_DATE_ERROR,
    ROOM_ID_ERROR,
    TOUR_ERROR,
    TOUR_STOCK_ERROR,
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


class InsurancesErrorIdSerializer(Serializer):
    detail = CharField(default=INSURANCE_ERROR)


class TourErrorBaseSerializer(Serializer):
    detail = CharField()


class TourErrorSerializer(Serializer):
    detail = CharField(default=TOUR_ERROR)


class TourStockErrorBaseSerializer(Serializer):
    detail = CharField()


class TourStockErrorSerializer(Serializer):
    detail = CharField(default=TOUR_STOCK_ERROR)


class RoomBaseEroorSerializer(Serializer):
    detail = CharField()


class RoomErrorIdSerializer(Serializer):
    detail = CharField(default=ROOM_ID_ERROR)


class RoomPhotoErrorIdSerializer(Serializer):
    detail = CharField(default=PHOTO_ERROR)


class RoomPhotoErrorFileSerializer(Serializer):
    photo = ListField(child=CharField(), default=[PHOTO_FILE_ERROR])


class RoomDateErrorBaseSerializer(Serializer):
    detail = CharField()


class RoomDateErrorHotelIdSerializer(Serializer):
    dateil = CharField(default=HOTEL_ID_ERROR)


class RoomDateErrorSerializer(Serializer):
    dateil = CharField(default=ROOM_DATE_ERROR)
