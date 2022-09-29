from lnschema_core.id import base62


def featureset() -> str:
    """Data object: 12 base62."""
    return base62(n_char=12)


def gene() -> str:
    """Data object: 4 base62.

    Allows >1.5e7 genes.
    """
    return base62(n_char=4)


def protein() -> str:
    """Data object: 5 base62.

    Allows >9.2e8 proteins.
    """
    return base62(n_char=5)


def species() -> str:
    """Data object: 2 base62.

    Allows >3844 species.
    """
    return base62(n_char=2)


def tissue() -> str:
    """Data object: 3 base62.

    Allows >2.4e5 tissues.
    """
    return base62(n_char=3)


def disease() -> str:
    """Data object: 3 base62.

    Allows >2.4e5 diseases.
    """
    return base62(n_char=3)


def cell_type() -> str:
    """Data object: 3 base62.

    Allows >2.4e5 cell types.
    """
    return base62(n_char=3)


def cell_marker() -> str:
    """Data object: 3 base62.

    Allows >2.4e5 cell markers.
    """
    return base62(n_char=3)
