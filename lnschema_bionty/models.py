from __future__ import annotations

from typing import List, Tuple, overload

import bionty_base
import numpy as np
from bionty_base import PublicOntology
from django.db import models
from django.db.models import CASCADE, PROTECT
from lamin_utils import logger
from lnschema_core.models import (
    Artifact,
    CanValidate,
    Feature,
    FeatureSet,
    HasParents,
    LinkORM,
    Registry,
    TracksRun,
    TracksUpdates,
)

from . import ids
from ._bionty import encode_uid, lookup2kwargs


class BioRegistry(Registry, HasParents, CanValidate):
    """Base Registry of bionty.

    BioRegistry inherits all methods from :class:`~lamindb.core.Registry` and provides additional methods
    including :meth:`~bionty.core.BioRegistry.public` and :meth:`~bionty.core.BioRegistry.from_public`.

    Notes:
        For more info, see tutorials:

        - :doc:`/bionty`
        - :doc:`bio-registries`
    """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # DB-facing constructor
        if len(args) == len(self._meta.concrete_fields):
            super().__init__(*args, **kwargs)
            return None

        # passing lookup result from bionty, which is a Tuple or List
        if (
            args
            and len(args) == 1
            and isinstance(args[0], (Tuple, List))
            and len(args[0]) > 0
        ):
            if isinstance(args[0], List) and len(args[0]) > 1:
                logger.warning(
                    "multiple lookup/search results are passed, only returning record from the first entry"
                )
            result = lookup2kwargs(self, *args, **kwargs)  # type:ignore
            # exclude "parents" from query arguments
            query_kwargs = {k: v for k, v in result.items() if k != "parents"}
            existing_record = self.filter(**query_kwargs).one_or_none()
            if existing_record is not None:
                from lamindb._registry import init_self_from_db

                init_self_from_db(self, existing_record)
                return None
            else:
                kwargs = result  # result already has encoded id
                args = ()
        # all other cases require encoding the id
        else:
            kwargs = encode_uid(orm=self, kwargs=kwargs)

        # raise error if no organism is passed
        if hasattr(self.__class__, "organism_id"):
            if kwargs.get("organism") is None and kwargs.get("organism_id") is None:
                import lnschema_bionty as lb

                if lb.settings.organism is not None:
                    kwargs["organism"] = lb.settings.organism
                else:
                    raise RuntimeError("please pass a organism!")
            elif kwargs.get("organism") is not None:
                if not isinstance(kwargs.get("organism"), Organism):
                    raise TypeError("organism must be a `bionty.Organism` record")

        # now continue with the user-facing constructor
        # set the direct parents as a private attribute
        # this is a list of strings that store the ontology id
        if "parents" in kwargs:
            parents = kwargs.pop("parents")
            # this checks if we receive a np.ndarray from pandas
            if isinstance(parents, (list, np.ndarray)) and len(parents) > 0:
                if not isinstance(parents[0], str):
                    raise ValueError(
                        "not a valid parents kwarg, got to be list of ontology ids"
                    )
                self._parents = parents

        super().__init__(*args, **kwargs)

    @classmethod
    def sources(cls, currently_used: bool = None) -> PublicSource:
        """Default public source for the registry.

        Args:
            currently_used: Only returns currently used sources

        Examples:
            >>> bionty.Gene.sources()
            >>> bionty.Gene.sources(currently_used=True)
        """
        filters = {}
        if currently_used is not None:
            filters["currently_used"] = currently_used
        return PublicSource.filter(entity=cls.__name__, **filters)

    @classmethod
    def public(
        cls,
        organism: str | Registry | None = None,
        public_source: PublicSource | None = None,
        **kwargs,
    ) -> PublicOntology:
        """The corresponding PublicOntology object.

        Note that the public source is auto-configured and tracked via :meth:`bionty.PublicSource`.

        See Also:
            `PublicOntology <https://lamin.ai/docs/public-ontologies>`__

        Examples:
            >>> celltype_pub = bionty.CellType.public()
            >>> celltype_pub
            PublicOntology
            Entity: CellType
            Organism: all
            Source: cl, 2023-04-20
            #terms: 2698
        """
        if cls.__module__.startswith("lnschema_bionty."):
            # backward compat with renaming species to organism
            if organism is None and kwargs.get("species") is not None:
                organism = kwargs.get("species")
            if isinstance(organism, Organism):
                organism = organism.name

            if public_source is not None:
                organism = public_source.organism
                source = public_source.source
                version = public_source.version
            else:
                import lnschema_bionty as lb

                if hasattr(cls, "organism_id"):
                    if organism is None and lb.settings.organism is not None:
                        organism = lb.settings.organism.name
                source = None
                version = None

            return getattr(bionty_base, cls.__name__)(
                organism=organism, source=source, version=version
            )

    @classmethod
    def from_public(
        cls, *, mute: bool = False, **kwargs
    ) -> BioRegistry | list[BioRegistry] | None:
        """Create a record or records from public reference based on a single field value.

        Notes:
            For more info, see tutorial :doc:`/bionty`

            Bulk create protein records via :class:`~lamindb.core.Registry.from_values`.

        Examples:
            Create a record by passing a field value:

            >>> record = bionty.Gene.from_public(symbol="TCF7", organism="human")

            Create a record from non-default source:

            >>> public_source = bionty.PublicSource.filter(entity="CellType", source="cl", version="2022-08-16").one()  # noqa
            >>> record = bionty.CellType.from_public(name="T cell", public_source=public_source)

        """
        # non-relationship kwargs
        kv = {
            k: v
            for k, v in kwargs.items()
            if k not in [i.name for i in cls._meta.fields if i.is_relation]
        }
        if len(kv) > 1:
            raise AssertionError(
                "Only one field can be passed to generate record from public reference"
            )
        elif len(kv) == 0:
            return None
        else:
            k = next(iter(kv))
            v = kwargs.pop(k)
            results = cls.from_values([v], field=getattr(cls, k), mute=mute, **kwargs)
            if len(results) == 1:
                return results[0]
            elif len(results) == 0:
                return None
            else:
                return results

    def _save_ontology_parents(self, mute: bool = False):  # saving records of parents
        if hasattr(self, "_parents"):
            import lamindb as ln

            parents = self._parents
            # here parents is still a list of ontology ids
            logger.info(f"also saving parents of {self}")
            # bulk create parent records
            parents_records = self.from_values(
                parents, self.__class__.ontology_id, public_source=self.public_source
            )
            ln.save(parents_records, mute=mute)
            self.parents.set(parents_records)

    def save(self, parents: bool | None = None, *args, **kwargs) -> None:
        """Save the record and its parents recursively.

        Args:
            parents: `bool = True`. Whether to save parents records.
        """
        # save the record first without parents
        super().save(*args, **kwargs)
        from .core._settings import settings

        if parents is None:
            parents = settings.auto_save_parents

        if parents:
            self._save_ontology_parents()


