from django.contrib import admin
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_amenity import (
    HotelAmenityCommon,
    HotelAmenityInTheRoom,
    HotelAmenitySportsAndRecreation,
    HotelAmenityForChildren,
)
from hotels.models.hotel.models_hotel_photo import HotelPhoto
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_amenity import (
    RoomAmenityCommon,
    RoomAmenityCoffeeStation,
    RoomAmenityBathroom,
    RoomAmenityView,
)
# from hotels.models.room.models_room_category import RoomCategory
from hotels.models.room.models_room_discount import RoomDiscount
from hotels.models.room.models_room_photo import RoomPhoto
from hotels.models.room.models_room_unavailable import RoomUnavailable


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
        "price",
    )
    list_display_links = ("id", "category")


# @admin.register(HotelAmenityCommon)
# class HotelAmenityCommonAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(HotelAmenityInTheRoom)
# class HotelAmenityInTheRoomAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(HotelAmenitySportsAndRecreation)
# class HotelAmenitySportsAndRecreationAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(HotelAmenityForChildren)
# class HotelAmenityForChildrenAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


# @admin.register(RoomAmenityCommon)
# class RoomAmenityAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(RoomAmenityCoffeeStation)
# class RoomAmenityAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(RoomAmenityBathroom)
# class RoomAmenityAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#
#
# @admin.register(RoomAmenityView)
# class RoomAmenityAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


# @admin.register(RoomCategory)
# class RoomCategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")

@admin.register(RoomDiscount)
class RoomDiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "size", "start_date", "end_date",)

@admin.register(RoomUnavailable)
class RoomUnavailableAdmin(admin.ModelAdmin):
    list_display = ("id", "reason", "start_date", "end_date",)

@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelRules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
