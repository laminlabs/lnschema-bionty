# Generated by Django 4.2.1 on 2023-07-20 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0008_remove_gene_hgnc_id_remove_gene_mgi_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gene",
            name="ensembl_gene_id",
            field=models.CharField(db_index=True, default=None, max_length=64, null=True, unique=True),
        ),
    ]
