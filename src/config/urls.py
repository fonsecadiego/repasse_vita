from django.contrib import admin
from django.urls import include, path

from apps.repasse.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("repasse/", include("apps.repasse.urls")),
    path("api/repasse/", include("apps.repasse.urls")),
]
