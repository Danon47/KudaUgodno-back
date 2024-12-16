from django.contrib import admin

from tours.models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'name',
            'start_date',
            'end_date',
            'flight_to',
            'flight_to',
            'tour_operator',
            'hotel',
            'room',
            'country',
            'city',
            'type_of_holiday',
            'meal_cost',
            'price'
        )
    list_filter = ("tour_operator", "country")
    search_fields = ("start_date", "hotel")
