# Generated by Django 4.2.5 on 2023-10-12 09:03

import django.db.models.deletion
import lnschema_core.users
from django.db import migrations, models

import lnschema_bionty.ids


class Migration(migrations.Migration):
    replaces = [
        ("lnschema_bionty", "0001_initial"),
        ("lnschema_bionty", "0002_rename_gene_type_gene_biotype_and_more"),
        ("lnschema_bionty", "0003_alter_biontysource_entity_alter_biontysource_source_and_more"),
        ("lnschema_bionty", "0004_alter_cellline_bionty_source_and_more"),
        ("lnschema_bionty", "0005_rename_short_name_cellline_abbr_and_more"),
        ("lnschema_bionty", "0006_alter_biontysource_options_alter_cellline_options_and_more"),
        ("lnschema_bionty", "0007_rename_readout_experimental_factor"),
        ("lnschema_bionty", "0008_remove_gene_hgnc_id_remove_gene_mgi_id_and_more"),
        ("lnschema_bionty", "0009_alter_gene_ensembl_gene_id"),
        ("lnschema_bionty", "0010_alter_species_name"),
        ("lnschema_bionty", "0011_cellline_datasets_cellmarker_datasets_and_more"),
        ("lnschema_bionty", "0012_gene_stable_id"),
        ("lnschema_bionty", "0013_alter_cellmarker_species_alter_gene_species_and_more"),
        ("lnschema_bionty", "0014_ethnicity_developmentalstage"),
        ("lnschema_bionty", "0015_migrate_to_integer_pks"),
        ("lnschema_bionty", "0016_export_legacy_data"),
    ]

    dependencies = [
        ("lnschema_core", "0023_export_legacy_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="BiontySource",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.biontysource, max_length=8)),
                ("entity", models.CharField(db_index=True, max_length=64)),
                ("species", models.CharField(db_index=True, max_length=64)),
                ("currently_used", models.BooleanField(db_index=True, default=False)),
                ("source", models.CharField(db_index=True, max_length=64)),
                ("source_name", models.TextField(blank=True, db_index=True)),
                ("version", models.CharField(db_index=True, max_length=64)),
                ("url", models.TextField(default=None, null=True)),
                ("md5", models.TextField(default=None, null=True)),
                ("source_website", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_bionty_sources",
                        to="lnschema_core.user",
                    ),
                ),
            ],
            options={
                "unique_together": {("entity", "source", "species", "version")},
            },
        ),
        migrations.CreateModel(
            name="Species",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.species, max_length=4)),
                ("name", models.CharField(db_index=True, default=None, max_length=64, unique=True)),
                ("taxon_id", models.IntegerField(db_index=True, default=None, null=True, unique=True)),
                ("scientific_name", models.CharField(db_index=True, default=None, max_length=64, null=True, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                ("bionty_source", models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_bionty.biontysource")),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_species",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="species", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="species", to="lnschema_core.file")),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Protein",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.protein, max_length=12)),
                ("name", models.CharField(db_index=True, default=None, max_length=64, null=True)),
                ("uniprotkb_id", models.CharField(db_index=True, default=None, max_length=10, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("length", models.BigIntegerField(db_index=True, null=True)),
                ("gene_symbol", models.CharField(db_index=True, default=None, max_length=64, null=True)),
                ("ensembl_gene_ids", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="proteins", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_proteins",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="proteins", to="lnschema_core.dataset")),
                ("feature_sets", models.ManyToManyField(related_name="proteins", to="lnschema_core.featureset")),
                ("files", models.ManyToManyField(related_name="proteins", to="lnschema_core.file")),
                (
                    "species",
                    models.ForeignKey(
                        default=None, on_delete=django.db.models.deletion.PROTECT, related_name="proteins", to="lnschema_bionty.species"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Gene",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.gene, max_length=12)),
                ("symbol", models.CharField(db_index=True, default=None, max_length=64, null=True)),
                ("stable_id", models.CharField(db_index=True, default=None, max_length=64, null=True, unique=True)),
                ("ensembl_gene_id", models.CharField(db_index=True, default=None, max_length=64, null=True, unique=True)),
                ("ncbi_gene_ids", models.TextField(default=None, null=True)),
                ("biotype", models.CharField(db_index=True, default=None, max_length=64, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="genes", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_genes",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="genes", to="lnschema_core.dataset")),
                ("feature_sets", models.ManyToManyField(related_name="genes", to="lnschema_core.featureset")),
                ("files", models.ManyToManyField(related_name="genes", to="lnschema_core.file")),
                (
                    "species",
                    models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name="genes", to="lnschema_bionty.species"),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="CellMarker",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.cellmarker, max_length=12)),
                ("name", models.CharField(db_index=True, default=None, max_length=64, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("gene_symbol", models.CharField(db_index=True, default=None, max_length=64, null=True)),
                ("ncbi_gene_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("uniprotkb_id", models.CharField(db_index=True, default=None, max_length=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="cell_markers", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_cell_markers",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="cell_markers", to="lnschema_core.dataset")),
                ("feature_sets", models.ManyToManyField(related_name="cell_markers", to="lnschema_core.featureset")),
                ("files", models.ManyToManyField(related_name="cell_markers", to="lnschema_core.file")),
                (
                    "species",
                    models.ForeignKey(
                        default=None, on_delete=django.db.models.deletion.PROTECT, related_name="cell_markers", to="lnschema_bionty.species"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Tissue",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="tissues", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_tissues",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="tissues", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="tissues", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.tissue")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Phenotype",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="phenotypes", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_phenotypes",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="phenotypes", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="phenotypes", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.phenotype")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Pathway",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="pathways", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_pathways",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="pathways", to="lnschema_core.dataset")),
                ("feature_sets", models.ManyToManyField(related_name="pathways", to="lnschema_core.featureset")),
                ("files", models.ManyToManyField(related_name="pathways", to="lnschema_core.file")),
                ("genes", models.ManyToManyField(related_name="pathways", to="lnschema_bionty.gene")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.pathway")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="ExperimentalFactor",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("molecule", models.TextField(db_index=True, default=None, null=True)),
                ("instrument", models.TextField(db_index=True, default=None, null=True)),
                ("measurement", models.TextField(db_index=True, default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="experimental_factors", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_experimental_factors",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="experimental_factors", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="experimental_factors", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.experimentalfactor")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Ethnicity",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="ethnicities", to="lnschema_bionty.biontysource"
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
                ("datasets", models.ManyToManyField(related_name="ethnicities", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="ethnicities", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.ethnicity")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="Disease",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="diseases", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_diseases",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="diseases", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="diseases", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.disease")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="DevelopmentalStage",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="developmental_stages", to="lnschema_bionty.biontysource"
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
                ("datasets", models.ManyToManyField(related_name="developmental_stages", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="developmental_stages", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.developmentalstage")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="CellType",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="cell_types", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_cell_types",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="cell_types", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="cell_types", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.celltype")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
        migrations.CreateModel(
            name="CellLine",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("uid", models.CharField(unique=True, default=lnschema_bionty.ids.ontology, max_length=8)),
                ("name", models.CharField(db_index=True, max_length=256)),
                ("ontology_id", models.CharField(db_index=True, default=None, max_length=32, null=True)),
                ("abbr", models.CharField(db_index=True, default=None, max_length=32, null=True, unique=True)),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "bionty_source",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.PROTECT, related_name="cell_lines", to="lnschema_bionty.biontysource"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_cell_lines",
                        to="lnschema_core.user",
                    ),
                ),
                ("datasets", models.ManyToManyField(related_name="cell_lines", to="lnschema_core.dataset")),
                ("files", models.ManyToManyField(related_name="cell_lines", to="lnschema_core.file")),
                ("parents", models.ManyToManyField(related_name="children", to="lnschema_bionty.cellline")),
            ],
            options={
                "unique_together": {("name", "ontology_id")},
            },
            bases=(models.Model, lnschema_core.models.HasParents, lnschema_core.models.CanValidate),
        ),
    ]
