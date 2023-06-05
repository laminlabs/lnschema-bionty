# Generated by Django 4.2.1 on 2023-06-05 13:03

import django.db.models.deletion
import lnschema_core._users
from django.db import migrations, models

import lnschema_bionty.ids


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lnschema_core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BiontyVersions",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("entity", models.CharField(default=None, max_length=64)),
                ("source_name", models.TextField(blank=True, null=True)),
                ("source_key", models.CharField(default=None, max_length=64)),
                ("species", models.CharField(default=None, max_length=64)),
                ("version", models.CharField(default=None, max_length=64)),
                ("url", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("entity", "source_key", "species", "version")},
            },
        ),
        migrations.CreateModel(
            name="Species",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.species,
                        max_length=4,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
                ("taxon_id", models.IntegerField(blank=True, null=True, unique=True)),
                (
                    "scientific_name",
                    models.CharField(blank=True, max_length=64, null=True, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Protein",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.protein,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "uniprotkb_id",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                (
                    "uniprotkb_name",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("length", models.BigIntegerField()),
                ("gene_symbols", models.TextField(blank=True, null=True)),
                ("gene_synonyms", models.TextField(blank=True, null=True)),
                ("ensembl_transcript_ids", models.TextField(blank=True, null=True)),
                ("ncbi_gene_ids", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "featuresets",
                    models.ManyToManyField(related_name="proteins", to="lnschema_core.featureset"),
                ),
                (
                    "species",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.species",
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Gene",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.gene,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "ensembl_gene_id",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("symbol", models.CharField(blank=True, max_length=64, null=True)),
                ("gene_type", models.CharField(blank=True, max_length=64, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("ncbi_gene_id", models.BigIntegerField(blank=True, null=True)),
                ("hgnc_id", models.CharField(blank=True, max_length=10, null=True)),
                ("mgi_id", models.CharField(blank=True, max_length=11, null=True)),
                ("omim_id", models.CharField(blank=True, max_length=6, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("version", models.CharField(blank=True, max_length=64, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "featuresets",
                    models.ManyToManyField(related_name="genes", to="lnschema_core.featureset"),
                ),
                (
                    "species",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.species",
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="CurrentBiontyVersions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bionty_version",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        to="lnschema_bionty.biontyversions",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="CellMarker",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.cell_marker,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=64, null=True, unique=True),
                ),
                (
                    "ncbi_gene_id",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("gene_symbol", models.CharField(blank=True, max_length=64, null=True)),
                ("gene_name", models.TextField(blank=True, null=True)),
                (
                    "uniprotkb_id",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "featuresets",
                    models.ManyToManyField(related_name="cell_markers", to="lnschema_core.featureset"),
                ),
                (
                    "species",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.species",
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Tissue",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.tissue,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="tissues", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="Readout",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.readout,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("molecule", models.TextField(blank=True, null=True)),
                ("instrument", models.TextField(blank=True, null=True)),
                ("measurement", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="readouts", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="Phenotype",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.phenotype,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="phenotypes", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="Pathway",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.pathway,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "featuresets",
                    models.ManyToManyField(related_name="pathways", to="lnschema_core.featureset"),
                ),
                ("genes", models.ManyToManyField(to="lnschema_bionty.gene")),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="Disease",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.disease,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="diseases", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="CellType",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.cell_type,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="cell_types", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
        migrations.CreateModel(
            name="CellLine",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.cell_line,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=256, null=True)),
                ("short_name", models.CharField(blank=True, max_length=32, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("ontology_id", models.CharField(blank=True, max_length=16, null=True)),
                ("definition", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "files",
                    models.ManyToManyField(related_name="cell_lines", to="lnschema_core.file"),
                ),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "ontology_id")},
            },
        ),
    ]
