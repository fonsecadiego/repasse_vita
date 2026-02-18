from django.urls import path

from apps.repasse.views import DashboardGestorView, DashboardMedicoView, MirthIngestaoView

urlpatterns = [
    path("api/repasse/mirth/ingest/", MirthIngestaoView.as_view(), name="repasse-mirth-ingest"),
    path("api/repasse/me/dashboard/", DashboardMedicoView.as_view(), name="repasse-dashboard-medico"),
    path("api/repasse/gestor/dashboard/", DashboardGestorView.as_view(), name="repasse-dashboard-gestor"),
]
