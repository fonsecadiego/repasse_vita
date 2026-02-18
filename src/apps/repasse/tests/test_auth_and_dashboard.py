from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from apps.repasse.models import Medico, ProducaoLaudo


class AuthAndDashboardFlowTest(TestCase):
    def setUp(self):
        self.gestor_group = Group.objects.create(name="gestor")
        self.gestor = User.objects.create_user(username="gestor", password="123456")
        self.gestor.groups.add(self.gestor_group)

        self.med_user = User.objects.create_user(username="med", password="123456")
        self.medico = Medico.objects.create(nome="Dra Teste", crm="CRM999", user=self.med_user)

        ProducaoLaudo.objects.create(
            unidade="U1",
            leitura="Primeira",
            dt_laudo=date(2026, 2, 10),
            nr_prescricao=1001,
            nome_paciente="Paciente",
            ds_proced="PROC A",
            ds_tipo_proced="TIPO A",
            escala="PLANTAO",
            convenio="Conv A",
            quantidade="1",
            valor_exame="100.00",
            medico=self.medico,
            hash_idempotencia="hash-auth-dashboard",
        )

    def test_login_gestor_redireciona_dashboard_gestor(self):
        response = self.client.post(reverse("login"), {"username": "gestor", "password": "123456"})
        self.assertRedirects(response, reverse("repasse-dashboard-gestor"))

    def test_endpoint_options_retorna_distinct(self):
        self.client.login(username="gestor", password="123456")
        response = self.client.get(reverse("repasse-dashboard-options"), {"ano": 2026, "mes": 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn("U1", response.json()["unidade"])
