from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from promocodes.models import Promocode, PromocodePhoto
from promocodes.serializers import (
    PromoCodeCheckSerializer,
    PromocodePhotoSerializer,
    PromocodeSerializer,
)


@extend_schema_view(
    list=extend_schema(
        responses={
            200: OpenApiResponse(
                response=PromocodeSerializer(many=True),
                description="Пример списка промокодов",
            ),
        }
    ),
    create=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
)
class PromocodesModelViewSet(viewsets.ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer


@extend_schema_view(
    list=extend_schema(exclude=True),
    create=extend_schema(exclude=True),
    retrieve=extend_schema(exclude=True),
    update=extend_schema(exclude=True),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(exclude=True),
)
class PromocodesPhotoModelViewSet(viewsets.ModelViewSet):
    queryset = PromocodePhoto.objects.all()
    serializer_class = PromocodePhotoSerializer


@extend_schema_view(
    post=extend_schema(
        request=PromoCodeCheckSerializer,
        responses={
            200: PromoCodeCheckSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
)
class PromoCodeCheckView(APIView):
    def post(self, request):
        serializer = PromoCodeCheckSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)
