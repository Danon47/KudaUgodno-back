from rest_framework.routers import DefaultRouter

from tours.apps import ToursConfig
from tours.views import TourStockViewSet, TourViewSet


app_name = ToursConfig.name

router = DefaultRouter()
router.register("tours", TourViewSet, basename="tours")
router.register("stocks", TourStockViewSet, basename="tours_stocks")


urlpatterns = [] + router.urls
