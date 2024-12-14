from django.contrib import admin

from applications.models import Application


@admin.register(Application)
class AdminApplication(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """
    list_display = ("pk", "Tour", "email", "phone_number", "status")
    list_filter = ("Tour", "status")
    search_fields = ("Tour", "email")