class Organism(BioRegistry, TracksRun, TracksUpdates):
    """Organism - `NCBI Taxonomy <https://www.ncbi.nlm.nih.gov/taxonomy/>`__, `Ensembl Organism <https://useast.ensembl.org/info/about/species.html>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:organism`.


    Examples:
        >>> record = bionty.Organism.from_public(name="rabbit")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    """Name of a organism, required field."""
    ontology_id = models.CharField(
        max_length=32, unique=True, db_index=True, null=True, default=None
    )
    """NCBI Taxon ID."""
    scientific_name = models.CharField(
        max_length=64, db_index=True, unique=True, null=True, default=None
    )
    """Scientific name of a organism."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent organism records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="organisms"
    )
    """:class:`~bionty.PublicSource` this record associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactOrganism", related_name="organisms"
    )
    """Artifacts linked to the organism."""

    @overload
    def __init__(
        self,
        name: str,
        taxon_id: str | None,
        scientific_name: str | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Gene(BioRegistry, TracksRun, TracksUpdates):
    """Genes - `Ensembl <https://ensembl.org/>`__, `NCBI Gene <https://www.ncbi.nlm.nih.gov/gene/>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:gene`.

        Bulk create Gene records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Gene.from_public(symbol="TCF7", organism="human")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.gene)
    """A universal id (hash of selected field)."""
    symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """A unique short form of gene name."""
    stable_id = models.CharField(
        max_length=64, db_index=True, null=True, default=None, unique=True
    )
    """Stable ID of a gene that doesn't have ensembl_gene_id, e.g. a yeast gene."""
    ensembl_gene_id = models.CharField(
        max_length=64, db_index=True, null=True, default=None, unique=True
    )
    """Ensembl gene stable ID, in the form ENS[organism prefix][feature type prefix][a unique eleven digit number]."""
    ncbi_gene_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) NCBI Gene IDs that correspond to this Ensembl Gene ID.
    NCBI Gene ID, also known as Entrez Gene ID, in the form of numeric string, 1 to 9 digits.
    """
    biotype = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Type of the gene."""
    description = models.TextField(null=True, default=None)
    """Description of the gene."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this gene."""
    organism = models.ForeignKey(Organism, PROTECT, default=None, related_name="genes")
    """:class:`~bionty.Organism` this gene associates with."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="genes"
    )
    """:class:`~bionty.PublicSource` this gene associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactGene", related_name="genes"
    )
    """Artifacts linked to the gene."""
    feature_sets = models.ManyToManyField(
        FeatureSet, through="FeatureSetGene", related_name="genes"
    )
    """Featuresets linked to this gene."""

    @overload
    def __init__(
        self,
        symbol: str | None,
        stable_id: str | None,
        ensembl_gene_id: str | None,
        ncbi_gene_ids: str | None,
        biotype: str | None,
        description: str | None,
        synonyms: str | None,
        organism: Organism | None,
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Protein(BioRegistry, TracksRun, TracksUpdates):
    """Proteins - `Uniprot <https://www.uniprot.org/>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:protein`.

        Bulk create Protein records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Protein.from_public(name="Synaptotagmin-15B", organism="human")
        >>> record = bionty.Protein.from_public(gene_symbol="SYT15B", organism="human")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.protein)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Unique name of a protein."""
    uniprotkb_id = models.CharField(
        max_length=10, db_index=True, null=True, default=None, unique=True
    )
    """UniProt protein ID, 6 alphanumeric characters, possibly suffixed by 4 more."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this protein."""
    length = models.BigIntegerField(db_index=True, null=True)
    """Length of the protein sequence."""
    gene_symbol = models.CharField(
        max_length=64, db_index=True, null=True, default=None
    )
    """The primary gene symbol corresponds to this protein."""
    ensembl_gene_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) Ensembl Gene IDs that correspond to this protein."""
    organism = models.ForeignKey(
        Organism, PROTECT, default=None, related_name="proteins"
    )
    """:class:`~bionty.Organism` this protein associates with."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="proteins"
    )
    """:class:`~bionty.PublicSource` this protein associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactProtein", related_name="proteins"
    )
    """Artifacts linked to the protein."""
    feature_sets = models.ManyToManyField(
        FeatureSet, through="FeatureSetProtein", related_name="proteins"
    )
    """Featuresets linked to this protein."""

    @overload
    def __init__(
        self,
        name: str | None,
        uniprotkb_id: str | None,
        synonyms: str | None,
        length: int | None,
        gene_symbol: str | None,
        ensembl_gene_ids: str | None,
        organism: Organism | None,
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class CellMarker(BioRegistry, TracksRun, TracksUpdates):
    """Cell markers - `CellMarker <http://xteam.xbio.top/CellMarker>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:cell_marker`.

        Bulk create CellMarker records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.CellMarker.from_public(name="PD1", organism="human")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.cellmarker)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell marker."""
    gene_symbol = models.CharField(
        max_length=64, db_index=True, null=True, default=None
    )
    """Gene symbol that corresponds to this cell marker."""
    """Unique name of the cell marker."""
    ncbi_gene_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """NCBI gene id that corresponds to this cell marker."""
    uniprotkb_id = models.CharField(
        max_length=10, db_index=True, null=True, default=None
    )
    """Uniprotkb id that corresponds to this cell marker."""
    organism = models.ForeignKey(
        Organism, PROTECT, default=None, related_name="cell_markers"
    )
    """:class:`~bionty.Organism` this cell marker associates with."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="cell_markers"
    )
    """:class:`~bionty.PublicSource` this cell marker associates with."""
    artifacts = models.ManyToManyField(
        Artifact,
        through="ArtifactCellMarker",
        related_name="cell_markers",
    )
    """Artifacts linked to the cell marker."""
    feature_sets = models.ManyToManyField(
        FeatureSet, through="FeatureSetCellMarker", related_name="cell_markers"
    )
    """Featuresets linked to this cell marker."""

    @overload
    def __init__(
        self,
        name: str,
        synonyms: str | None,
        gene_symbol: str | None,
        ncbi_gene_id: str | None,
        uniprotkb_id: str | None,
        organism: Organism | None,
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Tissue(BioRegistry, TracksRun, TracksUpdates):
    """Tissues - `Uberon <http://obophenotype.github.io/uberon/>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` :doc:`docs:tissue`.

        Bulk create Tissue records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Tissue.from_public(name="brain")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the tissue."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the tissue."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of tissue."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this tissue."""
    description = models.TextField(null=True, default=None)
    """Description of the tissue."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent tissues records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="tissues"
    )
    """:class:`~bionty.PublicSource` this tissue associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactTissue", related_name="tissues"
    )
    """Artifacts linked to the tissue."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Tissue],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class CellType(BioRegistry, TracksRun, TracksUpdates):
    """Cell types - `Cell Ontology <https://obophenotype.github.io/cell-ontology/>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:cell_type`.

        Bulk create CellType records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.CellType.from_public(name="T cell")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the cell type."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the cell type."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of cell type."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell type."""
    description = models.TextField(null=True, default=None)
    """Description of the cell type."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent cell type records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="cell_types"
    )
    """:class:`~bionty.PublicSource` this cell type associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactCellType", related_name="cell_types"
    )
    """Artifacts linked to the cell type."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[CellType],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Disease(BioRegistry, TracksRun, TracksUpdates):
    """Diseases - `Mondo <https://mondo.monarchinitiative.org/>`__, `Human Disease <https://disease-ontology.org/>`__.

    Notes:
        Bulk create Disease records via :class:`~lamindb.core.Registry.from_values`.

        For more info, see tutorials: :doc:`docs:disease`.

    Examples:
        >>> record = bionty.Disease.from_public(name="Alzheimer disease")
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the disease."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the disease."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of disease."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this disease."""
    description = models.TextField(null=True, default=None)
    """Description of the disease."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent disease records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="diseases"
    )
    """:class:`~bionty.PublicSource` this disease associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactDisease", related_name="diseases"
    )
    """Artifacts linked to the disease."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Disease],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class CellLine(BioRegistry, TracksRun, TracksUpdates):
    """Cell lines - `Cell Line Ontology <https://github.com/CLO-ontology/CLO>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:cell_line`.

        Bulk create CellLine records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> standard_name = bionty.CellLine.public().standardize(["K562"])[0]
        >>> record = bionty.CellLine.from_public(name=standard_name)
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the cell line."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the cell line."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of cell line."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell line."""
    description = models.TextField(null=True, default=None)
    """Description of the cell line."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent cell line records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="cell_lines"
    )
    """:class:`~bionty.PublicSource` this cell line associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactCellLine", related_name="cell_lines"
    )
    """Artifacts linked to the cell line."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[CellLine],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Phenotype(BioRegistry, TracksRun, TracksUpdates):
    """Phenotypes - `Human Phenotype <https://hpo.jax.org/app/>`__,
    `Phecodes <https://phewascatalog.org/phecodes_icd10>`__,
    `Mammalian Phenotype <http://obofoundry.org/ontology/mp.html>`__,
    `Zebrafish Phenotype <http://obofoundry.org/ontology/zp.html>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:phenotype`.

        Bulk create Phenotype records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Phenotype.from_public(name="Arachnodactyly")
        >>> record.save()
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the phenotype."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the phenotype."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of phenotype."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this phenotype."""
    description = models.TextField(null=True, default=None)
    """Description of the phenotype."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent phenotype records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="phenotypes"
    )
    """:class:`~bionty.PublicSource` this phenotype associates with."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactPhenotype", related_name="phenotypes"
    )
    """Artifacts linked to the phenotype."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Phenotype],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Pathway(BioRegistry, TracksRun, TracksUpdates):
    """Pathways - `Gene Ontology <https://bioportal.bioontology.org/ontologies/GO>`__,
    `Pathway Ontology <https://bioportal.bioontology.org/ontologies/PW>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:pathway`.

        Bulk create Pathway records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Pathway.from_public(ontology_id="GO:1903353")
        >>> record.save()
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the pathway."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the pathway."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of pathway."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this pathway."""
    description = models.TextField(null=True, default=None)
    """Description of the pathway."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent pathway records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="pathways"
    )
    """:class:`~bionty.PublicSource` this pathway associates with."""
    genes = models.ManyToManyField("Gene", related_name="pathways")
    """Genes that signifies the pathway."""
    feature_sets = models.ManyToManyField(
        FeatureSet, through="FeatureSetPathway", related_name="pathways"
    )
    """Featuresets linked to the pathway."""
    artifacts = models.ManyToManyField(
        Artifact, through="ArtifactPathway", related_name="pathways"
    )
    """Artifacts linked to the pathway."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Pathway],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class ExperimentalFactor(BioRegistry, TracksRun, TracksUpdates):
    """Experimental factors - `Experimental Factor Ontology <https://www.ebi.ac.uk/ols/ontologies/efo>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:experimental_factor`.

        Bulk create ExperimentalFactor records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> standard_name = bionty.ExperimentalFactor.public().standardize(["scRNA-seq"])
        >>> record = bionty.ExperimentalFactor.from_public(name=standard_name)
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the experimental factor."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the experimental factor."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of experimental factor."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this experimental factor."""
    description = models.TextField(null=True, default=None)
    """Description of the experimental factor."""
    molecule = models.TextField(null=True, default=None, db_index=True)
    """Molecular experimental factor, parsed from EFO."""
    instrument = models.TextField(null=True, default=None, db_index=True)
    """Instrument used to measure the experimental factor, parsed from EFO."""
    measurement = models.TextField(null=True, default=None, db_index=True)
    """Phenotypic experimental factor, parsed from EFO."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent experimental factor records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="experimental_factors"
    )
    """:class:`~bionty.PublicSource` this experimental_factors associates with."""
    artifacts = models.ManyToManyField(
        Artifact,
        through="ArtifactExperimentalFactor",
        related_name="experimental_factors",
    )
    """Artifacts linked to the experimental_factors."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[ExperimentalFactor],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class DevelopmentalStage(BioRegistry, TracksRun, TracksUpdates):
    """Developmental stages - `Human Developmental Stages <https://github.com/obophenotype/developmental-stage-ontologies/wiki/HsapDv>`__,
    `Mouse Developmental Stages <https://github.com/obophenotype/developmental-stage-ontologies/wiki/MmusDv>`__.  # noqa.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:developmental_stage`.

        Bulk create DevelopmentalStage records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.DevelopmentalStage.from_public(name="neurula stage")
        >>> record.save()
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the developmental stage."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the developmental stage."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of developmental stage."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this developmental stage."""
    description = models.TextField(null=True, default=None)
    """Description of the developmental stage."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent developmental stage records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="developmental_stages"
    )
    """:class:`~bionty.PublicSource` this developmental stage associates with."""
    artifacts = models.ManyToManyField(
        Artifact,
        through="ArtifactDevelopmentalStage",
        related_name="developmental_stages",
    )
    """Artifacts linked to the developmental stage."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[DevelopmentalStage],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class Ethnicity(BioRegistry, TracksRun, TracksUpdates):
    """Ethnicity - `Human Ancestry Ontology <https://github.com/EBISPOT/hancestro>`__.

    Notes:
        For more info, see tutorials :doc:`bio-registries` and :doc:`docs:ethnicity`.

        Bulk create Ethnicity records via :class:`~lamindb.core.Registry.from_values`.

    Examples:
        >>> record = bionty.Ethnicity.from_public(name="European")
        >>> record.save()
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("name", "ontology_id"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the ethnicity."""
    ontology_id = models.CharField(
        max_length=32, db_index=True, null=True, default=None
    )
    """Ontology ID of the ethnicity."""
    abbr = models.CharField(
        max_length=32, db_index=True, unique=True, null=True, default=None
    )
    """A unique abbreviation of ethnicity."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this ethnicity."""
    description = models.TextField(null=True, default=None)
    """Description of the ethnicity."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent ethnicity records."""
    public_source = models.ForeignKey(
        "PublicSource", PROTECT, null=True, related_name="ethnicities"
    )
    """:class:`~bionty.PublicSource` this ethnicity associates with."""
    artifacts = models.ManyToManyField(
        Artifact,
        through="ArtifactEthnicity",
        related_name="ethnicities",
    )
    """Artifacts linked to the ethnicity."""

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: str | None,
        abbr: str | None,
        synonyms: str | None,
        description: str | None,
        parents: list[Ethnicity],
        public_source: PublicSource | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)


