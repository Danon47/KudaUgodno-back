from datetime import date, datetime

from django.db.models import IntegerField, OuterRef, Q, Subquery, Value
from django.db.models.expressions import RawSQL
from django_filters import (
    BooleanFilter,
    ChoiceFilter,
    DateFromToRangeFilter,
    FilterSet,
    MultipleChoiceFilter,
    NumberFilter,
    RangeFilter,
)
from rest_framework.exceptions import ValidationError

from all_fixture.choices import AmenitiesChoices, PlaceChoices, TypeOfHolidayChoices, TypeOfMealChoices
from all_fixture.filters.filter_fixture import filter_choices
from all_fixture.views_fixture import (
    MAX_ADULT_CHILDREN,
    MAX_DAYS,
    MAX_PRICE,
    MAX_RATING,
    MAX_STARS,
    MIN_ADULT,
    MIN_CHILDREN,
    MIN_PRICE,
    MIN_RATING,
    MIN_STARS,
)
from hotels.models import Hotel
from rooms.models import Room


class HotelFilter(FilterSet):
    """Класс фильтров для расширенного поиска отелей."""

    date_range = DateFromToRangeFilter(
        method="filter_by_dates",
        label="Диапазон дат в формате (YYYY-MM-DD)",
    )
    country = MultipleChoiceFilter(
        field_name="country",
        lookup_expr="iexact",
        label="Страна отеля",
        choices=filter_choices(model=Hotel, field="country"),
    )
    city = MultipleChoiceFilter(
        field_name="city",
        lookup_expr="iexact",
        label="Город отеля",
        choices=filter_choices(model=Hotel, field="city"),
    )
    type_of_rest = ChoiceFilter(
        field_name="type_of_rest",
        label="Тип отдыха",
        choices=TypeOfHolidayChoices.choices,
    )
    place = ChoiceFilter(
        field_name="place",
        label="Тип размещения",
        choices=PlaceChoices.choices,
    )
    type_of_meals = MultipleChoiceFilter(
        field_name="type_of_meals__name",
        label="Тип питания",
        choices=TypeOfMealChoices.choices,
    )
    number_of_adults = NumberFilter(
        field_name="rooms__number_of_adults",
        label="Количество взрослых",
    )
    number_of_children = NumberFilter(
        field_name="rooms__number_of_children",
        label="Количество детей до 17 лет",
    )
    price = RangeFilter(
        method="filter_by_price",
        label=f"Диапазон цен стоимости тура (от {MIN_PRICE} до {MAX_PRICE})",
    )
    user_rating = NumberFilter(
        field_name="user_rating",
        label=f"Пользовательская оценка (от {MIN_RATING} до {MAX_RATING})",
        lookup_expr="gte",
    )
    star_category = MultipleChoiceFilter(
        field_name="star_category",
        choices=[(i, str(i)) for i in range(MIN_STARS, MAX_STARS + 1)],
        label=f"Категория отеля (от {MIN_STARS} до {MAX_STARS})",
        lookup_expr="exact",
    )
    amenities = MultipleChoiceFilter(
        method="filter_by_amenities",
        label="Удобства",
        choices=AmenitiesChoices.choices,
    )
    number_of_adults = NumberFilter(
        method="filter_adults",
        label=f"Количество взрослых от {MIN_ADULT} человек",
    )
    number_of_children = NumberFilter(
        method="filter_childrens",
        label=f"Количество детей до 17 лет от {MIN_CHILDREN} человек",
    )
    is_active = BooleanFilter(
        method="filter_active",
        label="Тур активен?",
    )

    class Meta:
        model = Hotel
        fields = []

    def filter_active(self, queryset, name, value):
        self.is_active = value
        return queryset.filter(is_active=value)

    def _annotate_with_prices(self, queryset, start_date, end_date):
        price_sql = """
            WITH date_series AS (
                SELECT generate_series(%s::date, (%s::date - interval '1 day'), interval '1 day')::date AS day
            ),
            missing_days AS (
                SELECT r.id as room_id
                FROM date_series ds
                JOIN rooms_room r ON r.hotel_id = hotels_hotel.id
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM calendars_calendardate cd
                    JOIN calendars_calendarprice cp ON cp.calendar_date_id = cd.id
                    WHERE cp.room_id = r.id
                    AND ds.day BETWEEN cd.start_date AND cd.end_date
                )
                GROUP BY r.id
            ),
            room_prices AS (
                SELECT
                    r.id as room_id,
                    SUM(cp.price) as total_price_without_discount,
                    SUM(
                        CASE
                            WHEN cd.discount = TRUE AND cd.discount_amount IS NOT NULL THEN
                                CASE
                                    WHEN cd.discount_amount <= 1.0 THEN GREATEST(cp.price * (1 - cd.discount_amount), 0)
                                    ELSE GREATEST(cp.price - cd.discount_amount, 0)
                                END
                            ELSE cp.price
                        END
                    ) as total_price_with_discount
                FROM date_series ds
                JOIN rooms_room r ON r.hotel_id = hotels_hotel.id
                JOIN calendars_calendardate cd ON ds.day BETWEEN cd.start_date AND cd.end_date
                JOIN calendars_calendarprice cp ON cp.calendar_date_id = cd.id AND cp.room_id = r.id
                WHERE r.id NOT IN (SELECT room_id FROM missing_days)
                GROUP BY r.id
            )
            SELECT
                MIN(total_price_without_discount) as min_price_without_discount,
                MIN(total_price_with_discount) as min_price_with_discount
            FROM room_prices
        """
        params = (start_date, end_date)
        queryset = queryset.annotate(
            min_price_without_discount=RawSQL(
                f"SELECT min_price_without_discount FROM ({price_sql}) AS subquery",
                params,
            ),
            min_price_with_discount=RawSQL(
                f"SELECT min_price_with_discount FROM ({price_sql}) AS subquery",
                params,
            ),
            date_range_after=Value(start_date),
            date_range_before=Value(end_date),
            nights=Value((end_date - start_date).days),
        ).exclude(min_price_with_discount__isnull=True)
        return queryset

    def _validate_price(self, value):
        """Валидация цены."""
        if value.start is not None:
            price_min = float(value.start)
            if price_min < MIN_PRICE:
                raise ValidationError({"price": f"Минимальная цена не может быть меньше {MIN_PRICE}"})
        if value.stop is not None:
            price_max = float(value.stop)
            if price_max > MAX_PRICE:
                raise ValidationError({"price": f"Максимальная цена не может быть больше {MAX_PRICE}"})
        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError({"price": "Минимальная цена не может быть больше максимальной цены"})
        return price_min, price_max

    def filter_by_price(self, queryset, name, value):
        """Фильтрация по цене."""
        price_min, price_max = self._validate_price(value)
        price_filter = Q()
        if price_min:
            price_filter &= Q(min_price_with_discount__gte=price_min)
        if price_max:
            price_filter &= Q(min_price_with_discount__lte=price_max)
        queryset = queryset.filter(price_filter).order_by("min_price_with_discount")
        return queryset

    def _validate_date_range(self, value):
        """Валидация диапазона дат."""
        try:
            date_range_after = value.start.date() if isinstance(value.start, datetime) else value.start
            date_range_before = value.stop.date() if isinstance(value.stop, datetime) else value.stop
            if date_range_after < date.today():
                raise ValidationError({"date_range": "Дата заезда не может быть в прошлом"})
            if (date_range_before - date_range_after).days > MAX_DAYS:
                raise ValidationError({"date_range": f"Максимальный срок проживания - {MAX_DAYS} дней"})
            if date_range_before <= date_range_after:
                raise ValidationError({"date_range": "Дата выезда должна быть позже даты заезда"})
            return date_range_after, date_range_before
        except (TypeError, ValueError) as e:
            raise ValidationError({"date_range": "Неверный формат дат. Используйте YYYY-MM-DD"}) from e

    def filter_by_dates(self, queryset, name, value):
        """Фильтрация по датам."""
        date_range_after, date_range_before = self._validate_date_range(value)
        available_hotels_filter = Q(
            rooms__calendar_dates__start_date__lte=date_range_before,
            rooms__calendar_dates__end_date__gte=date_range_after,
            rooms__calendar_dates__available_for_booking=True,
        )
        queryset = queryset.filter(available_hotels_filter)
        queryset = self._annotate_with_prices(queryset, date_range_after, date_range_before)
        return queryset

    def filter_by_amenities(self, queryset, name, value):
        """Фильтрация по удобствам в полях amenities_*."""
        if not value:
            return queryset
        query = Q()
        for amenity in value:
            query |= (
                Q(amenities_common__contains=[amenity])
                | Q(amenities_in_the_room__contains=[amenity])
                | Q(amenities_sports_and_recreation__contains=[amenity])
                | Q(amenities_for_children__contains=[amenity])
            )
        return queryset.filter(query)

    def filter_adults(self, queryset, name, value):
        self.number_of_adults = value
        return queryset

    def filter_childrens(self, queryset, name, value):
        self.number_of_children = value
        return queryset

    def _filter_guests(self, queryset):
        adults_min = getattr(self, "number_of_adults", None)
        children_min = getattr(self, "number_of_children", None)

        if adults_min is None:
            adults_min = MIN_ADULT
            adults_max = MAX_ADULT_CHILDREN
        else:
            adults_max = adults_min + 1

        if children_min is None:
            children_min = MIN_CHILDREN
            children_max = MAX_ADULT_CHILDREN
        else:
            children_max = children_min + 1

        rooms_subquery = Room.objects.filter(
            hotel=OuterRef("pk"),
            number_of_adults__gte=adults_min,
            number_of_adults__lte=adults_max,
            number_of_children__gte=children_min,
            number_of_children__lte=children_max,
        ).order_by("number_of_adults", "number_of_children")

        queryset = queryset.annotate(
            number_of_adults=Subquery(rooms_subquery.values("number_of_adults")[:1], output_field=IntegerField()),
            number_of_children=Subquery(rooms_subquery.values("number_of_children")[:1], output_field=IntegerField()),
        ).filter(number_of_adults__isnull=False, number_of_children__isnull=False)
        return queryset

    def filter_queryset(self, queryset):
        """Основная фильтрация с учетом всех параметров."""
        try:
            queryset = super().filter_queryset(queryset)
            queryset = self._filter_guests(queryset)
            if not hasattr(self, "is_active"):
                queryset = queryset.filter(is_active=True)
            return queryset
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({"error": str(e)}) from None
