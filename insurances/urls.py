from rest_framework.routers import DefaultRouter

from insurances.apps import InsuranceConfig
from insurances.views import InsurancesView


app_name = InsuranceConfig.name

router = DefaultRouter()
router.register("", InsurancesView)

urlpatterns = [] + router.urls
