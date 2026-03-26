# PyZ3950 Modernization Assessment

Assessment date: 2026-03-26

## Provider status

### Library of Congress

- Status: public Z39.50 target is active.
- Official config:
  - Host: `lx2.loc.gov`
  - Port: `210`
  - Databases: `LCDB`, `LCDB_MARC8`, `NAF`, `SAF`, `NLSBPH`, `NLSBPH_MARC8`
  - Auth: not required
  - Query support: type-1 only, bib-1 only
  - Record syntaxes: MARC 21 and XML
- Notes:
  - LoC states that in July 2025 the backend changed from Voyager to Folio, but connection details did not change and supported attributes were reduced.
  - `PyZ3950` still ships a test against the older hostname `z3950.loc.gov`; for new work it should use the official `lx2.loc.gov` target.
- Sources:
  - https://www.loc.gov/z3950/lcserver.html

### LIBRIS

- Status: public Z39.50 target is active.
- Official config:
  - Host: `z3950.libris.kb.se`
  - Port: `210`
  - Database: `libr` or a library-specific sigel selection database
  - Protocol version: 3
  - Query type: 1 (RPN)
  - Attribute set: Bib-1
  - Record syntaxes: `MARC21`, `SUTRS`
  - Charset: `ISO 8859-1` (Latin-1)
- Notes:
  - KB also publishes SRU and Xsearch endpoints. For modern integrations those should be considered alongside Z39.50.
- Sources:
  - https://www.kb.se/for-bibliotekssektorn/tjanster-och-verktyg/arbeta-med-libris/att-anvanda-librisdata/postoverforing.html

### Sudoc

- Status: public Z39.50 target appears active.
- Verified connectivity:
  - Host: `carmin.sudoc.abes.fr`
  - Open ports observed locally: `210`, `8859`, `10646`
- Notes:
  - ABES still references Z39.50 exports in current documentation, but I have not yet located a current official public page with the full parameter matrix comparable to LoC/LIBRIS/BnF.
  - Likely split is by character set or service profile; this needs confirmation from ABES documentation before hard-coding defaults.
- Sources:
  - https://abes.fr/wp-content/uploads/2021/09/rapport-activites-abes-2020.pdf
  - Local TCP connectivity test on 2026-03-26

### BnF / BN-Opale Plus

- Status: public Z39.50 target is documented as active.
- Official config:
  - Documentation page shows examples using `z3950labs.bnf.fr:2211/TOUT-UTF8`
  - Parameter sheet lists:
    - Server: `z3950.bnf.fr`
    - Port: `2211`
    - User: `Z3950`
    - Password: `Z3950_BNF`
    - Databases: `TOUT`, `TOUT-UTF8`, `TOUT-LATIN1`, `TOUT-ANA1`, `TOUT-ANA1-UTF8`, `TOUT-ANA1-LATIN1`
    - Element set: `F`
  - Formats: `UNIMARC`, `INTERMARC`
- Notes:
  - The 2025 API page is current, but the documented hostnames did not resolve from my environment. This may be DNS, network, or host alias drift, so BnF should be validated with a real query before being treated as production-ready.
  - BnF also offers SRU over HTTP and that may be the safer modern path where Z39.50 is optional.
- Sources:
  - https://api.bnf.fr/fr/serveur-z3950-catalogue-general
  - https://multimedia-ext.bnf.fr/pdf/parametres%20_config_Z3950_bnf.pdf

### British Library

- Status: Z39.50 access appears to exist, but as a managed metadata service rather than an anonymous public target.
- Notes:
  - Current public materials point to metadata services and MARC distribution, but I have not found a current official public page that publishes hostname, port, database name, or credentials.
  - Historical third-party server lists mention British Library Z39.50 targets, but those are not strong enough to build against without BL confirmation.
  - Treat this as "supported after onboarding" rather than "self-serve public endpoint".

### COPAC / Library Hub Discover

