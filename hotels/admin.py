from django.contrib import admin

from hotels.models import (
    Hotel,
    Room,
    HotelAmenity,
    RoomAmenity,
    RoomCategory,
)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    list_display_links = ("id", "name")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "type_of_holiday",
        "nightly_price",
    )
    list_display_links = ("id", "category")


@admin.register(HotelAmenity)
class HotelAmenityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
