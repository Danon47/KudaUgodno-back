from django.contrib import admin
from hotels.models.models_hotel import Hotel
from hotels.models.models_hotel_amenity import HotelAmenity
from hotels.models.models_hotel_meal import MealPlan
from hotels.models.models_hotel_photo import HotelPhoto
from hotels.models.models_room import Room
from hotels.models.models_room_amenity import RoomAmenity
from hotels.models.models_room_caterogy import RoomCategory
from hotels.models.models_room_photo import RoomPhoto


class RoomInline(admin.StackedInline):
    model = Room
    # Количество пустых форм для добавления новых номеров
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_holiday", "name", "city", "address")
    list_display_links = ("id", "name")
    # Добавляем встроенный класс для номеров
    inlines = (RoomInline,)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "hotel",
        "nightly_price_no_meals",
        "nightly_price_ultra_all_inclusive",
        "nightly_price_all_inclusive",
        "nightly_price_full_board",
        "nightly_price_half_board",
        "nightly_price_only_breakfast",
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


@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_per_person", "hotel")
