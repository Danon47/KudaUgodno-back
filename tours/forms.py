from dal import autocomplete
from django import forms

from tours.models import Tour


class TourAdminForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = "__all__"
        widgets = {
            "hotel": autocomplete.ModelSelect2(
                url="tours:hotel_autocomplete",
            ),
            "room": autocomplete.ModelSelect2Multiple(
                url="tours:room_autocomplete",
                forward=["hotel"],  # Передаем поле hotel для фильтрации
            ),
            "type_of_meals": autocomplete.ModelSelect2Multiple(
                url="tours:type_of_meal_autocomplete",
                forward=["hotel"],  # Передаем поле hotel для фильтрации
            ),
        }
