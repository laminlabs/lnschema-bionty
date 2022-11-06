from typing import Union

from bionty import Gene, Protein, Species


def fields_from_knowledge(
    locals: dict,
    knowledge_table: Union[Species, Gene, Protein],
    default_factory_col="id",
):
    all_locals = locals.copy()
    if default_factory_col is not None:
        if all_locals.get(default_factory_col) is None:
            locals.pop(default_factory_col)
    kwargs = {}
    for k, v in all_locals.items():
        if v is None or k in {"self", "__class__"}:
            continue
        kwargs = knowledge_table(id=k).df.loc[v]
    init_kwargs = locals
    pydantic_attrs = kwargs
    return init_kwargs, pydantic_attrs


def init_sqlmodel_parent(parent, child, init_kwargs, pydantic_attrs):
    parent.__init__(**init_kwargs)

    if len(pydantic_attrs) == 0:
        return

    for k, v in pydantic_attrs.items():
        if k not in child.__fields__:
            continue
        parent.__setattr__(k, v)
