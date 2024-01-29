# Generated by Django 4.2.5 on 2023-10-11 13:34

from pathlib import Path

import lamindb_setup as ln_setup
from django.db import migrations

import bionty.models

CORE_MODELS = {
    "BiontySource": False,  # add this first
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
}


def import_registry(registry, directory, connection):
    import pandas as pd

    table_name = registry._meta.db_table
    df = pd.read_parquet(directory / f"{table_name}.parquet")
    old_foreign_key_columns = [column for column in df.columns if column.endswith("_old")]
    for column in old_foreign_key_columns:
        df.drop(column, axis=1, inplace=True)
    df.to_sql(table_name, connection, if_exists="append", index=False)


def import_db(apps, schema_editor):
    # import data from parquet files
    directory = Path(f"./lamindb_export/{ln_setup.settings.instance.identifier}/")
    if directory.exists():
        from sqlalchemy import create_engine

        engine = create_engine(ln_setup.settings.instance.db, echo=False)
        with engine.begin() as connection:
            if ln_setup.settings.instance.dialect == "postgresql":
                connection.execute("SET CONSTRAINTS ALL DEFERRED;")
            for model_name in CORE_MODELS.keys():
                registry = getattr(bionty.models, model_name)
                import_registry(registry, directory, connection)
                many_to_many_names = [field.name for field in registry._meta.many_to_many]
                for many_to_many_name in many_to_many_names:
                    link_orm = getattr(registry, many_to_many_name).through
                    import_registry(link_orm, directory, connection)


class Migration(migrations.Migration):
    dependencies = [
        ("bionty", "0001_initial_squashed_0016"),
        ("lnschema_core", "0024_import_legacy_data"),
    ]

    operations = [migrations.RunPython(import_db, reverse_code=migrations.RunPython.noop)]
