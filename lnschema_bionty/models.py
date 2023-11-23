from typing import List, Optional, Tuple, Union, overload  # noqa

import bionty as bt
import numpy as np
from django.db import models
from lamin_utils import logger
from lnschema_core.models import CanValidate, HasParents, Registry, User
from lnschema_core.users import current_user_id

from . import ids
from ._bionty import create_or_get_organism_record, encode_uid, lookup2kwargs


class BioRegistry(Registry, HasParents, CanValidate):
    """Base Registry of lnschema_bionty.

    BioRegistry inherits all methods from :class:`~lamindb.dev.Registry` and provides additional methods
    including :meth:`~lnschema_bionty.dev.BioRegistry.bionty` and :meth:`~lnschema_bionty.dev.BioRegistry.from_bionty`

    Notes:
        For more info, see tutorials:

        - :doc:`/lnschema-bionty`
        - :doc:`bio-registries`
    """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # DB-facing constructor
        if len(args) == len(self._meta.concrete_fields):
            super(BioRegistry, self).__init__(*args, **kwargs)
            return None

        # passing lookup result from bionty, which is a Tuple or List
        if args and len(args) == 1 and isinstance(args[0], (Tuple, List)) and len(args[0]) > 0:
            if isinstance(args[0], List) and len(args[0]) > 1:
                logger.warning("multiple lookup/search results are passed, only returning record from the first entry")
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
                    raise TypeError("organism must be a `lnschema_bionty.Organism` record")

        # now continue with the user-facing constructor
        # set the direct parents as a private attribute
        # this is a list of strings that store the ontology id
        if "parents" in kwargs:
            parents = kwargs.pop("parents")
            # this checks if we receive a np.ndarray from pandas
            if isinstance(parents, (list, np.ndarray)) and len(parents) > 0:
                if not isinstance(parents[0], str):
                    raise ValueError("not a valid parents kwarg, got to be list of ontology ids")
                self._parents = parents

        super().__init__(*args, **kwargs)

    @classmethod
    def bionty(
        cls,
        organism: Optional[Union[str, Registry]] = None,
        bionty_source: Optional["BiontySource"] = None,
        **kwargs,
    ) -> "bt.Bionty":
        """The corresponding Bionty object.

        e.g. lnschema_bionty.CellType.bionty() is equivalent to bionty.CellType().
        Note that the public source is auto-configured and tracked via :meth:`lnschema_bionty.BiontySource`.

        See Also:
            `Bionty <https://lamin.ai/docs/bionty/>`__

        Examples:
            >>> celltype_bt = lb.CellType.bionty()
            >>> celltype_bt
            CellType
            Organism: all
            Source: cl, 2023-04-20
            #terms: 2698
            ...
            📖 CellType.df(): ontology reference table
            🔎 CellType.lookup(): autocompletion of terms
            🎯 CellType.search(): free text search of terms
            🧐 CellType.inspect(): check if identifiers are mappable
            👽 CellType.standardize(): map synonyms to standardized names
            🔗 CellType.ontology: Pronto.Ontology object
        """
        if cls.__module__.startswith("lnschema_bionty."):
            if organism is None and kwargs.get("species") is not None:
                organism = kwargs.get("species")
            organism_record = create_or_get_organism_record(organism=organism, orm=cls)

            if bionty_source is not None:
                organism = bionty_source.organism
                source = bionty_source.source
                version = bionty_source.version
            else:
                organism = organism_record.name if organism_record is not None else None
                source = None
                version = None
            bionty_object = getattr(bt, cls.__name__)(organism=organism, source=source, version=version)

            return bionty_object

    @classmethod
    def from_bionty(cls, **kwargs) -> Optional[Union["BioRegistry", List["BioRegistry"]]]:
        """Create a record or records from bionty based on a single field value.

        Notes:
            For more info, see tutorial :doc:`/lnschema-bionty`

            Bulk create protein records via :class:`~lamindb.dev.Registry.from_values`.

        Examples:
            Create a record by passing a field value:

            >>> record = lb.Gene.from_bionty(symbol="TCF7", organism="human")

            Create a record from non-default source:

            >>> bionty_source = lb.BiontySource.filter(entity="CellType", source="cl", version="2022-08-16").one()  # noqa
            >>> record = lb.CellType.from_bionty(name="T cell", bionty_source=bionty_source)

        """
        # non-relationship kwargs
        kv = {k: v for k, v in kwargs.items() if k not in [i.name for i in cls._meta.fields if i.is_relation]}
        if len(kv) > 1:
            raise AssertionError("Only one field can be passed to generate record from Bionty")
        elif len(kv) == 0:
            return None
        else:
            k = next(iter(kv))
            v = kwargs.pop(k)
            results = cls.from_values([v], field=getattr(cls, k), **kwargs)
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
            parents_records = self.from_values(parents, self.__class__.ontology_id, bionty_source=self.bionty_source)
            ln.save(parents_records, mute=mute)
            self.parents.set(parents_records)

    def save(self, parents: Optional[bool] = None, *args, **kwargs) -> None:
        """Save the record and its parents recursively.

        Args:
            parents: `bool = True`. Whether to save parents records.
        """
        # save the record first without parents
        super(BioRegistry, self).save(*args, **kwargs)
        from .dev._settings import settings

        if parents is None:
            parents = settings.auto_save_parents

        if parents:
            self._save_ontology_parents()


