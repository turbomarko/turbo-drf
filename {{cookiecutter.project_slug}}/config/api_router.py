from django.conf import settings
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

urlpatterns = router.urls

urlpatterns = [
    # Schema
    path("api-schema", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api-docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="api-docs",
    ),
    # Authentication urls
    path("auth/", include("api.users.urls")),
    *urlpatterns,
]

# App urls
# ------------------------------------------------------------------------------
urlpatterns = [*urlpatterns]
