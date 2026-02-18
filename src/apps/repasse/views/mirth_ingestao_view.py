import json

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.repasse.services.ingestao_service import ingest_from_mirth

@method_decorator(csrf_exempt, name="dispatch")
class MirthIngestaoView(View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest):
        token = request.headers.get("X-INGEST-TOKEN")
        expected_token = getattr(settings, "MIRTH_INGEST_TOKEN", None)
        if not expected_token or token != expected_token:
            return JsonResponse({"detail": "Token de ingestão inválido"}, status=403)

        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"detail": "JSON inválido"}, status=400)

        if not isinstance(payload, list):
            return JsonResponse({"detail": "Payload deve ser uma lista de objetos"}, status=400)

        resultado = ingest_from_mirth(payload)
        return JsonResponse(
            {
                "recebidos": resultado.recebidos,
                "inseridos": resultado.inseridos,
                "ignorados_por_duplicidade": resultado.ignorados_por_duplicidade,
                "atualizados": resultado.atualizados,
            },
            status=200,
        )
