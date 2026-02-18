from datetime import date

from django.test import TestCase

from apps.repasse.models import TipoProcedCatalog
from apps.repasse.services.ingestao_service import ingest_from_mirth


class CatalogoIngestaoTest(TestCase):
    def test_nao_reativa_item_inativo_na_ingestao(self):
        TipoProcedCatalog.objects.create(nome="Tomografia Computadorizada", ativo=False)

        ingest_from_mirth(
            [
                {
                    "UNIDADE": "Hospital X",
                    "LEITURA": "PRIMEIRA",
                    "DT_LAUDO": date(2026, 2, 1),
                    "DT_EXAME": date(2026, 2, 1),
                    "NR_PRESCRICAO": 10,
                    "NM_MEDICO_CORRIGIDO": "Dr X",
                    "CRM_MEDICO_EXEC": "12345",
                    "NM_PACIENTE": "A",
                    "DS_PROCED": "PROC",
                    "DS_TIPO_PROCED": "Tomografia Computadorizada",
                    "ESCALA": "PLANTAO",
                    "CONVENIO": "Convênio X",
                    "QUANTIDADE": "1",
                    "VALOR_EXAME": "100",
                }
            ]
        )

        item = TipoProcedCatalog.objects.get(nome="Tomografia Computadorizada")
        self.assertFalse(item.ativo)
