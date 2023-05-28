"""v0.17.0."""
import lnschema_core
import sqlalchemy as sa
import sqlmodel
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic
from packaging import version

revision = "017ac3ec86c5"
down_revision = "3bd9e094a433"

if version.parse(lnschema_core.__version__) >= version.parse("0.34a2"):
    user_table_name = "lnschema_core_user"
    referent_schema = "public"
else:
    user_table_name = "user"
    referent_schema = "core"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    with op.batch_alter_table(f"{prefix}cell_line", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_line_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_line_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}cell_marker", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_marker_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_marker_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}cell_type", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}cell_type_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}cell_type_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}disease", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}disease_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}disease_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}gene", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}gene_created_by"),
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(batch_op.f(f"ix_bionty{delim}gene_updated_at"), ["updated_at"], unique=False)
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}gene_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}pathway", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}pathway_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}pathway_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}phenotype", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}phenotype_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}phenotype_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}protein", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}protein_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}protein_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}species", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}species_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}species_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    with op.batch_alter_table(f"{prefix}tissue", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("created_by_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
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
            ["created_by_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f(f"ix_bionty{delim}tissue_updated_at"),
            ["updated_at"],
            unique=False,
        )
        batch_op.create_foreign_key(
            batch_op.f(f"fk_bionty{delim}tissue_created_by_user"),
            user_table_name,
            ["created_by_id"],
            ["id"],
            referent_schema=referent_schema,
        )

    op.alter_column(
        table_name=f"{prefix}readout",
        column_name="created_by",
        new_column_name="created_by_id",
        schema=schema,
    )


def downgrade() -> None:
    pass
