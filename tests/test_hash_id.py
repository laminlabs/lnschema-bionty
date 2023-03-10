import pytest

from lnschema_bionty.dev._id import species


def test_hash_id():
    assert "vado" == species("NCBI_10090")
    assert "24Dy" == species("NCBI_10091")
    with pytest.raises(ValueError):
        species("test_12893")
