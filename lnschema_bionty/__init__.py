"""Registries for basic biological entities, coupled to public ontologies.

Features
========

- Create records from entries in public ontologies using `.from_bionty()`.
- Access full underlying public ontologies via `.bionty()` to search & bulk-create records.
- Create in-house ontologies by using hierarchical relationships among records (`.parents`).
- Use `.synonyms` and `.abbr` to manage synonyms.

All registries inherit from :class:`~lamindb.dev.CanValidate` &
:class:`~lamindb.dev.HasParents` to curate, validate & annotate data, and from
:class:`~lamindb.dev.Registry` for query & search.

.. dropdown:: How to ensure reproducibility across different versions of public ontologies?

   It's important to track versions of external data dependencies.

   `lnschema_bionty` manages it under the hood:

   - Versions of public databases are auto-tracked in :class:`BiontySource`.
   - Records are indexed by universal ids, created by hashing `name` & `ontology_id` for portability across databases.

.. note::

   Read the guides:

   - :doc:`/bio-registries`
   - :doc:`/validate`

   For more background on how public ontologies are accessed, see the utility
   library `Bionty <https://lamin.ai/docs/bionty>`__.

API
===

Import the package::

   import lnschema_bionty as lb

Basic biological registries:

.. autosummary::
   :toctree: .

   Organism
   Gene
   Protein
   CellMarker
   CellType
   CellLine
   Tissue
   Disease
   Pathway
   Phenotype
   ExperimentalFactor
   DevelopmentalStage
   Ethnicity

Settings:

.. autosummary::
   :toctree: .

   settings

Public ontology versions:

.. autosummary::
   :toctree: .

   BiontySource

Developer API:

.. autosummary::
   :toctree: .

   dev
"""

_schema_id = "zdno"
_name = "bionty"
__version__ = "0.35.2"  # Denote a release candidate of version 0.1.0 with 0.1rc1

from lamindb_setup import _check_instance_setup

from . import ids


# trigger instance loading if users
# want to access attributes
def __getattr__(name):
    if name not in {"models"}:
        _check_instance_setup(from_lamindb=True)
    return globals()[name]


if _check_instance_setup():
    del __getattr__  # delete so that imports work out
    from .dev._settings import settings
    from .models import (  # noqa
        BiontySource,
        CellLine,
        CellMarker,
        CellType,
        DevelopmentalStage,
        Disease,
        Ethnicity,
        ExperimentalFactor,
        Gene,
        Organism,
        Pathway,
        Phenotype,
        Protein,
        Tissue,
    )

    # backward compat
    Readout = ExperimentalFactor
    Species = Organism
