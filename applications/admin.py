from django.contrib import admin

from applications.models import Application, HotelApplication


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """

    list_display = ("pk", "tour", "email", "phone_number", "status")
    list_filter = ("tour", "status")
    search_fields = ("tour", "email")


@admin.register(HotelApplication)
class HotelApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели HotelApplication
    """

    list_display = ("pk", "hotel", "room", "email", "phone_number", "status")
    list_filter = ("hotel", "status")
    search_fields = ("hotel", "email")
