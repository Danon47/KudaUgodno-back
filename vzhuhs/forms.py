from dal import autocomplete
from django import forms

from hotels.models import HotelPhoto
from vzhuhs.models import Vzhuh


class VzhuhForm(forms.ModelForm):
    """
    Форма для модели Vzhuh, с автодополнением для туров и отелей, а также
    динамической фильтрацией главного фото по выбранным отелям.

    Особенности:
    - Поля 'tours' и 'hotels' используют виджеты с автокомплитом от django-autocomplete-light.
    - Поле 'main_photo' фильтруется по отелям, связанным с текущим экземпляром Vzhuh.
    """

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
            hotel_ids = instance.hotels.values_list("id", flat=True)
            self.fields["main_photo"].queryset = HotelPhoto.objects.filter(hotel_id__in=hotel_ids)
        else:
            self.fields["main_photo"].queryset = HotelPhoto.objects.none()
