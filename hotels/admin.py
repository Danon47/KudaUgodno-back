from django.contrib import admin
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_amenity import (HotelAmenityCommon, HotelAmenityInTheRoom,
                                                      HotelAmenitySportsAndRecreation, HotelAmenityForChildren)
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_amenity import RoomAmenity
from hotels.models.room.models_room_category import RoomCategory
from hotels.models.room.models_room_photo import RoomPhoto



@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_rest", "name", "city", "address")
    list_display_links = ("id", "name")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "hotel",
        "nightly_price",
    )
    list_display_links = ("id", "category")


@admin.register(HotelAmenityCommon)
class HotelAmenityCommonAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(HotelAmenityInTheRoom)
class HotelAmenityInTheRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(HotelAmenitySportsAndRecreation)
class HotelAmenitySportsAndRecreationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(HotelAmenityForChildren)
class HotelAmenityForChildrenAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelRules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
