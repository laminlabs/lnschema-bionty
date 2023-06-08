from django.db import models
from lnschema_core._users import current_user_id
from lnschema_core.models import BaseORM, User

from . import ids
from ._bionty import bionty_decorator


@bionty_decorator
class Species(BaseORM):
    """Species."""

    id = models.CharField(max_length=4, default=ids.species, primary_key=True)
    name = models.CharField(max_length=64, db_index=True)
    taxon_id = models.IntegerField(unique=True, db_index=True)
    scientific_name = models.CharField(max_length=64, db_index=True, unique=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@bionty_decorator
class Gene(BaseORM):
    """Genes."""

    id = models.CharField(max_length=8, default=ids.gene, primary_key=True)
    ensembl_gene_id = models.CharField(max_length=64, db_index=True)
    symbol = models.CharField(max_length=64, db_index=True)
    gene_type = models.CharField(max_length=64, db_index=True)
    description = models.TextField()
    ncbi_gene_id = models.BigIntegerField(db_index=True)
    hgnc_id = models.CharField(max_length=10, db_index=True)
    mgi_id = models.CharField(max_length=11, db_index=True)
    omim_id = models.CharField(max_length=6, db_index=True)
    synonyms = models.TextField()
    species = models.ForeignKey(Species, models.DO_NOTHING)
    version = models.CharField(max_length=64, db_index=True)
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="genes")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@bionty_decorator
class Protein(BaseORM):
    """Proteins."""

    id = models.CharField(max_length=8, default=ids.protein, primary_key=True)
    name = models.CharField(max_length=64, db_index=True)
    uniprotkb_id = models.CharField(max_length=10, db_index=True)
    uniprotkb_name = models.CharField(max_length=64, db_index=True)
    synonyms = models.TextField()
    length = models.BigIntegerField()
    species = models.ForeignKey(Species, models.DO_NOTHING)
    gene_symbols = models.TextField()
    gene_synonyms = models.TextField()
    ensembl_transcript_ids = models.TextField()
    ncbi_gene_ids = models.TextField()
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="proteins")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@bionty_decorator
class CellMarker(BaseORM):
    """Cell markers."""

    id = models.CharField(max_length=8, default=ids.cell_marker, primary_key=True)
    name = models.CharField(max_length=64, db_index=True, unique=True)
    ncbi_gene_id = models.CharField(max_length=32, db_index=True)
    gene_symbol = models.CharField(max_length=64, db_index=True)
    gene_name = models.TextField()
    uniprotkb_id = models.CharField(max_length=10, db_index=True)
    synonyms = models.TextField()
    species = models.ForeignKey(Species, models.DO_NOTHING)
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="cell_markers")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


@bionty_decorator
class Tissue(BaseORM):
    """Tissues."""

    id = models.CharField(max_length=8, default=ids.tissue, primary_key=True)
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    files = models.ManyToManyField("lnschema_core.File", related_name="tissues")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    files = models.ManyToManyField("lnschema_core.File", related_name="cell_types")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    files = models.ManyToManyField("lnschema_core.File", related_name="diseases")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    files = models.ManyToManyField("lnschema_core.File", related_name="cell_lines")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    files = models.ManyToManyField("lnschema_core.File", related_name="phenotypes")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    genes = models.ManyToManyField("Gene")
    featuresets = models.ManyToManyField("lnschema_core.Featureset", related_name="pathways")
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
    name = models.CharField(max_length=256, db_index=True)
    short_name = models.CharField(max_length=32, db_index=True)
    synonyms = models.TextField()
    ontology_id = models.CharField(max_length=16, db_index=True)
    definition = models.TextField()
    molecule = models.TextField(db_index=True)
    instrument = models.TextField(db_index=True)
    measurement = models.TextField(db_index=True)
    files = models.ManyToManyField("lnschema_core.File", related_name="readouts")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class BiontySource(BaseORM):
    """Versions of the Bionty tables."""

    id = models.BigAutoField(primary_key=True)
    entity = models.CharField(max_length=64, default=None, db_index=True)
    species = models.CharField(max_length=64, default=None, db_index=True)
    currently_used = models.BooleanField(default=False, db_index=True)
    source_name = models.TextField(blank=True, db_index=True)
    source_key = models.CharField(max_length=64, default=None, db_index=True)
    version = models.CharField(max_length=64, default=None, db_index=True)
    url = models.TextField(blank=True)
    md5 = models.TextField(blank=True)
    source_website = models.TextField(blank=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("entity", "source_key", "species", "version"),)
