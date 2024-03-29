# Generated by Django 4.2.5 on 2023-10-11 13:34

from pathlib import Path

import lamindb_setup as ln_setup
import pandas as pd
from django.db import migrations

import lnschema_bionty.models

CORE_MODELS = {
    "Species": False,
    "Gene": False,
    "Protein": False,
    "CellMarker": False,
    "Tissue": False,
    "CellType": False,
    "Disease": False,
    "CellLine": False,
    "Phenotype": False,
    "Pathway": False,
    "ExperimentalFactor": False,
    "DevelopmentalStage": False,
    "Ethnicity": False,
    "BiontySource": False,
}


def export_database(apps, schema_editor):
    def export_registry(registry, directory):
        table_name = registry._meta.db_table
        df = pd.read_sql_table(table_name, ln_setup.settings.instance.db)
        df.to_parquet(directory / f"{table_name}.parquet")

    # export data to parquet files
    directory = Path(f"./lamindb_export/{ln_setup.settings.instance.slug}/")
    directory.mkdir(parents=True, exist_ok=True)
    print(f"\nExporting data to parquet files in: {directory}\n")
    for model_name in CORE_MODELS.keys():
        registry = getattr(lnschema_bionty.models, model_name)
        export_registry(registry, directory)
        many_to_many_names = [field.name for field in registry._meta.many_to_many]
        for many_to_many_name in many_to_many_names:
            link_orm = getattr(registry, many_to_many_name).through
            export_registry(link_orm, directory)


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0015_migrate_to_integer_pks"),
    ]

    operations = [migrations.RunPython(export_database, reverse_code=migrations.RunPython.noop)]
