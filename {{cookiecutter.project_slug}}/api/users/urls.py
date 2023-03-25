from django.urls import include, path

app_name = "users"

# Authentication urls
urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
