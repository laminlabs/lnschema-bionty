"""Basic biological entities.

Import the package::

   import lnschema_bionty as lb

All Bionty registries are coupled to `Bionty <https://lamin.ai/docs/bionty>`__-managed ontologies for validation & knowledge-contextualization.

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

Settings:

.. autosummary::
   :toctree: .

   settings

Bionty sources (public ontology versions):

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
__version__ = "0.29.2"  # Denote a release candidate of version 0.1.0 with 0.1rc1

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
