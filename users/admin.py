from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для управления пользователями, с группами."""

    # Полностью убираем username
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "phone_number", "avatar", "birth_date")}),
        ("Роли и права", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups")}),
        ("Компания", {"fields": ("company_name", "documents")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )

    list_display = ("email", "first_name", "last_name", "role", "is_active", "is_staff", "is_superuser", "role")
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    readonly_fields = ("last_login", "date_joined")
    # Добавляем возможность управлять группами
    filter_horizontal = ("groups",)

    def get_queryset(self, request):
        """Фильтруем пользователей в зависимости от группы администратора"""
        qs = super().get_queryset(request)
        # Суперадмин видит всех
        if request.user.is_superuser:
            return qs
        # Админ не видит суперадминов
        if request.user.groups.filter(name="Admin").exists():
            return qs.exclude(role="Super Admin")
        # Туроператоры видят только туроператоров
        if request.user.groups.filter(name="Tour Operators").exists():
            return qs.filter(role="TOUR_OPERATOR")
        # Отельеры видят только отельеров
        if request.user.groups.filter(name="Hoteliers").exists():
            return qs.filter(role="HOTELIER")
        # Обычные пользователи не видят никого
        return qs.none()
