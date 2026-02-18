from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Medico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("crm", models.CharField(db_index=True, max_length=32, unique=True)),
                ("is_socio", models.BooleanField(default=False)),
                ("dt_admissao", models.DateField(blank=True, null=True)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="medico",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "repasse_medico", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="RegraRepasse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ativo", models.BooleanField(default=True)),
                (
                    "socio_tipo",
                    models.CharField(
                        choices=[("SOCIO", "Sócio"), ("NAO_SOCIO", "Não sócio"), ("AMBOS", "Ambos")],
                        default="AMBOS",
                        max_length=16,
                    ),
                ),
                (
                    "leitura",
                    models.CharField(
                        choices=[("PRIMEIRA", "Primeira"), ("SEGUNDA", "Segunda"), ("AMBAS", "Ambas")],
                        default="AMBAS",
                        max_length=16,
                    ),
                ),
                ("unidade", models.CharField(blank=True, default="*", max_length=255, null=True)),
                ("tipo_proced", models.CharField(blank=True, default="*", max_length=255, null=True)),
                ("procedimento", models.CharField(blank=True, default="*", max_length=255, null=True)),
                (
                    "escala_categoria",
                    models.CharField(
                        choices=[("PLANTAO", "Plantão"), ("FORA_PLANTAO", "Fora do plantão"), ("AMBOS", "Ambos")],
                        default="AMBOS",
                        max_length=16,
                    ),
                ),
                ("convenio", models.CharField(default="*", max_length=255)),
                ("tempo_empresa_min_meses", models.PositiveIntegerField(blank=True, null=True)),
                ("prioridade", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "repasse_regra", "ordering": ["-prioridade", "id"]},
        ),
        migrations.CreateModel(
            name="RegraRepasseVigencia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("vigente_de", models.DateField()),
                ("vigente_ate", models.DateField(blank=True, null=True)),
                ("tipo_calculo", models.CharField(choices=[("FIXO", "Fixo"), ("PERCENTUAL", "Percentual")], max_length=16)),
                ("valor_fixo", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("percentual", models.DecimalField(blank=True, decimal_places=4, max_digits=8, null=True)),
                ("motivo", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "regra",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vigencias", to="repasse.regrarepasse"),
                ),
            ],
            options={"db_table": "repasse_regra_vigencia", "ordering": ["-vigente_de", "-id"]},
        ),
        migrations.CreateModel(
            name="ProducaoLaudo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("unidade", models.CharField(max_length=255)),
                ("leitura", models.CharField(max_length=32)),
                ("dt_laudo", models.DateField(db_index=True)),
                ("dt_exame", models.DateField(blank=True, null=True)),
                ("nr_prescricao", models.BigIntegerField()),
                ("nome_paciente", models.CharField(max_length=255)),
                ("ds_proced", models.CharField(db_index=True, max_length=255)),
                ("ds_tipo_proced", models.CharField(db_index=True, max_length=255)),
                ("escala", models.CharField(db_index=True, max_length=255)),
                ("convenio", models.CharField(db_index=True, max_length=255)),
                ("quantidade", models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ("valor_exame", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("hash_idempotencia", models.CharField(max_length=64, unique=True)),
                ("repasse_calculado", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "medico",
                    models.ForeignKey(db_index=True, on_delete=django.db.models.deletion.PROTECT, related_name="producoes", to="repasse.medico"),
                ),
                (
                    "regra_aplicada",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="producoes_apuradas", to="repasse.regrarepasse"),
                ),
                (
                    "vigencia_aplicada",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="producoes_apuradas", to="repasse.regrarepassevigencia"),
                ),
            ],
            options={"db_table": "repasse_producao_laudo"},
        ),
        migrations.AddConstraint(
            model_name="regrarepassevigencia",
            constraint=models.CheckConstraint(
                condition=models.Q(("vigente_ate__isnull", True), ("vigente_ate__gte", models.F("vigente_de")), _connector="OR"),
                name="repasse_vigencia_periodo_valido",
            ),
        ),
        migrations.AddIndex(
            model_name="regrarepassevigencia",
            index=models.Index(fields=["regra", "vigente_de", "vigente_ate"], name="repasse_regr_regra_i_47478e_idx"),
        ),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["dt_laudo"], name="repasse_pro_dt_laudo_1afd8d_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["medico"], name="repasse_pro_medico__2f675e_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["convenio"], name="repasse_pro_conveni_7dd46c_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["ds_tipo_proced"], name="repasse_pro_ds_tipo_570905_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["ds_proced"], name="repasse_pro_ds_proc_957212_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["escala"], name="repasse_pro_escala_435ced_idx")),
        migrations.AddIndex(model_name="producaolaudo", index=models.Index(fields=["leitura"], name="repasse_pro_leitura_023f48_idx")),
    ]
