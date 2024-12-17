from django.contrib import admin

from hotels.models import (
    Hotel,
    Room,
    HotelAmenity,
    RoomAmenity,
    RoomCategory,
    RoomPhoto,
    HotelPhoto,
)

class RoomInline(admin.StackedInline):
    model = Room
    # Количество пустых форм для добавления новых номеров
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    list_display_links = ("id", "name")
    # Добавляем встроенный класс для номеров
    inlines = [RoomInline]


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


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")
