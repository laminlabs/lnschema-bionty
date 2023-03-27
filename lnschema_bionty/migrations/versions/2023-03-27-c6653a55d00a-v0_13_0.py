"""v0.13.0."""
import sqlalchemy as sa  # noqa
import sqlmodel
from alembic import op

revision = "c6653a55d00a"
down_revision = "5594b330a854"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
        pk = "pk_bionty."
        fk = "fk_bionty."
        idx_createdat = "ix_bionty.readout_created_at"
        idx_createdby = "ix_bionty.readout_created_by"
        idx_efoid = "ix_bionty.readout_efo_id"
        idx_updatedat = "ix_bionty.readout_updated_at"
    else:
        prefix, schema = "", "bionty"
        pk = "pk_bionty_"
        fk = "fk_bionty_"
        idx_createdat = "ix_bionty_readout_created_at"
        idx_createdby = "ix_bionty_readout_created_by"
        idx_efoid = "ix_bionty_readout_efo_id"
        idx_updatedat = "ix_bionty_readout_updated_at"

    op.create_table(
        f"{prefix}readout",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("efo_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("molecule", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("instrument", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("measurement", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
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
            name=op.f(f"{fk}readout_created_by_user"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f(f"{pk}readout")),
        schema=schema,
    )
    with op.batch_alter_table(f"{prefix}readout", schema=schema) as batch_op:
        batch_op.create_index(batch_op.f(idx_createdat), ["created_at"], unique=False)
        batch_op.create_index(batch_op.f(idx_createdby), ["created_by"], unique=False)
        batch_op.create_index(batch_op.f(idx_efoid), ["efo_id"], unique=True)
        batch_op.create_index(batch_op.f(idx_updatedat), ["updated_at"], unique=False)

    op.create_table(
        f"{prefix}file_readout",
        sa.Column("file_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("readout_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["core.file.id"],
            name=op.f(f"{fk}file_readout_file_id_file"),
        ),
        sa.ForeignKeyConstraint(
            ["readout_id"],
            ["bionty.readout.id"],
            name=op.f(f"{fk}file_readout_readout_id_readout"),
        ),
        sa.PrimaryKeyConstraint("file_id", "readout_id", name=op.f(f"{pk}file_readout")),
        schema=schema,
    )


def downgrade() -> None:
    pass
