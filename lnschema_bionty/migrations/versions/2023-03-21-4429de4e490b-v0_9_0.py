"""v0.9.0."""
import sqlalchemy as sa  # noqa
import sqlmodel
from alembic import op

revision = "4429de4e490b"
down_revision = "1df05e5b531f"


def upgrade() -> None:
    bind = op.get_bind()
    sqlite = bind.engine.name == "sqlite"

    if sqlite:
        prefix, schema = "bionty.", None
        idx = "ix_bionty."
        pkc = "pk_bionty."
    else:
        prefix, schema = "", "bionty"
        idx = "ix_bionty_"
        pkc = "pk_bionty_"

    op.create_table(
        f"{prefix}cell_line",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ontology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f(f"{pkc}cell_line")),
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}cell_line_name"),
        f"{prefix}cell_line",
        ["name"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}cell_line_ontology_id"),
        f"{prefix}cell_line",
        ["ontology_id"],
        unique=True,
        schema=schema,
    )

    op.create_table(
        f"{prefix}pathway",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ontology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f(f"{pkc}pathway")),
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}pathway_name"),
        f"{prefix}pathway",
        ["name"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}pathway_ontology_id"),
        f"{prefix}pathway",
        ["ontology_id"],
        unique=True,
        schema=schema,
    )

    op.create_table(
        f"{prefix}phenotype",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("ontology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f(f"{pkc}phenotype")),
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}phenotype_name"),
        f"{prefix}phenotype",
        ["name"],
        unique=False,
        schema=schema,
    )
    op.create_index(
        op.f(f"{idx}phenotype_ontology_id"),
        f"{prefix}phenotype",
        ["ontology_id"],
        unique=True,
        schema=schema,
    )


def downgrade() -> None:
    pass