class PublicSource(Registry, TracksRun, TracksUpdates):
    """Versions of public ontologies.

    .. warning::

        Do not modify the records unless you know what you are doing!
    """

    class Meta(BioRegistry.Meta, TracksRun.Meta, TracksUpdates.Meta):
        abstract = False
        unique_together = (("entity", "source", "organism", "version"),)

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.publicsource)
    """A universal id (hash of selected field)."""
    entity = models.CharField(max_length=64, db_index=True)
    """Entity class name."""
    organism = models.CharField(max_length=64, db_index=True)
    """Organism name, use 'all' if unknown or none applied."""
    currently_used = models.BooleanField(default=False, db_index=True)
    """Whether this record is currently used."""
    source = models.CharField(max_length=64, db_index=True)
    """Source key, short form, CURIE prefix for ontologies."""
    source_name = models.TextField(blank=True, db_index=True)
    """Source full name, long form."""
    version = models.CharField(max_length=64, db_index=True)
    """Version of the source."""
    url = models.TextField(null=True, default=None)
    """URL of the source file."""
    md5 = models.TextField(null=True, default=None)
    """Hash md5 of the source file."""
    source_website = models.TextField(null=True, default=None)
    """Website of the source."""

    @overload
    def __init__(
        self,
        entity: str,
        organism: str,
        currently_used: bool,
        source: str,
        version: str,
        source_name: str | None,
        url: str | None,
        md5: str | None,
        source_website: str | None,
    ):
        ...

    @overload
    def __init__(
        self,
        *db_args,
    ):
        ...

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        kwargs = encode_uid(orm=self, kwargs=kwargs)
        super().__init__(*args, **kwargs)

    def set_as_currently_used(self):
        """Set this record as the currently used public source.

        Examples:
            >>> record = bionty.PublicSource.filter(uid="...").one()
            >>> record.set_as_currently_used()
        """
        self.currently_used = True
        self.save()
        PublicSource.filter(
            entity=self.entity, organism=self.organism, source=self.source
        ).exclude(uid=self.uid).update(currently_used=False)
        logger.success(f"set {self} as currently used")
        logger.warning("please reload your instance to reflect the updates!")


