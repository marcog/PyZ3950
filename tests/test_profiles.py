from PyZ3950 import profiles


def test_known_profile_keys():
    assert profiles.keys() == ["bnf", "libris", "loc", "sudoc"]


def test_connect_applies_profile_defaults_without_network():
    conn = profiles.connect("loc", connect=False)

    assert conn.host == "lx2.loc.gov"
    assert conn.port == 210
    assert conn.databaseName == "LCDB"
    assert conn.preferredRecordSyntax == "USMARC"
    assert conn.elementSetName == "F"


def test_connect_allows_overrides():
    conn = profiles.connect(
        "bnf",
        connect=False,
        host="example.org",
        port=9999,
        databaseName="CUSTOM",
    )

    assert conn.host == "example.org"
    assert conn.port == 9999
    assert conn.databaseName == "CUSTOM"
    assert conn.preferredRecordSyntax == "UNIMARC"
    assert conn.user == "Z3950"
    assert conn.password == "Z3950_BNF"
