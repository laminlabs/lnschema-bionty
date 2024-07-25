# Generated by Django 5.1 on 2024-07-25 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0029_alter_cellline_previous_runs_and_more"),
        ("lnschema_core", "0055_artifact_type_artifactparamvalue_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PublicSource",
            new_name="Source",
        ),
        migrations.RenameField(
            model_name="cellline",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="cellmarker",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="celltype",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="developmentalstage",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="disease",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="ethnicity",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="experimentalfactor",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="gene",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="organism",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="pathway",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="phenotype",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="protein",
            old_name="public_source",
            new_name="source",
        ),
        migrations.RenameField(
            model_name="tissue",
            old_name="public_source",
            new_name="source",
        ),
        migrations.AddField(
            model_name="source",
            name="in_db",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AddField(
            model_name="source",
            name="artifacts",
            field=models.ManyToManyField(
                related_name="reference_of_sources", to="lnschema_core.artifact"
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="df",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reference_of_source",
                to="lnschema_core.artifact",
            ),
        ),
        migrations.RenameField(
            model_name="source",
            old_name="source",
            new_name="name",
        ),
    ]
