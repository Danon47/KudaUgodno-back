from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, DecimalField, ImageField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

# from hotels.models import Hotel
from promocodes.models import Promocode, PromocodePhoto
from tours.models import Tour


class PromocodePhotoSerializer(ModelSerializer):
    image = ImageField()

    class Meta:
        model = PromocodePhoto
        fields = (
            "id",
            "image",
        )


class PromocodeSerializer(ModelSerializer):
    discount_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default="0.17",
    )

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
    image = PromocodePhotoSerializer(
        many=True,
        source="promocode_image",
    )

    class Meta(PromocodeSerializer.Meta):
        fields = PromocodeSerializer.Meta.fields + ("image",)


class PromoCodeCheckSerializer(Serializer):
    promo_code = CharField()
    tour_id = IntegerField(required=False)
    hotel_id = IntegerField(required=False)

    def validate(self, data):
        promo_code_value = data["promo_code"]
        tour_id = data.get("tour_id")
        hotel_id = data.get("hotel_id")

        try:
            promo = Promocode.objects.get(code=promo_code_value)
        except Promocode.DoesNotExist:
            raise ValidationError("Промокод не найден.") from None

        if not promo.is_valid():
            raise ValidationError("Промокод просрочен или неактивен.") from None

        if tour_id:
            if not promo.tours.filter(id=tour_id).exists():
                raise ValidationError("Промокод не действует на данный тур.")
            tour = get_object_or_404(Tour, id=tour_id)
            return {
                "tour_price": tour.total_price,
                "discount_amount": promo.discount_amount,
                "total_price": promo.apply_discount(tour.total_price),
            }

        elif hotel_id:
            if not promo.hotels.filter(id=hotel_id).exists():
                raise ValidationError("Промокод не действует на данный отель.") from None
            # hotel = get_object_or_404(Hotel, id=hotel_id)
            return {
                "discount_amount": promo.discount_amount,
            }

        else:
            raise ValidationError("Нужно передать tour_id или hotel_id.") from None
