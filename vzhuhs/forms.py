from dal import autocomplete
from django import forms

from hotels.models import HotelPhoto
from vzhuhs.models import Vzhuh


class VzhuhForm(forms.ModelForm):
    class Meta:
        model = Vzhuh
        fields = "__all__"
        widgets = {
            "tours": autocomplete.ModelSelect2Multiple(
                url="vzhuhs:vzhuh_autocomplete_tours",
                forward=["arrival_city", "tours"],
            ),
            "hotels": autocomplete.ModelSelect2Multiple(
                url="vzhuhs:vzhuh_autocomplete_hotels",
                forward=["arrival_city", "hotels"],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance")
        if instance:
            # Ограничу список фото только теми, что относятся к выбранным отелям
            hotel_ids = instance.hotels.values_list("id", flat=True)
            self.fields["blog_photo"].queryset = HotelPhoto.objects.filter(hotel_id__in=hotel_ids)
        else:
            self.fields["blog_photo"].queryset = HotelPhoto.objects.none()
