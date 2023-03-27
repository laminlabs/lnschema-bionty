"""v0.10.0."""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "5594b330a854"
down_revision = "4429de4e490b"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
    else:
        prefix, schema = "", "bionty"

    op.alter_column(
        table_name=f"{prefix}cell_marker",
        column_name="ncbi_gene_ids",
        new_column_name="ncbi_gene_id",
        schema=schema,
    )

    op.alter_column(
        table_name=f"{prefix}cell_marker",
        column_name="gene_symbols",
        new_column_name="gene_symbol",
        schema=schema,
    )

    op.alter_column(
        table_name=f"{prefix}cell_marker",
        column_name="protein_names",
        new_column_name="gene_name",
        schema=schema,
    )

    op.alter_column(
        table_name=f"{prefix}cell_marker",
        column_name="uniprotkb_ids",
        new_column_name="uniprotkb_id",
        schema=schema,
    )


def downgrade() -> None:
    pass
