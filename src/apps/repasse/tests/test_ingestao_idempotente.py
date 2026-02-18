from datetime import date

from django.test import TestCase

from apps.repasse.models import ProducaoLaudo
from apps.repasse.services.ingestao_service import ingest_from_mirth


class IngestaoIdempotenteTest(TestCase):
    def test_nao_duplica_mesmo_item(self):
        payload = [
            {
                "UNIDADE": "HOSPITAL A",
                "LEITURA": "PRIMEIRA",
                "DT_LAUDO": date(2026, 1, 10),
                "DT_EXAME": date(2026, 1, 9),
                "NR_PRESCRICAO": 123,
                "NM_MEDICO_CORRIGIDO": "Dr. A",
                "CRM_MEDICO_EXEC": "111",
                "NM_PACIENTE": "Paciente A",
                "DS_PROCED": "RM - Cranio",
                "DS_TIPO_PROCED": "RM",
                "ESCALA": "PLANTAO",
                "CONVENIO": "Particular Extra",
                "QUANTIDADE": "1",
                "VALOR_EXAME": "100",
            }
        ]

        primeiro = ingest_from_mirth(payload)
        segundo = ingest_from_mirth(payload)

        self.assertEqual(primeiro.inseridos, 1)
        self.assertEqual(segundo.ignorados_por_duplicidade, 1)
        self.assertEqual(ProducaoLaudo.objects.count(), 1)
