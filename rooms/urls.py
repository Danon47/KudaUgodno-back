from django.urls import path

from rooms.apps import RoomsConfig
from rooms.views import RoomDateViewSet, RoomPhotoViewSet, RoomViewSet
from rooms.views_price_calendar import PriceCalendarViewSet


app_name = RoomsConfig.name


urlpatterns = [
    path(
        "<int:hotel_id>/rooms/",
        RoomViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-list",
    ),
    path(
        "<int:hotel_id>/rooms/<int:pk>/",
        RoomViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="rooms-detail",
    ),
    path(
        "rooms/<int:room_id>/photos/",
        RoomPhotoViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-photos-list",
    ),
    path(
        "rooms/<int:room_id>/photos/<int:pk>/",
        RoomPhotoViewSet.as_view({"delete": "destroy"}),
        name="rooms-photo-detail",
    ),
    path(
        "<int:hotel_id>/rooms/dates/",
        RoomDateViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-dates-list",
    ),
    path(
        "<int:hotel_id>/rooms/dates/<int:pk>/",
        RoomDateViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="rooms-dates-detail",
    ),
    path(
        "<int:hotel_id>/price_calendars/",
        PriceCalendarViewSet.as_view({"get": "list", "post": "create"}),
        name="rooms-dates-list_1",
    ),
    path(
        "<int:hotel_id>/price_calendars/<int:pk>/",
        PriceCalendarViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="rooms-dates-detail_1",
    ),
]
