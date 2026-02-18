from django import forms
from django.contrib.auth import get_user_model

from apps.repasse.models import (
    EscalaCategoria,
    LeituraTipo,
    Medico,
    RegraRepasse,
    RegraRepasseVigencia,
    SocioTipo,
)
from apps.repasse.selectors.catalog_selector import get_regra_form_choices


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["nome", "crm", "user", "is_socio", "dt_admissao", "ativo"]
        widgets = {"dt_admissao": forms.DateInput(attrs={"type": "date"})}


class RegraRepasseForm(forms.Form):
    ativo = forms.BooleanField(required=False)
    socio_tipo = forms.ChoiceField(choices=SocioTipo.choices)
    leitura = forms.ChoiceField()
    unidade = forms.ChoiceField()
    tipo_proced = forms.ChoiceField()
    procedimento = forms.ChoiceField()
    escala_categoria = forms.ChoiceField(choices=EscalaCategoria.choices)
    convenio = forms.ChoiceField()
    tempo_empresa_min_meses = forms.IntegerField(required=False, min_value=0)
    prioridade = forms.IntegerField(min_value=0)

    def __init__(self, *args, instance: RegraRepasse | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = get_regra_form_choices(
            unidade_atual=getattr(instance, "unidade", ""),
            convenio_atual=getattr(instance, "convenio", ""),
            escala_atual="",
            tipo_proced_atual=getattr(instance, "tipo_proced", ""),
            procedimento_atual=getattr(instance, "procedimento", ""),
            leitura_atual=getattr(instance, "leitura", ""),
        )
        self.fields["unidade"].choices = choices["unidade"]
        self.fields["tipo_proced"].choices = choices["tipo_proced"]
        self.fields["procedimento"].choices = choices["procedimento"]
        self.fields["convenio"].choices = choices["convenio"]

        leitura_choices = [("*", "* (qualquer)")] + list(LeituraTipo.choices)
        for nome, label in choices["leitura"]:
            if nome != "*" and nome not in {item[0] for item in leitura_choices}:
                leitura_choices.append((nome, label))
        self.fields["leitura"].choices = leitura_choices

        if instance:
            self.initial = {
                "ativo": instance.ativo,
                "socio_tipo": instance.socio_tipo,
                "leitura": instance.leitura,
                "unidade": instance.unidade,
                "tipo_proced": instance.tipo_proced,
                "procedimento": instance.procedimento,
                "escala_categoria": instance.escala_categoria,
                "convenio": instance.convenio,
                "tempo_empresa_min_meses": instance.tempo_empresa_min_meses,
                "prioridade": instance.prioridade,
            }

    def to_model_payload(self) -> dict:
        data = self.cleaned_data
        return {
            "ativo": data["ativo"],
            "socio_tipo": data["socio_tipo"],
            "leitura": data["leitura"],
            "unidade": data["unidade"],
            "tipo_proced": data["tipo_proced"],
            "procedimento": data["procedimento"],
            "escala_categoria": data["escala_categoria"],
            "convenio": data["convenio"],
            "tempo_empresa_min_meses": data["tempo_empresa_min_meses"],
            "prioridade": data["prioridade"],
        }


class RegraRepasseVigenciaForm(forms.ModelForm):
    class Meta:
        model = RegraRepasseVigencia
        fields = ["regra", "vigente_de", "vigente_ate", "tipo_calculo", "valor_fixo", "percentual", "motivo"]
        widgets = {
            "vigente_de": forms.DateInput(attrs={"type": "date"}),
            "vigente_ate": forms.DateInput(attrs={"type": "date"}),
        }


class CatalogItemForm(forms.Form):
    nome = forms.CharField(max_length=255)
    ativo = forms.BooleanField(required=False, initial=True)


class LoginForm(forms.Form):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if not get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário ou senha inválidos.")
        return username
