from django.contrib import admin

from hotels.models import (
    Hotel,
    Room,
    AmenityHotel,
    AmenityRoom,
    CategoryRoom,
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


@admin.register(AmenityHotel)
class AmenityHotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(AmenityRoom)
class AmenityRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(CategoryRoom)
class CategoryHotelRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
