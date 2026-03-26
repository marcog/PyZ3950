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
    charset: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
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
        user="Z3950",
        password="Z3950_BNF",
        charset="utf-8",
        notes=(
            "Based on current BnF documentation.",
            "Hostname resolution should be validated in the target deployment environment.",
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
