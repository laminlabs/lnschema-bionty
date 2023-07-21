from typing import List, Optional, Tuple, Union, overload  # noqa

import bionty as bt
import numpy as np
from django.db import models
from lamin_logger import logger
from lnschema_core.models import ORM, User
from lnschema_core.users import current_user_id

from . import ids
from ._bionty import create_or_get_species_record, encode_id, lookup2kwargs


class BioORM(ORM):
    """Base ORM of lnschema_bionty.

    BioORM inherits all methods from :class:`~lamindb.dev.ORM` and provides additional methods
    including :meth:`~lnschema_bionty.dev.BioORM.bionty` and :meth:`~lnschema_bionty.dev.BioORM.from_bionty`

    Notes:
        For more info, see tutorials:

        - :doc:`/lnschema-bionty`
        - :doc:`/biology/registries`
    """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        # set the direct parents as a private attribute
        # this is a list of strings that store the ontology id
        if args and len(args) == 1 and isinstance(args[0], (Tuple, List)) and len(args[0]) > 0:
            if isinstance(args[0], List) and len(args[0]) > 1:
                logger.warning("Multiple lookup/search results are passed, only returning record from the first entry")
            result = lookup2kwargs(self, *args, **kwargs)  # type:ignore
            try:
                existing_object = self.select(**result)[0]
                new_args = [getattr(existing_object, field.attname) for field in self._meta.concrete_fields]
                super().__init__(*new_args)
                self._state.adding = False  # mimic from_db
                self._state.db = "default"
                return None
            except IndexError:
                # result already has encoded id
                kwargs = result
                args = ()
        else:
            kwargs = encode_id(orm=self, kwargs=kwargs)

        if "parents" in kwargs:
            parents = kwargs.pop("parents")
            # this checks if we receive a np.ndarray from pandas
            if isinstance(parents, (list, np.ndarray)) and len(parents) > 0:
                if not isinstance(parents[0], str):
                    raise ValueError("Not a valid parents kwarg, got to be list of ontology ids")
                self._parents = parents

        super().__init__(*args, **kwargs)

    @classmethod
    def bionty(cls, species: Optional[Union[str, ORM]] = None) -> "bt.Bionty":
        """The corresponding Bionty object.

        e.g. lnschema_bionty.CellType.bionty() is equivalent to bionty.CellType().
        Note that the public source is auto-configured and tracked via :meth:`lnschema_bionty.BiontySource`.

        See Also:
            `Bionty <https://lamin.ai/docs/bionty/>`__

        Examples:
            >>> celltype_bt = lb.CellType.bionty()
            >>> celltype_bt
            CellType
            Species: all
            Source: cl, 2023-04-20
            #terms: 2698

            📖 CellType.df(): ontology reference table
            🔎 CellType.lookup(): autocompletion of terms
            🎯 CellType.search(): free text search of terms
            🧐 CellType.inspect(): check if identifiers are mappable
            👽 CellType.map_synonyms(): map synonyms to standardized names
            🔗 CellType.ontology: Pronto.Ontology object
        """
        if cls.__module__.startswith("lnschema_bionty."):
            species_record = create_or_get_species_record(species=species, orm=cls)

            bionty_object = getattr(bt, cls.__name__)(species=species_record.name if species_record is not None else None)

            return bionty_object

    @classmethod
    def from_bionty(cls, **kwargs) -> Optional[Union["BioORM", List["BioORM"]]]:
        """Create a record or records from bionty based on a single field value.

        Notes:
            For more info, see tutorial :doc:`/lnschema-bionty`

            Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

        Examples:
            Create a record by passing a field value:

            >>> record = lb.Gene.from_bionty(symbol="TCF7", species="human")
            💬 Created 1 Gene record from Bionty that matched symbol field (bionty_source_id=6dGw)
            >>> record
            Gene(id=0StEa7eEhivb, symbol=TCF7, ensembl_gene_id=ENSG00000081059, ncbi_gene_ids=6932, biotype=protein_coding, description=transcription factor 7 [Source:HGNC Symbol;Acc:HGNC:11639], synonyms=TCF-1, species_id=uHJU, bionty_source_id=6dGw, created_by_id=DzTjkKse) # noqa

            Synonyms are recognized:
            >>> record = lb.Gene.from_bionty(symbol="ABC1", species="human")
            💬 Created 1 Gene record from Bionty that matched synonyms (bionty_source_id=6dGw)
            >>> record
            Gene(id=WaOJkdppI1ct, symbol=HEATR6, ensembl_gene_id=ENSG00000068097, ncbi_gene_ids=63897, biotype=protein_coding, description=HEAT repeat containing 6 [Source:HGNC Symbol;Acc:HGNC:24076], synonyms=FLJ22087|ABC1, species_id=uHJU, bionty_source_id=6dGw, created_by_id=DzTjkKse) # noqa
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
            else:
                return results

    def _save_ontology_parents(self):  # saving records of parents
        if hasattr(self, "_parents"):
            import lamindb as ln

            parents = self._parents
            # here parents is still a list of ontology ids
            logger.info(f"Also saving parents of {self}")
            parents_records = self.from_values(parents, self.__class__.ontology_id)
            ln.save(parents_records)
            self.parents.set(parents_records)

    def save(self, parents: bool = True, *args, **kwargs) -> None:
        """Save the record and its parents recursively.

        Args:
            parents: `bool = True` Whether to save parents records.
        """
        # save the record first without parents
        super().save(*args, **kwargs)

        if parents:
            self._save_ontology_parents()


class Species(BioORM):
    """Species.

    Examples:
        >>> record = lb.Species.from_bionty(name="rabbit")
        💬 Created 1 Species record from Bionty that matched name field (bionty_source_id=KkPB)
        >>> record
        Species(id=2Nq8, name=rabbit, taxon_id=9986, scientific_name=oryctolagus_cuniculus, bionty_source_id=KkPB, created_by_id=DzTjkKse)
        >>> record.save()
    """

    id = models.CharField(max_length=4, default=ids.species, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    """Unique name of a species, required field."""
    taxon_id = models.IntegerField(unique=True, db_index=True, null=True, default=None)
    """NCBI Taxon ID."""
    scientific_name = models.CharField(max_length=64, db_index=True, unique=True, null=True, default=None)
    """Scientific name of a species."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
    """:class:`~lnschema_bionty.BiontySource` this record associates with."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.PROTECT, default=current_user_id, related_name="created_species")
    """Creator of record, a :class:`~lamindb.User`."""

    @overload
    def __init__(
        self,
        name: str,
        taxon_id: Optional[int],
        scientific_name: Optional[str],
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
        pass


class Gene(BioORM):
    """Genes.

    Notes:
        For more info, see tutorial :doc:`/biology/scrna`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Gene.from_bionty(symbol="TCF7", species="human")
        💬 Created 1 Gene record from Bionty that matched symbol field (bionty_source_id=6dGw)
        >>> record
        Gene(id=0StEa7eEhivb, symbol=TCF7, ensembl_gene_id=ENSG00000081059, ncbi_gene_ids=6932, biotype=protein_coding, description=transcription factor 7 [Source:HGNC Symbol;Acc:HGNC:11639], synonyms=TCF-1, species_id=uHJU, bionty_source_id=6dGw, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=12, default=ids.gene, primary_key=True)
    symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """A unique short form of gene name."""
    ensembl_gene_id = models.CharField(max_length=64, db_index=True, null=True, default=None, unique=True)
    """Ensembl gene stable ID, in the form ENS[species prefix][feature type prefix][a unique eleven digit number]."""
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
    species = models.ForeignKey(Species, models.PROTECT, null=True, related_name="genes")
    """:class:`~lnschema_bionty.Species` this gene associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="genes")
    """:class:`~lnschema_bionty.BiontySource` this gene associates with."""
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
        ensembl_gene_id: Optional[str],
        ncbi_gene_ids: Optional[str],
        biotype: Optional[str],
        description: Optional[str],
        synonyms: Optional[str],
        species: Optional[Species],
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
        pass


class Protein(BioORM):
    """Proteins.

    Notes:
        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Protein.from_bionty(name="Synaptotagmin-15B", species="human")
        💬 Created 1 Protein record from Bionty that matched name field (bionty_source_id=SFni)
        >>> record
        Protein(id=KiCrq9BBTviZ, name=Synaptotagmin-15B, uniprotkb_id=X6R8R1, synonyms=, length=474, gene_symbol=SYT15B, species_id=uHJU, bionty_source_id=SFni, created_by_id=DzTjkKse) # noqa

        >>> record = lb.Protein.from_bionty(gene_symbol="SYT15B", species="human")
        💬 Created 1 Protein record from Bionty that matched gene_symbol field (bionty_source_id=SFni)
        >>> record
        Protein(id=KiCrq9BBTviZ, name=Synaptotagmin-15B, uniprotkb_id=X6R8R1, synonyms=, length=474, gene_symbol=SYT15B, species_id=uHJU, bionty_source_id=SFni, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=12, default=ids.protein, primary_key=True)
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
    species = models.ForeignKey(Species, models.PROTECT, null=True, related_name="proteins")
    """:class:`~lnschema_bionty.Species` this protein associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="proteins")
    """:class:`~lnschema_bionty.BiontySource` this protein associates with."""
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
        species: Optional[Species],
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
        pass


class CellMarker(BioORM):
    """Cell markers.

    Notes:
        For more info, see tutorial :doc:`/biology/flow`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.CellMarker.from_bionty(name="PD1", species="human")
        💬 Created 1 CellMarker record from Bionty that matched name field (bionty_source_id=7agi)
        >>> record
        CellMarker(id=2VeZenLi2dj5, name=PD1, synonyms=PID1|PD-1|PD 1, gene_symbol=PDCD1, ncbi_gene_id=5133, uniprotkb_id=A0A0M3M0G7, species_id=uHJU, bionty_source_id=7agi, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=12, default=ids.cellmarker, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, default=None, unique=True)
    """Unique name of the cell marker."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell marker."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Gene symbol that corresponds to this cell marker."""
    ncbi_gene_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """NCBI gene id that corresponds to this cell marker."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """Uniprotkb id that corresponds to this cell marker."""
    species = models.ForeignKey(Species, models.PROTECT, null=True, related_name="cell_markers")
    """:class:`~lnschema_bionty.Species` this cell marker associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="cell_markers")
    """:class:`~lnschema_bionty.BiontySource` this cell marker associates with."""
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
        species: Optional[Species],
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
        pass


