from typing import Dict, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lamin_utils import logger
from lnschema_core.models import Registry  # TODO: import Registry instead of ORM

from . import ids


def create_or_get_organism_record(organism: Optional[Union[str, Registry]], orm: Registry) -> Optional[Registry]:
    # return None if an Registry doesn't have organism field
    organism_record = None
    if hasattr(orm, "organism"):
        # using global setting of organism
        from .dev._settings import settings

        if organism is None and settings.organism is not None:
            logger.debug(f"using global setting organism = {settings.organism.name}")
            return settings.organism

        if isinstance(organism, Registry):
            organism_record = organism
        elif isinstance(organism, str):
            from lnschema_bionty import Organism

            try:
                # existing organism record
                organism_record = Organism.objects.get(name=organism)
            except ObjectDoesNotExist:
                try:
                    # create a organism record from bionty reference
                    organism_record = Organism.from_bionty(name=organism)
                    # link the organism record to the default bionty source
                    organism_record.bionty_source = get_bionty_source_record(bt.Organism())  # type:ignore
                    organism_record.save()  # type:ignore
                except KeyError:
                    # no such organism is found in bionty reference
                    organism_record = None

        if organism_record is None:
            raise AssertionError(f"{orm.__name__} requires to specify a organism name via `organism=` or `lb.settings.organism=`!")

    return organism_record


def get_bionty_source_record(bionty_object: bt.Bionty):
    kwargs = dict(
        entity=bionty_object.__class__.__name__,
        organism=bionty_object.organism,
        source=bionty_object.source,
        version=bionty_object.version,
    )
    from .models import BiontySource

    source_record = BiontySource.objects.filter(**kwargs).get()
    return source_record


def encode_uid(orm: Registry, kwargs: dict):
    if kwargs.get("uid") is not None:
        # if uid is passed
        return kwargs
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
        concat_str = f'{kwargs.get("entity", "")}{kwargs.get("source", "")}{kwargs.get("organism", "")}{kwargs.get("version", "")}'  # noqa
    elif kwargs.get("ontology_id") is not None:
        concat_str = f"{kwargs.get('name', '')}{kwargs.get('ontology_id', '')}"
        ontology = True
    elif (kwargs.get("id") is not None) and (name == "organism") and (kwargs.get("uid") is None):
        # organism, it's not "uid", here, but the taxon id
        concat_str = kwargs.pop("id")
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

        # add organism and bionty_source
        organism_record = create_or_get_organism_record(orm=orm.__class__, organism=kwargs.get("organism"))
        if organism_record is not None:
            bionty_kwargs["organism"] = organism_record
        bionty_object = getattr(bt, orm.__class__.__name__)(organism=organism_record.name if organism_record is not None else None)
        bionty_kwargs["bionty_source"] = get_bionty_source_record(bionty_object)

        model_field_names = {i.name for i in orm._meta.fields}
        model_field_names.add("parents")
        bionty_kwargs = {k: v for k, v in bionty_kwargs.items() if k in model_field_names}
    return encode_uid(orm=orm, kwargs=bionty_kwargs)


# backward compat
create_or_get_species_record = create_or_get_organism_record
