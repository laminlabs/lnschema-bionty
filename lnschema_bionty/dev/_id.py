from lnschema_core.dev.id import base62


def featureset() -> str:
    """Data object: 12 base62."""
    return base62(n_char=12)


def gene() -> str:
    """Data object: 6 base62."""
    return base62(n_char=6)


def protein() -> str:
    """Data object: 7 base62."""
    return base62(n_char=7)


def species() -> str:
    """Data object: 3 base62."""
    return base62(n_char=3)


def tissue() -> str:
    """Data object: 5 base62."""
    return base62(n_char=5)


def disease() -> str:
    """Data object: 5 base62."""
    return base62(n_char=5)


def cell_type() -> str:
    """Data object: 5 base62."""
    return base62(n_char=5)


def cell_marker() -> str:
    """Data object: 5 base62."""
    return base62(n_char=5)
