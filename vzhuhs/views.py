import logging

from dal import autocomplete
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from all_fixture.fixture_views import vzhuh_settings
from hotels.models import Hotel
from tours.models import Tour
from vzhuhs.models import Vzhuh
from vzhuhs.serializers import VzhuhSerializer


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="Список Вжухов",
        tags=[vzhuh_settings["name"]],
        parameters=[
            OpenApiParameter(
                name="departure_city",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Фильтр по городу вылета",
                required=False,
            ),
        ],
    ),
    retrieve=extend_schema(exclude=True),
)
class VzhuhViewSet(ReadOnlyModelViewSet):
    """
    Представление только для чтения (ReadOnly) опубликованных объектов модели Vzhuh.

    - Использует сериализатор `VzhuhSerializer`

    - Возвращает только записи с `is_published=True`

    - Эндпоинт отображается в Swagger как "Список Вжухов"

    - Добавлена фильтрация по `departure_city` - городу отправления
    """

    queryset = Vzhuh.objects.prefetch_related(
        "tours__hotel__hotel_photos",
        "tours__stock",
        "hotels__tours",
        "hotels__hotel_photos",
        "photos",
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("departure_city",)
    serializer_class = VzhuhSerializer


class VzhuhAutocompleteHotel(autocomplete.Select2QuerySetView):
    """
    Autocomplete-представление для выбора отелей, отфильтрованных по городу прибытия
    и исключающих уже выбранные отели.

    Используется в админке при создании/редактировании объекта Vzhuh.
    """

    def get_queryset(self):
        qs = Hotel.objects.all()
        arrival_city = self.forwarded.get("arrival_city")
        selected_ids = self.forwarded.get("hotels", [])

        if arrival_city:
            qs = qs.filter(city__icontains=arrival_city)
        if selected_ids:
            qs = qs.exclude(id__in=selected_ids)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class VzhuhAutocompleteTour(autocomplete.Select2QuerySetView):
    """
    Autocomplete-представление для выбора туров, отфильтрованных по городу прибытия
    и исключающих уже выбранные туры.

    Используется в админке при создании/редактировании объекта Vzhuh.
    """

    def get_queryset(self):
        qs = Tour.objects.all()
        arrival_city = self.forwarded.get("arrival_city")
        selected_ids = self.forwarded.get("tours", [])

        if arrival_city:
            qs = qs.filter(arrival_city__icontains=arrival_city)
        if selected_ids:
            qs = qs.exclude(id__in=selected_ids)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
