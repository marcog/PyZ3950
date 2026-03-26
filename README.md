# PyZ3950

## Summary

Pure-python Z39.50 implementation

## Fork Status

This fork is maintained at [marcog/PyZ3950](https://github.com/marcog/PyZ3950).
It is intended to keep PyZ3950 usable on modern Python versions while upstream
maintenance is limited.

Current fork goals:

- keep editable/installable builds working on modern Python
- keep the core ZOOM client usable against still-active Z39.50 targets
- add small, practical helpers for real catalog integrations

Current fork baseline:

- Python `3.10+`
- packaging through `setuptools` and `pyproject.toml`
- focused pytest collection under `tests/`
- provider profile helpers for `LoC`, `LIBRIS`, `Sudoc`, and `BnF`

## Maintainer Notes

This fork deliberately prefers small compatibility changes over deep refactors.
The codebase still contains historical modules, examples, and partially tested
paths. The maintained surface is:

- `PyZ3950.zoom`
- `PyZ3950.ccl`
- `PyZ3950.profiles`
- tests under `tests/`

If upstream becomes active again, changes should be kept easy to cherry-pick.

## Quick Start

```bash
python -m pip install git+https://github.com/marcog/PyZ3950.git
```

```python
from PyZ3950 import profiles
from PyZ3950 import zoom

conn = profiles.connect("loc", connect=False)
conn.connect()
query = zoom.Query("CCL", 'ti="1066 and all that"')
result = conn.search(query)
print(len(result))
conn.close()
```

Available built-in profiles:

- `loc`
- `libris`
- `sudoc`
- `bnf`

## Legacy Notes

This code is updated to support both Python 2.7+ and Python 3.5+ using 2to3
and some hand changes.  The one test I got working in Python 2.7 is updated
to both remain a test script and a "unit test", and that leads to test coverage
of about 40%.

However, only code in PyZ3950 is actually covered by these tests. It should 
be assumed that the code in the example, ill, and other directories
are not working properly, despite the use of 2to3. 

Updating test/test2.py indicates only that the NLM Z39.50 server does
not support concurrent searches.

As such, it is too early to release a new version, but there is enough
here to continue.   In particular, it will be good to see whether we can
utilize the asn1 library and pymarc.

Dan Davis <dan@danizen.net>

## Original README

This code is licensed under the X license.  It requires Dave Beazley's
PLY parsing package from http://systems.cs.uchicago.edu/ply/, licensed
under the LGPL (I've tested with both 1.0 and 1.1), and Python 2.1
(or, in all probability, later versions.)
 
For Z39.50 functionality, you probably just want to use ZOOM, in
zoom.py.  An example is in test/test1.py, which just queries the
Library of Congress for works whose title begins with "1066 and all
that".  The documentation for the language-independent API is available
at http://zoom.z3950.org/api, and I hope that should be sufficient
when combined with the docstrings in zoom.py and the example.  (If
not, please write me.)

The ASN.1 functionality is designed to be usable separately, and
lives entirely in asn1.py.  I probably should split this out into
its own package.

Aaron Lav <asl2@pobox.com>

## License

X Consortium License (Note that since X-Windows is now covered by the MIT License, this may be soon, but I hesitate to change it without the constructive agreement of the author.)





