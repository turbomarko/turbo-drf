from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"
urlpatterns = router.urls

urlpatterns = [
    # Schema
    path("api-schema", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api-docs",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="api-docs",
    ),
    # Authentication urls
    path("auth/", include("api.users.urls")),
] + urlpatterns

# App urls
# ------------------------------------------------------------------------------
urlpatterns = [] + urlpatterns
