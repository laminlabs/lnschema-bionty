import pytest

from lnschema_bionty.ids import organism


def test_hash_id():
    assert "vado" == organism("NCBI_10090")
    assert "24Dy" == organism("NCBI_10091")
    with pytest.raises(ValueError):
        organism("test_12893")