# backward compat
Species = Organism
BiontySource = PublicSource


class FeatureSetGene(Registry, LinkORM):
    id = models.BigAutoField(primary_key=True)
    # follow the .lower() convention in link models
    featureset = models.ForeignKey(
        "lnschema_core.FeatureSet", CASCADE, related_name="+"
    )
    gene = models.ForeignKey("Gene", PROTECT, related_name="+")


class FeatureSetProtein(Registry, LinkORM):
    id = models.BigAutoField(primary_key=True)
    # follow the .lower() convention in link models
    featureset = models.ForeignKey(
        "lnschema_core.FeatureSet", CASCADE, related_name="+"
    )
    protein = models.ForeignKey("Protein", PROTECT, related_name="+")


class FeatureSetCellMarker(Registry, LinkORM):
    id = models.BigAutoField(primary_key=True)
    # follow the .lower() convention in link models
    featureset = models.ForeignKey(
        "lnschema_core.FeatureSet", CASCADE, related_name="+"
    )
    # follow the .lower() convention in link models
    cellmarker = models.ForeignKey("CellMarker", PROTECT, related_name="+")


class FeatureSetPathway(Registry, LinkORM):
    id = models.BigAutoField(primary_key=True)
    # follow the .lower() convention in link models
    featureset = models.ForeignKey(
        "lnschema_core.FeatureSet", CASCADE, related_name="+"
    )
    pathway = models.ForeignKey("Pathway", PROTECT, related_name="+")


