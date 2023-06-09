from django.db import models
from lnschema_core.models import BaseORM, User
from lnschema_core.users import current_user_id

from . import ids
from ._bionty import bionty_decorator


@bionty_decorator
class Species(BaseORM):
    """Species."""

    id = models.CharField(max_length=8, default=ids.species, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, default=None)
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

    class Meta:
        managed = True


@bionty_decorator
class Gene(BaseORM):
    """Genes."""

    id = models.CharField(max_length=12, default=ids.gene, primary_key=True)
    ensembl_gene_id = models.CharField(max_length=64, db_index=True)
    """Ensembl gene stable ID, in the form ENS[species prefix][feature type prefix][a unique eleven digit number]."""
    symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """A unique short form of gene name."""
    gene_type = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Type of the gene."""
    description = models.TextField(null=True, default=None)
    """Description of the gene."""
    ncbi_gene_id = models.BigIntegerField(db_index=True, null=True)
    """NCBI Gene ID, also known as Entrez Gene ID, in the form of numeric string, 1 to 9 digits."""
    hgnc_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """A unique ID provided by the HGNC for each gene with an approved symbol."""
    mgi_id = models.CharField(max_length=11, db_index=True, null=True, default=None)
    """Mouse Genome Informatics(MGI) Accession ID, in the form of MGI:nnnnnn, where n is a number."""
    omim_id = models.CharField(max_length=6, db_index=True, null=True, default=None)
    """Online Mendelian Inheritance in Man (OMIM) catalogue codes for diseases, genes, or phenotypes. 6 digits."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this gene."""
    species = models.ForeignKey(Species, models.PROTECT, null=True)
    """:class:`~lnschema_bionty.Species` this gene associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
    """:class:`~lnschema_bionty.BiontySource` this gene associates with."""
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="genes")
    """Featuresets linked to this gene."""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    """Time of creation of record."""
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    """Time of last update to record."""
    created_by = models.ForeignKey(User, models.PROTECT, default=current_user_id, related_name="created_genes")
    """Creator of record, a :class:`~lamindb.User`."""

    class Meta:
        managed = True


@bionty_decorator
class Protein(BaseORM):
    """Proteins."""

    id = models.CharField(max_length=12, default=ids.protein, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Unique name of a protein."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """UniProt protein ID, 6 alphanumeric characters, possibly suffixed by 4 more."""
    uniprotkb_name = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """UniProtKB/Swiss-Prot entry name."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this protein."""
    length = models.BigIntegerField(db_index=True, null=True)
    """Length of the protein sequence."""
    gene_symbols = models.TextField(null=True, default=None)
    """Bar-separated (|) gene symbols that correspond to this protein."""
    gene_synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) gene synonyms that correspond to this protein."""
    ensembl_transcript_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) Ensembl Transcript IDs that correspond to this protein."""
    ncbi_gene_ids = models.TextField(null=True, default=None)
    """Bar-separated (|) NCBI Gene IDs that correspond to this protein."""
    species = models.ForeignKey(Species, models.PROTECT, null=True)
    """:class:`~lnschema_bionty.Species` this protein associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
    """:class:`~lnschema_bionty.BiontySource` this protein associates with."""
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="proteins")
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

    class Meta:
        managed = True


@bionty_decorator
class CellMarker(BaseORM):
    """Cell markers."""

    id = models.CharField(max_length=12, default=ids.cell_marker, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, unique=True, null=True, default=None)
    """Unique name of the cell marker."""
    ncbi_gene_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Bar-separated (|) NCBI gene ids that correspond to this cell marker."""
    gene_symbol = models.CharField(max_length=64, db_index=True, null=True, default=None)
    """Bar-separated (|) gene symbols that correspond to this cell marker."""
    gene_name = models.TextField(null=True, default=None)
    """Bar-separated (|) gene names that correspond to this cell marker."""
    uniprotkb_id = models.CharField(max_length=10, db_index=True, null=True, default=None)
    """Bar-separated (|) uniprotkb ids that correspond to this cell marker."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell marker."""
    species = models.ForeignKey(Species, models.PROTECT, null=True)
    """:class:`~lnschema_bionty.Species` this cell marker associates with."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
    """:class:`~lnschema_bionty.BiontySource` this cell marker associates with."""
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="cell_markers")
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

    class Meta:
        managed = True


@bionty_decorator
class Tissue(BaseORM):
    """Tissues."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the tissue."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of tissue."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this tissue."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the tissue."""
    definition = models.TextField(null=True, default=None)
    """Definition of the tissue."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class CellType(BaseORM):
    """Cell types."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the cell type."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of cell type."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell type."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the cell type."""
    definition = models.TextField(null=True, default=None)
    """Definition of the cell type."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class Disease(BaseORM):
    """Diseases."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the disease."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of disease."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this disease."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the disease."""
    definition = models.TextField(null=True, default=None)
    """Definition of the disease."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class CellLine(BaseORM):
    """Cell lines."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the cell line."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of cell line."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this cell line."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the cell line."""
    definition = models.TextField(null=True, default=None)
    """Definition of the cell line."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class Phenotype(BaseORM):
    """Phenotypes."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the phenotype."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of phenotype."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this phenotype."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the phenotype."""
    definition = models.TextField(null=True, default=None)
    """Definition of the phenotype."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class Pathway(BaseORM):
    """Pathways."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the pathway."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of pathway."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this pathway."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the pathway."""
    definition = models.TextField(null=True, default=None)
    """Definition of the pathway."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
    """:class:`~lnschema_bionty.BiontySource` this pathway associates with."""
    genes = models.ManyToManyField("Gene")
    """Genes that signifies the pathway."""
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="pathways")
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
        managed = True
        unique_together = (("name", "ontology_id"),)


@bionty_decorator
class Readout(BaseORM):
    """Readouts."""

    id = models.CharField(max_length=8, default=ids.ontology, primary_key=True)
    name = models.CharField(max_length=256, db_index=True, null=True, default=None)
    """Name of the readout."""
    short_name = models.CharField(max_length=32, db_index=True, unique=True, null=True, default=None)
    """A unique short name of readout."""
    synonyms = models.TextField(null=True, default=None)
    """Bar-separated (|) synonyms that correspond to this readout."""
    ontology_id = models.CharField(max_length=32, db_index=True, null=True, default=None)
    """Ontology ID of the readout."""
    definition = models.TextField(null=True, default=None)
    """Definition of the readout."""
    molecule = models.TextField(null=True, default=None, db_index=True)
    """Molecular readout, parsed from EFO."""
    instrument = models.TextField(null=True, default=None, db_index=True)
    """Instrument used to measure the readout, parsed from EFO."""
    measurement = models.TextField(null=True, default=None, db_index=True)
    """Phenotypic readout, parsed from EFO."""
    bionty_source = models.ForeignKey("BiontySource", models.PROTECT, null=True)
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
        managed = True
        unique_together = (("name", "ontology_id"),)


class BiontySource(BaseORM):
    """Sources of the Bionty tables."""

    id = models.CharField(max_length=8, default=ids.source, primary_key=True)
    entity = models.CharField(max_length=64, default=None, db_index=True)
    species = models.CharField(max_length=64, default=None, db_index=True)
    currently_used = models.BooleanField(default=False, db_index=True)
    source_name = models.TextField(blank=True, db_index=True)
    source_key = models.CharField(max_length=64, default=None, db_index=True)
    version = models.CharField(max_length=64, default=None, db_index=True)
    url = models.TextField(null=True, default=None)
    md5 = models.TextField(null=True, default=None)
    source_website = models.TextField(null=True, default=None)
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
        managed = True
        unique_together = (("entity", "source_key", "species", "version"),)
