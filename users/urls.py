from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, AuthViewSet

app_name = "users"

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [path('', include(router.urls))]
