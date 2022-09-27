from datetime import datetime as datetime
from typing import Optional  # noqa

from lnschema_core._timestamps import CreatedAt
from sqlmodel import Field, SQLModel

from . import id as idg


class species(SQLModel, table=True):  # type: ignore
    """Species."""

    id: Optional[str] = Field(default_factory=idg.species, primary_key=True)
    common_name: str = Field(default=None, index=True, unique=True)
    taxon_id: str = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)
    short_name: Optional[str] = None


class featureset_gene(SQLModel, table=True):  # type: ignore
    """Link table."""

    featureset_id: str = Field(foreign_key="featureset.id", primary_key=True)
    gene_id: str = Field(foreign_key="gene.id", primary_key=True)


class featureset_protein(SQLModel, table=True):  # type: ignore
    """Link table."""

    featureset_id: str = Field(foreign_key="featureset.id", primary_key=True)
    protein_id: str = Field(foreign_key="protein.id", primary_key=True)


class featureset_cell_marker(SQLModel, table=True):  # type: ignore
    """Link table."""

    featureset_id: str = Field(foreign_key="featureset.id", primary_key=True)
    cell_marker_id: str = Field(foreign_key="cell_marker.id", primary_key=True)


class featureset(SQLModel, table=True):  # type: ignore
    """Sets of biological features.

    See the corresponding link tables.
    """

    id: Optional[str] = Field(default_factory=idg.featureset, primary_key=True)
    feature_entity: str
    name: str = Field(default=None, unique=True)


class gene(SQLModel, table=True):  # type: ignore
    """Genes."""

    id: Optional[str] = Field(default_factory=idg.gene, primary_key=True)
    ensembl_gene_id: Optional[str] = Field(default=None, index=True)
    symbol: Optional[str] = Field(default=None, index=True)
    gene_type: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None
    ncbi_gene_id: int = Field(default=None, index=True)
    hgnc_id: Optional[str] = Field(default=None, index=True)
    mgi_id: Optional[str] = Field(default=None, index=True)
    omim_id: Optional[int] = Field(default=None, index=True)
    synonyms: Optional[str] = Field(default=None, index=True)
    species_id: Optional[int] = Field(
        default=None, foreign_key="species.id", index=True
    )
    version: Optional[str] = None


class protein(SQLModel, table=True):  # type: ignore
    """Proteins."""

    id: Optional[str] = Field(default_factory=idg.protein, primary_key=True)
    name: str = Field(default=None, index=True)
    uniprotkb_id: str = Field(default=None, index=True)
    uniprotkb_name: str = Field(default=None, index=True)
    protein_names: Optional[str] = Field(default=None, index=True)
    length: Optional[int] = None
    species_id: int = Field(default=None, foreign_key="species.id")
    gene_symbols: Optional[str] = None
    gene_synonyms: Optional[str] = None
    ensembl_transcript_ids: Optional[str] = Field(default=None, index=True)
    ncbi_gene_ids: Optional[str] = Field(default=None, index=True)


class tissue(SQLModel, table=True):  # type: ignore
    """Tissues."""

    id: Optional[str] = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: Optional[str] = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class cell_type(SQLModel, table=True):  # type: ignore
    """Cell types."""

    id: Optional[str] = Field(default_factory=idg.cell_type, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class disease(SQLModel, table=True):  # type: ignore
    """Diseases."""

    id: Optional[str] = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class cell_marker(SQLModel, table=True):  # type: ignore
    """Cell markers: protein complexes."""

    id: Optional[str] = Field(default_factory=idg.cell_marker, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    gene_symbols: Optional[str] = None  # TODO: link table
    ncbi_gene_ids: Optional[str] = None  # TODO: link table
    protein_names: Optional[str] = None  # TODO: link table
    uniprotkb_ids: Optional[str] = None  # TODO: link table
    species_id: int = Field(default=None, foreign_key="species.id")


class version_zdno(SQLModel, table=True):  # type: ignore
    """Schema versions."""

    v: Optional[str] = Field(primary_key=True)
    migration: Optional[str] = None
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = CreatedAt


class migration_zdno(SQLModel, table=True):  # type: ignore
    """Latest migration.

    This stores the reference to the latest migration script deployed.
    """

    version_num: Optional[str] = Field(primary_key=True)
