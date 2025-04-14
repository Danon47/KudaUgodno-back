from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from all_fixture.fixture_views import insurance_id, insurance_settings
from insurances.models import Insurances
from insurances.serializers import InsuranceSerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary="Информация о страховке",
        description="Получение информации о страховке",
        tags=[insurance_settings["name"]],
        parameters=[insurance_id],
        responses={
            200: InsuranceSerializer,
            404: OpenApiResponse(description="Страховка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление страховки",
        description="Обновление всех полей страховки",
        request=InsuranceSerializer,
        tags=[insurance_settings["name"]],
        parameters=[insurance_id],
        responses={
            200: InsuranceSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Страховка не найдена"),
        },
    ),
)
class InsurancesView(ModelViewSet):
    queryset = Insurances.objects.all()
    serializer_class = InsuranceSerializer
