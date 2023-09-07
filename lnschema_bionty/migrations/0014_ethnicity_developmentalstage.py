# Generated by Django 4.2.1 on 2023-09-07 16:40

import django.db.models.deletion
import lnschema_core.models
import lnschema_core.users
from django.db import migrations, models

import lnschema_bionty.ids


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0017_dataset_initial_version_dataset_version"),
        (
            "lnschema_bionty",
            "0013_alter_cellmarker_species_alter_gene_species_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Ethnicity",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=256)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                (
                    "abbr",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ethnicities",
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_ethnicities",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "datasets",
                    models.ManyToManyField(related_name="ethnicities", to="lnschema_core.dataset"),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="ethnicities", to="lnschema_core.file"),
                ),
                (
                    "parents",
                    models.ManyToManyField(related_name="children", to="lnschema_bionty.ethnicity"),
                ),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(
                models.Model,
                lnschema_core.models.HasParents,
                lnschema_core.models.CanValidate,
            ),
        ),
        migrations.CreateModel(
            name="DevelopmentalStage",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=256)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                (
                    "abbr",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="developmental_stages",
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_developmental_stages",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "datasets",
                    models.ManyToManyField(related_name="developmental_stages", to="lnschema_core.dataset"),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="developmental_stages", to="lnschema_core.file"),
                ),
                (
                    "parents",
                    models.ManyToManyField(related_name="children", to="lnschema_bionty.developmentalstage"),
                ),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(
                models.Model,
                lnschema_core.models.HasParents,
                lnschema_core.models.CanValidate,
            ),
        ),
    ]