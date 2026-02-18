from django.contrib import admin

from apps.repasse.models import Medico, ProducaoLaudo, RegraRepasse, RegraRepasseVigencia


class RegraRepasseVigenciaInline(admin.TabularInline):
    model = RegraRepasseVigencia
    extra = 0


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "crm", "is_socio", "dt_admissao", "ativo")
    search_fields = ("nome", "crm")
    list_filter = ("is_socio", "ativo")


@admin.register(RegraRepasse)
class RegraRepasseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ativo",
        "socio_tipo",
        "leitura",
        "tipo_proced",
        "procedimento",
        "convenio",
        "prioridade",
    )
    list_filter = ("ativo", "socio_tipo", "leitura", "escala_categoria", "convenio")
    inlines = [RegraRepasseVigenciaInline]


@admin.register(ProducaoLaudo)
class ProducaoLaudoAdmin(admin.ModelAdmin):
    list_display = (
        "nr_prescricao",
        "medico",
        "dt_laudo",
        "ds_tipo_proced",
        "ds_proced",
        "convenio",
        "repasse_calculado",
    )
    list_filter = ("dt_laudo", "convenio", "escala", "leitura")
    search_fields = ("nr_prescricao", "medico__nome", "medico__crm", "nome_paciente")
