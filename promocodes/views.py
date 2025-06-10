from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from promocodes.filters import PromocodeFilterBackemd
from promocodes.models import Promocode, PromocodePhoto
from promocodes.serializers import (
    PromocodeListSerializer,
    PromocodePhotoSerializer,
    PromocodeSerializer,
)


class PromocodesModelViewSet(viewsets.ModelViewSet):
    queryset = Promocode.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = PromocodeFilterBackemd

    def get_serializer_class(self):
        if self.action == "list":
            return PromocodeListSerializer
        return PromocodeSerializer


class PromocodesPhotoModelViewSet(viewsets.ModelViewSet):
    queryset = PromocodePhoto.objects.all()
    serializer_class = PromocodePhotoSerializer
