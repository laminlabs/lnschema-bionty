"""v0.6.1.

Revision ID: a28d3b7a73b1
Revises: edff8c04b030
Create Date: 2022-11-18 22:23:01.664497

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a28d3b7a73b1"
down_revision = "edff8c04b030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.create_table(
            "bionty.bionty_versions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("table", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
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
                name=op.f("fk_bionty_bionty_versions_created_by_user"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_bionty_bionty_versions")),
        )

        with op.batch_alter_table("bionty.bionty_versions", schema=None) as batch_op:
            batch_op.create_index(
                batch_op.f("ix_bionty_bionty_versions_created_at"),
                ["created_at"],
                unique=False,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_bionty_versions_created_by"),
                ["created_by"],
                unique=False,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_bionty_versions_database"),
                ["database"],
                unique=False,
            )
            batch_op.create_index(
                batch_op.f("ix_bionty_bionty_versions_database_v"),
                ["database_v"],
                unique=False,
            )
            batch_op.create_index(batch_op.f("ix_bionty_bionty_versions_table"), ["table"], unique=False)
            batch_op.create_index(
                batch_op.f("ix_bionty_bionty_versions_updated_at"),
                ["updated_at"],
                unique=False,
            )
    else:
        op.create_table(
            "bionty_versions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("table", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database_v", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("database_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
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
                name=op.f("fk_bionty_versions_created_by_user"),
            ),
            sa.PrimaryKeyConstraint("id", name=op.f("pk_bionty_bionty_versions")),
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_created_at"),
            "bionty_versions",
            ["created_at"],
            unique=False,
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_created_by"),
            "bionty_versions",
            ["created_by"],
            unique=False,
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_database"),
            "bionty_versions",
            ["database"],
            unique=False,
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_database_v"),
            "bionty_versions",
            ["database_v"],
            unique=False,
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_table"),
            "bionty_versions",
            ["table"],
            unique=False,
            schema="bionty",
        )

        op.create_index(
            op.f("ix_bionty_versions_updated_at"),
            "bionty_versions",
            ["updated_at"],
            unique=False,
            schema="bionty",
        )


def downgrade() -> None:
    pass
