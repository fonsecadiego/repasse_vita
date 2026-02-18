from dataclasses import dataclass

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from apps.repasse.forms import CatalogItemForm
from apps.repasse.permissions import assert_gestor
from apps.repasse.selectors.catalog_selector import get_catalog_item_by_id, get_catalog_model, list_catalog_items
from apps.repasse.services.catalog_service import create_catalog_item, toggle_catalog_item, update_catalog_item


@dataclass(frozen=True)
class CatalogConfig:
    key: str
    title: str


CATALOG_CONFIGS = {
    "unidades": CatalogConfig(key="unidades", title="Unidades"),
    "convenios": CatalogConfig(key="convenios", title="Convênios"),
    "escalas": CatalogConfig(key="escalas", title="Escalas"),
    "tipos_proced": CatalogConfig(key="tipos_proced", title="Tipos de Procedimento"),
    "procedimentos": CatalogConfig(key="procedimentos", title="Procedimentos"),
    "leituras": CatalogConfig(key="leituras", title="Leituras"),
}


class GestorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        assert_gestor(request.user)
        return super().dispatch(request, *args, **kwargs)


class CatalogHomeView(GestorRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "repasse/cadastros/catalogos/home.html", {"catalogos": CATALOG_CONFIGS.values()})


class CatalogListCreateView(GestorRequiredMixin, View):
    def get(self, request: HttpRequest, key: str) -> HttpResponse:
        config = CATALOG_CONFIGS[key]
        model_class = get_catalog_model(key)
        search = (request.GET.get("q") or "").strip()
        items = list_catalog_items(model_class, search=search)
        return render(
            request,
            "repasse/cadastros/catalogos/list.html",
            {"config": config, "items": items, "form": CatalogItemForm(), "search": search},
        )

    def post(self, request: HttpRequest, key: str) -> HttpResponse:
        config = CATALOG_CONFIGS[key]
        model_class = get_catalog_model(key)
        form = CatalogItemForm(request.POST)
        if form.is_valid():
            try:
                create_catalog_item(model_class, form.cleaned_data["nome"], form.cleaned_data["ativo"])
                return redirect(reverse("repasse-cadastros-catalogos-list", kwargs={"key": key}))
            except ValueError as exc:
                form.add_error("nome", str(exc))

        items = list_catalog_items(model_class)
        return render(
            request,
            "repasse/cadastros/catalogos/list.html",
            {"config": config, "items": items, "form": form, "search": ""},
            status=400,
        )


class CatalogUpdateView(GestorRequiredMixin, View):
    def get(self, request: HttpRequest, key: str, id: int) -> HttpResponse:
        config = CATALOG_CONFIGS[key]
        model_class = get_catalog_model(key)
        item = get_catalog_item_by_id(model_class, id)
        form = CatalogItemForm(initial={"nome": item.nome, "ativo": item.ativo})
        return render(request, "repasse/cadastros/catalogos/form.html", {"config": config, "form": form, "item": item})

    def post(self, request: HttpRequest, key: str, id: int) -> HttpResponse:
        config = CATALOG_CONFIGS[key]
        model_class = get_catalog_model(key)
        item = get_catalog_item_by_id(model_class, id)
        form = CatalogItemForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "repasse/cadastros/catalogos/form.html",
                {"config": config, "form": form, "item": item},
                status=400,
            )

        try:
            update_catalog_item(item, nome=form.cleaned_data["nome"], ativo=form.cleaned_data["ativo"])
            return redirect(reverse("repasse-cadastros-catalogos-list", kwargs={"key": key}))
        except ValueError as exc:
            form.add_error("nome", str(exc))
            return render(
                request,
                "repasse/cadastros/catalogos/form.html",
                {"config": config, "form": form, "item": item},
                status=400,
            )


class CatalogToggleView(GestorRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, key: str, id: int) -> HttpResponse:
        model_class = get_catalog_model(key)
        item = get_catalog_item_by_id(model_class, id)
        toggle_catalog_item(item)
        return redirect(reverse("repasse-cadastros-catalogos-list", kwargs={"key": key}))
