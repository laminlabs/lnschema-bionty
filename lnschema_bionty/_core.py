from typing import Optional

import bionty as bt
from lnschema_core import Features
from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from . import _name as schema_name
from ._link import FeaturesCellMarker, FeaturesGene, FeaturesProtein
from .dev import id as idg
from .dev._bionty import knowledge

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


@knowledge(bt.Species)
class Species(SQLModel, table=True):  # type: ignore
    """Species."""

    id: str = Field(default_factory=idg.species, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    taxon_id: int = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)


class Gene(SQLModel, table=True):  # type: ignore
    """Genes."""

    id: str = Field(default_factory=idg.gene, primary_key=True)
    ensembl_gene_id: Optional[str] = Field(default=None, index=True)
    symbol: Optional[str] = Field(default=None, index=True)
    gene_type: Optional[str] = Field(default=None, index=True)
    description: Optional[str] = None
    ncbi_gene_id: int = Field(default=None, index=True)
    hgnc_id: Optional[str] = Field(default=None, index=True)
    mgi_id: Optional[str] = Field(default=None, index=True)
    omim_id: Optional[int] = Field(default=None, index=True)
    synonyms: Optional[str] = Field(default=None, index=True)
    species_id: Optional[str] = Field(default=None, foreign_key="bionty.species.id", index=True)
    version: Optional[str] = None
    features: Features = Relationship(
        back_populates="genes",
        sa_relationship_kwargs=dict(secondary=FeaturesGene.__table__),
    )


Features.genes = relationship(Gene, back_populates="features", secondary=FeaturesGene.__table__)


class Protein(SQLModel, table=True):  # type: ignore
    """Proteins."""

    id: str = Field(default_factory=idg.protein, primary_key=True)
    name: str = Field(default=None, index=True)
    uniprotkb_id: str = Field(default=None, index=True)
    uniprotkb_name: str = Field(default=None, index=True)
    protein_names: Optional[str] = Field(default=None, index=True)
    length: Optional[int] = None
    species_id: str = Field(default=None, foreign_key="bionty.species.id")
    gene_symbols: Optional[str] = None
    gene_synonyms: Optional[str] = None
    ensembl_transcript_ids: Optional[str] = Field(default=None, index=True)
    ncbi_gene_ids: Optional[str] = Field(default=None, index=True)
    features: Features = Relationship(
        back_populates="proteins",
        sa_relationship_kwargs=dict(secondary=FeaturesProtein.__table__),
    )


Features.proteins = relationship(Protein, back_populates="features", secondary=FeaturesProtein.__table__)


@knowledge(bt.Tissue)
class Tissue(SQLModel, table=True):  # type: ignore
    """Tissues."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


@knowledge(bt.CellType)
class CellType(SQLModel, table=True):  # type: ignore
    """Cell types."""

    __tablename__ = f"{prefix}cell_type"

    id: str = Field(default_factory=idg.cell_type, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


@knowledge(bt.Disease)
class Disease(SQLModel, table=True):  # type: ignore
    """Diseases."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class CellMarker(SQLModel, table=True):  # type: ignore
    """Cell markers: protein complexes."""

    __tablename__ = f"{prefix}cell_marker"

    id: str = Field(default_factory=idg.cell_marker, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    gene_symbols: Optional[str] = None  # TODO: link table
    ncbi_gene_ids: Optional[str] = None  # TODO: link table
    protein_names: Optional[str] = None  # TODO: link table
    uniprotkb_ids: Optional[str] = None  # TODO: link table
    species_id: str = Field(default=None, foreign_key="bionty.species.id")
    features: Features = Relationship(
        back_populates="cell_markers",
        sa_relationship_kwargs=dict(secondary=FeaturesCellMarker.__table__),
    )


Features.cell_markers = relationship(CellMarker, back_populates="features", secondary=FeaturesCellMarker.__table__)