class Organism(BioRegistry):
    """Organism - `NCBI Taxonomy <https://www.ncbi.nlm.nih.gov/taxonomy/>`__, `Ensembl Organism <https://useast.ensembl.org/info/about/species.html>`__.

    Examples:
        >>> record = lb.Organism.from_bionty(name="rabbit")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    """Name of a organism, required field."""
    ontology_id = models.CharField(max_length=32, unique=True, db_index=True, null=True, default=None)
    """NCBI Taxon ID."""
    scientific_name = models.CharField(max_length=64, db_index=True, unique=True, null=True, default=None)
    """Scientific name of a organism."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent organism records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="organisms")
    """:class:`~lnschema_bionty.BiontySource` this record associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="organism")
    """Files linked to the organism."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="organism")
    """Datasets linked to the organism."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.PROTECT, default=current_user_id, related_name="created_organism")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        taxon_id: Optional[str],
        scientific_name: Optional[str],
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
        super(Organism, self).__init__(*args, **kwargs)


class Gene(BioRegistry):
    """Genes - `Ensembl <https://ensembl.org/>`__, `NCBI Gene <https://www.ncbi.nlm.nih.gov/gene/>`__.

    Notes:
        Bulk create Gene records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Gene.from_bionty(symbol="TCF7", organism="human")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.gene)
    """A universal id (hash of selected field)."""
    symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """A unique short form of gene name."""
    stable_id = models.CharField(max_length=64, db_index=True, null=True, default=None, unique=True)
    """Stable ID of a gene that doesn't have ensembl_gene_id, e.g. a yeast gene."""
    ensembl_gene_id = models.CharField(max_length=64, db_index=True, null=True, default=None, unique=True)
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
    organism = models.ForeignKey(Organism, models.PROTECT, default=None, related_name="genes")
    """:class:`~lnschema_bionty.Organism` this gene associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="genes")
    """:class:`~lnschema_bionty.BiontySource` this gene associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="genes")
    """Files linked to the gene."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="genes")
    """Datasets linked to the gene."""
    feature_sets = models.ManyToManyField("lnschema_core.FeatureSet", related_name="genes")
    """Featuresets linked to this gene."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.PROTECT, default=current_user_id, related_name="created_genes")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        symbol: Optional[str],
        stable_id: Optional[str],
        ensembl_gene_id: Optional[str],
        ncbi_gene_ids: Optional[str],
        biotype: Optional[str],
        description: Optional[str],
        synonyms: Optional[str],
        organism: Optional[Organism],
        bionty_source: Optional["BiontySource"],
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
        super(Gene, self).__init__(*args, **kwargs)


