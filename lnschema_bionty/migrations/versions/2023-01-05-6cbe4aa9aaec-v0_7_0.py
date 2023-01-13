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

    op.alter_column(
        f"{prefix}species",
        column_name="common_name",
        new_column_name="name",
        schema=schema,
    )

    if sqlite:
        with op.batch_alter_table(f"{prefix}species") as batch_op:
            batch_op.drop_index("ix_bionty.species_common_name")
            batch_op.create_index(batch_op.f("ix_bionty.species_name"), ["name"], unique=True)
    else:
        op.drop_index("ix_bionty_species_common_name", table_name="species", schema=schema)
        op.create_index(
            op.f("ix_bionty_species_name"),
            "species",
            ["name"],
            unique=True,
            schema=schema,
        )


def downgrade() -> None:
    pass
