from django.db.models import F, Prefetch, Q
from django_filters import CharFilter, DateFilter, FilterSet, NumberFilter

from hotels.models import Hotel
from rooms.models import Room


class BaseHotelFilter(FilterSet):
    """Базовый класс фильтров для отелей с общими методами."""

    hotel_city = CharFilter(field_name="city", lookup_expr="iexact")
    check_in_date = DateFilter(method="filter_by_dates")
    check_out_date = DateFilter(method="filter_by_dates")
    guests = NumberFilter(method="filter_by_guests")

    class Meta:
        model = Hotel
        fields = []

    def filter_by_guests(self, queryset, name, value):
        """Фильтрация по количеству гостей."""
        try:
            self.guests_value = int(value)
            return queryset
        except (ValueError, TypeError):
            return queryset.none()

    def filter_by_dates(self, queryset, name, value):
        """Фильтрация по датам (базовая реализация)."""
        return queryset

    def build_room_queryset(self):
        """Создает базовый QuerySet для номеров с общими фильтрами."""
        room_query = Room.objects.all()

        if hasattr(self, "guests_value"):
            room_query = room_query.annotate(total_guests=F("number_of_adults") + F("number_of_children")).filter(
                total_guests__gte=self.guests_value
            )

        return room_query

    def apply_common_filters(self, queryset):
        """Применяет общие фильтры для отелей и номеров."""
        room_query = self.build_room_queryset()
        hotel_ids = room_query.values_list("hotel_id", flat=True).distinct()

        return (
            queryset.filter(id__in=hotel_ids)
            .prefetch_related(Prefetch("rooms", queryset=room_query, to_attr="filtered_rooms"))
            .distinct()
        )


class HotelSearchFilter(BaseHotelFilter):
    """Фильтр для базового поиска отелей."""

    def filter_queryset(self, queryset):
        """Основная логика фильтрации."""
        queryset = super().filter_queryset(queryset)
        return self.apply_common_filters(queryset)


class HotelExtendedFilter(BaseHotelFilter):
    """Расширенный фильтр с дополнительными параметрами поиска."""

    # Фильтры по отелям
    city = CharFilter(field_name="city", lookup_expr="iexact")
    type_of_rest = CharFilter(field_name="type_of_rest", lookup_expr="exact")
    place = CharFilter(field_name="place", lookup_expr="exact")
    price_gte = NumberFilter(method="filter_price")
    price_lte = NumberFilter(method="filter_price")
    user_rating = NumberFilter(field_name="user_rating", lookup_expr="gte")
    star_category = NumberFilter(field_name="star_category", lookup_expr="gte")

    def filter_price(self, queryset, name, value):
        """Фильтрация по цене номера."""
        try:
            value = float(value)
            if name == "price_gte":
                return queryset.filter(rooms__price__gte=value).distinct()
            elif name == "price_lte":
                return queryset.filter(rooms__price__lte=value).distinct()
            return queryset
        except (ValueError, TypeError):
            return queryset.none()

    def build_room_queryset(self):
        """Расширенная версия с дополнительными фильтрами для номеров."""
        room_query = super().build_room_queryset()

        # Фильтрация по цене
        price_filters = self._get_price_filters()
        if price_filters:
            room_query = room_query.filter(price_filters)
        return room_query

    def _get_price_filters(self):
        """Создает Q-объекты для фильтрации по цене."""
        price_filters = Q()
        if "price_gte" in self.data:
            try:
                price_filters &= Q(price__gte=float(self.data["price_gte"]))
            except (ValueError, TypeError):
                pass
        if "price_lte" in self.data:
            try:
                price_filters &= Q(price__lte=float(self.data["price_lte"]))
            except (ValueError, TypeError):
                pass
        return price_filters

    def filter_queryset(self, queryset):
        """Основная логика фильтрации с дополнительными условиями."""
        queryset = super().filter_queryset(queryset)
        return self.apply_common_filters(queryset)