class Protein(BioRegistry):
    """Proteins - `Uniprot <https://www.uniprot.org/>`__.

    Notes:
        Bulk create Protein records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Protein.from_bionty(name="Synaptotagmin-15B", organism="human")
        >>> record = lb.Protein.from_bionty(gene_symbol="SYT15B", organism="human")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.protein)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Unique name of a protein."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None, unique=True)
    """UniProt protein ID, 6 alphanumeric characters, possibly suffixed by 4 more."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this protein."""
    length = models.BigIntegerField(db_index=True, null=True)
    """Length of the protein sequence."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """The primary gene symbol corresponds to this protein."""
    ensembl_gene_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) Ensembl Gene IDs that correspond to this protein."""
    organism = models.ForeignKey(Organism, models.PROTECT, default=None, related_name="proteins")
    """:class:`~lnschema_bionty.Organism` this protein associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="proteins")
    """:class:`~lnschema_bionty.BiontySource` this protein associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="proteins")
    """Files linked to the protein."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="proteins")
    """Datasets linked to the protein."""
    feature_sets = models.ManyToManyField("lnschema_core.FeatureSet", related_name="proteins")
    """Featuresets linked to this protein."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_proteins",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: Optional[str],
        uniprotkb_id: Optional[str],
        synonyms: Optional[str],
        length: Optional[int],
        gene_symbol: Optional[str],
        ensembl_gene_ids: Optional[str],
        organism: Optional[Organism],
        bionty_source: Optional["BiontySource"],
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
        super(Protein, self).__init__(*args, **kwargs)


class CellMarker(BioRegistry):
    """Cell markers - `CellMarker <http://xteam.xbio.top/CellMarker>`__.

    Notes:
        Bulk create CellMarker records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.CellMarker.from_bionty(name="PD1", organism="human")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=12, default=ids.cellmarker)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell marker."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Gene symbol that corresponds to this cell marker."""
    """Unique name of the cell marker."""
    ncbi_gene_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """NCBI gene id that corresponds to this cell marker."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """Uniprotkb id that corresponds to this cell marker."""
    organism = models.ForeignKey(Organism, models.PROTECT, default=None, related_name="cell_markers")
    """:class:`~lnschema_bionty.Organism` this cell marker associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="cell_markers")
    """:class:`~lnschema_bionty.BiontySource` this cell marker associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="cell_markers")
    """Files linked to the cell marker."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="cell_markers")
    """Datasets linked to the cell marker."""
    feature_sets = models.ManyToManyField("lnschema_core.FeatureSet", related_name="cell_markers")
    """Featuresets linked to this cell marker."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_cell_markers",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        synonyms: Optional[str],
        gene_symbol: Optional[str],
        ncbi_gene_id: Optional[str],
        uniprotkb_id: Optional[str],
        organism: Optional[Organism],
        bionty_source: Optional["BiontySource"],
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
        super(CellMarker, self).__init__(*args, **kwargs)


class Tissue(BioRegistry):
    """Tissues - `Uberon <http://obophenotype.github.io/uberon/>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create Tissue records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Tissue.from_bionty(name="brain")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the tissue."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the tissue."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of tissue."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this tissue."""
    description = models.TextField(null=True, default=None)
    """Description of the tissue."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent tissues records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="tissues")
    """:class:`~lnschema_bionty.BiontySource` this tissue associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="tissues")
    """Files linked to the tissue."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="tissues")
    """Datasets linked to the tissue."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.PROTECT, default=current_user_id, related_name="created_tissues")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["Tissue"],
        bionty_source: Optional["BiontySource"],
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
        super(Tissue, self).__init__(*args, **kwargs)


class CellType(BioRegistry):
    """Cell types - `Cell Ontology <https://obophenotype.github.io/cell-ontology/>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create CellType records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.CellType.from_bionty(name="T cell")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the cell type."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the cell type."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of cell type."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell type."""
    description = models.TextField(null=True, default=None)
    """Description of the cell type."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent cell type records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="cell_types")
    """:class:`~lnschema_bionty.BiontySource` this cell type associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="cell_types")
    """Files linked to the cell type."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="cell_types")
    """Datasets linked to the cell type."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_cell_types",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["CellType"],
        bionty_source: Optional["BiontySource"],
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
        super(CellType, self).__init__(*args, **kwargs)


