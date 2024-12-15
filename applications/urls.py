from django.urls import path

from applications.apps import ApplicationsConfig
from applications.views import ApplicationListCreateView, ApplicationDetailView

app_name = ApplicationsConfig.name

urlpatterns = [
    # Заявка
    path("", ApplicationListCreateView.as_view(), name="application-list-create"),
    path("<int:pk>", ApplicationDetailView.as_view(), name="application-detail-update-delete"),
]