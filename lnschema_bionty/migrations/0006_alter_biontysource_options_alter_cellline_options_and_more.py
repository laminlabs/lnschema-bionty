# Generated by Django 4.2.1 on 2023-07-03 12:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0005_rename_short_name_cellline_abbr_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="biontysource",
            options={},
        ),
        migrations.AlterModelOptions(
            name="cellline",
            options={},
        ),
        migrations.AlterModelOptions(
            name="cellmarker",
            options={},
        ),
        migrations.AlterModelOptions(
            name="celltype",
            options={},
        ),
        migrations.AlterModelOptions(
            name="disease",
            options={},
        ),
        migrations.AlterModelOptions(
            name="gene",
            options={},
        ),
        migrations.AlterModelOptions(
            name="pathway",
            options={},
        ),
        migrations.AlterModelOptions(
            name="phenotype",
            options={},
        ),
        migrations.AlterModelOptions(
            name="protein",
            options={},
        ),
        migrations.AlterModelOptions(
            name="readout",
            options={},
        ),
        migrations.AlterModelOptions(
            name="species",
            options={},
        ),
        migrations.AlterModelOptions(
            name="tissue",
            options={},
        ),
    ]
