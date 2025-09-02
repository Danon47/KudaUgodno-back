from datetime import date

from django.db.models import Q
from django_filters import CharFilter, DateFromToRangeFilter, FilterSet
from rest_framework.exceptions import ValidationError

from flights.models import Flight


class FlightsFilter(FilterSet):
    """Класс фильтров для поиска рейсов."""

    search_field = CharFilter(
        method="filter_search_field",
        label="Поиск по рейсу/стране прилета/городу прилета/авиакомпании",
    )
    date_range = DateFromToRangeFilter(
        method="filter_date_range",
        label="Диапазон дат (YYYY-MM-DD)",
    )
    departure_country = CharFilter(
        field_name="departure_country",
        lookup_expr="exact",
        label="Страна вылета",
    )
    departure_city = CharFilter(
        field_name="departure_city",
        lookup_expr="exact",
        label="Город вылета",
    )
    arrival_country = CharFilter(
        field_name="arrival_country",
        lookup_expr="exact",
        label="Страна прилёта",
    )
    arrival_city = CharFilter(
        field_name="arrival_city",
        lookup_expr="exact",
        label="Город прилёта",
    )
    flight_number = CharFilter(
        field_name="flight_number",
        lookup_expr="exact",
        label="Номер рейса",
    )

    class Meta:
        model = Flight
        fields = []

    def filter_date_range(self, queryset, name, value):
        start_date = value.start
        end_date = value.stop
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Дата начала должна быть раньше даты окончания")
            if start_date < date.today():
                raise ValidationError({self.check_in_field: "Дата заезда не может быть в прошлом"})

            return queryset.filter(departure_date__gte=start_date, arrival_date__lte=end_date)
        elif start_date:
            return queryset.filter(arrival_date__gte=start_date)
        elif end_date:
            return queryset.filter(departure_date__lte=end_date)
        else:
            return queryset

    def filter_search_field(self, queryset, name, value):
        if not value:
            return queryset
        search_items = [item.strip() for item in value.split("_") if item.strip()]
        if not search_items:
            return queryset
        query_objects = Q()
        for item in search_items:
            query_item = (
                Q(arrival_country__icontains=item)
                | Q(arrival_city__icontains=item)
                | Q(airline__icontains=item)
                | Q(flight_number__icontains=item)
            )
            query_objects &= query_item
        return queryset.filter(query_objects)
