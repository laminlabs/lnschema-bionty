from datetime import datetime as datetime
from typing import Optional

from lnschema_core import Features, File
from lnschema_core._timestamps import CreatedAt, UpdatedAt
from lnschema_core._users import CreatedBy
from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlalchemy.orm import relationship
from sqlmodel import Field, Relationship

from . import _name as schema_name
from ._link import FeaturesCellMarker, FeaturesGene, FeaturesProtein, FileReadout
from .dev import id as idg
from .dev._bionty import knowledge

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


@knowledge
class Species(SQLModel, table=True):  # type: ignore
    """Species."""

    id: str = Field(default_factory=idg.species, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    taxon_id: int = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
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
    species: Species = Relationship()
    version: Optional[str] = None
    features: Features = Relationship(
        back_populates="genes",
        sa_relationship_kwargs=dict(secondary=FeaturesGene.__table__),
    )
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


Features.genes = relationship(Gene, back_populates="features", secondary=FeaturesGene.__table__)


@knowledge
class Protein(SQLModel, table=True):  # type: ignore
    """Proteins."""

    id: str = Field(default_factory=idg.protein, primary_key=True)
    name: str = Field(default=None, index=True)
    uniprotkb_id: str = Field(default=None, index=True)
    uniprotkb_name: str = Field(default=None, index=True)
    protein_names: Optional[str] = Field(default=None, index=True)
    length: Optional[int] = None
    species_id: str = Field(default=None, foreign_key="bionty.species.id")
    species: Species = Relationship()
    gene_symbols: Optional[str] = None
    gene_synonyms: Optional[str] = None
    ensembl_transcript_ids: Optional[str] = Field(default=None, index=True)
    ncbi_gene_ids: Optional[str] = Field(default=None, index=True)
    features: Features = Relationship(
        back_populates="proteins",
        sa_relationship_kwargs=dict(secondary=FeaturesProtein.__table__),
    )
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


Features.proteins = relationship(Protein, back_populates="features", secondary=FeaturesProtein.__table__)


@knowledge
class CellMarker(SQLModel, table=True):  # type: ignore
    """Cell markers."""

    __tablename__ = f"{prefix}cell_marker"

    id: str = Field(default_factory=idg.cell_marker, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    ncbi_gene_id: Optional[str] = Field(default=None, index=True)
    gene_symbol: Optional[str] = Field(default=None, index=True)
    gene_name: Optional[str] = Field(default=None, index=True)
    uniprotkb_id: Optional[str] = Field(default=None, index=True)
    synonyms: Optional[str] = Field(default=None, index=True)
    species_id: str = Field(default=None, foreign_key="bionty.species.id")
    species: Species = Relationship()
    features: Features = Relationship(
        back_populates="cell_markers",
        sa_relationship_kwargs=dict(secondary=FeaturesCellMarker.__table__),
    )
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


Features.cell_markers = relationship(CellMarker, back_populates="features", secondary=FeaturesCellMarker.__table__)


@knowledge
class Tissue(SQLModel, table=True):  # type: ignore
    """Tissues."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class CellType(SQLModel, table=True):  # type: ignore
    """Cell types."""

    __tablename__ = f"{prefix}cell_type"

    id: str = Field(default_factory=idg.cell_type, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class Disease(SQLModel, table=True):  # type: ignore
    """Diseases."""

    id: str = Field(default_factory=idg.disease, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class CellLine(SQLModel, table=True):  # type: ignore
    """Cell lines."""

    __tablename__ = f"{prefix}cell_line"

    id: str = Field(default_factory=idg.cell_line, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class Pathway(SQLModel, table=True):  # type: ignore
    """Pathways."""

    id: str = Field(default_factory=idg.pathway, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class Phenotype(SQLModel, table=True):  # type: ignore
    """Phenotypes."""

    id: str = Field(default_factory=idg.phenotype, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


@knowledge
class Readout(SQLModel, table=True):  # type: ignore
    """Biological readouts."""

    id: str = Field(default_factory=idg.readout, primary_key=True)
    efo_id: Optional[str] = Field(default=None, unique=True, index=True)
    name: Optional[str] = None
    molecule: Optional[str] = None
    instrument: Optional[str] = None
    measurement: Optional[str] = None
    created_by: str = CreatedBy
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt

    files: File = Relationship(
        back_populates="readouts",
        sa_relationship_kwargs=dict(secondary=FileReadout.__table__),
    )


File.readouts = relationship(
    Readout,
    back_populates="files",
    secondary=FileReadout.__table__,
)
File.__sqlmodel_relationships__["readouts"] = None
