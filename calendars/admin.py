from django.contrib import admin

from calendars.models import CalendarDate, CalendarPrice


@admin.register(CalendarPrice)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "price", "room", "calendar_date")
    list_filter = ("calendar_date__hotel",)


@admin.register(CalendarDate)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "hotel", "start_date", "end_date")
    list_filter = ("hotel",)
