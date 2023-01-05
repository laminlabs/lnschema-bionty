"""v0.3.1.

Revision ID: 7f9a3b24a42b
Revises:
Create Date: 2022-09-22 21:16:15.277390

"""
import sqlalchemy as sa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7f9a3b24a42b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("version_zdno", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )
        batch_op.create_index(batch_op.f("ix_version_zdno_created_at"), ["created_at"], unique=False)
        batch_op.drop_column("time_created")


def downgrade() -> None:
    pass
