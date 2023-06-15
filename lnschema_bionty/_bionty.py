from typing import Iterable, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lnschema_core.models import BaseORM

from . import ids


def fields_from_knowledge(
    locals: dict,
    bionty_object: bt.Bionty,
):
    df = bionty_object.df().reset_index()
    bionty_dict = {}
    if len(locals) > 1:
        raise AssertionError("Only 1 kwarg can be passed when populating fields from bionty!")
    elif len(locals) == 1:
        k = next(iter(locals))
        v = locals[k]
        try:
            bionty_dict = df.set_index(k).loc[v].to_dict()
        except KeyError:
            raise ValueError(
                f"No entry is found in bionty reference table with '{k}={v}'!\n Try passing a species other than {bionty_object.species}!"
            )
        bionty_dict[k] = v

    return bionty_dict


def create_or_get_species_record(species: Union[str, BaseORM]) -> Optional[BaseORM]:
    if isinstance(species, BaseORM):
        species_record = species
    elif isinstance(species, str) and species != "all":
        from lnschema_bionty import Species

        try:
            species_record = Species.objects.get(name=species)
        except ObjectDoesNotExist:
            species_record = Species.from_bionty(name=species)
            species_record.bionty_source = get_bionty_source_record(bt.Species())
            species_record.save()
    else:
        species_record = None

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


def get_bionty_object(model: BaseORM, species: Optional[str] = None):
    if model.__module__.startswith("lnschema_bionty."):
        import bionty as bt

        bionty_object = getattr(bt, model.__name__)(species=species)

        return bionty_object


def _add_synonym(synonym: Union[str, Iterable], record: BaseORM):
    """Append new synonym to a synonym field."""
    # nothing happens when passing an empty string
    if isinstance(synonym, str):
        if len(synonym) == 0:
            return
        synonym = [synonym]
    else:
        synonym = list(synonym)

    # because we use | as the separator
    if any(["|" in i for i in synonym]):
        raise AssertionError("A synonym can't contain '|'!")

    # only add if the passed synonym aren't already in synonyms
    synonyms = record.synonyms
    if synonyms is None or len(synonyms) == 0:
        synonyms_set = set()
    else:
        synonyms_set = set(synonyms.split("|"))

    synonyms_set.update(synonym)

    synonyms_updated = "|".join([s for s in synonyms_set])
    if len(synonyms_updated) == 0:
        synonyms_updated = None  # type:ignore
    record.synonyms = synonyms_updated


def bionty_decorator(django_class):
    @classmethod
    def bionty(cls, species: Optional[str] = None):
        """Bionty object of the entity."""
        return get_bionty_object(model=django_class, species=species)

    @classmethod
    def from_bionty(
        cls,
        lookup_result: Optional[tuple] = None,
        species: Union[str, BaseORM, None] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if species is not None:
            species = create_or_get_species_record(species)
        species_name = species.name if species is not None else None
        bionty_object = django_class.bionty(species=species_name)

        if isinstance(lookup_result, tuple) and lookup_result is not None:
            lookup_dict = lookup_result._asdict()  # type:ignore
            bionty_dict = _encode_id(lookup_dict)
        else:
            bionty_dict = fields_from_knowledge(locals=kwargs, bionty_object=bionty_object)
            bionty_dict = _encode_id(bionty_dict)

        if getattr(django_class, "species", False):
            if species is None:
                raise AssertionError("Must specify a species!")
            else:
                bionty_dict["species"] = species
        if getattr(django_class, "bionty_source", False):
            bionty_dict["bionty_source"] = get_bionty_source_record(bionty_object)

        # filter for model fields
        fields = [i.name for i in django_class._meta.fields]
        bionty_dict_fields = {k: v for k, v in bionty_dict.items() if k in fields}

        return django_class(**bionty_dict_fields)

    def _encode_id(kwargs: dict):
        name = django_class.__name__.lower()
        concat_str = ""
        if name == "gene":
            concat_str = "".join(
                [
                    v
                    for k, v in kwargs.items()
                    if k
                    in [
                        "ensembl_gene_id",
                        "ncbi_gene_id",
                        "symbol",
                        "hgnc_id",
                        "mgi_id",
                    ]
                    and v is not None  # noqa
                ]
            )
        elif name == "protein":
            concat_str = "uniprotkb_id"
        elif name == "cellmarker":
            concat_str = "name"
        elif "id" in kwargs:
            # species
            concat_str = kwargs["id"]
        if len(concat_str) > 0:
            try:
                id_encoder = getattr(ids, name)
                kwargs["id"] = id_encoder(concat_str)
            except Exception:
                pass
        return kwargs

    def add_synonym(self, synonym: Union[str, Iterable]):
        _add_synonym(synonym=synonym, record=self)

    django_class.from_bionty = from_bionty
    django_class.bionty = bionty
    django_class.add_synonym = add_synonym

    return django_class
