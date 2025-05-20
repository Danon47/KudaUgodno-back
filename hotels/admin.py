from django.contrib import admin

from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.photo.models_hotel_photo import HotelPhoto
from hotels.models.hotel.rules.models_hotel_rules import HotelRules
from hotels.models.hotel.type_of_meals.models_type_of_meals import TypeOfMeal
from hotels.models.hotel.what_about.models_hotel_what_about import HotelWhatAbout
from hotels.models.room.date.models_room_date import RoomCategory, RoomDate
from hotels.models.room.models_room import Room
from hotels.models.room.photo.models_room_photo import RoomPhoto
from hotels.models.room.rules.models_room_rules import RoomRules


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("id", "type_of_rest", "name", "country", "city", "address")
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
    )
    list_display_links = ("id", "category")


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(RoomRules)
class RoomRulesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "option")
    exclude = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TypeOfMeal)
class TypeOfMealsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(HotelPhoto)
class HotelPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "photo")


@admin.register(HotelRules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(RoomDate)
class RoomDateAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "end_date", "get_categories")

    def get_categories(self, obj):
        return ", ".join([str(category) for category in obj.categories.all()])

    get_categories.short_description = "Категории номеров"


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "price")
