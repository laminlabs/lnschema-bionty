# Generated by Django 4.2.1 on 2023-07-31 14:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bionty", "0011_cellline_datasets_cellmarker_datasets_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="gene",
            name="stable_id",
            field=models.CharField(db_index=True, default=None, max_length=64, null=True, unique=True),
        ),
    ]
