# VulnTriage AI

An AI-powered vulnerability triage and secure code review assistant.
Scans a repository's dependencies against real CVE data and its source
for insecure patterns, then uses an LLM grounded in OWASP and CWE
guidance to explain each finding, assess its severity in context, and
suggest a fix.

Work in progress.

## Planned

- **Kubernetes manifests** — run the full stack on a local cluster via
  `kind`. Managed Kubernetes has no meaningful free tier, so this runs
  locally and the deployed instance stays on Render.
- **Go CLI** — `vulntriage scan ./repo`, a single binary that calls the
  API and exits non-zero when it finds something critical, so it can
  fail a CI build.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the build workflow.
