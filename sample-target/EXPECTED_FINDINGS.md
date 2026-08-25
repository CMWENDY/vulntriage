# Expected findings

What OSV.dev returned for the pins in `requirements.txt`.
Used as the fixture for scanner tests.

**Verified: 2026-08-21.** Counts change as new CVEs are published against
old versions. Tests must mock a saved OSV response rather than calling the
live API, or they will break when this number moves.

## Dependency findings

| Package | Version | Raw records | Distinct flaws | Example CVE |
|---|---|---|---|---|
| requests | 2.19.1 | 10 | 5 | CVE-2018-18074 |
| flask | 0.12.2 | 8 | 4 | CVE-2018-1000656  |
| jinja2 | 2.10 | 12 | 6 | CVE-2019-10906 |
| pyyaml | 5.1 | 6 | 3 | CVE-2019-20477|
| itsdangerous | 2.2.0 | 0 | 0 | — |
| markupsafe | 2.1.5 | 0 | 0 | — |
| six | 1.16.0 | 0 | 0 | — |

Raw records are roughly double the distinct flaws, because OSV aggregates
several databases and returns a GHSA record and a PYSEC record for the same
underlying flaw. They cross-reference each other through `aliases`.

### requests 2.19.1, grouped

| CVE (canonical) | Aliased records |
|---|---|
| CVE-2018-18074 | GHSA-x84v-xcm2-53pg, PYSEC-2018-28 |
| CVE-2023-32681 | GHSA-j8r2-6x86-q33q, PYSEC-2023-74 |
| CVE-2024-35195 | GHSA-9wx4-h78v-vm56, PYSEC-2026-1873 |
| CVE-2024-47081 | GHSA-9hjg-9r4m-mvj7, PYSEC-2026-1872 |
| CVE-2026-25645 | GHSA-gc5v-m9x4-r6x2, PYSEC-2026-2275 |

## Code findings

Expected from the static scanner in Slice 3. See the file list in
`sample-target/README.md`.

| File | Pattern | CWE | Should fire? |
|---|---|---|---|
| `app/config.py` | Hardcoded AWS credentials | CWE-798 | yes |
| `app/auth.py` | MD5 on a password | CWE-916 | yes |
| `app/auth.py` | SHA-1 on a token | CWE-327 | yes |
| `app/db.py` | SQL via concatenation | CWE-89 | yes |
| `app/db.py` | SQL via f-string | CWE-89 | yes |
| `app/db.py` | Parameterised query | — | **no** |
| `app/client.py` | `verify=False` | CWE-295 | yes |
| `app/client.py` | Unverified SSL context | CWE-295 | yes |
| `app/tasks.py` | `pickle.loads` | CWE-502 | yes |
| `app/tasks.py` | `eval` | CWE-95 | yes |
| `app/tasks.py` | `exec` | CWE-95 | yes |
| `app/reports.py` | SQL injection across 3 functions | CWE-89 | **no — pattern rules cannot see it** |
| `cache.py` | MD5 for a cache key | — | **no — decoy** |
| `tests/test_helpers.py` | Fake key in a test | — | **no — decoy** |
