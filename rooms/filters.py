from django.db.models import Q
from django_filters import FilterSet, NumberFilter

from calendars.models import CalendarPrice
from rooms.models import Room


class RoomFilter(FilterSet):
    price_min = NumberFilter(method="filter_by_price_range")
    price_max = NumberFilter(method="filter_by_price_range")

    class Meta:
        model = Room
        fields = ("price_min", "price_max")

    def filter_by_price_range(self, queryset, name, value):
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        price_min = self.data.get("price_min")
        price_max = self.data.get("price_max")

        if price_min or price_max:
            price_filter = Q()
            if price_min:
                price_filter &= Q(price__gte=float(price_min))
            if price_max:
                price_filter &= Q(price__lte=float(price_max))
            room_ids = CalendarPrice.objects.filter(price_filter).values_list("room_id", flat=True).distinct()
            queryset = queryset.filter(id__in=room_ids)
        return queryset
