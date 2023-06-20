"""Biological entities (`zdno`).

Import the package::

   import lnschema_bionty as lb

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
   Readout


Bionty sources:

.. autosummary::
   :toctree: .

   BiontySource
"""
# This is lnschema-module zdno.
_schema_id = "zdno"
_name = "bionty"
__version__ = "0.23.1"  # Denote a release candidate of version 0.1.0 with 0.1rc1


from lamindb_setup._check_instance_setup import (
    check_instance_setup as _check_instance_setup,
)

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from .models import (  # noqa
        BiontySource,
        CellLine,
        CellMarker,
        CellType,
        Disease,
        Gene,
        Pathway,
        Phenotype,
        Protein,
        Readout,
        Species,
        Tissue,
    )
