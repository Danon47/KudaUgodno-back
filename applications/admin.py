from django.contrib import admin

from applications.models import (
    ApplicationCancellationInsurance,
    ApplicationHotel,
    ApplicationMedicalInsurance,
    ApplicationTour,
    ApplicationVisa,
)


@admin.register(ApplicationHotel)
class HotelApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели HotelApplication
    """

    list_display = ("pk", "hotel", "room", "email", "phone_number", "status")
    list_filter = ("hotel", "status")
    search_fields = ("hotel", "email")


@admin.register(ApplicationTour)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели Application
    """

    list_display = ("pk", "tour", "email", "phone_number", "status")
    list_filter = ("tour", "status")
    search_fields = ("tour", "email")


@admin.register(ApplicationVisa)
class VisaApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели VisaApplication
    """

    list_display = (
        "id",
        "count",
        "price",
        "total_price",
    )


@admin.register(ApplicationMedicalInsurance)
class MedicalInsuranceApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели ApplicationMedicalInsurance
    """

    list_display = (
        "id",
        "count",
        "price",
        "total_price",
    )


@admin.register(ApplicationCancellationInsurance)
class CancellationInsuranceApplicationAdmin(admin.ModelAdmin):
    """
    Админ панель для модели ApplicationCancellationInsurance
    """

    list_display = (
        "id",
        "total_price",
    )
