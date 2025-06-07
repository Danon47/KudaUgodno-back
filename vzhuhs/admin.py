from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from vzhuhs.forms import VzhuhForm
from vzhuhs.models import Vzhuh


class ArrivalCityFilter(admin.SimpleListFilter):
    """
    Кастомный фильтр по городу прибытия для списка объектов Vzhuh в админке.
    Показывает только уникальные значения поля arrival_city.
    """

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
    """
    Кастомный фильтр по наличию главного фото (main_photo).
    Показывает записи с/ или без установленного фото.
    """

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
    """
    Админка для модели Vzhuh с кастомной формой, фильтрами, действиями и отображением.

    Особенности:
    - Кастомные фильтры по городу и фото
    - Автозаполнение главного фото при сохранении (если не задано)
    - Отображение главного фото и статуса публикации в list_display
    """

    form = VzhuhForm

    list_display = (
        "display_route",
        "arrival_city",
        "colored_published",
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
        ("Туры", {"fields": ("tours",)}),
        ("Отели", {"fields": ("hotels", "description_hotel")}),
        ("Блог", {"fields": ("description_blog",)}),
        (
            "Системные",
            {"fields": ("is_published", "main_photo", "main_photo_preview", "created_at", "updated_at")},
        ),
    )

    formfield_overrides = {
        models.TextField: {"widget": admin.widgets.AdminTextareaWidget(attrs={"style": "width: 95%; height: 8em;"})},
        models.CharField: {"widget": admin.widgets.AdminTextInputWidget(attrs={"style": "width: 60%;"})},
    }

    actions = ["publish_vzhuhs", "unpublish_vzhuhs", "export_vzhuhs"]

    def main_photo_preview(self, obj):
        """
        Отображает превью главного фото в админке.
        """
        if obj.main_photo and obj.main_photo.photo:
            return format_html('<img src="{}" width="100" height="auto" />', obj.main_photo.photo.url)
        return "—"

    main_photo_preview.short_description = "Фото"

    def colored_published(self, obj):
        """
        Показывает цветной индикатор статуса публикации.
        """
        color = "green" if obj.is_published else "red"
        label = "Да" if obj.is_published else "Нет"
        return format_html('<span style="color: {};">{}</span>', color, label)

    colored_published.short_description = "Опубликован"

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        obj = form.instance
        if not obj.main_photo:
            first_hotel = obj.hotels.first()
            if first_hotel:
                first_photo = first_hotel.hotel_photos.first()
                if first_photo:
                    obj.main_photo = first_photo
                    obj.save()

    @admin.action(description="Опубликовать выбранные Вжухи")
    def publish_vzhuhs(self, request, queryset):
        """
        Действие для массовой публикации выбранных объектов.
        """
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные Вжухи")
    def unpublish_vzhuhs(self, request, queryset):
        """
        Действие для массового снятия объектов с публикации.
        """
        queryset.update(is_published=False)
