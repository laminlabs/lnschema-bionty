"""Schema module for universal biological entities (`zdno`).

Import the package::

   import lnschema_bionty

This is the complete API reference:

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
   featureset_gene
   featureset_protein
   featureset_cell_marker
   version_zdno

"""
# This is lnschema-module zdno.
_schema_module_id = "zdno"
__version__ = "0.2.2"

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
