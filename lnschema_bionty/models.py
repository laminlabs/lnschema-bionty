from django.db import models
from lnschema_core._users import current_user_id
from lnschema_core.models import BaseORM, User

from . import ids
from ._bionty import bionty_decorator


@bionty_decorator
class Species(BaseORM):
    """Species."""

    id = models.CharField(max_length=4, default=ids.species, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    taxon_id = models.IntegerField(unique=True, blank=True, null=True)
    scientific_name = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@bionty_decorator
class Gene(BaseORM):
    """Genes."""

    id = models.CharField(max_length=8, default=ids.gene, primary_key=True)
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


@bionty_decorator
class Protein(BaseORM):
    """Proteins."""

    id = models.CharField(max_length=8, default=ids.protein, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    uniprotkb_id = models.CharField(max_length=10, blank=True, null=True)
    uniprotkb_name = models.CharField(max_length=64, blank=True, null=True)
    synonyms = models.TextField(blank=True, null=True)
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


@bionty_decorator
class CellMarker(BaseORM):
    """Cell markers."""

    id = models.CharField(max_length=8, default=ids.cell_marker, primary_key=True)
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


@bionty_decorator
class Tissue(BaseORM):
    """Tissues."""

    id = models.CharField(max_length=8, default=ids.tissue, primary_key=True)
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


@bionty_decorator
class CellType(BaseORM):
    """Cell types."""

    id = models.CharField(max_length=8, default=ids.cell_type, primary_key=True)
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


@bionty_decorator
class Disease(BaseORM):
    """Diseases."""

    id = models.CharField(max_length=8, default=ids.disease, primary_key=True)
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


@bionty_decorator
class CellLine(BaseORM):
    """Cell lines."""

    id = models.CharField(max_length=8, default=ids.cell_line, primary_key=True)
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


@bionty_decorator
class Phenotype(BaseORM):
    """Phenotypes."""

    id = models.CharField(max_length=8, default=ids.phenotype, primary_key=True)
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


@bionty_decorator
class Pathway(BaseORM):
    """Pathways."""

    id = models.CharField(max_length=8, default=ids.pathway, primary_key=True)
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


@bionty_decorator
class Readout(BaseORM):
    """Readouts."""

    id = models.CharField(max_length=8, default=ids.readout, primary_key=True)
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
    entity = models.CharField(max_length=64, default=None)
    source_name = models.TextField(blank=True, null=True)
    source_key = models.CharField(max_length=64, default=None)
    species = models.CharField(max_length=64, default=None)
    version = models.CharField(max_length=64, default=None)
    url = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("entity", "source_key", "species", "version"),)


class CurrentBiontyVersions(BaseORM):
    """In-use version of the knowledge tables."""

    bionty_version = models.OneToOneField(BiontyVersions, models.DO_NOTHING, parent_link=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
