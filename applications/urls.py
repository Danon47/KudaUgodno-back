from rest_framework.routers import DefaultRouter
from django.urls import path

from applications.apps import ApplicationsConfig
from applications.views.views_application import ApplicationViewSet
from applications.views.views_guest import GuestListCreateView, GuestDetailView

app_name = ApplicationsConfig.name

router = DefaultRouter()
router.register("", ApplicationViewSet)

urlpatterns = [
    # Гости
    path("guests/", GuestListCreateView.as_view(), name="guest_list_create"),
    path("guests/<int:pk>", GuestDetailView.as_view(), name="guest_detail_update_delete"),
] + router.urls