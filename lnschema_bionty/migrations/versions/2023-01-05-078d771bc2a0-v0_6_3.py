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

    if not sqlite:
        # move to new schema
        op.execute(f"ALTER TABLE biontyversions set SCHEMA {schema}")
        op.execute(f"ALTER TABLE currentbiontyversions set SCHEMA {schema}")

    op.rename_table("biontyversions", f"{prefix}bionty_versions", schema=schema)
    op.rename_table("currentbiontyversions", f"{prefix}current_bionty_versions", schema=schema)

    op.drop_index("ix_biontyversions_created_at", table_name=f"{prefix}bionty_versions", schema=schema)
    op.drop_index("ix_biontyversions_created_by", table_name=f"{prefix}bionty_versions", schema=schema)
    op.drop_index(
        "ix_biontyversions_database",
        table_name=f"{prefix}bionty_versions",
        schema=schema,
    )
    op.drop_index(
        "ix_biontyversions_database_v",
        table_name=f"{prefix}bionty_versions",
        schema=schema,
    )
    op.drop_index("ix_biontyversions_entity", table_name=f"{prefix}bionty_versions", schema=schema)
    op.drop_index(
        "ix_biontyversions_updated_at",
        table_name=f"{prefix}bionty_versions",
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_created_at"),
        f"{prefix}bionty_versions",
        ["created_at"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_created_by"),
        f"{prefix}bionty_versions",
        ["created_by"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_database"),
        f"{prefix}bionty_versions",
        ["database"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_database_v"),
        f"{prefix}bionty_versions",
        ["database_v"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_entity"),
        f"{prefix}bionty_versions",
        ["entity"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_bionty_versions_updated_at"),
        f"{prefix}bionty_versions",
        ["updated_at"],
        unique=False,
        schema=schema,
    )
    op.drop_index(
        "ix_currentbiontyversions_created_at",
        table_name=f"{prefix}current_bionty_versions",
        schema=schema,
    )
    op.drop_index(
        "ix_currentbiontyversions_created_by",
        table_name=f"{prefix}current_bionty_versions",
        schema=schema,
    )
    op.drop_index(
        "ix_currentbiontyversions_entity",
        table_name=f"{prefix}current_bionty_versions",
        schema=schema,
    )
    op.drop_index(
        "ix_currentbiontyversions_updated_at",
        table_name=f"{prefix}current_bionty_versions",
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_current_bionty_versions_created_at"),
        f"{prefix}current_bionty_versions",
        ["created_at"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_current_bionty_versions_created_by"),
        f"{prefix}current_bionty_versions",
        ["created_by"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_current_bionty_versions_entity"),
        f"{prefix}current_bionty_versions",
        ["entity"],
        unique=True,
        schema=schema,
    )
    op.create_index(
        op.f("ix_bionty_current_bionty_versions_updated_at"),
        f"{prefix}current_bionty_versions",
        ["updated_at"],
        unique=False,
        schema=schema,
    )

    if sqlite:
        with op.batch_alter_table("bionty.bionty_versions", schema=None) as batch_op:
            batch_op.drop_index("ix_bionty_bionty_versions_created_at")
            batch_op.drop_index("ix_bionty_bionty_versions_created_by")
            batch_op.drop_index("ix_bionty_bionty_versions_database")
            batch_op.drop_index("ix_bionty_bionty_versions_database_v")
            batch_op.drop_index("ix_bionty_bionty_versions_entity")
            batch_op.drop_index("ix_bionty_bionty_versions_updated_at")
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_created_at"), ["created_at"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_created_by"), ["created_by"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_database"), ["database"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_database_v"), ["database_v"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_entity"), ["entity"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.bionty_versions_updated_at"), ["updated_at"], unique=False)

        with op.batch_alter_table("bionty.current_bionty_versions", schema=None) as batch_op:
            batch_op.drop_index("ix_bionty_current_bionty_versions_created_at")
            batch_op.drop_index("ix_bionty_current_bionty_versions_created_by")
            batch_op.drop_index("ix_bionty_current_bionty_versions_entity")
            batch_op.drop_index("ix_bionty_current_bionty_versions_updated_at")
            batch_op.create_index(batch_op.f("ix_bionty.current_bionty_versions_created_at"), ["created_at"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.current_bionty_versions_created_by"), ["created_by"], unique=False)
            batch_op.create_index(batch_op.f("ix_bionty.current_bionty_versions_entity"), ["entity"], unique=True)
            batch_op.create_index(batch_op.f("ix_bionty.current_bionty_versions_updated_at"), ["updated_at"], unique=False)


def downgrade() -> None:
    pass
