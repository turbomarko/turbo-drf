from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
{%- if cookiecutter.use_async == 'y' %}
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
{%- endif %}
from django.urls import include, path

urlpatterns = [
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),
    # API base url
    path("api/", include("config.api_router")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
{%- if cookiecutter.use_async == 'y' %}
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
{%- endif %}

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    if "drf_spectacular" in settings.INSTALLED_APPS:
        from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

        urlpatterns = [
            # Schema
            path("api/api-schema", SpectacularAPIView.as_view(), name="api-schema"),
            # Optional UI:
            path(
                "api/api-doc",
                SpectacularSwaggerView.as_view(url_name="api-schema"),
                name="api-doc",
            ),
        ] + urlpatterns
