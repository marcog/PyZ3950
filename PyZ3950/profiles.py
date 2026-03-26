"""Named connection profiles for common Z39.50 targets.

These helpers keep catalog-specific host, port, database, syntax, and
authentication defaults in one place while preserving the existing ZOOM API.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional

from PyZ3950 import zoom


@dataclass(frozen=True)
class ConnectionProfile:
    key: str
    name: str
    host: str
    port: int
    database_name: str
    preferred_record_syntax: str = "USMARC"
    element_set_name: str = "F"
    alternate_ports: tuple[int, ...] = field(default_factory=tuple)
    available_record_syntaxes: tuple[str, ...] = field(default_factory=tuple)
    charset: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    attribute_profile: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def option_map(self) -> Dict[str, object]:
        options: Dict[str, object] = {
            "databaseName": self.database_name,
            "preferredRecordSyntax": self.preferred_record_syntax,
            "elementSetName": self.element_set_name,
        }
        if self.charset is not None:
            options["charset"] = self.charset
        if self.user is not None:
            options["user"] = self.user
        if self.password is not None:
            options["password"] = self.password
        return options


PROFILES: Dict[str, ConnectionProfile] = {
    "loc": ConnectionProfile(
        key="loc",
        name="Library of Congress",
        host="lx2.loc.gov",
        port=210,
        database_name="LCDB",
        preferred_record_syntax="USMARC",
        available_record_syntaxes=("USMARC",),
        notes=(
            "Official public Z39.50 target.",
            "Library of Congress moved the backend to FOLIO in July 2025.",
        ),
    ),
    "libris": ConnectionProfile(
        key="libris",
        name="LIBRIS",
        host="z3950.libris.kb.se",
        port=210,
        database_name="libr",
        preferred_record_syntax="USMARC",
        available_record_syntaxes=("USMARC", "SUTRS"),
        charset="latin-1",
        notes=(
            "KB documents Bib-1 / type-1 queries.",
            "MARC21 is exposed through the existing USMARC handling in PyZ3950.",
        ),
    ),
    "sudoc": ConnectionProfile(
        key="sudoc",
        name="Sudoc",
        host="carmin.sudoc.abes.fr",
        port=210,
        database_name="sudoc",
        preferred_record_syntax="UNIMARC",
        available_record_syntaxes=("UNIMARC",),
        notes=(
            "Public host verified reachable from this fork's maintenance environment.",
            "Alternate Sudoc ports 8859 and 10646 likely map to charset-specific services.",
        ),
    ),
    "bnf": ConnectionProfile(
        key="bnf",
        name="BnF Catalogue general",
        host="z3950.bnf.fr",
        port=2211,
        database_name="TOUT-UTF8",
        preferred_record_syntax="UNIMARC",
        available_record_syntaxes=("UNIMARC", "INTERMARC"),
        user="Z3950",
        password="Z3950_BNF",
        charset="utf-8",
        notes=(
            "Based on current BnF documentation.",
            "Hostname resolution should be validated in the target deployment environment.",
        ),
    ),
    "sbn": ConnectionProfile(
        key="sbn",
        name="SBN OPAC",
        host="opac.sbn.it",
        port=2100,
        alternate_ports=(3950,),
        database_name="nopac",
        preferred_record_syntax="UNIMARC",
        available_record_syntaxes=("UNIMARC", "MARC21", "SUTRS"),
        charset="utf-8",
        attribute_profile=(
            "Bib-1 subset includes common use attributes such as personal name, title, ISBN, ISSN, subject, publication date, language, place, abstract, note, author-title, any, doc ID, possessing institution, and country of publication.",
            "Local SBN extensions include 5001/5002 for holdings, 5003/5004 for 4xx/5xx titles, 5008 hierarchical level, 5012 impronta, 5032 author VID, 5125/5128/5129/5139 music presentation and scoring data, 5423 contained work title, 5454 original title, 5801 record production date, 5921/5922/5927/5928/5929/5930 publisher mark and music representation fields, and 6xxx name-role.",
            "Relation attributes: 2, 3, 4. Position attribute: 3. Structure attributes: 1, 2, 4, 6. Truncation attributes: 1, 100. Completeness attribute: 1.",
        ),
        notes=(
            "Public SBN OPAC target verified reachable on ports 2100 and 3950.",
            "Profile details sourced from 'Attributi di Bib1 ed estensioni del profilo SBN - BOZZA'.",
        ),
    ),
}


def keys() -> Iterable[str]:
    return sorted(PROFILES.keys())


def get(name: str) -> ConnectionProfile:
    try:
        return PROFILES[name.lower()]
    except KeyError as exc:
        raise KeyError(
            "Unknown profile %r. Available profiles: %s"
            % (name, ", ".join(keys()))
        ) from exc


def connect(name: str, connect: bool = True, **overrides) -> zoom.Connection:
    profile = get(name)
    options = profile.option_map()
    host = overrides.pop("host", profile.host)
    port = overrides.pop("port", profile.port)
    options.update(overrides)
    return zoom.Connection(host, port, connect=connect, **options)


def describe() -> Mapping[str, ConnectionProfile]:
    return dict(PROFILES)
