from typing import Union

from bionty import Gene, Protein, Species


def populate_columns_from_knowledge(
    locals: dict,
    knowledge_table: Union[Species, Gene, Protein],
    default_factory_col=None,
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
    return locals, kwargs
