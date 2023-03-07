from bionty import Entity


def fields_from_knowledge(
    locals: dict,
    knowledge_table: Entity,
):
    kwargs = {}
    for k, v in locals.items():
        df = knowledge_table(id=k).df
        if v not in df.index:
            continue
        kwargs = df.loc[v].to_dict()
        if "ontology_id" in kwargs:
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


def knowledge(knowledge_table: Entity):
    def test(original_class):
        orig_init = original_class.__init__

        def __init__(self, **kwargs):
            pydantic_attrs = fields_from_knowledge(locals=kwargs, knowledge_table=knowledge_table)

            orig_init(self, **kwargs)

            init_sqlmodel_parent(self, pydantic_attrs)

        original_class.__init__ = __init__

        return original_class

    return test
