"""v0.18.0b."""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "c5ebdad85b31"
down_revision = "c3f38ffe9e04"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.drop_index(f"ix_bionty{delim}bionty_versions_created_at", table_name="lnschema_bionty_biontyversions")
    op.drop_index(f"ix_bionty{delim}bionty_versions_created_by", table_name="lnschema_bionty_biontyversions")
    op.drop_index(f"ix_bionty{delim}bionty_versions_database", table_name="lnschema_bionty_biontyversions")
    op.drop_index(f"ix_bionty{delim}bionty_versions_database_v", table_name="lnschema_bionty_biontyversions")
    op.drop_index(f"ix_bionty{delim}bionty_versions_entity", table_name="lnschema_bionty_biontyversions")
    op.drop_index(f"ix_bionty{delim}bionty_versions_updated_at", table_name="lnschema_bionty_biontyversions")
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_created_at"), "lnschema_bionty_biontyversions", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_created_by"), "lnschema_bionty_biontyversions", ["created_by"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_database"), "lnschema_bionty_biontyversions", ["database"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_database_v"), "lnschema_bionty_biontyversions", ["database_v"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_entity"), "lnschema_bionty_biontyversions", ["entity"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_biontyversions_updated_at"), "lnschema_bionty_biontyversions", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}cell_line_created_at", table_name="lnschema_bionty_cellline")
    op.drop_index(f"ix_bionty{delim}cell_line_created_by", table_name="lnschema_bionty_cellline")
    op.drop_index(f"ix_bionty{delim}cell_line_name", table_name="lnschema_bionty_cellline")
    op.drop_index(f"ix_bionty{delim}cell_line_ontology_id", table_name="lnschema_bionty_cellline")
    op.drop_index(f"ix_bionty{delim}cell_line_updated_at", table_name="lnschema_bionty_cellline")
    op.create_index(op.f("ix_lnschema_bionty_cellline_created_at"), "lnschema_bionty_cellline", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellline_created_by_id"), "lnschema_bionty_cellline", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellline_ontology_id"), "lnschema_bionty_cellline", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellline_updated_at"), "lnschema_bionty_cellline", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}cell_marker_created_at", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_created_by", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_gene_name", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_gene_symbol", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_name", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_ncbi_gene_id", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_synonyms", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_uniprotkb_id", table_name="lnschema_bionty_cellmarker")
    op.drop_index(f"ix_bionty{delim}cell_marker_updated_at", table_name="lnschema_bionty_cellmarker")
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_created_at"), "lnschema_bionty_cellmarker", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_created_by_id"), "lnschema_bionty_cellmarker", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_gene_name"), "lnschema_bionty_cellmarker", ["gene_name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_gene_symbol"), "lnschema_bionty_cellmarker", ["gene_symbol"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_name"), "lnschema_bionty_cellmarker", ["name"], unique=True)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_ncbi_gene_id"), "lnschema_bionty_cellmarker", ["ncbi_gene_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_synonyms"), "lnschema_bionty_cellmarker", ["synonyms"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_uniprotkb_id"), "lnschema_bionty_cellmarker", ["uniprotkb_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_cellmarker_updated_at"), "lnschema_bionty_cellmarker", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}cell_type_created_at", table_name="lnschema_bionty_celltype")
    op.drop_index(f"ix_bionty{delim}cell_type_created_by", table_name="lnschema_bionty_celltype")
    op.drop_index(f"ix_bionty{delim}cell_type_name", table_name="lnschema_bionty_celltype")
    op.drop_index(f"ix_bionty{delim}cell_type_ontology_id", table_name="lnschema_bionty_celltype")
    op.drop_index(f"ix_bionty{delim}cell_type_updated_at", table_name="lnschema_bionty_celltype")
    op.create_index(op.f("ix_lnschema_bionty_celltype_created_at"), "lnschema_bionty_celltype", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_celltype_created_by_id"), "lnschema_bionty_celltype", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_celltype_name"), "lnschema_bionty_celltype", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_celltype_ontology_id"), "lnschema_bionty_celltype", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_celltype_updated_at"), "lnschema_bionty_celltype", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}current_bionty_versions_created_at", table_name="lnschema_bionty_currentbiontyversions")
    op.drop_index(f"ix_bionty{delim}current_bionty_versions_created_by", table_name="lnschema_bionty_currentbiontyversions")
    op.drop_index(f"ix_bionty{delim}current_bionty_versions_entity", table_name="lnschema_bionty_currentbiontyversions")
    op.drop_index(f"ix_bionty{delim}current_bionty_versions_updated_at", table_name="lnschema_bionty_currentbiontyversions")
    op.create_index(
        op.f("ix_lnschema_bionty_currentbiontyversions_created_at"), "lnschema_bionty_currentbiontyversions", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_lnschema_bionty_currentbiontyversions_created_by"), "lnschema_bionty_currentbiontyversions", ["created_by"], unique=False
    )
    op.create_index(op.f("ix_lnschema_bionty_currentbiontyversions_entity"), "lnschema_bionty_currentbiontyversions", ["entity"], unique=True)
    op.create_index(
        op.f("ix_lnschema_bionty_currentbiontyversions_updated_at"), "lnschema_bionty_currentbiontyversions", ["updated_at"], unique=False
    )

    op.drop_index(f"ix_bionty{delim}disease_created_at", table_name="lnschema_bionty_disease")
    op.drop_index(f"ix_bionty{delim}disease_created_by", table_name="lnschema_bionty_disease")
    op.drop_index(f"ix_bionty{delim}disease_name", table_name="lnschema_bionty_disease")
    op.drop_index(f"ix_bionty{delim}disease_ontology_id", table_name="lnschema_bionty_disease")
    op.drop_index(f"ix_bionty{delim}disease_updated_at", table_name="lnschema_bionty_disease")
    op.create_index(op.f("ix_lnschema_bionty_disease_created_at"), "lnschema_bionty_disease", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_disease_created_by_id"), "lnschema_bionty_disease", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_disease_name"), "lnschema_bionty_disease", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_disease_ontology_id"), "lnschema_bionty_disease", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_disease_updated_at"), "lnschema_bionty_disease", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}gene_created_at", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_created_by", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_ensembl_gene_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_gene_type", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_hgnc_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_mgi_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_ncbi_gene_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_omim_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_species_id", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_symbol", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_synonyms", table_name="lnschema_bionty_gene")
    op.drop_index(f"ix_bionty{delim}gene_updated_at", table_name="lnschema_bionty_gene")
    op.create_index(op.f("ix_lnschema_bionty_gene_created_at"), "lnschema_bionty_gene", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_created_by_id"), "lnschema_bionty_gene", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_ensembl_gene_id"), "lnschema_bionty_gene", ["ensembl_gene_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_gene_type"), "lnschema_bionty_gene", ["gene_type"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_hgnc_id"), "lnschema_bionty_gene", ["hgnc_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_mgi_id"), "lnschema_bionty_gene", ["mgi_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_ncbi_gene_id"), "lnschema_bionty_gene", ["ncbi_gene_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_omim_id"), "lnschema_bionty_gene", ["omim_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_species_id"), "lnschema_bionty_gene", ["species_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_symbol"), "lnschema_bionty_gene", ["symbol"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_synonyms"), "lnschema_bionty_gene", ["synonyms"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_gene_updated_at"), "lnschema_bionty_gene", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}pathway_created_at", table_name="lnschema_bionty_pathway")
    op.drop_index(f"ix_bionty{delim}pathway_created_by", table_name="lnschema_bionty_pathway")
    op.drop_index(f"ix_bionty{delim}pathway_name", table_name="lnschema_bionty_pathway")
    op.drop_index(f"ix_bionty{delim}pathway_ontology_id", table_name="lnschema_bionty_pathway")
    op.drop_index(f"ix_bionty{delim}pathway_updated_at", table_name="lnschema_bionty_pathway")
    op.create_index(op.f("ix_lnschema_bionty_pathway_created_at"), "lnschema_bionty_pathway", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_pathway_created_by_id"), "lnschema_bionty_pathway", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_pathway_name"), "lnschema_bionty_pathway", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_pathway_ontology_id"), "lnschema_bionty_pathway", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_pathway_updated_at"), "lnschema_bionty_pathway", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}phenotype_created_at", table_name="lnschema_bionty_phenotype")
    op.drop_index(f"ix_bionty{delim}phenotype_created_by", table_name="lnschema_bionty_phenotype")
    op.drop_index(f"ix_bionty{delim}phenotype_name", table_name="lnschema_bionty_phenotype")
    op.drop_index(f"ix_bionty{delim}phenotype_ontology_id", table_name="lnschema_bionty_phenotype")
    op.drop_index(f"ix_bionty{delim}phenotype_updated_at", table_name="lnschema_bionty_phenotype")
    op.create_index(op.f("ix_lnschema_bionty_phenotype_created_at"), "lnschema_bionty_phenotype", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_phenotype_created_by_id"), "lnschema_bionty_phenotype", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_phenotype_name"), "lnschema_bionty_phenotype", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_phenotype_ontology_id"), "lnschema_bionty_phenotype", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_phenotype_updated_at"), "lnschema_bionty_phenotype", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}protein_created_at", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_created_by", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_ensembl_transcript_ids", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_name", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_ncbi_gene_ids", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_protein_names", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_uniprotkb_id", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_uniprotkb_name", table_name="lnschema_bionty_protein")
    op.drop_index(f"ix_bionty{delim}protein_updated_at", table_name="lnschema_bionty_protein")
    op.create_index(op.f("ix_lnschema_bionty_protein_created_at"), "lnschema_bionty_protein", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_created_by_id"), "lnschema_bionty_protein", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_ensembl_transcript_ids"), "lnschema_bionty_protein", ["ensembl_transcript_ids"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_name"), "lnschema_bionty_protein", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_ncbi_gene_ids"), "lnschema_bionty_protein", ["ncbi_gene_ids"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_protein_names"), "lnschema_bionty_protein", ["protein_names"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_uniprotkb_id"), "lnschema_bionty_protein", ["uniprotkb_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_uniprotkb_name"), "lnschema_bionty_protein", ["uniprotkb_name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_protein_updated_at"), "lnschema_bionty_protein", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}readout_created_at", table_name="lnschema_bionty_readout")
    op.drop_index(f"ix_bionty{delim}readout_created_by", table_name="lnschema_bionty_readout")
    op.drop_index(f"ix_bionty{delim}readout_efo_id", table_name="lnschema_bionty_readout")
    op.drop_index(f"ix_bionty{delim}readout_updated_at", table_name="lnschema_bionty_readout")
    op.create_index(op.f("ix_lnschema_bionty_readout_created_at"), "lnschema_bionty_readout", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_readout_created_by_id"), "lnschema_bionty_readout", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_readout_updated_at"), "lnschema_bionty_readout", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}species_created_at", table_name="lnschema_bionty_species")
    op.drop_index(f"ix_bionty{delim}species_created_by", table_name="lnschema_bionty_species")
    op.drop_index(f"ix_bionty{delim}species_name", table_name="lnschema_bionty_species")
    op.drop_index(f"ix_bionty{delim}species_scientific_name", table_name="lnschema_bionty_species")
    op.drop_index(f"ix_bionty{delim}species_taxon_id", table_name="lnschema_bionty_species")
    op.drop_index(f"ix_bionty{delim}species_updated_at", table_name="lnschema_bionty_species")
    op.create_index(op.f("ix_lnschema_bionty_species_created_at"), "lnschema_bionty_species", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_species_created_by_id"), "lnschema_bionty_species", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_species_name"), "lnschema_bionty_species", ["name"], unique=True)
    op.create_index(op.f("ix_lnschema_bionty_species_scientific_name"), "lnschema_bionty_species", ["scientific_name"], unique=True)
    op.create_index(op.f("ix_lnschema_bionty_species_taxon_id"), "lnschema_bionty_species", ["taxon_id"], unique=True)
    op.create_index(op.f("ix_lnschema_bionty_species_updated_at"), "lnschema_bionty_species", ["updated_at"], unique=False)

    op.drop_index(f"ix_bionty{delim}tissue_created_at", table_name="lnschema_bionty_tissue")
    op.drop_index(f"ix_bionty{delim}tissue_created_by", table_name="lnschema_bionty_tissue")
    op.drop_index(f"ix_bionty{delim}tissue_name", table_name="lnschema_bionty_tissue")
    op.drop_index(f"ix_bionty{delim}tissue_ontology_id", table_name="lnschema_bionty_tissue")
    op.drop_index(f"ix_bionty{delim}tissue_updated_at", table_name="lnschema_bionty_tissue")
    op.create_index(op.f("ix_lnschema_bionty_tissue_created_at"), "lnschema_bionty_tissue", ["created_at"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_tissue_created_by_id"), "lnschema_bionty_tissue", ["created_by_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_tissue_name"), "lnschema_bionty_tissue", ["name"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_tissue_ontology_id"), "lnschema_bionty_tissue", ["ontology_id"], unique=False)
    op.create_index(op.f("ix_lnschema_bionty_tissue_updated_at"), "lnschema_bionty_tissue", ["updated_at"], unique=False)

    with op.batch_alter_table("lnschema_bionty_cellline", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_cellline_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_cellline_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_cellline_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_cellline_name_ontology_id", ["name", "ontology_id"])

    with op.batch_alter_table("lnschema_bionty_celltype", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_celltype_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_celltype_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_celltype_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_celltype_name_ontology_id", ["name", "ontology_id"])

    with op.batch_alter_table("lnschema_bionty_disease", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_disease_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_disease_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_disease_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_disease_name_ontology_id", ["name", "ontology_id"])

    with op.batch_alter_table("lnschema_bionty_pathway", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_pathway_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_pathway_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_pathway_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_pathway_name_ontology_id", ["name", "ontology_id"])

    with op.batch_alter_table("lnschema_bionty_phenotype", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_phenotype_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_phenotype_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_phenotype_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_phenotype_name_ontology_id", ["name", "ontology_id"])

    with op.batch_alter_table("lnschema_bionty_readout", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("ontology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(batch_op.f("ix_lnschema_bionty_readout_name"), ["name"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_readout_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_readout_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_readout_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_readout_name_ontology_id", ["name", "ontology_id"])
        batch_op.drop_column("efo_id")

    with op.batch_alter_table("lnschema_bionty_tissue", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_tissue_definition"),
            ["definition"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_tissue_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(batch_op.f("ix_lnschema_bionty_tissue_synonyms"), ["synonyms"], unique=False)
        batch_op.create_unique_constraint("uq_tissue_name_ontology_id", ["name", "ontology_id"])


def downgrade() -> None:
    pass
