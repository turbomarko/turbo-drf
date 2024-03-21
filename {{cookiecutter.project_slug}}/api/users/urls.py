from django.urls import include
from django.urls import path

app_name = "users"

# Authentication urls
urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
