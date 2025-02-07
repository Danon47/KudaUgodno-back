from django.urls import include, path
from rest_framework.routers import DefaultRouter


from users.views import UserViewSet, AuthViewSet
from users.apps import UsersConfig


app_name = UsersConfig.name


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')  # Регистрация UserViewSet
router.register(r'auth', AuthViewSet, basename='auth')  # Отдельная регистрация AuthViewSet


urlpatterns = [
   path('', include(router.urls)),  # Включаем все маршруты
]
