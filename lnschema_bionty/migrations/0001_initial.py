# Generated by Django 4.2.1 on 2023-06-09 14:14

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
            name="BiontySource",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.source,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "entity",
                    models.CharField(db_index=True, default=None, max_length=64),
                ),
                (
                    "species",
                    models.CharField(db_index=True, default=None, max_length=64),
                ),
                ("currently_used", models.BooleanField(db_index=True, default=False)),
                ("source_name", models.TextField(blank=True, db_index=True)),
                (
                    "source_key",
                    models.CharField(db_index=True, default=None, max_length=64),
                ),
                (
                    "version",
                    models.CharField(db_index=True, default=None, max_length=64),
                ),
                ("url", models.TextField(default=None, null=True)),
                ("md5", models.TextField(default=None, null=True)),
                ("source_website", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_bionty_sources",
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
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_index=True, default=None, max_length=64)),
                (
                    "taxon_id",
                    models.IntegerField(db_index=True, default=None, null=True, unique=True),
                ),
                (
                    "scientific_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_species",
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
                        max_length=12,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=64, null=True),
                ),
                (
                    "uniprotkb_id",
                    models.CharField(db_index=True, default=None, max_length=10, null=True),
                ),
                (
                    "uniprotkb_name",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("length", models.BigIntegerField(db_index=True, null=True)),
                ("gene_symbols", models.TextField(default=None, null=True)),
                ("gene_synonyms", models.TextField(default=None, null=True)),
                ("ensembl_transcript_ids", models.TextField(default=None, null=True)),
                ("ncbi_gene_ids", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_proteins",
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
                        max_length=12,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("ensembl_gene_id", models.CharField(db_index=True, max_length=64)),
                (
                    "symbol",
                    models.CharField(db_index=True, default=None, max_length=64, null=True),
                ),
                (
                    "gene_type",
                    models.CharField(db_index=True, default=None, max_length=64, null=True),
                ),
                ("description", models.TextField(default=None, null=True)),
                ("ncbi_gene_id", models.BigIntegerField(db_index=True, null=True)),
                (
                    "hgnc_id",
                    models.CharField(db_index=True, default=None, max_length=10, null=True),
                ),
                (
                    "mgi_id",
                    models.CharField(db_index=True, default=None, max_length=11, null=True),
                ),
                (
                    "omim_id",
                    models.CharField(db_index=True, default=None, max_length=6, null=True),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_genes",
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
            name="CellMarker",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_bionty.ids.cell_marker,
                        max_length=12,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                        unique=True,
                    ),
                ),
                (
                    "ncbi_gene_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                (
                    "gene_symbol",
                    models.CharField(db_index=True, default=None, max_length=64, null=True),
                ),
                ("gene_name", models.TextField(default=None, null=True)),
                (
                    "uniprotkb_id",
                    models.CharField(db_index=True, default=None, max_length=10, null=True),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_cell_markers",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_tissues",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("molecule", models.TextField(db_index=True, default=None, null=True)),
                (
                    "instrument",
                    models.TextField(db_index=True, default=None, null=True),
                ),
                (
                    "measurement",
                    models.TextField(db_index=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_readouts",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_phenotypes",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_pathways",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_diseases",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_cell_types",
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
                        default=lnschema_bionty.ids.ontology,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(db_index=True, default=None, max_length=256, null=True),
                ),
                (
                    "short_name",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                (
                    "ontology_id",
                    models.CharField(db_index=True, default=None, max_length=32, null=True),
                ),
                ("definition", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="lnschema_bionty.biontysource",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core._users.current_user_id,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="created_cell_lines",
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