class Disease(BioRegistry):
    """Diseases - `Mondo <https://mondo.monarchinitiative.org/>`__, `Human Disease <https://disease-ontology.org/>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create Disease records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Disease.from_bionty(name="Alzheimer disease")
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the disease."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the disease."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of disease."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this disease."""
    description = models.TextField(null=True, default=None)
    """Description of the disease."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent disease records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="diseases")
    """:class:`~lnschema_bionty.BiontySource` this disease associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="diseases")
    """Files linked to the disease."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="diseases")
    """Datasets linked to the disease."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_diseases",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["Disease"],
        bionty_source: Optional["BiontySource"],
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
        super(Disease, self).__init__(*args, **kwargs)


class CellLine(BioRegistry):
    """Cell lines - `Cell Line Ontology <https://github.com/CLO-ontology/CLO>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create CellLine records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> standard_name = lb.CellLine.bionty().standardize(["K562"])[0]
        >>> record = lb.CellLine.from_bionty(name=standard_name)
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the cell line."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the cell line."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of cell line."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell line."""
    description = models.TextField(null=True, default=None)
    """Description of the cell line."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent cell line records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="cell_lines")
    """:class:`~lnschema_bionty.BiontySource` this cell line associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="cell_lines")
    """Files linked to the cell line."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="cell_lines")
    """Datasets linked to the cell line."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_cell_lines",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["CellLine"],
        bionty_source: Optional["BiontySource"],
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
        super(CellLine, self).__init__(*args, **kwargs)


class Phenotype(BioRegistry):
    """Phenotypes - `Human Phenotype <https://hpo.jax.org/app/>`__,
    `Phecodes <https://phewascatalog.org/phecodes_icd10>`__,
    `Mammalian Phenotype <http://obofoundry.org/ontology/mp.html>`__,
    `Zebrafish Phenotype <http://obofoundry.org/ontology/zp.html>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create Phenotype records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Phenotype.from_bionty(name="Arachnodactyly")
        >>> record.save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the phenotype."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the phenotype."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of phenotype."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this phenotype."""
    description = models.TextField(null=True, default=None)
    """Description of the phenotype."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent phenotype records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="phenotypes")
    """:class:`~lnschema_bionty.BiontySource` this phenotype associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="phenotypes")
    """Files linked to the phenotype."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="phenotypes")
    """Datasets linked to the phenotype."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_phenotypes",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["Phenotype"],
        bionty_source: Optional["BiontySource"],
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
        super(Phenotype, self).__init__(*args, **kwargs)


