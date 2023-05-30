import lnschema_core
from lnschema_core.dev.sqlmodel import get_orm
from packaging import version
from sqlmodel import Field

from . import __name__ as module_name

SQLModel = get_orm(module_name)

prefix = "lnschema_core_" if version.parse(lnschema_core.__version__) > version.parse("0.4a1") else "core."


class FeaturesGene(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    features_id: str = Field(foreign_key=f"{prefix}features.id", primary_key=True)
    gene_id: str = Field(foreign_key="lnschema_bionty_gene.id", primary_key=True)


class FeaturesProtein(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    features_id: str = Field(foreign_key=f"{prefix}features.id", primary_key=True)
    protein_id: str = Field(foreign_key="lnschema_bionty_protein.id", primary_key=True)


class FeaturesCellMarker(SQLModel, table=True):  # type: ignore
    """Genes as features."""

    features_id: str = Field(foreign_key=f"{prefix}features.id", primary_key=True)
    cell_marker_id: str = Field(foreign_key="lnschema_bionty_cellmarker.id", primary_key=True)


class FileReadout(SQLModel, table=True):  # type: ignore
    """Links for `File` and `Readout`."""

    file_id: str = Field(foreign_key=f"{prefix}file.id", primary_key=True)
    readout_id: str = Field(foreign_key="lnschema_bionty_readout.id", primary_key=True)


class PathwayGene(SQLModel, table=True):  # type: ignore
    """Links for `Pathway` and `Gene`."""

    pathway_id: str = Field(foreign_key="lnschema_bionty_pathway.id", primary_key=True)
    gene_id: str = Field(foreign_key="lnschema_bionty_gene.id", primary_key=True)
