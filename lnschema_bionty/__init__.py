"""Biological entities (`zdno`).

Import the package::

   import lnschema_bionty

Biological entities, all initialized via `Bionty <https://lamin.ai/docs/bionty>`__:

.. autosummary::
   :toctree: .

   Gene
   Protein
   CellMarker
   CellType
   CellLine
   Species
   Tissue
   Disease
   Pathway
   Phenotype
   Readout

Development tools:

.. autosummary::
   :toctree: .

   dev
   link

"""
# This is lnschema-module zdno.
_schema_id = "zdno"
_name = "bionty"
_migration = "ac1ac6270009"
__version__ = "0.18.3"  # Denote a release candidate of version 0.1.0 with 0.1rc1


from lamindb_setup import _USE_DJANGO
from lamindb_setup._check_instance_setup import (
    check_instance_setup as _check_instance_setup,
)

_INSTANCE_SETUP = _check_instance_setup()

if _INSTANCE_SETUP:
    from . import dev, link  # noqa
    from .dev import id  # backward compat

    if not _USE_DJANGO:
        from ._core import (  # noqa
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
    else:
        from .models import (  # noqa
            BiontyVersions,
            CellLine,
            CellMarker,
            CellType,
            CurrentBiontyVersions,
            Disease,
            Gene,
            Pathway,
            Phenotype,
            Protein,
            Readout,
            Species,
            Tissue,
        )
