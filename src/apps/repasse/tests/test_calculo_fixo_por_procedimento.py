from datetime import date
from decimal import Decimal

from django.test import TestCase

from apps.repasse.models import Medico, ProducaoLaudo, RegraRepasse, TipoCalculo
from apps.repasse.services.apuracao_service import calcular_mes
from apps.repasse.services.regra_repasse_service import criar_vigencia


class CalculoFixoPorProcedimentoTest(TestCase):
    def test_calcula_fixo_por_procedimento_especifico(self):
        medico = Medico.objects.create(nome="Dr. B", crm="222")
        ProducaoLaudo.objects.create(
            unidade="HOSPITAL A",
            leitura="PRIMEIRA",
            dt_laudo=date(2026, 1, 5),
            dt_exame=date(2026, 1, 5),
            nr_prescricao=456,
            nome_paciente="Paciente B",
            ds_proced="RM - Cranio",
            ds_tipo_proced="RM",
            escala="FORA_PLANTAO",
            convenio="UNIMED",
            quantidade=Decimal("2"),
            valor_exame=Decimal("200"),
            medico=medico,
            hash_idempotencia="h1",
        )

        regra = RegraRepasse.objects.create(
            leitura="AMBAS",
            procedimento="RM - Cranio",
            tipo_proced="*",
            convenio="*",
            prioridade=100,
        )
        criar_vigencia(regra.id, date(2026, 1, 1), TipoCalculo.FIXO, valor_fixo=Decimal("30.00"))

        calcular_mes(2026, 1)

        item = ProducaoLaudo.objects.get(hash_idempotencia="h1")
        self.assertEqual(item.repasse_calculado, Decimal("60.00"))
