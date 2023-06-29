from typing import List, Optional, Tuple

import numpy as np
from django.db import models
from lamin_logger import logger
from lnschema_core.models import BaseORM, User
from lnschema_core.users import current_user_id

from . import ids
from ._bionty import get_bionty_object, lookup2kwargs


class BioORM(BaseORM):
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
                return self
            except IndexError:
                kwargs = result
                args = ()

        if "parents" in kwargs:
            parents = kwargs.pop("parents")
            # this checks if we receive a np.ndarray from pandas
            if isinstance(parents, (list, np.ndarray)) and len(parents) > 0:
                if not isinstance(parents[0], str):
                    raise ValueError("Not a valid parents kwarg, got to be list of ontology ids")
                self._parents = parents

        super().__init__(*args, **kwargs)

    @classmethod
    def bionty(cls, species: Optional[str] = None):
        return get_bionty_object(orm=cls, species=species)

    @classmethod
    def from_bionty(cls, **kwargs):
        """Create a record or records from bionty based on a single field value."""
        kv = {k: v for k, v in kwargs.items() if k not in [i.name for i in cls._meta.fields if i.is_relation]}
        if len(kv) > 1:
            raise AssertionError("Only one field can be passed to generate record from Bionty")
        elif len(kv) == 0:
            return None
        else:
            k = next(iter(kv))
            v = kwargs.pop(k)
            results = cls.from_values(values=[v], field=getattr(cls, k), **kwargs)
            if len(results) == 1:
                return results[0]
            else:
                return results

    def save(self, *args, **kwargs):
        if hasattr(self, "_parents"):
            parents = self._parents
            # here parents is still a list of ontology ids
            logger.info(f"Also saving parents of {self}")
            parents_records = self.from_values(parents, self.__class__.ontology_id)
            for record in parents_records:
                record.save()
        super().save(*args, **kwargs)
        if hasattr(self, "_parents"):
            self.parents.set(parents_records)


class Species(BioORM):
    """Species."""

    id = models.CharField(max_length=4, default=ids.species, primary_key=True)
    name = models.CharField(max_length=64, db_index=True)
    """Name of a species, required field."""
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


class Gene(BioORM):
    """Genes."""

    id = models.CharField(max_length=12, default=ids.gene, primary_key=True)
    symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """A unique short form of gene name."""
    ensembl_gene_id = models.CharField(max_length=64, db_index=True)
    """Ensembl gene stable ID, in the form ENS[species prefix][feature type prefix][a unique eleven digit number]."""
    ncbi_gene_id = models.BigIntegerField(db_index=True, null=True)
    """NCBI Gene ID, also known as Entrez Gene ID, in the form of numeric string, 1 to 9 digits."""
    biotype = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Type of the gene."""
    description = models.TextField(null=True, default=None)
    """Description of the gene."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this gene."""
    hgnc_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """A unique ID provided by the HGNC for each gene with an approved symbol."""
    mgi_id = models.CharField(max_length=11, db_index=True, null=True, default=None)
    """Mouse Genome Informatics(MGI) Accession ID, in the form of MGI:nnnnnn, where n is a number."""
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


class Protein(BioORM):
    """Proteins."""

    id = models.CharField(max_length=12, default=ids.protein, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Unique name of a protein."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """UniProt protein ID, 6 alphanumeric characters, possibly suffixed by 4 more."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this protein."""
    length = models.BigIntegerField(db_index=True, null=True)
    """Length of the protein sequence."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """The primary gene symbol corresponds to this protein."""
    ncbi_gene_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) NCBI Gene IDs that correspond to this protein."""
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


class CellMarker(BioORM):
    """Cell markers."""

    id = models.CharField(max_length=12, default=ids.cellmarker, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, unique=True)
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell marker."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Gene symbol that corresponds to this cell marker."""
    """Unique name of the cell marker."""
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


class Tissue(BioORM):
    """Tissues."""

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


class CellType(BioORM):
    """Cell types."""

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


class Disease(BioORM):
    """Diseases."""

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


class CellLine(BioORM):
    """Cell lines."""

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


class Phenotype(BioORM):
    """Phenotypes."""

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


class Pathway(BioORM):
    """Pathways."""

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


class Readout(BioORM):
    """Readouts."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True)
    """Name of the readout."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the readout."""
    abbr = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique abbreviation of readout."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this readout."""
    description = models.TextField(null=True, default=None)
    """Description of the readout."""
    molecule = models.TextField(null=True, default=None, db_index=True)
    """Molecular readout, parsed from EFO."""
    instrument = models.TextField(null=True, default=None, db_index=True)
    """Instrument used to measure the readout, parsed from EFO."""
    measurement = models.TextField(null=True, default=None, db_index=True)
    """Phenotypic readout, parsed from EFO."""
    parents = models.ManyToManyField("self", symmetrical=False, related_name="children")
    """Parent readout records."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True, related_name="readouts")
    """:class:`~lnschema_bionty.BiontySource` this readout associates with."""
    files = models.ManyToManyField("lnschema_core.File", related_name="readouts")
    """Files linked to the readout."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(
        User,
        models.PROTECT,
        default=current_user_id,
        related_name="created_readouts",
    )
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        unique_together = (("name", "ontology_id"),)


class BiontySource(BaseORM):
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
