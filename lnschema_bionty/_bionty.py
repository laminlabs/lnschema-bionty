from typing import Dict, List, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lnschema_core.models import ORM

from . import ids


def fields_from_knowledge(
    locals: dict,
    bionty_object: bt.Bionty,
) -> List:
    if len(locals) > 1:
        raise AssertionError("Only 1 kwarg can be passed when populating fields from bionty!")
    df = bionty_object._df

    k = next(iter(locals))
    v = locals[k]
    try:
        bionty_dicts = df.set_index(k).loc[[v]].reset_index().to_dict(orient="records")
    except KeyError:
        raise KeyError(f"No entry is found in bionty reference table with '{k}={v}'!\n Try passing a species other than {bionty_object.species}!")

    return bionty_dicts


def create_or_get_species_record(species: Union[str, ORM], orm: ORM) -> Optional[ORM]:
    # return None if an ORM doesn't have species field
    species_record = None
    if hasattr(orm, "species"):
        if isinstance(species, ORM):
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
                    species_record.bionty_source = get_bionty_source_record(bt.Species())
                    species_record.save()
                except KeyError:
                    # no such species is found in bionty reference
                    species_record = None
        if species_record is None:
            raise AssertionError(f"{orm.__name__} table requires to specify a species name via `species=`!")

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
    if not source_record.currently_used:
        raise AssertionError("Currently used resources are not correctly configured! Please reload your instance!")

    return source_record


def get_bionty_object(orm: ORM, species: Union[str, ORM] = None):
    if orm.__module__.startswith("lnschema_bionty."):
        import bionty as bt

        if isinstance(species, ORM):
            species_name = species.name
        else:
            species_name = species

        bionty_object = getattr(bt, orm.__name__)(species=species_name)

        return bionty_object


def encode_id(orm: ORM, kwargs: dict):
    try:
        name = orm.__name__.lower()
    except AttributeError:
        name = orm.__class__.__name__.lower()
    ontology = False
    concat_str = ""
    if name == "gene":
        if kwargs.get("hgnc_id") is not None:
            concat_str = kwargs.get("hgnc_id", "")
        elif kwargs.get("mgi_id") is not None:
            concat_str = kwargs.get("mgi_id", "")
        else:
            concat_str = ""
        concat_str = f"{concat_str}{kwargs.get('ensembl_gene_id', '')}{kwargs.get('ncbi_gene_id', '')}{kwargs.get('symbol', '')}"  # noqa
    elif name == "protein":
        concat_str = kwargs.get("uniprotkb_id", "")
    elif name == "cellmarker":
        concat_str = kwargs.get("name", "")
    elif kwargs.get("id") is not None:
        # species
        concat_str = kwargs.get("id", "")
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
        kwargs["id"] = id_encoder(concat_str)
    return kwargs


def lookup2kwargs(orm: ORM, *args, **kwargs) -> Dict:
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
    return encode_id(orm=orm, kwargs=bionty_kwargs)
