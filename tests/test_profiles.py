from PyZ3950 import profiles


def test_known_profile_keys():
    assert profiles.keys() == ["bnf", "libris", "loc", "sbn", "sudoc"]


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


def test_sbn_profile_defaults():
    conn = profiles.connect("sbn", connect=False)
    profile = profiles.get("sbn")

    assert conn.host == "opac.sbn.it"
    assert conn.port == 2100
    assert conn.databaseName == "nopac"
    assert conn.preferredRecordSyntax == "UNIMARC"
    assert conn.charset == "utf-8"
    assert profile.alternate_ports == (3950,)
    assert profile.available_record_syntaxes == ("UNIMARC", "MARC21", "SUTRS")
    assert len(profile.attribute_profile) == 3
