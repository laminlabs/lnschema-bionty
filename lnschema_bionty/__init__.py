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
   Species
   Tissue
   Disease

Development tools:

.. autosummary::
   :toctree: .

   dev

"""
# This is lnschema-module zdno.
_schema_id = "zdno"
_name = "bionty"
_migration = "a28d3b7a73b1"
__version__ = "0.6.0"

from . import dev  # noqa
from ._core import (  # noqa
    CellMarker,
    CellType,
    Disease,
    Gene,
    Protein,
    Species,
    Tissue,
    features_cell_marker,
    features_gene,
    features_protein,
)
from .dev import id  # backward compat
