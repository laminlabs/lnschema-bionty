# Generated by Django 4.2.1 on 2023-07-18 13:13

import pandas as pd
from django.db import IntegrityError, migrations, models, transaction


def forwards_func(apps, schema_editor):
    """Drop duplicated ensembl_gene_ids."""
    Gene = apps.get_model("lnschema_bionty", "Gene")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            Gene.objects.using(db_alias).filter(ensembl_gene_id="").update(
                ensembl_gene_id=None
            )
            df = pd.DataFrame(Gene.objects.using(db_alias).values())
            if "ensembl_gene_id" in df.columns:
                dup_ids = df[df["ensembl_gene_id"].duplicated()].id.tolist()
                if len(dup_ids) > 0:
                    Gene.objects.using(db_alias).filter(id__in=dup_ids).all().delete()

    except IntegrityError:
        pass


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0007_rename_readout_experimental_factor"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gene",
            name="hgnc_id",
        ),
        migrations.RemoveField(
            model_name="gene",
            name="mgi_id",
        ),
        migrations.RemoveField(
            model_name="gene",
            name="ncbi_gene_id",
        ),
        migrations.RemoveField(
            model_name="protein",
            name="ncbi_gene_ids",
        ),
        migrations.AddField(
            model_name="gene",
            name="ncbi_gene_ids",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="protein",
            name="ensembl_gene_ids",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="cellmarker",
            name="name",
            field=models.CharField(
                db_index=True, default=None, max_length=64, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="gene",
            name="ensembl_gene_id",
            field=models.CharField(
                db_index=True, default=None, max_length=64, null=True
            ),
        ),
        migrations.AlterField(
            model_name="protein",
            name="uniprotkb_id",
            field=models.CharField(
                db_index=True, default=None, max_length=10, null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="species",
            name="name",
            field=models.CharField(db_index=True, default=None, max_length=64),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
