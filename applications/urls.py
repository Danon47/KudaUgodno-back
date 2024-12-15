from django.urls import path

from applications.apps import ApplicationsConfig
from applications.views import ApplicationListCreateView

app_name = ApplicationsConfig.name

urlpatterns = [
    path("", ApplicationListCreateView.as_view(), name="application-list-create"),
]