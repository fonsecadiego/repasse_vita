from django.urls import path
from apps.repasse.views import DashboardGestorView, DashboardMedicoView, MirthIngestaoView

urlpatterns = [
    path("mirth/ingest/", MirthIngestaoView.as_view(), name="repasse-mirth-ingest"),
    path("me/dashboard/", DashboardMedicoView.as_view(), name="repasse-dashboard-medico"),
    path("gestor/dashboard/", DashboardGestorView.as_view(), name="repasse-dashboard-gestor"),
]
