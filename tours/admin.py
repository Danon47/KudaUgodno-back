from django.contrib import admin

from tours.models import Tour


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_date",
        "end_date",
        "flight_to",
        "flight_from",  # <-- было дублирование flight_to
        "get_tour_operator_name",  # <-- красивое отображение компании
        "arrival_city",
        "hotel",
        "price",
        "room",
    )
    list_filter = ("tour_operator",)
    search_fields = ("start_date", "hotel__name", "tour_operator__company_name")

    @admin.display(description="Туроператор")
    def get_tour_operator_name(self, obj):
        if obj.tour_operator:
            return obj.tour_operator.company_name or obj.tour_operator.email
        return "-"
