from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from apps.repasse.forms import MedicoForm, RegraRepasseForm, RegraRepasseVigenciaForm
from apps.repasse.permissions import assert_gestor
from apps.repasse.selectors.cadastro_selector import (
    get_vigencia_by_id,
    list_medicos,
    list_regras,
    list_vigencias_by_regra,
)
from apps.repasse.services.cadastro_service import (
    atualizar_medico,
    atualizar_regra,
    atualizar_vigencia,
    criar_medico,
    criar_regra,
    criar_vigencia,
)


class GestorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        assert_gestor(request.user)
        return super().dispatch(request, *args, **kwargs)


class CadastrosHomeView(GestorRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "repasse/cadastros/home.html")


class MedicoListView(GestorRequiredMixin, View):
    def get(self, request):
        return render(request, "repasse/cadastros/medicos/list.html", {"medicos": list_medicos()})


class MedicoCreateView(GestorRequiredMixin, View):
    def get(self, request):
        return render(request, "repasse/cadastros/medicos/form.html", {"form": MedicoForm(), "titulo": "Novo médico"})

    def post(self, request):
        form = MedicoForm(request.POST)
        if not form.is_valid():
            return render(request, "repasse/cadastros/medicos/form.html", {"form": form, "titulo": "Novo médico"}, status=400)

        criar_medico(form.cleaned_data)
        return redirect("repasse-cadastros-medicos")


class MedicoUpdateView(GestorRequiredMixin, View):
    def get(self, request, id: int):
        medico = get_object_or_404(list_medicos(), id=id)
        return render(request, "repasse/cadastros/medicos/form.html", {"form": MedicoForm(instance=medico), "titulo": "Editar médico"})

    def post(self, request, id: int):
        medico = get_object_or_404(list_medicos(), id=id)
        form = MedicoForm(request.POST, instance=medico)
        if not form.is_valid():
            return render(request, "repasse/cadastros/medicos/form.html", {"form": form, "titulo": "Editar médico"}, status=400)

        atualizar_medico(medico, form.cleaned_data)
        return redirect("repasse-cadastros-medicos")


class RegraListView(GestorRequiredMixin, View):
    def get(self, request):
        return render(request, "repasse/cadastros/regras/list.html", {"regras": list_regras()})


class RegraCreateView(GestorRequiredMixin, View):
    def get(self, request):
        return render(request, "repasse/cadastros/regras/form.html", {"form": RegraRepasseForm(), "titulo": "Nova regra", "is_create": True})

    def post(self, request):
        form = RegraRepasseForm(request.POST)
        if not form.is_valid():
            return render(request, "repasse/cadastros/regras/form.html", {"form": form, "titulo": "Nova regra", "is_create": True}, status=400)

        regra = criar_regra(form.to_model_payload())
        return redirect(reverse("repasse-cadastros-regras-vigencias", kwargs={"id": regra.id}))


class RegraUpdateView(GestorRequiredMixin, View):
    def get(self, request, id: int):
        regra = get_object_or_404(list_regras(), id=id)
        return render(request, "repasse/cadastros/regras/form.html", {"form": RegraRepasseForm(instance=regra), "titulo": "Editar regra", "is_create": False})

    def post(self, request, id: int):
        regra = get_object_or_404(list_regras(), id=id)
        form = RegraRepasseForm(request.POST, instance=regra)
        if not form.is_valid():
            return render(request, "repasse/cadastros/regras/form.html", {"form": form, "titulo": "Editar regra", "is_create": False}, status=400)

        atualizar_regra(regra, form.to_model_payload())
        return redirect("repasse-cadastros-regras")


class RegraVigenciasView(GestorRequiredMixin, View):
    def get(self, request, id: int):
        regra = get_object_or_404(list_regras(), id=id)
        return render(
            request,
            "repasse/cadastros/regras/vigencias.html",
            {
                "regra": regra,
                "vigencias": list_vigencias_by_regra(regra.id),
                "form": RegraRepasseVigenciaForm(initial={"regra": regra}),
            },
        )

    def post(self, request, id: int):
        regra = get_object_or_404(list_regras(), id=id)
        form = RegraRepasseVigenciaForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "repasse/cadastros/regras/vigencias.html",
                {"regra": regra, "vigencias": list_vigencias_by_regra(regra.id), "form": form},
                status=400,
            )

        try:
            criar_vigencia(form.cleaned_data)
            return redirect(reverse("repasse-cadastros-regras-vigencias", kwargs={"id": regra.id}))
        except ValueError as exc:
            form.add_error(None, str(exc))
            messages.error(request, str(exc))
            return render(
                request,
                "repasse/cadastros/regras/vigencias.html",
                {"regra": regra, "vigencias": list_vigencias_by_regra(regra.id), "form": form},
                status=400,
            )


class VigenciaUpdateView(GestorRequiredMixin, View):
    def get(self, request, id: int):
        vigencia = get_vigencia_by_id(id)
        return render(
            request,
            "repasse/cadastros/vigencias/form.html",
            {"form": RegraRepasseVigenciaForm(instance=vigencia), "vigencia": vigencia},
        )

    def post(self, request, id: int):
        vigencia = get_vigencia_by_id(id)
        form = RegraRepasseVigenciaForm(request.POST, instance=vigencia)
        if not form.is_valid():
            return render(
                request,
                "repasse/cadastros/vigencias/form.html",
                {"form": form, "vigencia": vigencia},
                status=400,
            )

        try:
            atualizar_vigencia(vigencia, form.cleaned_data)
            return redirect(reverse("repasse-cadastros-regras-vigencias", kwargs={"id": vigencia.regra_id}))
        except ValueError as exc:
            form.add_error(None, str(exc))
            return render(
                request,
                "repasse/cadastros/vigencias/form.html",
                {"form": form, "vigencia": vigencia},
                status=400,
            )
