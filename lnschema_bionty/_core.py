from typing import Optional  # noqa

from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlmodel import Field

from . import _name as schema_name
from . import id as idg

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class Species(SQLModel, table=True):  # type: ignore
    """Species."""

    id: str = Field(default_factory=idg.species, primary_key=True)
    common_name: str = Field(default=None, index=True, unique=True)
    taxon_id: str = Field(default=None, index=True, unique=True)
    scientific_name: str = Field(default=None, index=True, unique=True)
    short_name: Optional[str] = None


class FeaturesetGene(SQLModel, table=True):  # type: ignore
    """Link table."""

    __tablename__ = "{prefix}featureset_gene"

    featureset_id: str = Field(foreign_key="bionty.featureset.id", primary_key=True)
    gene_id: str = Field(foreign_key="bionty.gene.id", primary_key=True)


class FeaturesetProtein(SQLModel, table=True):  # type: ignore
    """Link table."""

    __tablename__ = "{prefix}featureset_protein"

    featureset_id: str = Field(foreign_key="bionty.featureset.id", primary_key=True)
    protein_id: str = Field(foreign_key="bionty.protein.id", primary_key=True)


class FeaturesetCellMarker(SQLModel, table=True):  # type: ignore
    """Link table."""

    __tablename__ = "{prefix}featureset_cell_marker"

    featureset_id: str = Field(foreign_key="bionty.featureset.id", primary_key=True)
    cell_marker_id: str = Field(foreign_key="bionty.cell_marker.id", primary_key=True)


class Featureset(SQLModel, table=True):  # type: ignore
    """Sets of biological features.

    See the corresponding link tables.
    """

    id: str = Field(default_factory=idg.featureset, primary_key=True)
    feature_entity: str
    name: str = Field(default=None, unique=True)


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


class Tissue(SQLModel, table=True):  # type: ignore
    """Tissues."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: Optional[str] = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class CellType(SQLModel, table=True):  # type: ignore
    """Cell types."""

    __tablename__ = "{prefix}cell_type"

    id: str = Field(default_factory=idg.cell_type, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class Disease(SQLModel, table=True):  # type: ignore
    """Diseases."""

    id: str = Field(default_factory=idg.tissue, primary_key=True)
    ontology_id: str = Field(default=None, index=True, unique=True)
    name: str = Field(default=None, index=True)


class CellMarker(SQLModel, table=True):  # type: ignore
    """Cell markers: protein complexes."""

    __tablename__ = "{prefix}cell_marker"

    id: str = Field(default_factory=idg.cell_marker, primary_key=True)
    name: str = Field(default=None, index=True, unique=True)
    gene_symbols: Optional[str] = None  # TODO: link table
    ncbi_gene_ids: Optional[str] = None  # TODO: link table
    protein_names: Optional[str] = None  # TODO: link table
    uniprotkb_ids: Optional[str] = None  # TODO: link table
    species_id: str = Field(default=None, foreign_key="bionty.species.id")
