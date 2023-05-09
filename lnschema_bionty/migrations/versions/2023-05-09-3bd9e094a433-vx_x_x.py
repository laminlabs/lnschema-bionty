"""vX.X.X."""
import sqlalchemy as sa  # noqa
import sqlmodel as sqm  # noqa
from alembic import op
from lnschema_core.dev.sqlmodel import get_sqlite_prefix_schema_delim_from_alembic

revision = "3bd9e094a433"
down_revision = "c6653a55d00a"


def upgrade() -> None:
    sqlite, prefix, schema, delim = get_sqlite_prefix_schema_delim_from_alembic()

    op.add_column(
        f"{prefix}cell_marker",
        sa.Column("synonyms", sqm.sql.sqltypes.AutoString(), nullable=True),
        schema=schema,
    )
    op.create_index(
        op.f(f"ix_bionty{delim}cell_marker_synonyms"),
        f"{prefix}cell_marker",
        ["synonyms"],
        unique=False,
        schema=schema,
    )

    op.create_index(
        op.f(f"ix_bionty{delim}cell_marker_ncbi_gene_id"),
        f"{prefix}cell_marker",
        ["ncbi_gene_id"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"ix_bionty{delim}cell_marker_gene_symbol"),
        f"{prefix}cell_marker",
        ["gene_symbol"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"ix_bionty{delim}cell_marker_gene_name"),
        f"{prefix}cell_marker",
        ["gene_name"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"ix_bionty{delim}cell_marker_uniprotkb_id"),
        f"{prefix}cell_marker",
        ["uniprotkb_id"],
        unique=False,
        schema=schema,
    )


def downgrade() -> None:
    pass
