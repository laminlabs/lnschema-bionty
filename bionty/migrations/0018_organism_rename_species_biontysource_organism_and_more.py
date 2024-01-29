# Generated by Django 4.2.1 on 2023-10-19 15:39

import django.db.models.deletion
import lnschema_core.models
import lnschema_core.users
from django.db import IntegrityError, migrations, models, transaction

import bionty.ids


def forwards_func(apps, schema_editor):
    """Replace strings in registry and registries."""
    Feature = apps.get_model("lnschema_core", "Feature")
    FeatureSet = apps.get_model("lnschema_core", "FeatureSet")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            for record in Feature.objects.using(db_alias).all():
                if isinstance(record.registries, str):
                    record.registries = record.registries.replace("bionty.Species", "bionty.Organism")
                    record.save()
            for record in FeatureSet.objects.using(db_alias).all():
                if isinstance(record.registry, str):
                    record.registry = record.registry.replace("bionty.Species", "bionty.Organism")
                    record.save()

    except IntegrityError:
        pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0024_import_legacy_data"),
        ("bionty", "0017_import_legacy_data"),
    ]
    operations = [
        migrations.RenameField(
            model_name="biontysource",
            old_name="species",
            new_name="organism",
        ),
        migrations.AlterUniqueTogether(
            name="biontysource",
            unique_together={("entity", "source", "organism", "version")},
        ),
        migrations.RenameModel(old_name="Species", new_name="Organism"),
        migrations.AlterField(
            model_name="organism",
            name="uid",
            field=models.CharField(unique=True, max_length=4, default=bionty.ids.organism),
        ),
        migrations.AlterField(
            model_name="organism",
            name="bionty_source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="bionty.biontysource",
            ),
        ),
        migrations.AlterField(
            model_name="organism",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_organism",
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="organism",
            name="datasets",
            field=models.ManyToManyField(related_name="organism", to="lnschema_core.dataset"),
        ),
        migrations.AlterField(
            model_name="organism",
            name="files",
            field=models.ManyToManyField(related_name="organism", to="lnschema_core.file"),
        ),
        migrations.RenameField(
            model_name="cellmarker",
            old_name="species",
            new_name="organism",
        ),
        migrations.AlterField(
            model_name="cellmarker",
            name="organism",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cell_markers",
                to="bionty.organism",
            ),
        ),
        migrations.RenameField(
            model_name="gene",
            old_name="species",
            new_name="organism",
        ),
        migrations.AlterField(
            model_name="gene",
            name="organism",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="genes",
                to="bionty.organism",
            ),
        ),
        migrations.RenameField(
            model_name="protein",
            old_name="species",
            new_name="organism",
        ),
        migrations.AlterField(
            model_name="protein",
            name="organism",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="proteins",
                to="bionty.organism",
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
