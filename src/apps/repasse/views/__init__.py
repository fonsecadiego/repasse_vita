from .auth_view import LoginView, LogoutView
from .cadastros_view import (
    CadastrosHomeView,
    MedicoCreateView,
    MedicoListView,
    MedicoUpdateView,
    RegraCreateView,
    RegraListView,
    RegraUpdateView,
    RegraVigenciasView,
    VigenciaUpdateView,
)
from .catalogos_view import CatalogHomeView, CatalogListCreateView, CatalogToggleView, CatalogUpdateView
from .dashboard_gestor_view import DashboardGestorView, DashboardOptionsView
from .dashboard_medico_view import DashboardMedicoView
from .mirth_ingestao_view import MirthIngestaoView

__all__ = [
    "CadastrosHomeView",
    "CatalogHomeView",
    "CatalogListCreateView",
    "CatalogToggleView",
    "CatalogUpdateView",
    "DashboardGestorView",
    "DashboardMedicoView",
    "DashboardOptionsView",
    "LoginView",
    "LogoutView",
    "MedicoCreateView",
    "MedicoListView",
    "MedicoUpdateView",
    "MirthIngestaoView",
    "RegraCreateView",
    "RegraListView",
    "RegraUpdateView",
    "RegraVigenciasView",
    "VigenciaUpdateView",
]
