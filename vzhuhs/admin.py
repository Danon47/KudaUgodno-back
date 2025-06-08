from django.contrib import admin
from django.utils.html import format_html

from vzhuhs.forms import VzhuhForm
from vzhuhs.models import Vzhuh, VzhuhPhoto


class ArrivalCityFilter(admin.SimpleListFilter):
    """Кастомный фильтр по городу прибытия для списка объектов Vzhuh в админке."""

    title = "Город прибытия"
    parameter_name = "arrival_city"

    def lookups(self, request, model_admin):
        cities = Vzhuh.objects.values_list("arrival_city", flat=True).distinct()
        return [(city, city) for city in cities if city]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(arrival_city=self.value())
        return queryset


class VzhuhPhotoInline(admin.TabularInline):
    """
    Инлайн-фотографии, иллюстрирующие направление Вжуха (город).
    """

    model = VzhuhPhoto
    extra = 1
    fields = ("photo", "caption")


@admin.register(Vzhuh)
class VzhuhAdmin(admin.ModelAdmin):
    """
    Админка для модели Vzhuh.
    """

    form = VzhuhForm
    inlines = [VzhuhPhotoInline]

    list_display = (
        "display_route",
        "arrival_city",
        "colored_published",
        "created_at",
    )
    search_fields = ("description",)
    list_filter = ("created_at", "updated_at", ArrivalCityFilter)
    readonly_fields = (
        "created_at",
        "updated_at",
        "blog_photo_preview",
        "hotel_photos_preview",
    )
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
        ("Отели", {"fields": ("hotels", "description_hotel", "hotel_photos_preview")}),
        ("Блог", {"fields": ("description_blog", "blog_photo", "blog_photo_preview")}),
        (
            "Системные",
            {
                "fields": (
                    "is_published",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def blog_photo_preview(self, obj):
        if obj.blog_photo and obj.blog_photo.photo:
            return format_html('<img src="{}" width="100" height="auto" />', obj.blog_photo.photo.url)
        return "—"

    blog_photo_preview.short_description = "Фото блога"

    def hotel_photos_preview(self, obj):
        """
        Показывает по одному фото для каждого отеля:
        - сначала первое;
        - если нет — второе;
        - если и его нет — '—'.
        """
        html = ""
        for hotel in obj.hotels.all():
            photo_qs = hotel.hotel_photos.all()
            chosen_photo = photo_qs[0] if photo_qs else None
            if not chosen_photo and len(photo_qs) > 1:
                chosen_photo = photo_qs[1]
            if chosen_photo and chosen_photo.photo:
                html += f"""
                    <div style="margin-bottom: 10px;">
                        <strong>{hotel.name}</strong><br/>
                        <img src="{chosen_photo.photo.url}" width="100" style="margin-top: 3px;" />
                    </div>
                """
        return format_html(html or "—")

    hotel_photos_preview.short_description = "Фото отелей"

    def colored_published(self, obj):
        """Показывает цветной индикатор публикации."""
        color = "green" if obj.is_published else "red"
        label = "Да" if obj.is_published else "Нет"
        return format_html('<span style="color: {};">{}</span>', color, label)

    colored_published.short_description = "Опубликован"

    @admin.action(description="Опубликовать выбранные Вжухи")
    def publish_vzhuhs(self, request, queryset):
        """Массовая публикация Вжухов."""
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные Вжухи")
    def unpublish_vzhuhs(self, request, queryset):
        """Массовое снятие Вжухов с публикации."""
        queryset.update(is_published=False)
