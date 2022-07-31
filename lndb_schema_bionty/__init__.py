"""Biological entities schema module.

Import the package::

   import lndb_schema_bionty

This is the complete API reference:

.. autosummary::
   :toctree: .

   gene
   protein
   species
   featureset
   featureset_gene
   featureset_protein

"""

__version__ = "0.1.2"

from ._core import (  # noqa
    featureset,
    featureset_gene,
    featureset_protein,
    gene,
    protein,
    species,
)
