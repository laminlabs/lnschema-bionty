from typing import Optional

import bionty


# https://stackoverflow.com/questions/128573/using-property-on-classmethods/64738850#64738850
class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        """Get."""
        return self.fget(owner_cls)


def fields_from_knowledge(
    locals: dict,
    entity: bionty.Entity,
):
    kwargs = {}
    for k, v in locals.items():
        df = entity.df.reset_index().set_index(k)
        if v not in df.index:
            continue
        kwargs = df.loc[v].to_dict()
        if "ontology_id" in kwargs:
            # TODO: save to Readout.df like others
            if entity.entity == "readout":
                kwargs = entity.get(kwargs["ontology_id"])
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
    Entity = getattr(bionty, name)
    entity = Entity()

    features_entities = ["Gene", "Protein", "CellMarker"]

    @classproperty
    def lookup(cls):
        return entity.lookup

    @classproperty
    def df(cls):
        return entity.df

    @classproperty
    def ontology(cls):
        return entity.ontology

    orig_init = sqlmodel_class.__init__
    orig_new = sqlmodel_class.__new__

    def __init__(
        self,
        database: Optional[str] = None,
        version: Optional[str] = None,
        species: Optional[str] = None,
        knowledge_coupling: Optional[bool] = None,
        **kwargs,
    ):
        orig_init(self, **kwargs)

        if knowledge_coupling is None:
            if name in features_entities:
                knowledge_coupling = False
            else:
                knowledge_coupling = True

        if knowledge_coupling:
            pydantic_attrs = fields_from_knowledge(locals=kwargs, entity=entity)
            set_attributes(self, pydantic_attrs)

    def __new__(
        cls,
        database: Optional[str] = None,
        version: Optional[str] = None,
        species: Optional[str] = None,
        knowledge_coupling: bool = True,
        **kwargs,
    ):
        entity_kwargs = {k: v for k, v in locals().items() if v is not None and k in ["database", "version", "species"]}
        if database is not None or species is not None:
            return Entity(**entity_kwargs)
        else:
            return orig_new(cls)

    def add_attributes(sqlmodel_class):
        sqlmodel_class.lookup = lookup
        sqlmodel_class.df = df
        sqlmodel_class.ontology = ontology
        setattr(sqlmodel_class, "lookup_field", entity.lookup_field)
        setattr(sqlmodel_class, "curate", classmethod(entity.curate))
        setattr(sqlmodel_class, "database", entity.database)
        setattr(sqlmodel_class, "version", entity.version)

    def __call__(cls, knowledge_coupling=True, **kwargs):
        return sqlmodel_class(knowledge_coupling=knowledge_coupling, **kwargs)

    sqlmodel_class.__init__ = __init__
    sqlmodel_class.__new__ = __new__
    if name not in features_entities:
        add_attributes(sqlmodel_class)
    Entity.__call__ = __call__

    return sqlmodel_class
