from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ("repasse", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UnidadeCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_unidade", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="ConvenioCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_convenio", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="EscalaCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_escala", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="TipoProcedCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_tipo_proced", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="ProcedimentoCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_procedimento", "ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="LeituraCatalog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "repasse_catalog_leitura", "ordering": ["nome"]},
        ),
        migrations.AddConstraint(
            model_name="unidadecatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_unidade_nome_ci_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="conveniocatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_convenio_nome_ci_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="escalacatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_escala_nome_ci_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="tipoprocedcatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_tipo_proced_nome_ci_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="procedimentocatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_proced_nome_ci_uniq",
            ),
        ),
        migrations.AddConstraint(
            model_name="leituracatalog",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("nome"),
                name="repasse_catalog_leitura_nome_ci_uniq",
            ),
        ),
    ]
