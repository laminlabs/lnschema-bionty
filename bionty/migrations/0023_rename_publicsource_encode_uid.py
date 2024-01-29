# Generated by Django 4.2.9 on 2024-01-09 07:41

import django.db.models.deletion
import lnschema_core.users
from django.db import IntegrityError, migrations, models, transaction


def _encode_uid(orm, kwargs: dict) -> str:
    from bionty._bionty import encode_uid

    uid = kwargs.pop("uid")
    encoded = encode_uid(orm, kwargs)
    return encoded.get("uid", uid)


def forwards_func(apps, schema_editor):
    """Re-encode uids."""
    for model_name in [
        "CellLine",
        "CellMarker",
        "CellType",
        "DevelopmentalStage",
        "Disease",
        "Ethnicity",
        "ExperimentalFactor",
        "Gene",
        "Organism",
        "Pathway",
        "Phenotype",
        "Protein",
        "Tissue",
        "PublicSource",
    ]:
        model = apps.get_model("bionty", model_name)
        db_alias = schema_editor.connection.alias
        # see https://stackoverflow.com/a/23326971
        try:
            with transaction.atomic():
                records = model.objects.using(db_alias).all()
                for record in records:
                    record.uid = _encode_uid(model, record.__dict__)
                model.objects.using(db_alias).bulk_update(records, ["uid"])
        except IntegrityError:
            pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_core",
            "0039_remove_collection_artifacts_collectionartifact_and_more",
        ),
        ("bionty", "0022_rename_datasets_cellline_collections_and_more"),
    ]

    operations = [
        migrations.RenameModel(old_name="BiontySource", new_name="PublicSource"),
        migrations.AlterField(
            model_name="publicsource",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_public_sources",
                to="lnschema_core.user",
            ),
        ),
        migrations.RenameField(
            model_name="cellline",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="cellmarker",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="celltype",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="developmentalstage",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="disease",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="ethnicity",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="experimentalfactor",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="gene",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="organism",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="pathway",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="phenotype",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="protein",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RenameField(
            model_name="tissue",
            old_name="bionty_source",
            new_name="public_source",
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
