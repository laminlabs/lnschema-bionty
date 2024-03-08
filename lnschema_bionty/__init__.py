"""Registries for basic biological entities, coupled to public ontologies.

Since version 0.40.0, `bionty` replaces `lnschema-bionty` as the user-facing package!

"""

__version__ = "0.41.1"  # Denote a release candidate of version 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup
from . import ids

if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .dev._settings import settings
    from .models import (  # noqa
        CellLine,
        CellMarker,
        CellType,
        DevelopmentalStage,
        Disease,
        Ethnicity,
        ExperimentalFactor,
        Gene,
        Organism,
        Pathway,
        Phenotype,
        Protein,
        PublicSource,
        Tissue,
    )

    # backward compat
    Readout = ExperimentalFactor
    Species = Organism
    BiontySource = PublicSource
