from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "phone_number", "user_type", "is_active")
    list_filter = ("user_type", "phone_number")
    search_fields = ("phone_number", "last_name")
