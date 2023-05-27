"""vX.X.X."""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "c5ebdad85b31"
down_revision = "c3f38ffe9e04"


def upgrade() -> None:
    with op.batch_alter_table("lnschema_bionty_cellline", schema=None) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("definition", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index("ix_lnschema_bionty_cellline_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_cellline_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_celltype_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_celltype_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_disease_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_disease_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_pathway_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_pathway_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_phenotype_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_phenotype_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_readout_efo_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_readout_definition"),
            ["definition"],
            unique=False,
        )
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
        batch_op.drop_index("ix_lnschema_bionty_tissue_ontology_id")
        batch_op.create_index(
            batch_op.f("ix_lnschema_bionty_tissue_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
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
