from datetime import timedelta

from django.db.models import F, Q
from django_filters import (
    ChoiceFilter,
    DateFilter,
    FilterSet,
    MultipleChoiceFilter,
    NumberFilter,
    NumericRangeFilter,
)
from rest_framework.exceptions import ValidationError

from all_fixture.choices import PlaceChoices, TypeOfHolidayChoices
from all_fixture.views_fixture import MAX_PRICE, MAX_STARS, MIN_PRICE, MIN_STARS
from tours.models import Tour
from users.models import User


class TourFilter(FilterSet):
    """Фильтры для расширенного поиска туров."""

    departure_city = ChoiceFilter(
        field_name="departure_city",
        lookup_expr="iexact",
        label="Город вылета",
        choices=[
            (name, name)
            for name in Tour.objects.values_list("departure_city", flat=True).distinct().order_by("departure_city")
            if name
        ],
    )
    arrival_country = MultipleChoiceFilter(
        field_name="arrival_country",
        lookup_expr="iexact",
        label="Страна прибытия",
        choices=[
            (name, name)
            for name in Tour.objects.values_list("arrival_country", flat=True).distinct().order_by("arrival_country")
            if name
        ],
    )
    arrival_city = MultipleChoiceFilter(
        field_name="arrival_city",
        lookup_expr="iexact",
        label="Город прибытия",
        choices=[
            (name, name)
            for name in Tour.objects.values_list("arrival_city", flat=True).distinct().order_by("arrival_city")
            if name
        ],
    )
    start_date = DateFilter(
        field_name="start_date",
        # lookup_expr="gte",
        label="Дата начала тура",
    )
    nights = NumberFilter(
        method="filter_by_nights",
        label="Количество ночей",
    )
    type_of_rest = ChoiceFilter(
        field_name="hotel__type_of_rest",
        label="Тип отдыха",
        choices=TypeOfHolidayChoices.choices,
    )
    place = ChoiceFilter(
        field_name="hotel__place",
        choices=PlaceChoices.choices,
        label="Тип размещения",
    )
    price = NumericRangeFilter(
        method="filter_by_price",
        label=f"Диапазон цен стоимости тура (от {MIN_PRICE} до {MAX_PRICE})",
    )
    user_rating = NumberFilter(
        field_name="hotel__user_rating",
        lookup_expr="gte",
        label="Рейтинг отеля",
    )
    star_category = MultipleChoiceFilter(
        field_name="hotel__star_category",
        choices=[(i, i) for i in range(MIN_STARS, MAX_STARS + 1)],
        label=f"Категория отеля (от {MIN_STARS} до {MAX_STARS})",
    )
    distance_to_the_airport = NumberFilter(
        field_name="hotel__distance_to_the_airport",
        lookup_expr="gte",
        label="Расстояние до аэропорта",
    )
    tour_operator = ChoiceFilter(
        field_name="tour_operator__company_name",
        choices=[
            (name, name)
            for name in User.objects.values_list("company_name", flat=True).distinct().order_by("company_name")
            if name
        ],
        lookup_expr="exact",
        label="Туроператор",
    )
    number_of_adults = NumberFilter(
        field_name="rooms__number_of_adults",
        label="Количество взрослых",
    )
    number_of_children = NumberFilter(
        field_name="rooms__number_of_children",
        lookup_expr="gte",
        label="Количество детей до 17 лет",
    )

    class Meta:
        model = Tour
        fields = []

    def _validate_price(self, value):
        """Валидация цены."""
        price_gte = None
        price_lte = None
        if value.start is not None:
            try:
                price_gte = float(value.start)
                if price_gte < MIN_PRICE:
                    raise ValidationError({"price": f"Минимальная цена не может быть меньше {MIN_PRICE}"})
            except (ValueError, TypeError) as e:
                raise ValidationError({"price": "Минимальная цена должна быть числом"}) from e
        if value.stop is not None:
            try:
                price_lte = float(value.stop)
                if price_lte > MAX_PRICE:
                    raise ValidationError({"price": f"Максимальная цена не может быть больше {MAX_PRICE}"})
            except (ValueError, TypeError) as e:
                raise ValidationError({"price": "Максимальная цена должна быть числом"}) from e
        if price_gte is not None and price_lte is not None and price_gte > price_lte:
            raise ValidationError({"price": "Минимальная цена не может быть больше максимальной цены"})
        return price_gte, price_lte

    def filter_by_nights(self, queryset, name, value):
        """Фильтрация по 'start_date'."""
        try:
            nights = int(value)
            return queryset.filter(
                end_date__gte=F("start_date") + timedelta(days=nights),
            )
        except (ValueError, TypeError):
            return queryset.none()

    def filter_by_price(self, queryset, name, value):
        """Фильтрация по цене."""
        self.price_gte, self.price_lte = self._validate_price(value)
        return queryset

    def filter_queryset(self, queryset):
        """Основная фильтрация с обработкой ошибок валидации."""
        try:
            queryset = super().filter_queryset(queryset)
            if hasattr(self, "price_gte") or hasattr(self, "price_lte"):
                price_filter = Q()
                if hasattr(self, "price_gte") and self.price_gte:
                    price_filter &= Q(total_price__gte=self.price_gte)
                if hasattr(self, "price_lte") and self.price_lte:
                    price_filter &= Q(total_price__lte=self.price_lte)
                queryset = queryset.filter(price_filter)
            return queryset.distinct().order_by("total_price")
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({"error": str(e)}) from None
