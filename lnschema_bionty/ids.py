"""IDs.

Entity-related generators:

.. autosummary::
   :toctree: .

   organism
   gene
   protein
   cell_marker
   ontology
   source

"""
import base64
import hashlib
from typing import Optional

from lnschema_core.ids import base62


# same function exists in lamindb
def to_b64_str(bstr: bytes) -> str:
    b64 = base64.urlsafe_b64encode(bstr).decode().strip("=")
    return b64


# very similar function exists in lamindb
def hash_str(s: str) -> str:
    bstr = s.encode("utf-8")
    # as we're truncating at a short length, we choose md5 over sha512
    return to_b64_str(hashlib.md5(bstr).digest())


def hash_id(input_id: Optional[str] = None, *, n_char: int) -> str:
    if input_id is None:
        return base62(n_char=n_char)
    else:
        return hash_str(input_id)[:n_char].replace("_", "0").replace("-", "0")


def gene(input_id: Optional[str] = None) -> str:
    """12 base62."""
    return hash_id(input_id, n_char=12)


def protein(input_id: Optional[str] = None) -> str:
    """12 base62."""
    return hash_id(input_id, n_char=12)


def cellmarker(input_id: Optional[str] = None) -> str:
    """12 base62."""
    return hash_id(input_id, n_char=12)


def ontology(input_id: Optional[str] = None):
    """8 base62."""
    return hash_id(input_id, n_char=8)


def biontysource(input_id: Optional[str] = None):
    """4 base62."""
    return hash_id(input_id, n_char=4)


# backward compat
source = biontysource
organism = ontology
species = organism
