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
   link

"""
# This is lnschema-module zdno.
_schema_id = "zdno"
_name = "bionty"
_migration = "1df05e5b531f"
__version__ = "0.6.9"

from . import dev, link  # noqa
from ._core import CellMarker, CellType, Disease, Gene, Protein, Species, Tissue  # noqa
from .dev import id  # backward compat
