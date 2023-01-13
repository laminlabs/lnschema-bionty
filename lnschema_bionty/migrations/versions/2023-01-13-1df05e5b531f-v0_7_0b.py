"""v0.7.0b.

Revision ID: 1df05e5b531f
Revises: 6cbe4aa9aaec
Create Date: 2023-01-13 20:47:24.871767

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1df05e5b531f"
down_revision = "6cbe4aa9aaec"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
    else:
        prefix, schema = "", "bionty"

    op.alter_column(
        f"{prefix}species",
        "taxon_id",
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        existing_nullable=True,
        schema=schema,
    )


def downgrade() -> None:
    pass
