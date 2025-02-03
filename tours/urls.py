from tours.apps import ToursConfig
from tours.views import TourViewSet

from rest_framework.routers import DefaultRouter

app_name = ToursConfig.name

router = DefaultRouter()
router.register("", TourViewSet)

urlpatterns = [

] + router.urls
