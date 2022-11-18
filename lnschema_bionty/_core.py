from typing import Optional

import bionty as bt
from lnschema_core import Features
from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from . import _name as schema_name
from .dev import id as idg
from .dev._bionty import knowledge

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


@knowledge(bt.Species)
class Species(SQLModel, table=True):  # type: ignore
    """Species."""

    id: str = Field(default_factory=idg.species, primary_key=True)
    common_name: str = Field(default=None, index=True, unique=True)
    taxon_id: str = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)


features_gene = Table(
    f"{prefix}features_gene",
    SQLModel.metadata,
    Column("features_id", ForeignKey("core.features.id"), primary_key=True),
    Column("gene_id", ForeignKey("bionty.gene.id"), primary_key=True),
)

features_protein = Table(
    f"{prefix}features_protein",
    SQLModel.metadata,
    Column("features_id", ForeignKey("core.features.id"), primary_key=True),
    Column("protein_id", ForeignKey("bionty.protein.id"), primary_key=True),
)

features_cell_marker = Table(
    f"{prefix}features_cell_marker",
    SQLModel.metadata,
    Column("features_id", ForeignKey("core.features.id"), primary_key=True),
    Column("cell_marker_id", ForeignKey("bionty.cell_marker.id"), primary_key=True),
)


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
    species_id: Optional[str] = Field(
        default=None, foreign_key="bionty.species.id", index=True
    )
    version: Optional[str] = None
    features: Features = Relationship(
        back_populates="genes", sa_relationship_kwargs=dict(secondary=features_gene)
    )


Features.genes = relationship(Gene, back_populates="features", secondary=features_gene)


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
        sa_relationship_kwargs=dict(secondary=features_protein),
    )


Features.proteins = relationship(
    Protein, back_populates="features", secondary=features_protein
)


@knowledge(bt.Tissue)
class Tissue(SQLModel, table=True):  # type: ignore
    """Tissues."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: Optional[str] = Field(default=None, index=True, unique=True)
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
        sa_relationship_kwargs=dict(secondary=features_cell_marker),
    )


Features.cell_markers = relationship(
    CellMarker, back_populates="features", secondary=features_cell_marker
)
