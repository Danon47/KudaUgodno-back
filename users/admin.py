from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для управления пользователями, с группами."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "phone_number", "avatar", "birth_date")}),
        ("Роли и права", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups")}),
        ("Компания", {"fields": ("company_name", "documents")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff", "is_superuser")
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")

    # Добавляем возможность управлять группами
    filter_horizontal = ("groups",)


class TourOperatorAdmin(CustomUserAdmin):
    """Админка только для Туроператоров."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="TOUR_OPERATOR")


class HotelierAdmin(CustomUserAdmin):
    """Админка только для Отельеров."""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(role="HOTELIER")


# Регистрируем пользователей и группы в админке
admin.site.register(User, CustomUserAdmin)
admin.site.register(User, TourOperatorAdmin, name="Туроператоры")
admin.site.register(User, HotelierAdmin, name="Отельеры")
# Добавляем управление группами в Django Admin
admin.site.register(Group)
