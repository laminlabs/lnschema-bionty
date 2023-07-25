"""Basic biological entities.

Import the package::

   import lnschema_bionty as lb

Settings:

.. autosummary::
   :toctree: .

   settings

All Bionty ORMs are coupled to `Bionty <https://lamin.ai/docs/bionty>`__ entities:

.. autosummary::
   :toctree: .

   Species
   Gene
   Protein
   CellMarker
   CellType
   CellLine
   Tissue
   Disease
   Pathway
   Phenotype
   ExperimentalFactor

Bionty sources:

.. autosummary::
   :toctree: .

   BiontySource

Developer API:

.. autosummary::
   :toctree: .

   dev
"""
_schema_id = "zdno"
_name = "bionty"
__version__ = "0.28.1"  # Denote a release candidate of version 0.1.0 with 0.1rc1

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
        BiontySource,
        CellLine,
        CellMarker,
        CellType,
        Disease,
        ExperimentalFactor,
        Gene,
        Pathway,
        Phenotype,
        Protein,
        Species,
        Tissue,
    )

    # backward compat
    Readout = ExperimentalFactor
