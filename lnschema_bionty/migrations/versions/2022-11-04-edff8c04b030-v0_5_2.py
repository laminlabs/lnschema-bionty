"""v0.5.2.

Revision ID: edff8c04b030
Revises: afda12fc80a8
Create Date: 2022-11-04 23:31:50.006936

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "edff8c04b030"
down_revision = "afda12fc80a8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("bionty.species", "short_name")

    with op.batch_alter_table("bionty.featureset", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_bionty_featureset_created_at"), ["created_at"], unique=False
        )
        batch_op.add_column(
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False)
        )
        batch_op.create_index(
            batch_op.f("ix_bionty_featureset_created_by"), ["created_by"], unique=False
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_bionty_featureset_created_by_user"),
            "core.user",
            ["created_by"],
            ["id"],
        )


def downgrade() -> None:
    pass
