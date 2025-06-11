from django.contrib import admin

from promocodes.models import Promocode, PromocodePhoto


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "start_date", "end_date", "discount_amount", "description")
    list_filter = ("tours", "hotels")
    search_fields = ("name", "description")


@admin.register(PromocodePhoto)
class PromocodePhotoAdmin(admin.ModelAdmin):
    list_display = ("promocode", "image")
