from datetime import date
from decimal import Decimal

from django.test import TestCase

from apps.repasse.models import Medico, ProducaoLaudo, RegraRepasse, TipoCalculo
from apps.repasse.services.apuracao_service import calcular_mes
from apps.repasse.services.regra_repasse_service import criar_vigencia


class CalculoPercentualParticularExtraTest(TestCase):
    def test_calcula_percentual_particular_extra(self):
        medico = Medico.objects.create(nome="Dr. C", crm="333")
        ProducaoLaudo.objects.create(
            unidade="HOSPITAL A",
            leitura="PRIMEIRA",
            dt_laudo=date(2026, 1, 6),
            dt_exame=date(2026, 1, 6),
            nr_prescricao=789,
            nome_paciente="Paciente C",
            ds_proced="TC Torax",
            ds_tipo_proced="Tomografia",
            escala="PLANTAO",
            convenio="Particular Extra",
            quantidade=Decimal("1"),
            valor_exame=Decimal("500"),
            medico=medico,
            hash_idempotencia="h2",
        )

        regra = RegraRepasse.objects.create(
            leitura="AMBAS",
            tipo_proced="Tomografia",
            procedimento="*",
            convenio="Particular Extra",
            prioridade=120,
        )
        criar_vigencia(regra.id, date(2026, 1, 1), TipoCalculo.PERCENTUAL, percentual=Decimal("0.10"))

        calcular_mes(2026, 1)

        item = ProducaoLaudo.objects.get(hash_idempotencia="h2")
        self.assertEqual(item.repasse_calculado, Decimal("50.00"))
