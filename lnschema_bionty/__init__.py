"""Schema module for universal biological entities (`zdno`).

Import the package::

   import lnschema_bionty

Biological entities, all initialized via `Bionty <https://lamin.ai/docs/bionty>`__:

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
_migration = "7f9a3b24a42b"
__version__ = "0.3.1"

from ._core import (  # noqa
    cell_marker,
    cell_type,
    disease,
    featureset,
    featureset_cell_marker,
    featureset_gene,
    featureset_protein,
    gene,
    migration_zdno,
    protein,
    species,
    tissue,
    version_zdno,
)
