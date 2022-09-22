from lnschema_core.id import base62


def gene() -> str:
    """Data object: 4 base62.

    Allows >1.5e7 genes.
    """
    return base62(n_char=4)
