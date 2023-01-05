"""v0.6.4.

Revision ID: 076bc2188ec3
Revises: 078d771bc2a0
Create Date: 2023-01-05 18:14:17.293599

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "076bc2188ec3"
down_revision = "078d771bc2a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
    else:
        prefix, schema = "", "bionty"

    if not sqlite:
        # move to new schema
        op.execute(f"ALTER TABLE features_gene set SCHEMA {schema}")
        op.execute(f"ALTER TABLE features_protein set SCHEMA {schema}")
        op.execute(f"ALTER TABLE features_cell_marker set SCHEMA {schema}")
    else:
        op.rename_table("features_gene", f"{prefix}features_gene", schema=schema)
        op.rename_table("features_protein", f"{prefix}features_protein", schema=schema)
        op.rename_table("features_cell_marker", f"{prefix}features_cell_marker", schema=schema)


def downgrade() -> None:
    pass