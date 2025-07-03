from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from all_fixture.views_fixture import INSURANCE_ID, INSURANCE_SETTINGS
from insurances.models import Insurances
from insurances.serializers import InsuranceSerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary="Информация о страховке",
        description="Получение информации о страховке",
        tags=[INSURANCE_SETTINGS["name"]],
        parameters=[INSURANCE_ID],
        responses={
            200: InsuranceSerializer,
            404: OpenApiResponse(description="Страховка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление страховки",
        description="Обновление всех полей страховки",
        request=InsuranceSerializer,
        tags=[INSURANCE_SETTINGS["name"]],
        parameters=[INSURANCE_ID],
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