class Tissue(BioORM):
    """Tissues.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Tissue.from_bionty(name="brain")
        💬 Created 1 Tissue record from Bionty that matched name field (bionty_source_id=XrS9)
        >>> record
        Tissue(id=7HcGzG0l, name=brain, ontology_id=UBERON:0000955, description=The Brain Is The Center Of The Nervous System In All Vertebrate, And Most Invertebrate, Animals. Some Primitive Animals Such As Jellyfish And Starfish Have A Decentralized Nervous System Without A Brain, While Sponges Lack Any Nervous System At All. In Vertebrates, The Brain Is Located In The Head, Protected By The Skull And Close To The Primary Sensory Apparatus Of Vision, Hearing, Balance, Taste, And Smell[Wp]., bionty_source_id=XrS9, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["Tissue"]],
        children: Optional[List["Tissue"]],
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
        pass


class CellType(BioORM):
    """Cell types.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.CellType.from_bionty(name="T cell")
        💬 Created 1 CellType record from Bionty that matched name field (bionty_source_id=ivhQ)
        >>> record
        CellType(id=BxNjby0x, name=T cell, ontology_id=CL:0000084, synonyms=T-cell|T lymphocyte|T-lymphocyte, description=A Type Of Lymphocyte Whose Defining Characteristic Is The Expression Of A T Cell Receptor Complex., bionty_source_id=ivhQ, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["CellType"]],
        children: Optional[List["CellType"]],
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
        pass


