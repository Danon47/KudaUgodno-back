from django.contrib import admin

from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.hotel.models_hotel_what_about import HotelWhatAbout
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_discount import RoomDiscount
from hotels.models.room.models_room_photo import RoomPhoto
from hotels.models.room.models_room_unavailable import RoomUnavailable


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_rest", "name", "country", "warm", "city", "address")
    list_display_links = ("id", "name")


@admin.register(HotelWhatAbout)
class HotelWhatAboutAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_set",
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "hotel",
        "price",
    )
    list_display_links = ("id", "category")


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(RoomDiscount)
class RoomDiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "size",
        "start_date",
        "end_date",
    )


@admin.register(RoomUnavailable)
class RoomUnavailableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reason",
        "start_date",
        "end_date",
    )


@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelRules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
