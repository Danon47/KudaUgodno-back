from django.contrib import admin

from vzhuh.models import Vzhuh


@admin.register(Vzhuh)
class VzhuhAdmin(admin.ModelAdmin):
    list_display = ("display_route", "departure_city", "arrival_city", "is_published", "created_at")
    search_fields = ("departure_city", "description")
    list_filter = ("created_at", "updated_at", "is_published")
    # Для ManyToMany — удобный выбор
    filter_horizontal = ("tours", "hotels")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {"fields": ("departure_city", "arrival_city", "description", "best_time_to_travel", "suitable_for_whom")},
        ),
        ("Туры", {"fields": ("tours", "description_tour")}),
        ("Отели", {"fields": ("hotels", "description_hotel")}),
        ("Блог", {"fields": ("description_blog",)}),
        ("Системные", {"fields": ("created_at", "updated_at", "is_published")}),
    )
