from django.urls import path

from applications.apps import ApplicationsConfig
from applications.views.views_application import ApplicationListCreateView, ApplicationDetailView
from applications.views.views_guest import GuestListCreateView, GuestDetailView

app_name = ApplicationsConfig.name

urlpatterns = [
    # Заявка
    path("", ApplicationListCreateView.as_view(), name="application_list_create"),
    path("<int:pk>", ApplicationDetailView.as_view(), name="application_detail_update_delete"),
    # Гости
    path("guests/", GuestListCreateView.as_view(), name="guest_list_create"),
    path("guests/<int:pk>", GuestDetailView.as_view(), name="guest_detail_update_delete"),
]