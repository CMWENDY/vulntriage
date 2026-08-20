# Contributing

This is a solo project, but it follows a normal team workflow on purpose.

## Slices

Work is organised into slices.

A slice is one feature built all the way through, so you can actually use it
when it's finished. The unit of "done" is a working thing, not a finished
component. Not "the database is done" — instead, "you can upload a file and see
real CVEs on a page." That one feature needed a database, backend code, an
endpoint, and a web page, so a bit of each got built.

There are 11 slices, numbered 0 to 10. Each one is a branch and a pull request,
and takes roughly one to two weeks.

Two rules:

- Do not start a slice before the previous one is merged and deployed.
- If a slice is taking too long, cut its scope rather than moving on to the
  next one.

## Branching

`main` is protected. No one pushes to it directly, including me.

All work happens on a feature branch, one branch per slice:

| Branch | Slice |
|---|---|
| `feature/dependency-scanner` | 1 — manifest scanning and first deploy |
| `feature/repo-url-ingestion` | 2 — scanning a repo by URL |
| `feature/static-scanner` | 3 — code pattern rules |
| `feature/sarif-import` | 4 — importing other scanners' results |
| `feature/llm-triage` | 5 — knowledge base and AI triage |
| `feature/local-embeddings` | 6 — local vs hosted embedding comparison |
| `feature/remediation-workflow` | 7 — marking findings fixed, trend chart |
| `feature/jwt-auth` | 8 — accounts and login |
| `feature/hardening` | 9 — tests, Docker, CI |
| `feature/portfolio-polish` | 10 — README and demo |

Branch names use `feature/` followed by a short description with dashes.

To start work:

```bash
git checkout main
git pull
git checkout -b feature/some-name
```

## Commits

Write the message in present tense, and say what changed and why.

Good:

- `Add OSV querybatch client with alias deduplication`
- `Fix OSV ecosystem string casing — "pypi" returned empty results`

Not good:

- `update`
- `fix stuff`

Commit several times inside a slice rather than once at the end. Add specific
files instead of everything:

```bash
git add backend/app/services/osv.py
git commit -m "Add OSV querybatch client"
```

## Pull requests

Every change goes through a pull request, even though I am the only person
working on this.

The PR description should say:

- what changed
- why
- anything I decided along the way, and what I chose instead

Required approvals is set to 0, because I cannot approve my own pull request.
The pull request itself is still required.

## Continuous integration

From Slice 3, GitHub Actions runs the backend tests and the frontend build on
every pull request.

Do not merge a pull request with a failing check. Fix it or close it.

## Secrets

- Never commit `.env`. It is in `.gitignore`.
- `.env.example` lists the variable names with fake values. Update it whenever
  a new variable is added.
- No API keys, passwords, or database URLs in code. Read them from environment
  variables.

If a secret does get committed: rotate the key first, then clean the history.
Deleting the file in a later commit does not remove it from earlier commits.