- Status: COPAC is historical. Current service is Library Hub Discover.
- Notes:
  - This is not a straight "target profile" problem. It is a service migration problem.
  - Current official Jisc materials describe Library Hub Discover as the active aggregated catalog service.
  - I have not yet obtained current public Z39.50 parameters for Library Hub Discover, and their support pages are protected by Cloudflare, which limited automated inspection.
  - We should assume that a modern client may need SRU/API support here instead of Z39.50, pending confirmation.
- Sources:
  - https://www.jisc.ac.uk/library-hub-discover

### CCUC

- Status: current public Z39.50 availability is unconfirmed.
- Notes:
  - I did not find a current official CSUC page publishing a public CCUC Z39.50 hostname/port/database.
  - The current discovery stack is Alma/Primo-based, which suggests SRU and other modern APIs may be the supported external integration surface.
  - We should not hard-code CCUC as a deliverable target until a current official connection profile is obtained.

## Local codebase findings

### What works today

- The package can now be installed editable under Python 3.13 with a minimal PEP 517 setup.
- The codebase compiles with `python -m compileall PyZ3950`.
- Several target hosts still accept TCP connections from this environment:
  - `lx2.loc.gov:210`
  - `z3950.libris.kb.se:210`
  - `carmin.sudoc.abes.fr:210`
  - `carmin.sudoc.abes.fr:8859`
  - `carmin.sudoc.abes.fr:10646`
- After minimal compatibility fixes, the current focused test run passes on Python 3.13.

### Initial failures observed in a modern Python environment

- Packaging is legacy:
  - `distutils`-based `setup.py`
  - dependencies are not declared in install metadata
  - tox targets Python 2.7 and 3.5 only
- Runtime compatibility is partial:
  - `PyZ3950.ccl` failed on Python 3.13 because inline regex flags such as `(?i)` were embedded in ways now rejected by `re`
  - `string.atoi` is still present
- Test suite quality is low for modern work:
  - examples are collected as tests
  - one network test still uses outdated LoC details
  - there is no stable provider test matrix

### Local proof-of-life changes already applied

- Added `pyproject.toml` so editable install works in a modern toolchain.
- Switched `setup.py` from `distutils` imports to `setuptools`.
- Declared runtime dependencies in package metadata.
- Restricted pytest collection to `tests/` so example scripts are not treated as unit tests.
- Fixed Python 3.13 regex incompatibilities in `PyZ3950.ccl`.
- Replaced the `string.atoi` usage reached during the CCL code path.

## Recommended modernization plan

1. Packaging baseline
   - Replace `distutils` with `setuptools`.
   - Add a `pyproject.toml`.
   - Declare runtime dependencies (`ply`, `pyasn1`) and test dependencies explicitly.
   - Add Python support metadata and CI for 3.10 to 3.13.

2. Compatibility pass
   - Remove remaining Python 2 compatibility shims.
   - Fix regex/parser code for modern `re`.
   - Replace `string.atoi` and similar leftovers.
   - Audit bytes/str boundaries in MARC, ASN.1, and socket paths.

3. Test strategy
   - Separate unit tests from examples.
   - Mark live-network tests as optional and provider-scoped.
   - Update LoC tests to the current official target.
   - Add smoke tests for import, query construction, and record parsing without network.

4. Provider abstraction
   - Add named connection profiles for confirmed targets:
     - LoC
     - LIBRIS
     - Sudoc
     - BnF
   - Model authenticated or uncertain targets separately:
     - British Library
     - CCUC
     - Library Hub Discover

5. Protocol surface decision
   - Keep Z39.50 support for the targets that clearly still use it.
   - Add SRU support or a parallel adapter layer for providers where Z39.50 is unclear, deprecated, or gated.
   - Do not force all targets through one protocol if the catalogs have already moved on.

## Proposed execution order

1. Stabilize package install and import on Python 3.13.
2. Get one real query working against LoC using the official `lx2.loc.gov` endpoint.
3. Add provider profiles and smoke tests for LIBRIS and Sudoc.
4. Validate BnF with a real search or fall back to SRU if Z39.50 remains unstable.
5. Resolve access strategy for British Library, CCUC, and Library Hub Discover before promising them as supported targets.
