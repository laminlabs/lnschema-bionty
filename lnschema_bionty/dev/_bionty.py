from typing import Iterable, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lnschema_core.models import BaseORM

from ..dev import id


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
        if "ontology_id" in bionty_dict:
            bionty_dict["id"] = bionty_dict["ontology_id"]

    return bionty_dict


def create_species_record(species: Union[str, BaseORM]):
    if isinstance(species, BaseORM):
        species_record = species
    elif isinstance(species, str):
        from lnschema_bionty import Species

        try:
            species_record = Species.objects.get(name="mouse")
        except ObjectDoesNotExist:
            species_record = Species.from_bionty(name=species)
    else:
        raise TypeError("species must be a string or a Species record!")

    return species_record


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


def knowledge(django_class):
    name = django_class.__name__
    bionty_class = getattr(bt, name)

    @classmethod
    def bionty(cls, **init_kwargs):
        """Bionty object of the entity."""
        return bionty_class(**init_kwargs)

    @classmethod
    def from_bionty(
        cls,
        lookup_result: Optional[tuple] = None,
        species: Union[str, BaseORM, None] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if species is not None:
            species = create_species_record(species)
            species_name = species.name
        else:
            species_name = None

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
            id_encoder = getattr(id, django_class.bionty()._entity)
            pydantic_attrs["id"] = id_encoder(pydantic_attrs["id"])
        return pydantic_attrs

    def add_synonym(self, synonym: Union[str, Iterable]):
        _add_synonym(synonym=synonym, record=self)

    django_class.from_bionty = from_bionty
    django_class.bionty = bionty
    django_class.add_synonym = add_synonym

    return django_class


# deprecated
def sqlmodel_knowledge(sqlmodel_class):
    from sqlmodel import SQLModel

    name = sqlmodel_class.__name__
    Entity = getattr(bt, name)

    def create_species_record_(species: Union[str, SQLModel]):
        if isinstance(species, SQLModel):
            species_record = species
        elif isinstance(species, str):
            import lamindb as ln

            from .._core import Species

            species_record = ln.select(Species, name=species).one_or_none()
            if species_record is None:
                species_record = Species.from_bionty(name=species)
        else:
            raise TypeError("species must be a string or a SQLModel record!")

        return species_record

    @classmethod
    def bionty(cls, **init_kwargs):
        """Bionty object of the entity."""
        return Entity(**init_kwargs)

    @classmethod
    def from_bionty(
        cls,
        lookup_result: Optional[tuple] = None,
        species: Union[str, SQLModel, None] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if species is not None:
            species = create_species_record_(species)

        if isinstance(lookup_result, tuple) and lookup_result is not None:
            lookup_dict = lookup_result._asdict()  # type:ignore
            lookup_dict = _encode_id(lookup_dict)
        else:
            entity = sqlmodel_class.bionty() if species is None else sqlmodel_class.bionty(species=species.name)
            bionty_dict = fields_from_knowledge(locals=kwargs, bionty_object=entity)
            bionty_dict = _encode_id(bionty_dict)

        if "species_id" in sqlmodel_class.__fields__:
            if "species" not in kwargs and "species_id" not in kwargs and species is None:
                raise AssertionError("Must specify a species!")
            elif species is not None:
                lookup_dict["species"] = create_species_record_(species)

        return sqlmodel_class(**bionty_dict)

    def _encode_id(pydantic_attrs: dict):
        if "id" in pydantic_attrs:
            id_encoder = getattr(id, sqlmodel_class.bionty()._entity)
            pydantic_attrs["id"] = id_encoder(pydantic_attrs["id"])
        return pydantic_attrs

    def add_synonym(self, synonym: Union[str, Iterable]):
        _add_synonym(synonym=synonym, record=self)

    sqlmodel_class.from_bionty = from_bionty
    sqlmodel_class.bionty = bionty
    sqlmodel_class.add_synonym = add_synonym

    return sqlmodel_class
