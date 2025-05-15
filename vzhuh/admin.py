from django.contrib import admin

from vzhuh.models import Vzhuh


# Это кастомный фильтр
class DepartureCityFilter(admin.SimpleListFilter):
    title = "Город вылета"
    parameter_name = "departure_city"

    def lookups(self, request, model_admin):
        cities = Vzhuh.objects.values_list("departure_city", flat=True).distinct()
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(departure_city=self.value())
        return queryset


# Обновлённая админка
@admin.register(Vzhuh)
class VzhuhAdmin(admin.ModelAdmin):
    list_display = ("display_route", "departure_city", "arrival_city", "is_published", "created_at")
    search_fields = ("departure_city", "description")
    # тут используем кастомный фильтр
    list_filter = ("created_at", "updated_at", "is_published", DepartureCityFilter)
    # для МэниТуМэни
    filter_horizontal = ("tours", "hotels")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "departure_city",
                    "arrival_city",
                    "description",
                    "best_time_to_travel",
                    "suitable_for_whom",
                ),
            },
        ),
        ("Туры", {"fields": ("tours", "description_tour")}),
        ("Отели", {"fields": ("hotels", "description_hotel")}),
        ("Блог", {"fields": ("description_blog",)}),
        ("Системные", {"fields": ("created_at", "updated_at", "is_published")}),
    )


@admin.action(description="Опубликовать выбранные Вжухи")
def publish_vzhuhs(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Снять с публикации выбранные Вжухи")
def unpublish_vzhuhs(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description="Экспортировать выбранные Вжухи в JSON")
def export_vzhuhs(modeladmin, request, queryset):
    import json

    from django.http import HttpResponse

    data = list(queryset.values())
    response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), content_type="application/json")
    response["Content-Disposition"] = "attachment; filename=vzhuhs_export.json"
    return response
