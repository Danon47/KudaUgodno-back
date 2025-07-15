from django.db.models.expressions import RawSQL
from django_filters import DateFromToRangeFilter, FilterSet
from rest_framework.exceptions import ValidationError

from rooms.models import Room


def annotate_with_prices(queryset, start_date, end_date):
    if start_date > end_date:
        raise ValidationError("start_date должна быть меньше end_date")

    nights = (end_date - start_date).days
    if nights < 0:
        nights = 0

    price_sql = """
        WITH date_series AS (
            SELECT generate_series(%s::date, (%s::date - interval '1 day'), interval '1 day')::date AS day
        )
        SELECT 
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
    """

    params = (start_date, end_date)
    queryset = queryset.annotate(
        total_price_without_discount=RawSQL(
            f"SELECT (SELECT total_price_without_discount FROM ({price_sql}) AS subquery)",
            params,
        ),
        total_price_with_discount=RawSQL(
            f"SELECT (SELECT total_price_with_discount FROM ({price_sql}) AS subquery)",
            params,
        ),
    )
    return queryset


class RoomFilter(FilterSet):
    date_range = DateFromToRangeFilter(
        method="filter_date_range",
        label="Диапазон дат (YYYY-MM-DD)",
    )

    class Meta:
        model = Room
        fields = ("date_range",)

    def filter_date_range(self, queryset, name, value):
        start_date = value.start
        end_date = value.stop
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Дата начала должна быть раньше даты окончания")
            queryset = queryset.filter(
                calendar_dates__start_date__lte=end_date,
                calendar_dates__end_date__gte=start_date,
                calendar_dates__available_for_booking=True,
            ).distinct()
            return annotate_with_prices(queryset, start_date, end_date)
        return queryset

    @property
    def qs(self):
        qs = super().qs
        return qs.distinct()
