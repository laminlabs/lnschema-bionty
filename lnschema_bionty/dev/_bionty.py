from typing import Optional, Union

import bionty as bt
from sqlmodel import SQLModel

from ..dev import id


def fields_from_knowledge(
    locals: dict,
    entity: bt.Bionty,
):
    df = entity.df().reset_index()
    bionty_dict = {}
    if len(locals) > 1:
        raise AssertionError("Only 1 kwarg can be passed when populating fields from bionty!")
    elif len(locals) == 1:
        k = next(iter(locals))
        v = locals[k]
        try:
            bionty_dict = df.set_index(k).loc[v].to_dict()
        except KeyError:
            raise ValueError(f"No entry is found in bionty reference table with '{k}={v}'!\n Try passing a species other than {entity.species}!")
        bionty_dict[k] = v
        if "ontology_id" in bionty_dict:
            bionty_dict["id"] = bionty_dict["ontology_id"]

    return bionty_dict


def create_species_record(species: Union[str, SQLModel]):
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


def knowledge(sqlmodel_class):
    name = sqlmodel_class.__name__
    Entity = getattr(bt, name)

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
            species = create_species_record(species)

        if isinstance(lookup_result, tuple) and lookup_result is not None:
            return sqlmodel_class(lookup_result=lookup_result, species=species)
        else:
            entity = sqlmodel_class.bionty() if species is None else sqlmodel_class.bionty(species=species.name)
            bionty_dict = fields_from_knowledge(locals=kwargs, entity=entity)
            bionty_dict = _encode_id(bionty_dict)

            if "species_id" in sqlmodel_class.__fields__ and species is not None:
                bionty_dict["species"] = species

            return sqlmodel_class(**bionty_dict)

    def _encode_id(pydantic_attrs: dict):
        if "id" in pydantic_attrs:
            id_encoder = getattr(id, sqlmodel_class.bionty()._entity)
            pydantic_attrs["id"] = id_encoder(pydantic_attrs["id"])
        return pydantic_attrs

    orig_init = sqlmodel_class.__init__

    def __init__(self, lookup_result: Optional[tuple] = None, **kwargs):
        if isinstance(lookup_result, tuple) and lookup_result is not None:
            lookup_dict = lookup_result._asdict()  # type:ignore
            lookup_dict = _encode_id(lookup_dict)
            if "species_id" in sqlmodel_class.__fields__:
                if "species" not in kwargs and "species_id" not in kwargs:
                    raise AssertionError("Must specify a species!")
                elif kwargs["species"] is not None:
                    lookup_dict["species"] = create_species_record(kwargs["species"])
            kwargs = lookup_dict

        orig_init(self, **kwargs)

    sqlmodel_class.__init__ = __init__
    sqlmodel_class.from_bionty = from_bionty
    sqlmodel_class.bionty = bionty

    return sqlmodel_class