class Pathway(BioRegistry):
    """Pathways - `Gene Ontology <https://bioportal.bioontology.org/ontologies/GO>`__,
    `Pathway Ontology <https://bioportal.bioontology.org/ontologies/PW>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create Pathway records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Pathway.from_bionty(ontology_id="GO:1903353")
        >>> record.save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the pathway."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the pathway."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of pathway."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this pathway."""
    description = models.TextField(null=True, default=None)
    """Description of the pathway."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent pathway records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="pathways")
    """:class:`~lnschema_bionty.BiontySource` this pathway associates with."""
    genes = models.ManyToManyField("Gene", related_name="pathways")
    """Genes that signifies the pathway."""
    feature_sets = models.ManyToManyField("lnschema_core.FeatureSet", related_name="pathways")
    """Featuresets linked to the pathway."""
    files = models.ManyToManyField("lnschema_core.File", related_name="pathways")
    """Files linked to the pathway."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="pathways")
    """Datasets linked to the pathway."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_pathways",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["Pathway"],
        bionty_source: Optional["BiontySource"],
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
        super(Pathway, self).__init__(*args, **kwargs)


class ExperimentalFactor(BioRegistry):
    """Experimental factors - `Experimental Factor Ontology <https://www.ebi.ac.uk/ols/ontologies/efo>`__.


    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create ExperimentalFactor records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> standard_name = lb.ExperimentalFactor.bionty().standardize(["scRNA-seq"])
        >>> record = lb.ExperimentalFactor.from_bionty(name=standard_name)
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the experimental factor."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the experimental factor."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
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
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="experimental_factors")
    """:class:`~lnschema_bionty.BiontySource` this experimental_factors associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="experimental_factors")
    """Files linked to the experimental_factors."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="experimental_factors")
    """Datasets linked to the experimental factor."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_experimental_factors",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["ExperimentalFactor"],
        bionty_source: Optional["BiontySource"],
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
        super(ExperimentalFactor, self).__init__(*args, **kwargs)


class DevelopmentalStage(BioRegistry):
    """Developmental stages - `Human Developmental Stages <https://github.com/obophenotype/developmental-stage-ontologies/wiki/HsapDv>`__,
    `Mouse Developmental Stages <https://github.com/obophenotype/developmental-stage-ontologies/wiki/MmusDv>`__.  # noqa

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create DevelopmentalStage records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.DevelopmentalStage.from_bionty(name="neurula stage")
        >>> record.save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the developmental stage."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the developmental stage."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of developmental stage."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this developmental stage."""
    description = models.TextField(null=True, default=None)
    """Description of the developmental stage."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent developmental stage records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="developmental_stages")
    """:class:`~lnschema_bionty.BiontySource` this developmental stage associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="developmental_stages")
    """Files linked to the developmental stage."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="developmental_stages")
    """Datasets linked to the developmental stage."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_developmental_stages",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["DevelopmentalStage"],
        bionty_source: Optional["BiontySource"],
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
        super(DevelopmentalStage, self).__init__(*args, **kwargs)


class Ethnicity(BioRegistry):
    """Ethnicity - `Human Ancestry Ontology <https://github.com/EBISPOT/hancestro>`__.

    Notes:
        For more info, see tutorial :doc:`bio-registries`

        Bulk create Ethnicity records via :class:`~lamindb.dev.Registry.from_values`.

    Examples:
        >>> record = lb.Ethnicity.from_bionty(name="European")
        >>> record.save()
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.ontology)
    """A universal id (hash of selected field)."""
    name = models.CharField(max_length=256, db_index=True)
    """Name of the ethnicity."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the ethnicity."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of ethnicity."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this ethnicity."""
    description = models.TextField(null=True, default=None)
    """Description of the ethnicity."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent ethnicity records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="ethnicities")
    """:class:`~lnschema_bionty.BiontySource` this ethnicity associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="ethnicities")
    """Files linked to the ethnicity."""
    datasets = models.ManyToManyField("lnschema_core.Dataset", related_name="ethnicities")
    """Datasets linked to the ethnicity."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_ethnicities",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)

    @overload
    def __init__(
        self,
        name: str,
        ontology_id: Optional[str],
        abbr: Optional[str],
        synonyms: Optional[str],
        description: Optional[str],
        parents: List["Ethnicity"],
        bionty_source: Optional["BiontySource"],
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
        super(Ethnicity, self).__init__(*args, **kwargs)


class BiontySource(Registry):
    """Versions of public ontologies.

    .. warning::

        Do not modify the records unless you know what you are doing!
    """

    id = models.AutoField(primary_key=True)
    """Internal id, valid only in one DB instance."""
    uid = models.CharField(unique=True, max_length=8, default=ids.biontysource)
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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_bionty_sources",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("entity", "source", "organism", "version"),)

    @overload
    def __init__(
        self,
        entity: str,
        organism: str,
        currently_used: bool,
        source: str,
        version: str,
        source_name: Optional[str],
        url: Optional[str],
        md5: Optional[str],
        source_website: Optional[str],
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
        super(BiontySource, self).__init__(*args, **kwargs)


# backward compat
Species = Organism
