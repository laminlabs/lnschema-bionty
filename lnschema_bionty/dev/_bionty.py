from bionty import Entity


# https://stackoverflow.com/questions/128573/using-property-on-classmethods/64738850#64738850
class classproperty(object):
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        """Get."""
        return self.fget(owner_cls)


def fields_from_knowledge(
    locals: dict,
    entity: Entity,
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
                kwargs = entity.get_term(kwargs["ontology_id"])
            kwargs["id"] = kwargs["ontology_id"]
    pydantic_attrs = kwargs
    return pydantic_attrs


def init_sqlmodel_parent(model, pydantic_attrs):
    if len(pydantic_attrs) == 0:
        return

    for k, v in pydantic_attrs.items():
        if k not in model.__fields__:
            continue
        model.__setattr__(k, v)


def knowledge(bioentity: Entity):
    entity = bioentity()

    @classproperty
    def lookup(cls):
        return entity.lookup

    @classproperty
    def df(cls):
        return entity.df

    @classproperty
    def ontology(cls):
        return entity.ontology

    def wrapper(original_class):
        orig_init = original_class.__init__

        def __init__(self, **kwargs):
            pydantic_attrs = fields_from_knowledge(locals=kwargs, entity=entity)

            orig_init(self, **kwargs)

            init_sqlmodel_parent(self, pydantic_attrs)

        original_class.__init__ = __init__
        setattr(original_class, "curate", classmethod(entity.curate))
        original_class.lookup = lookup
        original_class.df = df
        original_class.ontology = ontology
        setattr(original_class, "database", entity.database)
        setattr(original_class, "version", entity.version)
        setattr(original_class, "lookup_field", entity.lookup_field)

        return original_class

    return wrapper
