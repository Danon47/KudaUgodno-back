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
                forward=["arrival_city"],
            ),
            "hotels": autocomplete.ModelSelect2Multiple(
                url="vzhuhs:vzhuh_autocomplete_hotels",
                forward=["arrival_city"],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance")
        if instance and instance.pk:
            hotel_ids = instance.hotels.values_list("id", flat=True)
            self.fields["main_photo"].queryset = HotelPhoto.objects.filter(hotel_id__in=hotel_ids)
        else:
            self.fields["main_photo"].queryset = HotelPhoto.objects.none()

        self.fields["hotels"].widget.forward = ["arrival_city", "selected_hotels"]
        self.fields["tours"].widget.forward = ["arrival_city", "selected_tours"]

        # добавляем временные поля (в шаблоне они не рендерятся)
        self.fields["selected_hotels"] = forms.CharField(required=False, widget=forms.HiddenInput())
        self.fields["selected_tours"] = forms.CharField(required=False, widget=forms.HiddenInput())
