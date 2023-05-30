"""v0.18.1."""
import sqlalchemy as sa  # noqa
import sqlmodel
from alembic import op

revision = "6649cb6a5d2e"
down_revision = "c5ebdad85b31"


def upgrade() -> None:
    op.create_table(
        "lnschema_bionty_pathwaygene",
        sa.Column("pathway_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("gene_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["gene_id"],
            ["lnschema_bionty_gene.id"],
            name=op.f("fk_lnschema_bionty_pathwaygene_gene_id_lnschema_bionty_gene"),
        ),
        sa.ForeignKeyConstraint(
            ["pathway_id"],
            ["lnschema_bionty_pathway.id"],
            name=op.f("fk_lnschema_bionty_pathwaygene_pathway_id_lnschema_bionty_pathway"),
        ),
        sa.PrimaryKeyConstraint("pathway_id", "gene_id", name=op.f("pk_lnschema_bionty_pathwaygene")),
    )


def downgrade() -> None:
    pass
