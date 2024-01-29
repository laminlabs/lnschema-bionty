# Generated by Django 4.2.1 on 2023-11-13 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bionty", "0019_rename_taxon_id_organism_ontology_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organism",
            name="bionty_source",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="organisms",
                to="bionty.biontysource",
            ),
        ),
    ]
