"""v0.4.0.

Revision ID: 267d12e6f6f1
Revises: 7f9a3b24a42b
Create Date: 2022-09-22 23:01:53.991160

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

# revision identifiers, used by Alembic.
revision = "267d12e6f6f1"
down_revision = "7f9a3b24a42b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("gene", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_gene_gene_type"), ["gene_type"], unique=False)
        batch_op.create_index(batch_op.f("ix_gene_hgnc_id"), ["hgnc_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_gene_mgi_id"), ["mgi_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_gene_omim_id"), ["omim_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_gene_species_id"), ["species_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_gene_synonyms"), ["synonyms"], unique=False)

    with op.batch_alter_table("protein", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_protein_ensembl_transcript_ids"),
            ["ensembl_transcript_ids"],
            unique=False,
        )
        batch_op.create_index(batch_op.f("ix_protein_ncbi_gene_ids"), ["ncbi_gene_ids"], unique=False)
        batch_op.create_index(batch_op.f("ix_protein_protein_names"), ["protein_names"], unique=False)


def downgrade() -> None:
    pass
