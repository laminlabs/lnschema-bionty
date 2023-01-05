"""v0.7.0.

Revision ID: 6cbe4aa9aaec
Revises: 076bc2188ec3
Create Date: 2023-01-05 21:31:43.834874

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6cbe4aa9aaec"
down_revision = "076bc2188ec3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
    else:
        prefix, schema = "", "bionty"

    with op.batch_alter_table(f"{prefix}species", schema=schema) as batch_op:
        batch_op.add_column(sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        batch_op.drop_index("ix_bionty.species_common_name")
        batch_op.create_index(batch_op.f("ix_bionty.species_name"), ["name"], unique=True)
        batch_op.drop_column("common_name")


def downgrade() -> None:
    pass
