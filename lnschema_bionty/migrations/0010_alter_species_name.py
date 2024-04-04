# Generated by Django 4.2.1 on 2023-07-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0009_alter_gene_ensembl_gene_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="species",
            name="name",
            field=models.CharField(
                db_index=True, default=None, max_length=64, unique=True
            ),
        ),
    ]
