from datetime import datetime as datetime
from typing import Optional  # noqa

from sqlmodel import Field, SQLModel


def utcnow():
    return datetime.utcnow().replace(microsecond=0)


class species(SQLModel, table=True):  # type: ignore
    """Species table that stores each species as a row."""

    id: Optional[int] = Field(default=None, primary_key=True)
    common_name: str = Field(default=None, index=True, unique=True)
    taxon_id: str = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)
    short_name: Optional[str] = None


class featureset_gene(SQLModel, table=True):  # type: ignore
    """Link table between geneset and gene."""

    featureset_id: Optional[int] = Field(
        default=None, foreign_key="featureset.id", primary_key=True
    )
    gene_id: Optional[int] = Field(
        default=None, foreign_key="gene.id", primary_key=True
    )


class featureset_protein(SQLModel, table=True):  # type: ignore
    """Link table between proteinset and protein."""

    featureset_id: Optional[int] = Field(
        default=None, foreign_key="featureset.id", primary_key=True
    )
    protein_id: Optional[int] = Field(
        default=None, foreign_key="protein.id", primary_key=True
    )


class featureset_cell_marker(SQLModel, table=True):  # type: ignore
    """Link table between proteinset and protein."""

    featureset_id: Optional[int] = Field(
        default=None, foreign_key="featureset.id", primary_key=True
    )
    cell_marker_id: Optional[int] = Field(
        default=None, foreign_key="cell_marker.id", primary_key=True
    )


class featureset(SQLModel, table=True):  # type: ignore
    """A set of features."""

    id: Optional[int] = Field(default=None, primary_key=True)
    feature_entity: str
    name: str = Field(default=None, unique=True)


class gene(SQLModel, table=True):  # type: ignore
    """Gene table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    ensembl_gene_id: str = Field(default=None, index=True)
    symbol: str = Field(default=None, index=True)
    gene_type: Optional[str] = None
    ncbi_gene_id: int = Field(default=None, index=True)
    hgnc_id: Optional[str] = None
    mgi_id: Optional[str] = None
    omim_id: Optional[int] = None
    synonyms: Optional[str] = None
    species_id: int = Field(default=None, foreign_key="species.id")


class protein(SQLModel, table=True):  # type: ignore
    """Gene table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)
    uniprotkb_id: str = Field(default=None, index=True)
    uniprotkb_name: str = Field(default=None, index=True)
    protein_names: Optional[str] = None
    length: Optional[int] = None
    species_id: int = Field(default=None, foreign_key="species.id")
    gene_symbols: Optional[str] = None
    gene_synonyms: Optional[str] = None
    ensembl_transcript_ids: Optional[str] = None
    ncbi_gene_ids: Optional[str] = None


class tissue(SQLModel, table=True):  # type: ignore
    """Tissue table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class cell_type(SQLModel, table=True):  # type: ignore
    """Cell type table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class disease(SQLModel, table=True):  # type: ignore
    """Disease table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class cell_marker(SQLModel, table=True):  # type: ignore
    """Cell marker table."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    gene_symbols: Optional[str] = None  # TODO: link table
    ncbi_gene_ids: Optional[str] = None  # TODO: link table
    protein_names: Optional[str] = None  # TODO: link table
    uniprotkb_ids: Optional[str] = None  # TODO: link table
    species_id: int = Field(default=None, foreign_key="species.id")


class version_zdno(SQLModel, table=True):  # type: ignore
    """Schema module version."""

    v: Optional[str] = Field(primary_key=True)
    migration: Optional[str] = None
    user_id: str = Field(foreign_key="user.id")
    time_created: datetime = Field(default_factory=utcnow, nullable=False)


class migration_zdno(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
