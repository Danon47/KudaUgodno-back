import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ReadOnlyModelViewSet

from vzhuh.models import Vzhuh
from vzhuh.serializers import VzhuhSerializer


logger = logging.getLogger(__name__)

vzhuh_settings = {
    "name": "Вжухи",
    "description": "Список актуальных спецпредложений по направлениям",
}


@extend_schema_view(
    list=extend_schema(summary="Список Вжухов", tags=["Вжухи"], operation_id="vzhuh_list"),
    retrieve=extend_schema(exclude=True),
)
class VzhuhViewSet(ReadOnlyModelViewSet):
    """Только список опубликованных Вжухов."""

    queryset = Vzhuh.objects.filter(is_published=True)
    serializer_class = VzhuhSerializer
