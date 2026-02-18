from datetime import date

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from apps.repasse.permissions import assert_gestor
from apps.repasse.services.apuracao_service import calcular_mes


class DashboardGestorView(View):
    http_method_names = ["get"]

    def get(self, request: HttpRequest):
        assert_gestor(request.user)

        hoje = date.today()
        ano_raw = request.GET.get("ano")
        mes_raw = request.GET.get("mes")

        try:
            ano = int(ano_raw) if ano_raw else hoje.year
            mes = int(mes_raw) if mes_raw else hoje.month
        except (TypeError, ValueError):
            return JsonResponse({"detail": "Parâmetros 'ano' e 'mes' inválidos"}, status=400)

        if not (1 <= mes <= 12):
            return JsonResponse({"detail": "Parâmetro 'mes' deve estar entre 1 e 12"}, status=400)

        filtros = {
            "unidade": request.GET.get("unidade"),
            "ds_tipo_proced": request.GET.get("tipo_proced"),
            "ds_proced": request.GET.get("procedimento"),
            "convenio": request.GET.get("convenio"),
            "escala": request.GET.get("escala"),
            "leitura": request.GET.get("leitura"),
        }

        resultado = calcular_mes(ano=ano, mes=mes, **filtros)

        if request.GET.get("format") == "json":
            return JsonResponse(
                {
                    "ano": resultado.ano,
                    "mes": resultado.mes,
                    "totais_por_medico": resultado.totais_por_medico,
                    "breakdown": resultado.breakdown,
                }
            )

        contexto = {
            "ano": resultado.ano,
            "mes": resultado.mes,
            "filtros": filtros,
            "totais_por_medico": resultado.totais_por_medico,
            "breakdown": resultado.breakdown,
        }

        return render(request, "repasse/dashboard_gestor.html", contexto)
