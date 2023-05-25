"""vX.X.X."""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "83669c1e990a"
down_revision = "017ac3ec86c5"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    with op.batch_alter_table(f"{prefix}cell_line", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}cell_line_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_cell_line_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_line_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}cell_marker", schema=schema) as batch_op:
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_marker_species_id_species"),
            "species",
            ["species_id"],
            ["id"],
            referent_schema="bionty",
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_marker_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}cell_type", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}cell_type_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_cell_type_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_type_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}disease", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}disease_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}disease_synonyms"), ["synonyms"], unique=False)
        batch_op.create_unique_constraint("uq_disease_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}disease_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}gene", schema=schema) as batch_op:
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}gene_species_id_species"),
            "species",
            ["species_id"],
            ["id"],
            referent_schema="bionty",
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}gene_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}pathway", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}pathway_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}pathway_synonyms"), ["synonyms"], unique=False)
        batch_op.create_unique_constraint("uq_pathway_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}pathway_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}phenotype", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}phenotype_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_synonyms"),
            ["synonyms"],
            unique=False,
        )
        batch_op.create_unique_constraint("uq_phenotype_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}phenotype_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}protein", schema=schema) as batch_op:
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}protein_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}protein_species_id_species"),
            "species",
            ["species_id"],
            ["id"],
            referent_schema="bionty",
        )

    with op.batch_alter_table(f"{prefix}readout", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}readout_name"), ["name"], unique=False)
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}readout_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}readout_synonyms"), ["synonyms"], unique=False)

    with op.batch_alter_table(f"{prefix}species", schema=schema) as batch_op:
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}species_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table(f"{prefix}tissue", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("short_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.add_column(sa.Column("synonyms", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index(f"ix_bionty{delim}tissue_ontology_id")
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_ontology_id"),
            ["ontology_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_short_name"),
            ["short_name"],
            unique=False,
        )
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}tissue_synonyms"), ["synonyms"], unique=False)
        batch_op.create_unique_constraint("uq_tissue_name_ontology_id", ["name", "ontology_id"])
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}tissue_created_by_user"),
            "user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )


def downgrade() -> None:
    pass
