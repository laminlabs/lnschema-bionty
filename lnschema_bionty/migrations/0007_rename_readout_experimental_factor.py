# Generated by Django 4.2.1 on 2023-07-17 14:22
import django
import lnschema_core.users
from django.db import IntegrityError, migrations, models, transaction


def forwards_func(apps, schema_editor):
    """Rename Readout entity in BiontySource table."""
    BiontySource = apps.get_model("lnschema_bionty", "BiontySource")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            BiontySource.objects.using(db_alias).filter(entity="Readout").update(entity="ExperimentalFactor")
    except IntegrityError:
        pass


def reverse_func(apps, schema_editor):
    """Rename Readout entity in BiontySource table."""
    BiontySource = apps.get_model("lnschema_bionty", "BiontySource")
    db_alias = schema_editor.connection.alias
    try:
        with transaction.atomic():
            BiontySource.objects.using(db_alias).filter(entity="ExperimentalFactor").update(entity="Readout")
    except IntegrityError:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0008_file_hash_type_transform_parents"),
        (
            "lnschema_bionty",
            "0006_alter_biontysource_options_alter_cellline_options_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(old_name="Readout", new_name="ExperimentalFactor"),
        migrations.AlterField(
            model_name="experimentalfactor",
            name="files",
            field=models.ManyToManyField(to="lnschema_core.File", related_name="experimental_factors"),
        ),
        migrations.AlterField(
            model_name="experimentalfactor",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_experimental_factors",
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="experimentalfactor",
            name="bionty_source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="experimental_factors",
                to="lnschema_bionty.biontysource",
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]