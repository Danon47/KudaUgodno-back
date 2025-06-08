from datetime import datetime, timedelta

from django.db.models import Exists, F, OuterRef, Prefetch, Q, Subquery
from django.utils import timezone
from django_filters import CharFilter, DateFilter, FilterSet, NumberFilter

from all_fixture.fixture_views import MAX_DAYS_CHECK_OUT
from hotels.models import Hotel
from rooms.models import Room, RoomCategory


class BaseHotelFilter(FilterSet):
    """Базовый класс фильтров для отелей."""

    hotel_city = CharFilter(field_name="city", lookup_expr="iexact")
    check_in_date = DateFilter(method="filter_by_dates")
    check_out_date = DateFilter(method="filter_by_dates")
    guests = NumberFilter(method="filter_by_guests")

    class Meta:
        model = Hotel
        fields = []

    def filter_by_guests(self, queryset, name, value):
        """Инициализация гостей для поиска."""
        try:
            self.guests_value = int(value)
            return queryset
        except (ValueError, TypeError):
            return queryset.none()

    def filter_by_dates(self, queryset, name, value):
        """Инициализация дат для поиска."""
        if name == "check_out_date" and not self.data.get("check_in_date"):
            self.data = self.data.copy()
            self.data["check_in_date"] = timezone.now().date().isoformat()
        elif name == "check_in_date" and not self.data.get("check_out_date"):
            self.data = self.data.copy()
            self.data["check_out_date"] = (timezone.now().date() + timedelta(days=MAX_DAYS_CHECK_OUT)).isoformat()
        return queryset

    def _get_date_filters(self):
        """Поиск доступных комнат по датам в RoomDate."""
        check_in = self.data.get("check_in_date")
        check_out = self.data.get("check_out_date")
        if not check_in and not check_out:
            return Q()
        if not check_in:
            check_in = timezone.now().date().isoformat()
            self.data["check_in_date"] = check_in
        try:
            check_in_obj = datetime.strptime(check_in, "%Y-%m-%d").date()
            if check_out:
                check_out_obj = datetime.strptime(check_out, "%Y-%m-%d").date()
                date_filter = Q(
                    room_date__available_for_booking=True,
                    room_date__start_date__lte=check_out_obj,
                    room_date__end_date__gte=check_in_obj,
                    room=OuterRef("pk"),
                )
            else:
                date_filter = Q(
                    room_date__available_for_booking=True, room_date__start_date__gte=check_in_obj, room=OuterRef("pk")
                )
            return Q(Exists(RoomCategory.objects.filter(date_filter)))
        except ValueError:
            return Q()

    def build_room_queryset(self):
        """ "Построение запроса для поиска комнат."""
        room_query = Room.objects.all()
        if hasattr(self, "guests_value"):
            room_query = room_query.annotate(total_guests=F("number_of_adults") + F("number_of_children")).filter(
                total_guests__gte=self.guests_value
            )
        date_filters = self._get_date_filters()
        if date_filters:
            room_query = room_query.filter(date_filters).distinct()
        return room_query

    def apply_common_filters(self, queryset):
        """Построение запроса для отелей с доступными комнатами."""
        room_query = self.build_room_queryset()
        hotel_ids = room_query.values_list("hotel_id", flat=True).distinct()
        if not hotel_ids:
            return queryset.none()
        self.room_ids = room_query.values_list("id", flat=True).distinct()
        return (
            queryset.filter(id__in=hotel_ids)
            .prefetch_related(Prefetch("rooms", queryset=room_query, to_attr="filtered_rooms"))
            .distinct()
        )


class HotelSearchFilter(BaseHotelFilter):
    """Класс фильтров для поиска отелей."""

    def filter_queryset(self, queryset):
        """Построение основного запроса с вычислением минимальной цены комнаты по отелю."""
        queryset = super().filter_queryset(queryset)
        queryset = self.apply_common_filters(queryset)
        if not getattr(self, "room_ids", None):
            return queryset
        check_in = self.data.get("check_in_date")
        check_out = self.data.get("check_out_date")
        if not check_in or not check_out:
            return queryset
        try:
            check_in_obj = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_obj = datetime.strptime(check_out, "%Y-%m-%d").date()
            min_price_subquery = (
                RoomCategory.objects.filter(
                    room_date__available_for_booking=True,
                    room_date__start_date__lte=check_out_obj,
                    room_date__end_date__gte=check_in_obj,
                    room_id__in=self.room_ids,
                    room__hotel=OuterRef("pk"),
                )
                .order_by("price")
                .values("price")[:1]
            )
            return queryset.annotate(min_price=Subquery(min_price_subquery))
        except ValueError:
            return queryset


class HotelExtendedFilter(HotelSearchFilter):
    """Класс фильтров для расширенного поиска отелей."""

    city = CharFilter(field_name="city", lookup_expr="iexact")
    type_of_rest = CharFilter(field_name="type_of_rest", lookup_expr="exact")
    place = CharFilter(field_name="place", lookup_expr="exact")
    price_gte = NumberFilter(method="filter_price")
    price_lte = NumberFilter(method="filter_price")
    user_rating = NumberFilter(field_name="user_rating", lookup_expr="gte")
    star_category = NumberFilter(field_name="star_category", lookup_expr="gte")

    def filter_price(self, queryset, name, value):
        """Инициализация цен для поиска."""
        try:
            value = float(value)
            if name == "price_gte":
                self.price_gte_value = value
            elif name == "price_lte":
                self.price_lte_value = value
            return queryset
        except (ValueError, TypeError):
            return queryset.none()

    def build_room_queryset(self):
        """ "Построение запроса для поиска комнат."""
        room_query = super().build_room_queryset()
        price_filters = Q()
        if hasattr(self, "price_gte_value"):
            price_filters &= Q(price__gte=self.price_gte_value)
        if hasattr(self, "price_lte_value"):
            price_filters &= Q(price__lte=self.price_lte_value)
        if price_filters:
            room_query = room_query.filter(Exists(RoomCategory.objects.filter(price_filters, room=OuterRef("pk"))))
        return room_query

    def filter_queryset(self, queryset):
        """Построение основного запроса с вычислением минимальной цены доступной комнаты по отелю."""
        queryset = super().filter_queryset(queryset)
        if not getattr(self, "room_ids", None):
            return queryset
        check_in = self.data.get("check_in_date")
        check_out = self.data.get("check_out_date")
        price_gte = getattr(self, "price_gte_value", None)
        price_lte = getattr(self, "price_lte_value", None)
        try:
            if check_in and check_out:
                check_in_obj = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_obj = datetime.strptime(check_out, "%Y-%m-%d").date()
                price_filters = Q(
                    room_date__available_for_booking=True,
                    room_date__start_date__lte=check_out_obj,
                    room_date__end_date__gte=check_in_obj,
                )
            else:
                price_filters = Q(room_date__available_for_booking=True)
            if price_gte is not None:
                price_filters &= Q(price__gte=price_gte)
            if price_lte is not None:
                price_filters &= Q(price__lte=price_lte)
            min_price_subquery = (
                RoomCategory.objects.filter(price_filters, room_id__in=self.room_ids, room__hotel=OuterRef("pk"))
                .order_by("price")
                .values("price")[:1]
            )
            return queryset.annotate(min_price=Subquery(min_price_subquery))
        except ValueError:
            return queryset
