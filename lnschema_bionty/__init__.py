"""Registries for basic biological entities, coupled to public ontologies.

Since version 0.40.0, `bionty` replaces `lnschema-bionty` as the user-facing package!

"""

__version__ = "0.40.2"  # Denote a release candidate of version 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup

from . import ids


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
    return globals()[name]


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
