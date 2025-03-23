from rest_framework.routers import DefaultRouter

from guests.views import GuestViewSet


router = DefaultRouter()
router.register("guests", GuestViewSet, basename="guest")

urlpatterns = router.urls
