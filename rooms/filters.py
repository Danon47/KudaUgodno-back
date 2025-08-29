from datetime import date, datetime

from django.db.models import Prefetch
from django.db.models.expressions import RawSQL
from django_filters import (
    DateFromToRangeFilter,
    FilterSet,
    MultipleChoiceFilter,
)
from rest_framework.exceptions import ValidationError

from all_fixture.choices import RoomCategoryChoices
from all_fixture.views_fixture import MAX_DAYS
from calendars.models import CalendarDate
from rooms.models import Room


def annotate_with_prices(queryset, start_date, end_date):
    total_nights = max((end_date - start_date).days, 1)

    price_sql = """
        WITH date_series AS (
            SELECT generate_series(%s::date, (%s::date - interval '1 day'), interval '1 day')::date AS day
        ),
        calculations AS (
            SELECT 
                COUNT(DISTINCT CASE WHEN cd.available_for_booking = TRUE THEN ds.day END) AS nights,
                COALESCE(SUM(cp.price), 0) AS total_price_without_discount,
                COALESCE(
                    SUM(
                        CASE 
                            WHEN cd.discount = TRUE AND cd.discount_amount IS NOT NULL THEN 
                                CASE 
                                    WHEN cd.discount_amount <= 1.0 THEN GREATEST(cp.price * (1 - cd.discount_amount), 0)
                                    ELSE GREATEST(cp.price - cd.discount_amount, 0)
                                END
                            ELSE cp.price
                        END
                    ),
                    0
                ) AS total_price_with_discount
            FROM date_series ds
            JOIN calendars_calendardate cd ON ds.day BETWEEN cd.start_date AND cd.end_date
            JOIN calendars_calendarprice cp ON cp.calendar_date_id = cd.id
            WHERE cp.room_id = rooms_room.id
        )
        SELECT 
            total_price_without_discount AS price_without_discount,
            total_price_with_discount AS price_with_discount,
            nights AS available_count
        FROM calculations
    """

    params = (start_date, end_date)
    queryset = queryset.annotate(
        total_price_without_discount=RawSQL(
            f"SELECT price_without_discount FROM ({price_sql}) AS subquery",
            params,
        ),
        total_price_with_discount=RawSQL(
            f"SELECT price_with_discount FROM ({price_sql}) AS subquery",
            params,
        ),
        nights=RawSQL(
            f"SELECT available_count FROM ({price_sql}) AS subquery",
            params,
        ),
    )
    # Фильтруем по полному покрытию
    queryset = queryset.filter(nights=total_nights)
    return queryset


class RoomFilter(FilterSet):
    date_range = DateFromToRangeFilter(
        method="filter_date_range",
        label="Диапазон дат (YYYY-MM-DD)",
    )
    number_of_adults = MultipleChoiceFilter(
        field_name="number_of_adults",
        choices=[(i, str(i)) for i in range(1, 10)],
        conjoined=False,
        label="Количество взрослых",
    )
    number_of_children = MultipleChoiceFilter(
        field_name="number_of_children",
        choices=[(i, str(i)) for i in range(1, 10)],
        conjoined=False,
        label="Количество детей",
    )
    category = MultipleChoiceFilter(
        field_name="category",
        choices=RoomCategoryChoices.choices,
        label="Категория номера",
    )

    class Meta:
        model = Room
        fields = (
            "date_range",
            "number_of_adults",
            "number_of_children",
            "category",
        )

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

    def filter_date_range(self, queryset, name, value):
        date_range_after, date_range_before = self._validate_date_range(value)
        print(date_range_after, date_range_before)
        queryset = annotate_with_prices(queryset, date_range_after, date_range_before)
        print(date_range_after, date_range_before)
        # Добавляем prefetch_related для отображения дат
        prefetch_queryset = CalendarDate.objects.filter(
            start_date__lte=date_range_before,
            end_date__gte=date_range_after,
            available_for_booking=True,
        )
        queryset = queryset.prefetch_related(Prefetch("calendar_dates", queryset=prefetch_queryset))
        return queryset
