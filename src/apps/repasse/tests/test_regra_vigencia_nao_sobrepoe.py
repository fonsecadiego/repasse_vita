from datetime import date

from django.test import TestCase

from apps.repasse.models import RegraRepasse, TipoCalculo
from apps.repasse.services.regra_repasse_service import criar_vigencia


class RegraVigenciaNaoSobrepoeTest(TestCase):
    def test_reajuste_fecha_vigencia_anterior_sem_sobrepor(self):
        regra = RegraRepasse.objects.create(prioridade=10)

        primeira = criar_vigencia(
            regra_id=regra.id,
            vigente_de=date(2026, 1, 1),
            tipo_calculo=TipoCalculo.FIXO,
            valor_fixo="50.00",
            motivo="valor antigo",
        )
        segunda = criar_vigencia(
            regra_id=regra.id,
            vigente_de=date(2026, 3, 1),
            tipo_calculo=TipoCalculo.FIXO,
            valor_fixo="60.00",
            motivo="reajuste",
        )

        primeira.refresh_from_db()
        self.assertEqual(primeira.vigente_ate, date(2026, 2, 28))
        self.assertEqual(segunda.vigente_de, date(2026, 3, 1))
