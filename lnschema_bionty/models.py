from django.db import models
from lnschema_core._users import current_user_id
from lnschema_core.models import BaseORM, User

from .dev import id as idg
from .dev._bionty import knowledge


@knowledge
class Species(BaseORM):
    """Species."""

    id = models.CharField(max_length=4, default=idg.species, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    taxon_id = models.IntegerField(unique=True, blank=True, null=True)
    scientific_name = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@knowledge
class Gene(BaseORM):
    """Genes."""

    id = models.CharField(max_length=8, default=idg.gene, primary_key=True)
    ensembl_gene_id = models.CharField(max_length=64, blank=True, null=True)
    symbol = models.CharField(max_length=64, blank=True, null=True)
    gene_type = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ncbi_gene_id = models.BigIntegerField(blank=True, null=True)
    hgnc_id = models.CharField(max_length=10, blank=True, null=True)
    mgi_id = models.CharField(max_length=11, blank=True, null=True)
    omim_id = models.CharField(max_length=6, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    version = models.CharField(max_length=64, blank=True, null=True)
    features = models.ManyToManyField("lnschema_core.Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@knowledge
class Protein(BaseORM):
    """Proteins."""

    id = models.CharField(max_length=8, default=idg.protein, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    uniprotkb_id = models.CharField(max_length=10, blank=True, null=True)
    uniprotkb_name = models.CharField(max_length=64, blank=True, null=True)
    # TODO: rename to synonyms
    protein_names = models.TextField(blank=True, null=True)
    length = models.BigIntegerField()
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    gene_symbols = models.TextField(blank=True, null=True)
    gene_synonyms = models.TextField(blank=True, null=True)
    ensembl_transcript_ids = models.TextField(blank=True, null=True)
    ncbi_gene_ids = models.TextField(blank=True, null=True)
    features = models.ManyToManyField("lnschema_core.Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@knowledge
class CellMarker(BaseORM):
    """Cell markers."""

    id = models.CharField(max_length=8, default=idg.cell_marker, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True, unique=True)
    ncbi_gene_id = models.CharField(max_length=32, blank=True, null=True)
    gene_symbol = models.CharField(max_length=64, blank=True, null=True)
    gene_name = models.TextField(blank=True, null=True)
    uniprotkb_id = models.CharField(max_length=10, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    features = models.ManyToManyField("lnschema_core.Features", related_name="cell_markers")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@knowledge
class Tissue(BaseORM):
    """Tissues."""

    id = models.CharField(max_length=8, default=idg.tissue, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class CellType(BaseORM):
    """Cell types."""

    id = models.CharField(max_length=8, default=idg.cell_type, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class Disease(BaseORM):
    """Diseases."""

    id = models.CharField(max_length=8, default=idg.disease, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class CellLine(BaseORM):
    """Cell lines."""

    id = models.CharField(max_length=8, default=idg.cell_line, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class Phenotype(BaseORM):
    """Phenotypes."""

    id = models.CharField(max_length=8, default=idg.phenotype, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class Pathway(BaseORM):
    """Pathways."""

    id = models.CharField(max_length=8, default=idg.pathway, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    genes = models.ManyToManyField("Gene")
    features = models.ManyToManyField("lnschema_core.Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


@knowledge
class Readout(BaseORM):
    """Readouts."""

    id = models.CharField(max_length=8, default=idg.readout, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.TextField(blank=True, null=True)
    molecule = models.TextField(blank=True, null=True)
    instrument = models.TextField(blank=True, null=True)
    measurement = models.TextField(blank=True, null=True)
    files = models.ManyToManyField("lnschema_core.File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class BiontyVersions(BaseORM):
    """Versions of the Bionty tables."""

    id = models.BigAutoField(primary_key=True)
    entity = models.CharField(max_length=64)
    database = models.CharField(max_length=64)
    database_v = models.CharField(max_length=64)
    database_url = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CurrentBiontyVersions(BaseORM):
    """In-use version of the knowledge tables."""

    bionty_version = models.OneToOneField(BiontyVersions, models.DO_NOTHING, parent_link=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
