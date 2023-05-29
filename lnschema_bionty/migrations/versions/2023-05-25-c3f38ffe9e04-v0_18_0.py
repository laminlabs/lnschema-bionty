"""v0.18.0."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "c3f38ffe9e04"
down_revision = "017ac3ec86c5"


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="bionty.species", new_table_name="lnschema_bionty_species")
        op.rename_table(old_table_name="bionty.gene", new_table_name="lnschema_bionty_gene")
        op.rename_table(old_table_name="bionty.protein", new_table_name="lnschema_bionty_protein")
        op.rename_table(
            old_table_name="bionty.cell_marker",
            new_table_name="lnschema_bionty_cellmarker",
        )
        op.rename_table(old_table_name="bionty.tissue", new_table_name="lnschema_bionty_tissue")
        op.rename_table(old_table_name="bionty.disease", new_table_name="lnschema_bionty_disease")
        op.rename_table(old_table_name="bionty.cell_type", new_table_name="lnschema_bionty_celltype")
        op.rename_table(old_table_name="bionty.cell_line", new_table_name="lnschema_bionty_cellline")
        op.rename_table(old_table_name="bionty.pathway", new_table_name="lnschema_bionty_pathway")
        op.rename_table(
            old_table_name="bionty.phenotype",
            new_table_name="lnschema_bionty_phenotype",
        )
        op.rename_table(old_table_name="bionty.readout", new_table_name="lnschema_bionty_readout")
        op.rename_table(
            old_table_name="bionty.features_gene",
            new_table_name="lnschema_bionty_featuresgene",
        )
        op.rename_table(
            old_table_name="bionty.features_protein",
            new_table_name="lnschema_bionty_featuresprotein",
        )
        op.rename_table(
            old_table_name="bionty.features_cell_marker",
            new_table_name="lnschema_bionty_featurescellmarker",
        )
        op.rename_table(
            old_table_name="bionty.file_readout",
            new_table_name="lnschema_bionty_filereadout",
        )
        op.rename_table(
            old_table_name="bionty.bionty_versions",
            new_table_name="lnschema_bionty_biontyversions",
        )
        op.rename_table(
            old_table_name="bionty.current_bionty_versions",
            new_table_name="lnschema_bionty_currentbiontyversions",
        )
    else:
        op.rename_table(
            old_table_name="species",
            new_table_name="lnschema_bionty_species",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="gene",
            new_table_name="lnschema_bionty_gene",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="protein",
            new_table_name="lnschema_bionty_protein",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="cell_marker",
            new_table_name="lnschema_bionty_cellmarker",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="tissue",
            new_table_name="lnschema_bionty_tissue",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="disease",
            new_table_name="lnschema_bionty_disease",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="cell_type",
            new_table_name="lnschema_bionty_celltype",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="cell_line",
            new_table_name="lnschema_bionty_cellline",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="pathway",
            new_table_name="lnschema_bionty_pathway",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="phenotype",
            new_table_name="lnschema_bionty_phenotype",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="readout",
            new_table_name="lnschema_bionty_readout",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="features_gene",
            new_table_name="lnschema_bionty_featuresgene",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="features_protein",
            new_table_name="lnschema_bionty_featuresprotein",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="features_cell_marker",
            new_table_name="lnschema_bionty_featurescellmarker",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="file_readout",
            new_table_name="lnschema_bionty_filereadout",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="bionty_versions",
            new_table_name="lnschema_bionty_biontyversions",
            schema="bionty",
        )
        op.rename_table(
            old_table_name="current_bionty_versions",
            new_table_name="lnschema_bionty_currentbiontyversions",
            schema="bionty",
        )
        # there seems to be a bug in alembic autogenerate that doesn't pick this up
        op.execute("alter table bionty.lnschema_bionty_species set schema public")
        op.execute("alter table bionty.lnschema_bionty_gene set schema public")
        op.execute("alter table bionty.lnschema_bionty_protein set schema public")
        op.execute("alter table bionty.lnschema_bionty_cellmarker set schema public")
        op.execute("alter table bionty.lnschema_bionty_tissue set schema public")
        op.execute("alter table bionty.lnschema_bionty_disease set schema public")
        op.execute("alter table bionty.lnschema_bionty_celltype set schema public")
        op.execute("alter table bionty.lnschema_bionty_cellline set schema public")
        op.execute("alter table bionty.lnschema_bionty_pathway set schema public")
        op.execute("alter table bionty.lnschema_bionty_phenotype set schema public")
        op.execute("alter table bionty.lnschema_bionty_readout set schema public")
        op.execute("alter table bionty.lnschema_bionty_featuresgene set schema public")
        op.execute("alter table bionty.lnschema_bionty_featuresprotein set schema public")
        op.execute("alter table bionty.lnschema_bionty_featurescellmarker set schema public")
        op.execute("alter table bionty.lnschema_bionty_filereadout set schema public")
        op.execute("alter table bionty.lnschema_bionty_biontyversions set schema public")
        op.execute("alter table bionty.lnschema_bionty_currentbiontyversions set schema public")


def downgrade() -> None:
    pass
