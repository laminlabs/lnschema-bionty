from django.db import models
from lnschema_core._users import current_user_id
from lnschema_core.models import BaseORM, User

from .dev import id as idg


class Species(BaseORM):
    """Species."""

    id = models.CharField(max_length=4, default=idg.species, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    taxon_id = models.IntegerField(max_length=7, unique=True, blank=True, null=True)
    scientific_name = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Gene(BaseORM):
    """Genes."""

    id = models.CharField(max_length=8, default=idg.gene, primary_key=True)
    ensembl_gene_id = models.CharField(max_length=64, blank=True, null=True)
    symbol = models.CharField(max_length=64, blank=True, null=True)
    gene_type = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    ncbi_gene_id = models.BigIntegerField(max_length=32, blank=True, null=True)
    hgnc_id = models.CharField(max_length=10, blank=True, null=True)
    mgi_id = models.CharField(max_length=11, blank=True, null=True)
    omim_id = models.CharField(max_length=6, blank=True, null=True)
    synonyms = models.CharField(max_length=500, blank=True, null=True)
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    version = models.CharField(max_length=64, blank=True, null=True)
    features = models.ManyToManyField("Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Protein(BaseORM):
    """Proteins."""

    id = models.CharField(max_length=8, default=idg.protein, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    uniprotkb_id = models.CharField(max_length=10, blank=True, null=True)
    uniprotkb_name = models.CharField(max_length=64, blank=True, null=True)
    # TODO: rename to synonyms
    protein_names = models.CharField(max_length=300, blank=True, null=True)
    length = models.BigIntegerField(max_length=8)
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    gene_symbols = models.CharField(max_length=500, blank=True, null=True)
    gene_synonyms = models.CharField(max_length=500, blank=True, null=True)
    # TODO: this field has max_length of 3825 in the current version
    ensembl_transcript_ids = models.CharField(blank=True, null=True)
    ncbi_gene_ids = models.CharField(max_length=500, blank=True, null=True)
    features = models.ManyToManyField("Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class CellMarker(BaseORM):
    """Cell markers."""

    id = models.CharField(max_length=8, default=idg.cell_marker, primary_key=True)
    name = models.CharField(max_length=64, blank=True, null=True, unique=True)
    ncbi_gene_id = models.CharField(max_length=9, blank=True, null=True)
    gene_symbol = models.CharField(max_length=64, blank=True, null=True)
    gene_name = models.CharField(max_length=164, blank=True, null=True)
    uniprotkb_id = models.CharField(max_length=10, blank=True, null=True)
    synonyms = models.CharField(max_length=64, blank=True, null=True)
    species = models.ForeignKey(Species, models.DO_NOTHING, blank=True, null=True)
    features = models.ManyToManyField("Features", related_name="cell_markers")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True


class Tissue(BaseORM):
    """Tissues."""

    id = models.CharField(max_length=8, default=idg.tissue, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    # max_length 2804
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    # max_length 1682
    definition = models.CharField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class CellType(BaseORM):
    """Cell types."""

    id = models.CharField(max_length=8, default=idg.cell_type, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class Disease(BaseORM):
    """Diseases."""

    id = models.CharField(max_length=8, default=idg.disease, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class CellLine(BaseORM):
    """Cell lines."""

    id = models.CharField(max_length=8, default=idg.cell_line, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class Phenotype(BaseORM):
    """Phenotypes."""

    id = models.CharField(max_length=8, default=idg.phenotype, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class Pathway(BaseORM):
    """Pathways."""

    id = models.CharField(max_length=8, default=idg.pathway, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    genes = models.ManyToManyField("Gene")
    features = models.ManyToManyField("Features")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)


class Readout(BaseORM):
    """Readouts."""

    id = models.CharField(max_length=8, default=idg.readout, primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    short_name = models.CharField(max_length=32, blank=True, null=True)
    synonyms = models.CharField(blank=True, null=True)
    ontology_id = models.CharField(max_length=16, blank=True, null=True)
    definition = models.CharField(blank=True, null=True)
    molecule = models.CharField(max_length=64, blank=True, null=True)
    instrument = models.CharField(max_length=128, blank=True, null=True)
    measurement = models.CharField(max_length=128, blank=True, null=True)
    files = models.ManyToManyField("File")
    created_by = models.ForeignKey(User, models.DO_NOTHING, default=current_user_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = (("name", "ontology_id"),)
