import sys
from typing import Optional

import bionty as bt

from ..dev import id


# https://stackoverflow.com/questions/128573/using-property-on-classmethods/64738850#64738850
class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        """Get."""
        if "sphinx" not in sys.modules:
            return self.fget(owner_cls)
        else:
            return "sphinx-build: property"


def fields_from_knowledge(
    locals: dict,
    entity: bt.Bionty,
):
    kwargs = {}
    for k, v in locals.items():
        df = entity.df().reset_index().set_index(k)
        if v not in df.index:
            continue
        kwargs = df.loc[v].to_dict()
        kwargs[k] = v
        if "ontology_id" in kwargs:
            kwargs["id"] = kwargs["ontology_id"]
    pydantic_attrs = kwargs
    return pydantic_attrs


def set_attributes(model, pydantic_attrs):
    if len(pydantic_attrs) == 0:
        return

    for k, v in pydantic_attrs.items():
        if k not in model.__fields__:
            continue
        model.__setattr__(k, v)


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
        species: Optional[str] = None,
        **kwargs,
    ):
        """Auto-complete additional fields based on bionty reference."""
        if isinstance(lookup_result, tuple) and lookup_result is not None:
            return sqlmodel_class(lookup_result=lookup_result)
        else:
            entity = sqlmodel_class.bionty() if species is None else sqlmodel_class.bionty(species=species)
            pydantic_attrs = fields_from_knowledge(locals=kwargs, entity=entity)
            if len(pydantic_attrs) == 0:
                raise ValueError(f"No entry is found in bionty reference table with {kwargs}!\nTry passing a species other than '{entity.species}'!")
            pydantic_attrs = _encode_id(pydantic_attrs)
            if "species_id" not in pydantic_attrs and "species" not in pydantic_attrs:
                pydantic_attrs = _add_species(pydantic_attrs, species=species)
            return sqlmodel_class(**pydantic_attrs)

    def _add_species(
        pydantic_attrs: dict,
        species: Optional[str] = None,
    ):
        if "species_id" in sqlmodel_class.__fields__:
            import lamindb as ln

            from .._core import Species

            if species is None:
                # using the default species
                species = sqlmodel_class.bionty().species
            sp = ln.select(Species, name=species).one_or_none()
            if sp is None:
                sp = Species.from_bionty(name=species)
            pydantic_attrs["species"] = sp

        return pydantic_attrs

    def _encode_id(pydantic_attrs: dict):
        if "id" in pydantic_attrs:
            id_encoder = getattr(id, sqlmodel_class.bionty()._entity)
            pydantic_attrs["id"] = id_encoder(pydantic_attrs["id"])
        return pydantic_attrs

    orig_init = sqlmodel_class.__init__

    def __init__(self, lookup_result: Optional[tuple] = None, **kwargs):
        if isinstance(lookup_result, tuple) and lookup_result is not None:
            kwargs = lookup_result._asdict()  # type:ignore
            kwargs = _encode_id(kwargs)
            if "species_id" not in kwargs and "species" not in kwargs:
                kwargs = _add_species(kwargs)

        orig_init(self, **kwargs)

    # def __init__(
    #     self,
    #     database: Optional[str] = None,
    #     version: Optional[str] = None,
    #     species: Optional[str] = None,
    #     knowledge_coupling: Optional[bool] = None,
    #     **kwargs,
    # ):
    #     orig_init(self, **kwargs)

    #     if knowledge_coupling is None:
    #         if name in features_entities:
    #             knowledge_coupling = False
    #         else:
    #             knowledge_coupling = True

    #     if knowledge_coupling:
    #         pydantic_attrs = fields_from_knowledge(locals=kwargs, entity=entity)
    #         set_attributes(self, pydantic_attrs)

    # def __new__(
    #     cls,
    #     database: Optional[str] = None,
    #     version: Optional[str] = None,
    #     species: Optional[str] = None,
    #     knowledge_coupling: bool = True,
    #     **kwargs,
    # ):
    #     entity_kwargs = {
    #         k: v
    #         for k, v in locals().items()
    #         if v is not None and k in ["database", "version", "species"]
    #     }
    #     if database is not None or species is not None:
    #         return Entity(**entity_kwargs)
    #     else:
    #         return orig_new(cls)

    # def __call__(cls, knowledge_coupling=True, **kwargs):
    #     return sqlmodel_class(knowledge_coupling=knowledge_coupling, **kwargs)

    sqlmodel_class.__init__ = __init__
    # sqlmodel_class.__new__ = __new__
    # Entity.__call__ = __call__
    sqlmodel_class.from_bionty = from_bionty
    sqlmodel_class.bionty = bionty

    return sqlmodel_class
