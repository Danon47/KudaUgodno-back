from rest_framework.routers import DefaultRouter

from applications.apps import ApplicationsConfig
from applications.views_application import ApplicationViewSet


app_name = ApplicationsConfig.name

router = DefaultRouter()
router.register("", ApplicationViewSet)

urlpatterns = [] + router.urls
