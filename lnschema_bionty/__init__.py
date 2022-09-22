"""Schema module for universal biological entities (`zdno`).

Import the package::

   import lnschema_bionty

Biological entities:

.. autosummary::
   :toctree: .

   gene
   protein
   cell_marker
   cell_type
   species
   tissue
   disease
   featureset

Link tables:

.. autosummary::
   :toctree: .

   featureset_gene
   featureset_protein
   featureset_cell_marker

Tracking versions & migrations:

.. autosummary::
   :toctree: .

   version_zdno
   migration_zdno

"""
# This is lnschema-module zdno.
_schema = "zdno"
_migration = None
__version__ = "0.2.4"

from ._core import (  # noqa
    cell_marker,
    cell_type,
    disease,
    featureset,
    featureset_cell_marker,
    featureset_gene,
    featureset_protein,
    gene,
    protein,
    species,
    tissue,
    version_zdno,
)
