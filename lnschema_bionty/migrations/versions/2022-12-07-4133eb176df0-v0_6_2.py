"""v0.6.2.

Revision ID: 4133eb176df0
Revises: a28d3b7a73b1
Create Date: 2022-12-07 08:50:14.221094

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4133eb176df0"
down_revision = "a28d3b7a73b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(
            old_table_name="bionty.bionty_versions",
            new_table_name="bionty.biontyversions",
        )
        op.alter_column(
            table_name="bionty.biontyversions",
            column_name="table",
            new_column_name="entity",
        )

        op.create_table(
            "bionty.currentbiontyversions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("entity", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["created_by"],
                ["core.user.id"],
                name=op.f("fk_bionty_currentbiontyversions_created_by_user"),
            ),
            sa.ForeignKeyConstraint(
                ["id"],
                ["bionty.biontyversions.id"],
                name=op.f("fk_bionty_currentbiontyversions_id_biontyversions"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_bionty_currentbiontyversions")),
        )
        with op.batch_alter_table("bionty.currentbiontyversions", schema=None) as batch_op:
            batch_op.create_index(
                batch_op.f("ix_bionty_currentbiontyversions_created_at"),
                ["created_at"],
                unique=False,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_currentbiontyversions_created_by"),
                ["created_by"],
                unique=False,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_currentbiontyversions_entity"),
                ["entity"],
                unique=True,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_currentbiontyversions_updated_at"),
                ["updated_at"],
                unique=False,
            )
    else:
        op.rename_table(
            old_table_name="bionty_versions",
            new_table_name="biontyversions",
            schema="bionty",
        )
        op.alter_column(
            table_name="biontyversions",
            column_name="table",
            new_column_name="entity",
            schema="bionty",
        )

        op.create_table(
            "currentbiontyversions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("entity", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("created_by", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(
                ["created_by"],
                ["core.user.id"],
                name=op.f("fk_bionty_currentbiontyversions_created_by_user"),
            ),
            sa.ForeignKeyConstraint(
                ["id"],
                ["bionty.biontyversions.id"],
                name=op.f("fk_bionty_currentbiontyversions_id_biontyversions"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_bionty_currentbiontyversions")),
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_currentbiontyversions_created_at"),
            "currentbiontyversions",
            ["created_at"],
            unique=False,
            schema="bionty",
        )
        op.create_index(
            op.f("ix_bionty_currentbiontyversions_created_by"),
            "currentbiontyversions",
            ["created_by"],
            unique=False,
            schema="bionty",
        )
        op.create_index(
            op.f("ix_bionty_currentbiontyversions_entity"),
            "currentbiontyversions",
            ["entity"],
            unique=True,
            schema="bionty",
        )
        op.create_index(
            op.f("ix_bionty_currentbiontyversions_updated_at"),
            "currentbiontyversions",
            ["updated_at"],
            unique=False,
            schema="bionty",
        )
