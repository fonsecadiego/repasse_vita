from django.db.models import Count, Sum


def get_totais_por_medico_mes(queryset):
    return list(
        queryset.values("medico_id", "medico__nome", "medico__crm")
        .annotate(
            qtd_laudos=Count("id"),
            total_valor_exame=Sum("valor_exame"),
            total_repasse=Sum("repasse_calculado"),
        )
        .order_by("medico__nome")
    )


def get_breakdown(queryset):
    return list(
        queryset.values("medico_id", "ds_tipo_proced", "ds_proced", "leitura", "escala", "convenio")
        .annotate(
            qtd_laudos=Count("id"),
            total_valor_exame=Sum("valor_exame"),
            total_repasse=Sum("repasse_calculado"),
        )
        .order_by("medico_id", "ds_tipo_proced", "ds_proced")
    )
