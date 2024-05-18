# Generated by Django 5.0.6 on 2024-05-18 21:18

import django.db.models.deletion
import lnschema_core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_bionty", "0026_artifactcellline_cell_line_ref_is_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artifactcellline",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactcellline",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactcellmarker",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactcellmarker",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactcelltype",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactcelltype",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactdevelopmentalstage",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactdevelopmentalstage",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactdisease",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactdisease",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactethnicity",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactethnicity",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactexperimentalfactor",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactexperimentalfactor",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactgene",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactgene",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactorganism",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactorganism",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactpathway",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactpathway",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactphenotype",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactphenotype",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifactprotein",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifactprotein",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="artifacttissue",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="artifacttissue",
            name="created_by",
        ),
        migrations.AlterField(
            model_name="artifactcellline",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactcellmarker",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactcelltype",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactdevelopmentalstage",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactdisease",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactethnicity",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactexperimentalfactor",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactgene",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactorganism",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactpathway",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactphenotype",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifactprotein",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="artifacttissue",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name="FeatureSetCellMarker",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "cellmarker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_bionty.cellmarker",
                    ),
                ),
                (
                    "featureset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lnschema_core.featureset",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.LinkORM),
        ),
        migrations.CreateModel(
            name="FeatureSetGene",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "featureset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lnschema_core.featureset",
                    ),
                ),
                (
                    "gene",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_bionty.gene",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.LinkORM),
        ),
        migrations.CreateModel(
            name="FeatureSetPathway",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "featureset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lnschema_core.featureset",
                    ),
                ),
                (
                    "pathway",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_bionty.pathway",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.LinkORM),
        ),
        migrations.CreateModel(
            name="FeatureSetProtein",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "featureset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="lnschema_core.featureset",
                    ),
                ),
                (
                    "protein",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="lnschema_bionty.protein",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, lnschema_core.models.LinkORM),
        ),
        migrations.RunSQL(
            """
            INSERT INTO lnschema_bionty_featuresetgene (featureset_id, gene_id)
            SELECT featureset_id, gene_id
            FROM lnschema_bionty_gene_feature_sets;
            """
        ),
        migrations.RunSQL(
            """
            INSERT INTO lnschema_bionty_featuresetprotein (featureset_id, protein_id)
            SELECT featureset_id, protein_id
            FROM lnschema_bionty_protein_feature_sets;
            """
        ),
        migrations.RunSQL(
            """
            INSERT INTO lnschema_bionty_featuresetcellmarker (featureset_id, cellmarker_id)
            SELECT featureset_id, cellmarker_id
            FROM lnschema_bionty_cellmarker_feature_sets;
            """
        ),
        migrations.RunSQL(
            """
            INSERT INTO lnschema_bionty_featuresetpathway (featureset_id, pathway_id)
            SELECT featureset_id, pathway_id
            FROM lnschema_bionty_pathway_feature_sets;
            """
        ),
        # Remove the old ManyToMany fields and replace them with the new through models
        migrations.RemoveField(
            model_name="gene",
            name="feature_sets",
        ),
        migrations.AddField(
            model_name="gene",
            name="feature_sets",
            field=models.ManyToManyField(
                through="lnschema_bionty.FeatureSetGene",
                to="lnschema_core.FeatureSet",
                related_name="genes",
            ),
        ),
        migrations.RemoveField(
            model_name="protein",
            name="feature_sets",
        ),
        migrations.AddField(
            model_name="protein",
            name="feature_sets",
            field=models.ManyToManyField(
                through="lnschema_bionty.FeatureSetProtein",
                to="lnschema_core.FeatureSet",
                related_name="proteins",
            ),
        ),
        migrations.RemoveField(
            model_name="cellmarker",
            name="feature_sets",
        ),
        migrations.AddField(
            model_name="cellmarker",
            name="feature_sets",
            field=models.ManyToManyField(
                through="lnschema_bionty.FeatureSetCellMarker",
                to="lnschema_core.FeatureSet",
                related_name="cell_markers",
            ),
        ),
        migrations.RemoveField(
            model_name="pathway",
            name="feature_sets",
        ),
        migrations.AddField(
            model_name="pathway",
            name="feature_sets",
            field=models.ManyToManyField(
                through="lnschema_bionty.FeatureSetPathway",
                to="lnschema_core.FeatureSet",
                related_name="pathways",
            ),
        ),
        migrations.RenameField(
            model_name="artifactcellline",
            old_name="cell_line",
            new_name="cellline",
        ),
        migrations.RenameField(
            model_name="artifactcellmarker",
            old_name="cell_marker",
            new_name="cellmarker",
        ),
        migrations.RenameField(
            model_name="artifactcelltype",
            old_name="cell_type",
            new_name="celltype",
        ),
        migrations.RenameField(
            model_name="artifactdevelopmentalstage",
            old_name="developmental_stage",
            new_name="developmentalstage",
        ),
    ]
