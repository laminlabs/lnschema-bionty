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

import lamindb_setup as _lamindb_setup

try:
    from lamindb_setup import _USE_DJANGO
except Exception:
    _USE_DJANGO = False


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
