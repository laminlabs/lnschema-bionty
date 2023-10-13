from typing import Dict, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lamin_utils import logger
from lnschema_core.models import Registry  # TODO: import Registry instead of ORM

from . import ids


def create_or_get_species_record(species: Optional[Union[str, Registry]], orm: Registry) -> Optional[Registry]:
    # return None if an Registry doesn't have species field
    species_record = None
    if hasattr(orm, "species"):
        # using global setting of species
        from .dev._settings import settings

        if species is None and settings.species is not None:
            logger.debug(f"using global setting species = {settings.species.name}")
            return settings.species

        if isinstance(species, Registry):
            species_record = species
        elif isinstance(species, str):
            from lnschema_bionty import Species

            try:
                # existing species record
                species_record = Species.objects.get(name=species)
            except ObjectDoesNotExist:
                try:
                    # create a species record from bionty reference
                    species_record = Species.from_bionty(name=species)
                    # link the species record to the default bionty source
                    species_record.bionty_source = get_bionty_source_record(bt.Species())  # type:ignore
                    species_record.save()  # type:ignore
                except KeyError:
                    # no such species is found in bionty reference
                    species_record = None

        if species_record is None:
            raise AssertionError(f"{orm.__name__} requires to specify a species name via `species=` or `lb.settings.species=`!")

    return species_record


def get_bionty_source_record(bionty_object: bt.Bionty):
    kwargs = dict(
        entity=bionty_object.__class__.__name__,
        species=bionty_object.species,
        source=bionty_object.source,
        version=bionty_object.version,
    )
    from .models import BiontySource

    source_record = BiontySource.objects.filter(**kwargs).get()
    return source_record


def encode_uid(orm: Registry, kwargs: dict):
    try:
        name = orm.__name__.lower()
    except AttributeError:
        name = orm.__class__.__name__.lower()
    ontology = False
    concat_str = ""
    if name == "gene":
        concat_str = f"{kwargs.get('stable_id', '')}{kwargs.get('ensembl_gene_id', '')}{kwargs.get('symbol', '')}"
    elif name == "protein":
        concat_str = kwargs.get("uniprotkb_id", "")
    elif name == "cellmarker":
        concat_str = kwargs.get("name", "")
    elif name == "biontysource":
        concat_str = f'{kwargs.get("entity", "")}{kwargs.get("source", "")}{kwargs.get("species", "")}{kwargs.get("version", "")}'  # noqa
    elif kwargs.get("id") is not None:
        # species, it's not "uid", here, but the taxon id
        concat_str = kwargs.pop("id")
    elif kwargs.get("ontology_id") is not None:
        concat_str = f"{kwargs.get('name', '')}{kwargs.get('ontology_id', '')}"
        ontology = True
    if len(concat_str) > 0:
        if ontology:
            id_encoder = ids.ontology
        else:
            try:
                id_encoder = getattr(ids, name)
            except Exception:
                return kwargs
        kwargs["uid"] = id_encoder(concat_str)
    return kwargs


def lookup2kwargs(orm: Registry, *args, **kwargs) -> Dict:
    """Pass bionty search/lookup results."""
    arg = args[0]
    if isinstance(arg, tuple):
        bionty_kwargs = arg._asdict()  # type:ignore
    else:
        bionty_kwargs = arg[0]._asdict()

    if len(bionty_kwargs) > 0:
        import bionty as bt

        # add species and bionty_source
        species_record = create_or_get_species_record(orm=orm.__class__, species=kwargs.get("species"))
        if species_record is not None:
            bionty_kwargs["species"] = species_record
        bionty_object = getattr(bt, orm.__class__.__name__)(species=species_record.name if species_record is not None else None)
        bionty_kwargs["bionty_source"] = get_bionty_source_record(bionty_object)

        model_field_names = {i.name for i in orm._meta.fields}
        model_field_names.add("parents")
        bionty_kwargs = {k: v for k, v in bionty_kwargs.items() if k in model_field_names}
    return encode_uid(orm=orm, kwargs=bionty_kwargs)
