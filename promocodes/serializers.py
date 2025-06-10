from rest_framework.fields import ImageField
from rest_framework.serializers import ModelSerializer

from promocodes.models import Promocode, PromocodePhoto


class PromocodePhotoSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = PromocodePhoto
        fields = ("id", "image")


class PromocodeSerializer(ModelSerializer):

    class Meta:
        model = Promocode
        fields = (
            "id",
            "start_date",
            "end_date",
            "name",
            "code",
            "discount_amount",
            "description",
            "tours",
            "hotels",
            "is_active",
        )


class PromocodeListSerializer(PromocodeSerializer):
    image = PromocodePhotoSerializer(many=True, source="promocode_image")

    class Meta(PromocodeSerializer.Meta):
        fields = PromocodeSerializer.Meta.fields + ("image",)
