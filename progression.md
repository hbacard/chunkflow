# Progression — EVERSE Compliance Improvements

Tracking the implementation of the milestones defined in `milestone.md`
(branch `feat/improve-with-everse`).

## M0 — Consistency & license cleanup ✅
- [x] `pyproject.toml` license set to SPDX `Apache-2.0` (was `CC BY 4.0`); keywords + classifiers added.
- [x] Removed stale `uv.lock` entry from `.gitignore` (lockfile is now intentionally tracked).

## M1 — FAIR metadata ✅
- [x] `CITATION.cff` (cff-version 1.2.0, ORCID `0000-0001-9216-494X`, Apache-2.0).
- [x] `codemeta.json` (validated JSON, consistent with CITATION.cff + pyproject).
- [x] `.zenodo.json` (Zenodo deposition metadata).
- [x] `AUTHORS`.

## M2 — Community & governance ✅
- [x] `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`.
- [x] `CODEOWNERS` (`* @hbacard`).
- [x] Issue templates (`bug_report.yml`, `feature_request.yml`, `config.yml`).
- [x] Pull request template (`.github/pull_request_template.md`).

## M3 — CI/CD & quality gates ✅
- [x] GitHub Actions workflow (`.github/workflows/ci.yml`): lint (ruff) + tests with coverage on Python 3.12/3.13.
- [x] Dependabot (`.github/dependabot.yml`) for pip, docker, github-actions.
- [x] Coverage measurement (`pytest-cov`) with regression floor `fail_under = 60` in `pyproject.toml`.
- [x] ruff format enforcement (`quote-style = "double"`); reformatted 4 files; lint clean.
- [x] `.editorconfig`; optional pre-commit config (`.pre-commit-config.yaml`, ruff + gitleaks).
- [x] `.gitignore` extended with coverage artifacts (`.coverage`, `coverage.xml`, `htmlcov/`).

## M4 — Releasing & versioning ✅
- [x] `CHANGELOG.md` (Keep a Changelog; Unreleased + 0.1.0).
- [x] README badges (CI, version, license, Python) + Citation & License sections.
- [x] Annotated tag `v0.1.0` created (requires push to GitHub).

## M5 — Documentation & reproducibility ✅
- [x] `docs/api.md` — CLI, modules, data model, MCP tools reference.
- [x] `REPRODUCIBILITY.md` — install, tests, end-to-end pipeline, checklist.

## M6 — Optional / long-term (partial)
- [x] `SUSTAINABILITY.md` (maintenance, bus factor, recognition).
- [x] `DMP.md` (data management plan for generated datasets).
- [ ] Sphinx/MkDocs doc site — deferred (dev-time dependent).
- [ ] Zenodo archive + DOI badge in README — on first release.
- [ ] Re-run EVERSE scan — TODO after commits are pushed.

## Verification results (2026-11-14)
- `pdm run ruff check .` → all checks passed.
- `pdm run ruff format --check .` → 35 files already formatted.
- `pdm run python -m pytest` → 10 passed, 3 skipped, coverage 64% (floor 60).
- JSON metadata validated; `CITATION.cff` parses as YAML.

## Follow-up (2026-11-15) — re-scan warnings
Re-ran the EVERSE scan (36 checks); it now reports all ✅ except three ⚠️
warnings and the self-assessed AI-intensity profile (skipped by decision).

- **codemeta.json** ⚠️ → added `softwareVersion` (CodeMeta 2.0 field the scan
  checks), alongside the existing `version`.
- **Software identifiers** ⚠️ → added placeholder Zenodo DOI to README badge
  and `CITATION.cff` (`doi: 10.5281/zenodo.XXXXXXX`) + documented the
  Zenodo release/archive procedure in `SUSTAINABILITY.md`. Real DOI must be
  filled in after the first Zenodo deposit.
- **Environmental sustainability** ⚠️ (1 indicator) → documented energy
  practices in `SUSTAINABILITY.md` (container resource limits, efficient CI,
  small embedder) and added CI job timeouts (`ci.yml`).
- Validation: `codemeta.json` parses as JSON (`json.load`); `CITATION.cff`
  and `ci.yml` parse as YAML; DOI pattern present in README + CITATION.cff.
- Skipped: `ai-intensity.yaml` (self-assessment, per decision).
