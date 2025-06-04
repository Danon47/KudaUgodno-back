from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from vzhuhs.forms import VzhuhForm
from vzhuhs.models import Vzhuh


class ArrivalCityFilter(admin.SimpleListFilter):
    title = "Город прибытия"
    parameter_name = "arrival_city"

    def lookups(self, request, model_admin):
        cities = Vzhuh.objects.values_list("arrival_city", flat=True).distinct()
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(arrival_city=self.value())
        return queryset


class HasPhotoFilter(admin.SimpleListFilter):
    title = "Есть фото"
    parameter_name = "has_photo"

    def lookups(self, request, model_admin):
        return (("yes", "Да"), ("no", "Нет"))

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.exclude(main_photo__isnull=True)
        elif self.value() == "no":
            return queryset.filter(main_photo__isnull=True)
        return queryset


@admin.register(Vzhuh)
class VzhuhAdmin(admin.ModelAdmin):
    form = VzhuhForm

    list_display = (
        "display_route",
        "arrival_city",
        "colored_published",
        "main_photo_preview",
        "created_at",
    )
    search_fields = ("description",)
    list_filter = (
        "created_at",
        "updated_at",
        ArrivalCityFilter,
        HasPhotoFilter,
    )
    readonly_fields = ("created_at", "updated_at", "main_photo_preview")

    filter_horizontal = ("tours", "hotels")
    list_per_page = 30
    list_max_show_all = 300
    ordering = ("-created_at",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "arrival_city",
                    "description",
                    "best_time_to_travel",
                    "suitable_for_whom",
                )
            },
        ),
        ("Туры", {"fields": ("tours",), "classes": ["collapse"]}),
        ("Отели", {"fields": ("hotels", "description_hotel"), "classes": ["collapse"]}),
        ("Блог", {"fields": ("description_blog",), "classes": ["collapse"]}),
        (
            "Системные",
            {
                "fields": ("is_published", "main_photo", "main_photo_preview", "created_at", "updated_at"),
                "classes": ["collapse"],
            },
        ),
    )

    formfield_overrides = {
        models.TextField: {"widget": admin.widgets.AdminTextareaWidget(attrs={"style": "width: 95%; height: 8em;"})},
        models.CharField: {"widget": admin.widgets.AdminTextInputWidget(attrs={"style": "width: 60%;"})},
    }

    actions = ["publish_vzhuhs", "unpublish_vzhuhs", "export_vzhuhs"]

    def main_photo_preview(self, obj):
        if obj.main_photo and obj.main_photo.photo:
            return format_html('<img src="{}" width="100" height="auto" />', obj.main_photo.photo.url)
        return "—"

    main_photo_preview.short_description = "Фото"

    def colored_published(self, obj):
        color = "green" if obj.is_published else "red"
        label = "Да" if obj.is_published else "Нет"
        return format_html('<span style="color: {};">{}</span>', color, label)

    colored_published.short_description = "Опубликован"

    def save_model(self, request, obj, form, change):
        # Сохраняем объект, чтобы появился obj.pk
        super().save_model(request, obj, form, change)

        # Если нет главного фото — берём первое из отелей
        if not obj.main_photo:
            first_hotel = obj.hotels.first()
            if first_hotel:
                first_photo = first_hotel.hotel_photos.first()
                if first_photo:
                    obj.main_photo = first_photo
                    obj.save()

    @admin.action(description="Опубликовать выбранные Вжухи")
    def publish_vzhuhs(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные Вжухи")
    def unpublish_vzhuhs(self, request, queryset):
        queryset.update(is_published=False)
