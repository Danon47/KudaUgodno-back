import logging

from dal import autocomplete
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from all_fixture.fixture_views import vzhuh_settings
from hotels.models import Hotel
from tours.models import Tour
from vzhuhs.models import Vzhuh
from vzhuhs.serializers import VzhuhSerializer


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="Список Вжухов", tags=[vzhuh_settings["name"]], operation_id="vzhuh_list"),
    retrieve=extend_schema(exclude=True),
)
class VzhuhViewSet(ReadOnlyModelViewSet):
    queryset = Vzhuh.objects.filter(is_published=True)
    serializer_class = VzhuhSerializer


class VzhuhAutocompleteHotel(autocomplete.Select2QuerySetView):
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