class Disease(BioORM):
    """Diseases.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Disease.from_bionty(name="Alzheimer's disease")
        💬 Created 1 Disease record from Bionty that matched synonyms (bionty_source_id=eeie)
        >>> record
        Disease(id=nUmxpVTE, name=Alzheimer disease, ontology_id=MONDO:0004975, synonyms=Alzheimer's disease|Alzheimer's dementia|Alzheimers dementia|Alzheimers disease|Alzheimer dementia|Alzheimer disease|presenile and senile dementia|AD, description=A Progressive, Neurodegenerative Disease Characterized By Loss Of Function And Death Of Nerve Cells In Several Areas Of The Brain Leading To Loss Of Cognitive Function Such As Memory And Language., bionty_source_id=eeie, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["Disease"]],
        children: Optional[List["Disease"]],
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
        pass


class CellLine(BioORM):
    """Cell lines.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.CellLine.from_bionty(name="K562")
        💬 Created 1 CellLine record from Bionty that matched synonyms (bionty_source_id=ls6p)
        >>> record
        CellLine(id=akITPKqK, name=K 562 cell, ontology_id=CLO:0007050, synonyms=K-562|KO|GM05372E|K.562|K562|GM05372|K 562, description=disease: leukemia, chronic myeloid, bionty_source_id=ls6p, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["CellLine"]],
        children: Optional[List["CellLine"]],
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
        pass


