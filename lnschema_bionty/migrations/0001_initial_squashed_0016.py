# Generated by Django 4.2.5 on 2023-10-12 09:03

from django.db import migrations


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
        ("lnschema_core", "0024_import_legacy_data"),
    ]
