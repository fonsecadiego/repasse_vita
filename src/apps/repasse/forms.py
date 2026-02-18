from django import forms
from django.contrib.auth import get_user_model

from apps.repasse.models import Medico, RegraRepasse, RegraRepasseVigencia


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["nome", "crm", "user", "is_socio", "dt_admissao", "ativo"]
        widgets = {"dt_admissao": forms.DateInput(attrs={"type": "date"})}


class RegraRepasseForm(forms.ModelForm):
    class Meta:
        model = RegraRepasse
        fields = [
            "ativo",
            "socio_tipo",
            "leitura",
            "unidade",
            "tipo_proced",
            "procedimento",
            "escala_categoria",
            "convenio",
            "tempo_empresa_min_meses",
            "prioridade",
        ]


class RegraRepasseVigenciaForm(forms.ModelForm):
    class Meta:
        model = RegraRepasseVigencia
        fields = ["regra", "vigente_de", "vigente_ate", "tipo_calculo", "valor_fixo", "percentual", "motivo"]
        widgets = {
            "vigente_de": forms.DateInput(attrs={"type": "date"}),
            "vigente_ate": forms.DateInput(attrs={"type": "date"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário ou senha inválidos.")
        return username
