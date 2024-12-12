from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API бронирования туров или отелей",
        default_version="v0.1",
        description='API сервис для веб-сайта "Куда Угодно"',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('users/', include("users.urls", namespace="users")),
    path('tours/', include("tours.urls", namespace="tours")),
    path('flights/', include("flights.urls", namespace="flights")),
    path('hotels/', include("hotels.urls", namespace="hotels")),
    path('applications/', include("applications.urls", namespace="applications")),
]
