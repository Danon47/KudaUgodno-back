from django.urls import path

from tours.apps import ToursConfig
from tours.views import TourListCreateView, TourDetailView

app_name = ToursConfig.name

urlpatterns = [
    path("", TourListCreateView.as_view(), name="tour_list_create"),
    path("<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
]
