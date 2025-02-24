from rest_framework.routers import DefaultRouter

from applications.apps import ApplicationsConfig
from applications.views.views_application import ApplicationViewSet
from applications.views.views_guest import GuestViewSet


app_name = ApplicationsConfig.name

router = DefaultRouter()
router.register("", ApplicationViewSet)
router.register("/guests", GuestViewSet)

urlpatterns = [] + router.urls
