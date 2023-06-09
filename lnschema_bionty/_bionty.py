from typing import Iterable, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model

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


def create_or_get_species_record(species: Union[str, Model]) -> Optional[Model]:
    if isinstance(species, Model):
        species_record = species
    elif isinstance(species, str) and species != "all":
        from lnschema_bionty import Species

        try:
            species_record = Species.objects.get(name=species)
        except ObjectDoesNotExist:
            species_record = Species.from_bionty(name=species)
            species_record.save()
    else:
        species_record = None

    return species_record


# def link_bionty_version(bionty_object: bt.Bionty):
#     entity = bionty_object.__class__.__name__
#     species = bionty_object.species

#     pass


def get_bionty_object(model: Model, species: Optional[str] = None, **init_kwargs):
    if model.__module__.startswith("lnschema_bionty."):
        import bionty as bt

        bionty_object = getattr(bt, model.__name__)(species=species, **init_kwargs)

        return bionty_object


def _add_synonym(synonym: Union[str, Iterable], record: Model):
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
    def bionty(cls, species: Optional[str] = None, **init_kwargs):
        """Bionty object of the entity."""
        return get_bionty_object(model=django_class, species=species, **init_kwargs)

    @classmethod
    def from_bionty(
        cls,
        lookup_result: Optional[tuple] = None,
        species: Union[str, Model, None] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if species is not None:
            species = create_or_get_species_record(species)
        species_name = species.name if species is not None else None

        if isinstance(lookup_result, tuple) and lookup_result is not None:
            lookup_dict = lookup_result._asdict()  # type:ignore
            bionty_dict = _encode_id(lookup_dict)
        else:
            bionty_object = django_class.bionty(species=species_name)
            bionty_dict = fields_from_knowledge(locals=kwargs, bionty_object=bionty_object)
            bionty_dict = _encode_id(bionty_dict)

        if getattr(django_class, "species", False):
            if species is None:
                raise AssertionError("Must specify a species!")
            else:
                bionty_dict["species"] = species

        # filter for model fields
        fields = [i.name for i in django_class._meta.fields]
        bionty_dict_fields = {k: v for k, v in bionty_dict.items() if k in fields}

        return django_class(**bionty_dict_fields)

    def _encode_id(pydantic_attrs: dict):
        if "id" in pydantic_attrs:
            try:
                id_encoder = getattr(ids, django_class.bionty()._entity)
                pydantic_attrs["id"] = id_encoder(pydantic_attrs["id"])
            except Exception:
                pass
        return pydantic_attrs

    def add_synonym(self, synonym: Union[str, Iterable]):
        _add_synonym(synonym=synonym, record=self)

    django_class.from_bionty = from_bionty
    django_class.bionty = bionty
    django_class.add_synonym = add_synonym

    return django_class
