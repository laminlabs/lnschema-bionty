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

Feature sets:

.. autosummary::
   :toctree: .

   Featureset
   FeaturesetGene
   FeaturesetProtein
   FeaturesetCellMarker

Development tools:

.. autosummary::
   :toctree: .

   dev

"""
# This is lnschema-module zdno.
_schema_id = "zdno"
_name = "bionty"
_migration = "267d12e6f6f1"
__version__ = "0.4.5"

from . import dev  # noqa
from ._core import (  # noqa
    CellMarker,
    CellType,
    Disease,
    Featureset,
    FeaturesetCellMarker,
    FeaturesetGene,
    FeaturesetProtein,
    Gene,
    Protein,
    Species,
    Tissue,
)
from .dev import id  # backward compat
