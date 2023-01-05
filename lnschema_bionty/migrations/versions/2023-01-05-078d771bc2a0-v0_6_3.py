"""v0.6.3.

Revision ID: 078d771bc2a0
Revises: 4133eb176df0
Create Date: 2023-01-05 15:20:44.311685
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "078d771bc2a0"
down_revision = "4133eb176df0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
    else:
        prefix, schema = "", "bionty"

    if sqlite:
        op.rename_table("biontyversions", f"{prefix}bionty_versions")
        op.rename_table("currentbiontyversions", f"{prefix}current_bionty_versions")
    else:
        op.execute(f"ALTER TABLE biontyversions RENAME TO {schema}.bionty_versions")
        op.execute(
            "ALTER TABLE currentbiontyversions RENAME TO"
            f" {schema}.current_bionty_versions"
        )


def downgrade() -> None:
    pass
