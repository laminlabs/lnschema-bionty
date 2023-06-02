"""vX.X.X."""
import sqlalchemy as sa
import sqlmodel
from alembic import op

revision = "ac1ac6270009"
down_revision = "6649cb6a5d2e"


def upgrade() -> None:
    op.create_table(
        "lnschema_bionty_featurespathway",
        sa.Column("features_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("pathway_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["features_id"],
            ["lnschema_core_features.id"],
            name=op.f("fk_lnschema_bionty_featurespathway_features_id_lnschema_core_features"),
        ),
        sa.ForeignKeyConstraint(
            ["pathway_id"],
            ["lnschema_bionty_pathway.id"],
            name=op.f("fk_lnschema_bionty_featurespathway_pathway_id_lnschema_bionty_pathway"),
        ),
        sa.PrimaryKeyConstraint("features_id", "pathway_id", name=op.f("pk_lnschema_bionty_featurespathway")),
    )


def downgrade() -> None:
    pass
