from django.urls import re_path
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..urls import urlpatterns


class ExampleProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        return Response(dict(success=True))

    def post(self, *args, **kwargs):
        return Response(dict(success=True))


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def get_csrf_cookie(request):
    return Response()


urlpatterns += [
    re_path(
        r"^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    re_path(
        r"^account-email-verification-sent/$",
        TemplateView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    re_path(r"^protected-view/$", ExampleProtectedView.as_view()),
    re_path(r"^getcsrf/", get_csrf_cookie, name="getcsrf"),
]
