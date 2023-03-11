from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path("grappelli/", include("grappelli.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    # API base url
    path("", include("config.api_router")),
    # Django allauth dummy endpoints to avoid exception
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-email-verification-sent/",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = "api.utils.error_views.server_error"
handler400 = "api.utils.error_views.bad_request"

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
