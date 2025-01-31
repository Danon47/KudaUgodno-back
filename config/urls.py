from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("users/", include("users.urls")),
    path("tours/", include("tours.urls")),
    path("flights/", include("flights.urls")),
    path("", include("hotels.urls.urls_hotel")),
    path("", include("hotels.urls.urls_room")),
    path("applications/", include("applications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
