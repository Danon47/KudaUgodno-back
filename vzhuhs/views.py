import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from all_fixture.fixture_views import vzhuh_settings
from vzhuhs.models import Vzhuh
from vzhuhs.serializers import VzhuhSerializer


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="Список Вжухов", tags=[vzhuh_settings["name"]], operation_id="vzhuh_list"),
    retrieve=extend_schema(exclude=True),
)
class VzhuhViewSet(ReadOnlyModelViewSet):
    """Только список опубликованных Вжухов."""

    queryset = Vzhuh.objects.filter(is_published=True)
    serializer_class = VzhuhSerializer
