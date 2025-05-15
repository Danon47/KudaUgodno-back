from django_filters import rest_framework as filters

from vzhuh.models import Vzhuh


class VzhuhFilterSet(filters.FilterSet):
    departure_city = filters.CharFilter(lookup_expr="icontains", label="Город вылета (поиск по вхождению)")
    arrival_city = filters.CharFilter(lookup_expr="icontains", label="Город прибытия (поиск по вхождению)")
    created_after = filters.DateFilter(field_name="created_at", lookup_expr="gte", label="Создан после даты")
    created_before = filters.DateFilter(field_name="created_at", lookup_expr="lte", label="Создан до даты")
    updated_after = filters.DateFilter(field_name="updated_at", lookup_expr="gte", label="Обновлён после")
    updated_before = filters.DateFilter(field_name="updated_at", lookup_expr="lte", label="Обновлён до")
    tour_date_after = filters.DateFilter(
        field_name="tours__start_date", lookup_expr="gte", label="Начало тура не раньше"
    )
    tour_date_before = filters.DateFilter(
        field_name="tours__start_date", lookup_expr="lte", label="Начало тура не позже"
    )
    is_published = filters.BooleanFilter(field_name="is_published", label="Опубликован")

    class Meta:
        model = Vzhuh
        fields = [
            "departure_city",
            "arrival_city",
            "is_published",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
            "tour_date_after",
            "tour_date_before",
        ]
