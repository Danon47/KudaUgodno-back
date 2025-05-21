from datetime import timedelta

from django.db.models import Exists, F, OuterRef
from django_filters import CharFilter, DateFilter, FilterSet, NumberFilter

from hotels.models.room.models_room import Room
from tours.models import Tour


class TourSearchFilter(FilterSet):
    """Фильтры для поиска туров."""

    departure_city = CharFilter(field_name="departure_city", lookup_expr="iexact")
    arrival_city = CharFilter(field_name="arrival_city", lookup_expr="iexact")
    start_date = DateFilter(field_name="start_date", lookup_expr="gte")
    nights = NumberFilter(method="filter_by_nights")
    guests = NumberFilter(method="filter_by_guests")

    class Meta:
        model = Tour
        fields = []

    def filter_by_nights(self, queryset, name, value):
        """Фильтрация по 'start_date'."""
        try:
            nights = int(value)
            return queryset.filter(end_date=F("start_date") + timedelta(days=nights))
        except (ValueError, TypeError):
            return queryset.none()

    def filter_by_guests(self, queryset, name, value):
        """Фильтрация по количеству гостей."""
        try:
            guests = int(value)
            return queryset.filter(
                Exists(
                    Room.objects.filter(hotel=OuterRef("hotel"), category=OuterRef("room"), number_of_adults__gte=1)
                    .annotate(total_guests=F("number_of_adults") + F("number_of_children"))
                    .filter(total_guests__gte=guests)
                )
            )
        except (ValueError, TypeError):
            return queryset.none()


class TourExtendedFilter(TourSearchFilter):
    """Фильтры для расширенного поиска туров."""

    # Фильтры
    city = CharFilter(field_name="hotel__city", lookup_expr="iexact")
    type_of_rest = CharFilter(field_name="hotel__type_of_rest", lookup_expr="exact")
    place = CharFilter(field_name="hotel__place", lookup_expr="exact")
    price_gte = NumberFilter(field_name="price", lookup_expr="gte")
    price_lte = NumberFilter(field_name="price", lookup_expr="lte")
    user_rating = NumberFilter(field_name="hotel__user_rating", lookup_expr="gte")
    star_category = NumberFilter(field_name="hotel__star_category", lookup_expr="gte")
    distance_to_the_airport = NumberFilter(field_name="hotel__distance_to_the_airport", lookup_expr="lte")
    tour_operator = CharFilter(field_name="tour_operator__company_name", lookup_expr="exact")
