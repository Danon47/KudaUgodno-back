from django.contrib import admin

from applications.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """

    list_display = ("pk", "tour", "hotel", "room", "email", "phone_number", "status")
    list_filter = ("tour", "status")
    search_fields = ("tour", "email")
