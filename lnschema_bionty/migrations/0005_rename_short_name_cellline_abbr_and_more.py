# Generated by Django 4.2.1 on 2023-06-29 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0004_alter_cellline_bionty_source_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cellline",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="cellline",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="cellmarker",
            old_name="featuresets",
            new_name="feature_sets",
        ),
        migrations.RenameField(
            model_name="celltype",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="celltype",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="disease",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="disease",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="gene",
            old_name="featuresets",
            new_name="feature_sets",
        ),
        migrations.RenameField(
            model_name="pathway",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="pathway",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="pathway",
            old_name="featuresets",
            new_name="feature_sets",
        ),
        migrations.RenameField(
            model_name="phenotype",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="phenotype",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="protein",
            old_name="featuresets",
            new_name="feature_sets",
        ),
        migrations.RenameField(
            model_name="readout",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="readout",
            old_name="definition",
            new_name="description",
        ),
        migrations.RenameField(
            model_name="tissue",
            old_name="short_name",
            new_name="abbr",
        ),
        migrations.RenameField(
            model_name="tissue",
            old_name="definition",
            new_name="description",
        ),
        migrations.AddField(
            model_name="cellline",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.cellline"),
        ),
        migrations.AddField(
            model_name="celltype",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.celltype"),
        ),
        migrations.AddField(
            model_name="disease",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.disease"),
        ),
        migrations.AddField(
            model_name="pathway",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.pathway"),
        ),
        migrations.AddField(
            model_name="phenotype",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.phenotype"),
        ),
        migrations.AddField(
            model_name="readout",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.readout"),
        ),
        migrations.AddField(
            model_name="tissue",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_bionty.tissue"),
        ),
    ]