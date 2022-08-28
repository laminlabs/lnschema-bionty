"""Schema module for universal biological entities (`zdno`).

Import the package::

   import lnschema_bionty

This is the complete API reference:

.. autosummary::
   :toctree: .

   gene
   protein
   species
   featureset
   featureset_gene
   featureset_protein
   version_zdno

"""
# This is lnschema-module zdno.
_schema_module_id = "zdno"
__version__ = "0.2.2"

from ._core import (  # noqa
    featureset,
    featureset_gene,
    featureset_protein,
    gene,
    protein,
    species,
    version_zdno,
)
