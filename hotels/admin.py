from django.contrib import admin

from hotels.models import Hotel, HotelRoom, AmenityHotel, AmenityRoom


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    list_display_links = ("id", "name")
    # search_fields = ("name", "city", "address")


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "type_of_holiday", "nightly_price", "start_date", "end_date")
    list_display_links = ("id", "category")
    # search_fields = ("category", "type_of_holiday")


@admin.register(AmenityHotel)
class AmenityHotelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(AmenityRoom)
class AmenityRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
