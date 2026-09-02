# API Contract

Decided before implementation, 2026-08-25. Every endpoint follows this.

Authentication is added in Slice 8; until then no route requires a token.

## Status codes

| Code | Meaning |
|---|---|
| 200 | Success, response body contains the data |
| 201 | Created |
| 202 | Accepted — work continues in the background, poll for the result |
| 400 | Understood, but not allowed |
| 401 | Not authenticated (Slice 8 onward) |
| 404 | No such resource |
| 422 | Request was the wrong shape |
| 500 | Unexpected server error |
| 502 | An upstream service (OSV.dev, OpenAI) failed |

`422` means the request had the wrong **shape**. `400` means the shape was
right but the content was not allowed.

## Error shape

Every failing response uses exactly this body:

```json
{
  "error_code": "REPO_URL_NOT_ALLOWED",
  "message": "Only github.com and gitlab.com URLs are accepted.",
  "details": {"host": "evil.com"}
}
```

- `error_code` — stable string, uppercase with underscores. Clients branch
  on this. Never renamed once shipped.
- `message` — human-readable sentence, safe to display to a user.
- `details` — object with extra context. `{}` when there is none. Never
  absent.

Errors never contain stack traces, file paths, library versions, SQL, or
environment variables.

### error_code values

| error_code | Status | When |
|---|---|---|
| VALIDATION_ERROR | 422 | Body or path parameter was the wrong shape |
| REPO_NOT_FOUND | 404 | No repository with that id |
| SCAN_NOT_FOUND | 404 | No scan with that id |
| FINDING_NOT_FOUND | 404 | No finding with that id |
| REPO_URL_NOT_ALLOWED | 400 | URL failed the allowlist |
| MANIFEST_NOT_FOUND | 400 | No recognisable manifest in the upload |
| UNSUPPORTED_FILE_TYPE | 400 | Upload was not a manifest or a .zip |
| FILE_TOO_LARGE | 400 | Upload exceeded the size limit |
| INVALID_STATUS | 400 | PATCH status was not one of the allowed values |
| SCAN_IN_PROGRESS | 400 | A scan is already running for this repository |
| UPSTREAM_UNAVAILABLE | 502 | OSV.dev or OpenAI failed |
| INTERNAL_ERROR | 500 | Anything unexpected |

## Enumerated values

Scan status: `running`, `complete`, `failed`
Finding status: `open`, `fixed`, `false_positive`, `accepted_risk`
Severity: `critical`, `high`, `medium`, `low`
Finding type: `dependency`, `code_pattern`

Timestamps are ISO 8601 in UTC: `2026-08-25T14:03:00Z`.

## Endpoints

### POST /repos

Create a repository. Accepts either an uploaded manifest or, from Slice 2,
a URL.

Request:
```json
{"name": "practice-app", "url": "https://github.com/wendy/practice-app"}
```

`201`:
```json
{
  "id": 7,
  "name": "practice-app",
  "source_type": "url",
  "clone_url": "https://github.com/wendy/practice-app",
  "created_at": "2026-08-25T14:01:00Z"
}
```

Errors: `422` VALIDATION_ERROR, `400` REPO_URL_NOT_ALLOWED

### POST /repos/{id}/scan

Start a scan. Returns immediately; the work runs in the background.

`202`:
```json
{"scan_id": 42, "status": "running"}
```

Errors: `404` REPO_NOT_FOUND, `400` SCAN_IN_PROGRESS

### GET /scans/{id}

Scan status. The frontend polls this every 2 seconds while a scan runs.

`200`:
```json
{
  "id": 42,
  "repository_id": 7,
  "status": "running",
  "started_at": "2026-08-25T14:02:11Z",
  "finished_at": null,
  "error_message": null,
  "counts": {"critical": 0, "high": 3, "medium": 1, "low": 0, "total": 4}
}
```

`error_message` is null unless `status` is `failed`.

Errors: `404` SCAN_NOT_FOUND

### GET /scans/{id}/findings

All findings for a scan, sorted by severity descending.

`200`:
```json
{
  "findings": [ ... ],
  "total": 5
}
```

Both finding types share one shape. `type` says which fields are filled in.

Dependency finding:
```json
{
  "id": 103,
  "scan_id": 42,
  "type": "dependency",
  "severity": "high",
  "status": "open",
  "summary": "Insufficiently Protected Credentials in Requests",
  "cve_id": "CVE-2018-18074",
  "cwe_id": "CWE-522",
  "source_tool": "osv",
  "dependency": {
    "name": "requests",
    "version": "2.19.1",
    "ecosystem": "PyPI",
    "fixed_in": "2.20.0"
  },
  "file_path": null,
  "line_number": null,
  "rule_id": null,
  "triage": null
}
```

Code-pattern finding:
```json
{
  "id": 104,
  "scan_id": 42,
  "type": "code_pattern",
  "severity": "high",
  "status": "open",
  "summary": "Password hashed with MD5",
  "cve_id": null,
  "cwe_id": "CWE-916",
  "source_tool": "vulntriage",
  "dependency": null,
  "file_path": "app/auth.py",
  "line_number": 6,
  "rule_id": "weak-password-hash",
  "triage": null
}
```

`triage` is null until Slice 5, then:
```json
{
  "explanation": "...",
  "contextual_severity": "medium",
  "suggested_fix": "...",
  "confidence": 0.8,
  "triaged_at": "2026-08-25T14:03:00Z"
}
```

Errors: `404` SCAN_NOT_FOUND

### PATCH /findings/{id}

Change a finding's status. Slice 7.

Request:
```json
{"status": "fixed", "note": "Upgraded to requests 2.32.4"}
```

`200` returns the updated finding, in the shape above.

Errors: `404` FINDING_NOT_FOUND, `400` INVALID_STATUS

### GET /dashboard/summary

Counts for the dashboard and trend chart. Slice 7.

`200`:
```json
{
  "open_by_severity": {"critical": 0, "high": 3, "medium": 1, "low": 0},
  "total_open": 4,
  "total_fixed": 1,
  "trend": [
    {"date": "2026-08-24", "critical": 0, "high": 4, "medium": 1, "low": 0},
    {"date": "2026-08-25", "critical": 0, "high": 3, "medium": 1, "low": 0}
  ]
}
```

## Not in this version

- Authentication — Slice 8
- Pagination on `/findings` — the envelope leaves room for it
- Filtering and sorting via query parameters — done client-side for now
