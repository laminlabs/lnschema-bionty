from bionty import EntityTable


def fields_from_knowledge(
    locals: dict,
    knowledge_table: EntityTable,
    default_factory_col="id",
):
    all_locals = locals.copy()
    if (default_factory_col is not None) and (default_factory_col in locals):
        locals.pop(default_factory_col)
    kwargs = {}
    for k, v in all_locals.items():
        df = knowledge_table(id=k).df
        if v not in df.index:
            continue
        kwargs = df.loc[v].to_dict()
    pydantic_attrs = kwargs
    return pydantic_attrs


def init_sqlmodel_parent(model, pydantic_attrs):
    if len(pydantic_attrs) == 0:
        return

    for k, v in pydantic_attrs.items():
        if k not in model.__fields__:
            continue
        model.__setattr__(k, v)


def knowledge(knowledge_table: EntityTable):
    def test(original_class):
        orig_init = original_class.__init__

        def __init__(self, **kwargs):
            pydantic_attrs = fields_from_knowledge(locals=kwargs, knowledge_table=knowledge_table)

            orig_init(self, **kwargs)

            init_sqlmodel_parent(self, pydantic_attrs)

        original_class.__init__ = __init__

        return original_class

    return test
