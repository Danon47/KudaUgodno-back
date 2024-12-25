from django.contrib import admin

from tours.models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'start_date',
            'end_date',
            'flight_to',
            'flight_to',
            'tour_operator',
            'hotel',
            'price'
        )
    list_filter = ("tour_operator",)
    search_fields = ("start_date", "hotel")
