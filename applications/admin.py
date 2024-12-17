from django.contrib import admin

from applications.models import Application, Guest


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """
    list_display = ("pk", "tour", "email", "phone_number", "status")
    list_filter = ("tour", "status")
    search_fields = ("tour", "email")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    """
    Админ панель для модели Guest
    """

    list_display = ("pk", "firstname", "lastname", "surname", "date_born")
    search_fields = ("firstname", "lastname", "surname")