class Phenotype(BioORM):
    """Phenotypes.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Phenotype.from_bionty(name="Arachnodactyly")
        💬 Created 1 Phenotype record from Bionty that matched name field (bionty_source_id=2Uqu)
        >>> record
        Phenotype(id=Cbc4RCc0, name=Arachnodactyly, ontology_id=HP:0001166, synonyms=Long slender fingers|Long, slender fingers|Spider fingers, description=Abnormally Long And Slender Fingers ("Spider Fingers")., bionty_source_id=2Uqu, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["Phenotype"]],
        children: Optional[List["Phenotype"]],
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
        pass


class Pathway(BioORM):
    """Pathways.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.Pathway.from_bionty(ontology_id="GO:1903353")
        💬 Created 1 Pathway record from Bionty that matched ontology_id field (bionty_source_id=Zo0l)
        >>> record
        Pathway(id=fwv8v1X9, name=regulation of nucleus organization, ontology_id=GO:1903353, synonyms=regulation of nuclear organisation|regulation of nuclear organization, description=Any Process That Modulates The Frequency, Rate Or Extent Of Nucleus Organization., bionty_source_id=Zo0l, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        parents: Optional[List["Pathway"]],
        children: Optional[List["Pathway"]],
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
        pass


class ExperimentalFactor(BioORM):
    """Experimental factors.

    Notes:
        For more info, see tutorial :doc:`/biology/registries`

        Bulk create protein records via :class:`~lamindb.dev.ORM.from_values`.

    Examples:
        >>> record = lb.ExperimentalFactor.from_bionty(name="scRNA-seq")
        💬 Created 1 ExperimentalFactor record from Bionty that matched synonyms (bionty_source_id=4otL)
        >>> record
        ExperimentalFactor(id=068T1Df6, name=single-cell RNA sequencing, ontology_id=EFO:0008913, synonyms=single-cell RNA-seq|single-cell transcriptome sequencing|scRNA-seq|single cell RNA sequencing, description=A Protocol That Provides The Expression Profiles Of Single Cells Via The Isolation And Barcoding Of Single Cells And Their Rna, Reverse Transcription, Amplification, Library Generation And Sequencing., molecule=RNA assay, instrument=single cell sequencing, bionty_source_id=4otL, created_by_id=DzTjkKse) # noqa
        >>> record.save()
    """

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
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
        molecule: Optional[str],
        instrument: Optional[str],
        measurement: Optional[str],
        parents: Optional[List["ExperimentalFactor"]],
        children: Optional[List["ExperimentalFactor"]],
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
        pass


class BiontySource(ORM):
    """Sources of the Bionty tables."""

    id = models.CharField(max_length=8, default=ids.source, primary_key=True)
    entity = models.CharField(max_length=64, db_index=True)
    """Entity class name."""
    species = models.CharField(max_length=64, db_index=True)
    """Species name, use 'all' if unknown or none applied."""
    currently_used = models.BooleanField(default=False, db_index=True)
    """Whether this record is currently used."""
    source = models.CharField(max_length=64, db_index=True)
    """Source key, short form, CURIE prefix for ontologies"""
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
        unique_together = (("entity", "source", "species", "version"),)

    @overload
    def __init__(
        self,
        entity: str,
        species: str,
        source: str,
        version: str,
        source_name: Optional[str],
        url: Optional[str],
        md5: Optional[str],
        source_website: Optional[str],
        currently_used: bool = False,
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
        pass
