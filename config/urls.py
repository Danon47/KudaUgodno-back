from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config import settings


admin.site.site_header = 'Администрирование "Куда Угодно"'
admin.site.site_title = 'Администрирование "Куда Угодно"'
admin.site.index_title = 'Администрирование "Куда Угодно"'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("guests.urls")),
    path("api/v1/tours/", include("tours.urls")),
    path("api/v1/flights/", include("flights.urls")),
    path("api/v1/", include("hotels.urls.urls_hotel")),
    path("api/v1/hotels/", include("hotels.urls.urls_room")),
    path("api/v1/applications/", include("applications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
