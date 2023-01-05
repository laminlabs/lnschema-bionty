"""v0.5.0.

Revision ID: 98da12fc80a8
Revises: 267d12e6f6f1
Create Date: 2022-10-31
"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

revision = "afda12fc80a8"
down_revision = "267d12e6f6f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.engine.name == "sqlite":
        op.rename_table(old_table_name="gene", new_table_name="bionty.gene")
        op.rename_table(old_table_name="protein", new_table_name="bionty.protein")
        op.rename_table(old_table_name="cell_marker", new_table_name="bionty.cell_marker")
        op.rename_table(old_table_name="cell_type", new_table_name="bionty.cell_type")
        op.rename_table(old_table_name="species", new_table_name="bionty.species")
        op.rename_table(old_table_name="tissue", new_table_name="bionty.tissue")
        op.rename_table(old_table_name="disease", new_table_name="bionty.disease")
        op.rename_table(old_table_name="featureset", new_table_name="bionty.featureset")
        op.rename_table(old_table_name="featureset_gene", new_table_name="bionty.featureset_gene")
        op.rename_table(
            old_table_name="featureset_protein",
            new_table_name="bionty.featureset_protein",
        )
        op.rename_table(
            old_table_name="featureset_cell_marker",
            new_table_name="bionty.featureset_cell_marker",
        )
    else:
        op.execute("alter table public.gene set schema bionty")
        op.execute("alter table public.protein set schema bionty")
        op.execute("alter table public.cell_marker set schema bionty")
        op.execute("alter table public.cell_type set schema bionty")
        op.execute("alter table public.species set schema bionty")
        op.execute("alter table public.tissue set schema bionty")
        op.execute("alter table public.disease set schema bionty")
        op.execute("alter table public.featureset set schema bionty")
        op.execute("alter table public.featureset_gene set schema bionty")
        op.execute("alter table public.featureset_protein set schema bionty")
        op.execute("alter table public.featureset_cell_marker set schema bionty")


def downgrade() -> None:
    pass