class ArtifactOrganism(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="organism_links")
    organism = models.ForeignKey("Organism", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactorganism_links"
    )
    organism_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactGene(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="gene_links")
    gene = models.ForeignKey("Gene", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactgene_links"
    )
    gene_ref_is_symbol = models.BooleanField(null=True, default=None)
    feature_ref_is_symbol = models.BooleanField(null=True, default=None)


class ArtifactProtein(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="protein_links")
    protein = models.ForeignKey("Protein", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactprotein_links"
    )
    protein_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactCellMarker(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="cell_marker_links")
    # follow the .lower() convention in link models
    cellmarker = models.ForeignKey("CellMarker", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="artifactcellmarker_links",
    )
    cell_marker_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactTissue(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="tissue_links")
    tissue = models.ForeignKey("Tissue", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifacttissue_links"
    )
    tissue_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactCellType(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="cell_type_links")
    # follow the .lower() convention in link models
    celltype = models.ForeignKey("CellType", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactcelltype_links"
    )
    cell_type_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactDisease(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="disease_links")
    disease = models.ForeignKey("Disease", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactdisease_links"
    )
    disease_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactCellLine(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="cell_line_links")
    # follow the .lower() convention in link models
    cellline = models.ForeignKey("CellLine", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactcellline_links"
    )
    cell_line_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactPhenotype(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="phenotype_links")
    phenotype = models.ForeignKey("Phenotype", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="artifactphenotype_links",
    )
    phenotype_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactPathway(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="pathway_links")
    pathway = models.ForeignKey("Pathway", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature, PROTECT, null=True, default=None, related_name="artifactpathway_links"
    )
    pathway_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactExperimentalFactor(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="experimental_factor_links"
    )
    experimental_factor = models.ForeignKey(
        "ExperimentalFactor", PROTECT, related_name="artifact_links"
    )
    feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="artifactexperimentalfactor_links",
    )
    experimental_factor_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactDevelopmentalStage(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(
        Artifact, CASCADE, related_name="developmental_stage_links"
    )
    # follow the .lower() convention in link models
    developmentalstage = models.ForeignKey(
        "DevelopmentalStage", PROTECT, related_name="artifact_links"
    )
    feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="artifactdevelopmentalstage_links",
    )
    developmental_stage_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)


class ArtifactEthnicity(Registry, LinkORM, TracksRun):
    id = models.BigAutoField(primary_key=True)
    artifact = models.ForeignKey(Artifact, CASCADE, related_name="ethnicity_links")
    ethnicity = models.ForeignKey("Ethnicity", PROTECT, related_name="artifact_links")
    feature = models.ForeignKey(
        Feature,
        PROTECT,
        null=True,
        default=None,
        related_name="artifactethnicity_links",
    )
    ethnicity_ref_is_name = models.BooleanField(null=True, default=None)
    feature_ref_is_name = models.BooleanField(null=True, default=None)
