"""vX.X.X."""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "017ac3ec86c5"
down_revision = "3bd9e094a433"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    with op.batch_alter_table(f"{prefix}cell_line", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_line_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.cell_marker", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_marker_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_marker_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_marker_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_marker_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.cell_type", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_type_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.disease", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}disease_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.gene", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}gene_created_at"), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}gene_created_by"), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}gene_updated_at"), ["updated_at"], unique=False)
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}gene_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.pathway", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}pathway_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.phenotype", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}phenotype_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.protein", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}protein_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}protein_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}protein_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}protein_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.species", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}species_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}species_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}species_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}species_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )

    with op.batch_alter_table("bionty.tissue", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=True))
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_created_at"),
            ["created_at"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_created_by"),
            ["created_by"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}tissue_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
            referent_schema="core",
        )


def downgrade() -> None:
    pass
