from lnschema_core.dev.sqlmodel import schema_sqlmodel
from sqlmodel import Field

from . import _name as schema_name

SQLModel, prefix, schema_arg = schema_sqlmodel(schema_name)


class FeaturesGene(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    __tablename__ = f"{prefix}features_gene"

    features_id: str = Field(foreign_key="core.features.id", primary_key=True)
    gene_id: str = Field(foreign_key="bionty.gene.id", primary_key=True)


class FeaturesProtein(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    __tablename__ = f"{prefix}features_protein"

    features_id: str = Field(foreign_key="core.features.id", primary_key=True)
    protein_id: str = Field(foreign_key="bionty.protein.id", primary_key=True)


class FeaturesCellMarker(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    __tablename__ = f"{prefix}features_cell_marker"

    features_id: str = Field(foreign_key="core.features.id", primary_key=True)
    cell_marker_id: str = Field(foreign_key="bionty.cell_marker.id", primary_key=True)
