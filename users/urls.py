from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from users.apps import UsersConfig

app_name = UsersConfig.name

# Инициализируем роутер и регистрируем наш ViewSet.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Включаем все маршруты, сгенерированные роутером.
    path('', include(router.urls)),
]
