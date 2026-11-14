# ChunkFlow — EVERSE Compliance Improvement Milestones

**Source**: `everse-scan-report.md` (scan date 2026-11-13, tier 2 Tool/Library, active dev)
**Branch**: `feat/improve-with-everse`
**Goal**: Close the failing/warning RSQKit indicators, prioritizing effort × impact.

## Decisions (confirmed with maintainer)

| Item | Decision |
|------|----------|
| Canonical license | **Apache-2.0** — LICENSE file already present; update `pyproject.toml` from `CC BY 4.0` to SPDX `Apache-2.0` |
| ORCID | `0000-0001-9216-494X` (Hugo Bacard) — fill into CITATION.cff / codemeta.json / .zenodo.json |
| Optional items | Sphinx/MkDocs site, DMP.md, SUSTAINABILITY.md → included as **optional** milestones, not blocking |

## Status legend

- Effort: **S** small (~1h), **M** medium (~half day), **L** large (~1+ day)
- Impact: 🟢 high, 🟡 medium, 🔴 low

---

## M0 — Consistency & license cleanup (S, 🟢)

Fix small inconsistencies that would conflict with metadata added later.

**Tasks**
- [ ] `pyproject.toml`: change `license = {text = "CC BY 4.0"}` → `license = {text = "Apache-2.0"}` (SPDX)
- [ ] Remove stale `uv.lock` entry from `.gitignore` (`uv.lock` is committed and must stay committed for reproducible installs)
- [ ] Confirm `LICENSE` file is the full Apache-2.0 text and README mentions the license

**Acceptance**
- `grep -c "Apache-2.0" pyproject.toml` and LICENSE file both consistent
- `.gitignore` no longer lists `uv.lock`

**Scan refs**: §3.2 LICENSE ⚠️, §3.13 Reproducible environments · AGENTS.md-progression note: record M0 in `progression.md`

---

## M1 — FAIR metadata: CITATION.cff, codemeta.json, .zenodo.json (M, 🟢)

> Quick wins with the highest impact (Findability dimension is a ❌ today).

**Tasks**
- [ ] Create `CITATION.cff` (`cff-version: 1.2.0`, title "ChunkFlow", version 0.1.0, license Apache-2.0, repository `https://github.com/hbacard/chunkflow`). Authors:
  - Hugo Bacard — `orcid: 0000-0001-9216-494X`, email `hbacard@pm.me` (+ `hugo.bacard@ijclab.in2p3.fr`)
- [ ] Create `codemeta.json` consistent with CITATION.cff + pyproject.toml (name, description, license, author, codeRepository, dateCreated/Modified, programmingLanguage Python, keywords)
- [ ] Create `.zenodo.json` for Zenodo deposition (title, description, upload_type `software`, license `Apache-2.0`, creators with ORCID, keywords)
- [ ] Optional `AUTHORS` file for multi-author credit

**Acceptance**
- `cffconvert` validates `CITATION.cff` with no errors
- `codemeta.json` validates against the codemeta schema (e.g. https://codemeta.github.io or `codemetapy`)
- 3 files above agree on license (Apache-2.0), author, and version

**Scan refs**: §3.3 CITATION.cff ❌, §3.4 codemeta.json ❌, §3.18/3.19 Authorship+ORCID ⚠️, §3.15 Software identifiers ⚠️

---

## M2 — Community & governance files (M, 🟡)

> Documentation of how to contribute, report issues/security, and behave in the project.

**Tasks**
- [ ] `CONTRIBUTING.md` — setup, dev workflow (pdm/uv), test/lint commands, PR process
- [ ] `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1
- [ ] Issue templates: `.github/ISSUE_TEMPLATE/bug_report.yml`, `feature_request.yml`, `config.yml`
- [ ] PR template: `.github/pull_request_template.md`
- [ ] `SECURITY.md` — vulnerability reporting (private channel / maintainer email, response expectations)
- [ ] `CODEOWNERS` — default owners (`@hbacard`), root-level for whole repo

**Acceptance**
- All 6 files present under repo root / `.github/`
- Templates render correctly when opening a new issue/PR

**Scan refs**: §3.25 CONTRIBUTING ⚠️, §3.26 Code of conduct ⚠️, §3.27 Issue templates ⚠️, §3.14 Code review ⚠️ (PR template/CODEOWNERS), §3.12 Security ⚠️

---

## M3 — CI/CD & automated quality gates (L, 🟢)

> The biggest structural gap (CI/CD is ❌). Automates tests, lint, format, coverage, and dependency updates.

**Tasks**
- [ ] Add `pytest-cov` to dev dependency group + coverage config `[tool.coverage.report]` in `pyproject.toml` (fail-below threshold, e.g. 80%)
- [ ] Add `[tool.ruff]` / `[tool.ruff.format]` config (target-version py312, line-length 88) and enforce `ruff format` + `ruff check`
- [ ] Create `.github/workflows/ci.yml` (trigger: push + pull_request, Python 3.12 & 3.13 matrix):
  - `lint` job: `ruff check` + `ruff format --check`
  - `test` job: install via `uv`/pdm from lockfiles, `pytest --cov`, upload coverage artifact
- [ ] Create `.github/dependabot.yml` — ecosystems: pip (pdm/uv lockfiles), docker, github-actions; weekly schedule
- [ ] Add `.editorconfig` (root, consistent indentation/trailing whitespace/end-of-line)
- [ ] Optional: pre-commit config (`pre-commit` with `ruff`, `gitleaks` for secret scanning)

**Acceptance**
- CI workflow is green on a PR for the matrix
- Coverage measured and threshold enforced
- Dependabot opens at least one dependency PR after enabling
- `ruff format --check` and `gitleaks` pass locally

**Scan refs**: §3.9 CI/CD ❌, §3.7 Tests ⚠️ (coverage), §3.17 Readable code ⚠️ (formatter/editorconfig), §3.12 Security ⚠️, §3.20 Dependency management ⚠️

---

## M4 — Releasing & versioning (M, 🟡)

**Tasks**
- [ ] Create `CHANGELOG.md` (Keep a Changelog format) with an `Unreleased` and initial `0.1.0` section summarizing existing milestones
- [ ] Add version tags: annotated `git tag -a v0.1.0`, push tag
- [ ] Add README badges: CI status, license (Apache-2.0), coverage, version — after CI exists (M3)
- [ ] Document the release checklist (what to update: CHANGELOG, tags, image build, Zenodo)

**Acceptance**
- `git tag` shows `v0.1.0`
- README shows live CI badge; CHANGELOG reflects 0.1.0
- Release process repeatable (CHANGELOG → tag → CI → archive)

**Scan refs**: §3.16 Releasing ⚠️, §3.6 Version control ⚠️ (tags), §3.24 Changelog ⚠️

---

## M5 — Documentation & reproducibility (M, 🟡)

**Tasks**
- [ ] Create `docs/api.md` — module/CLI reference (`chunkflow chunk|embed|ingest`) and MCP server tools (hybrid retrieve), documenting inputs/outputs/JSON contract (good docstrings already exist: 82)
- [ ] Create `REPRODUCIBILITY.md` / `CHECKLIST.md` — lockfiles (uv.lock, pdm.lock), `pdm install` / docker-compose steps, env vars (from `env.example`), how to run tests, sample pipeline smoke test
- [ ] Add coverage measurement + coverage badge in README (ties to M3)
- [ ] Optional: lightweight `DMP.md` (data management plan) if pipeline output datasets (chunks/embeddings) are to be shared; otherwise document N/A in REPRODUCIBILITY.md

**Acceptance**
- `docs/api.md` covers every public module + CLI + MCP tools
- A fresh user can reproduce install/test/pipeline end-to-end following REPRODUCIBILITY.md

**Scan refs**: §3.23 API documentation ⚠️, §3.30 Reproducibility checklist ⚠️, §3.8 Documentation ⚠️ (doc-site), §3.29 DMP ⚠️

---

## M6 — Optional / long-term (L, 🟡)

> Non-blocking follow-ups; scheduled after M1–M5 are verified.

- [ ] **Doc site** — Sphinx or MkDocs setup on `docs/` for nicer generated API docs (only if dev-time is available)
- [ ] **SUSTAINABILITY.md** — maintenance commitments, bus factor, funding/recognition plan
- [ ] **Zenodo archiving + DOI badge** — on first release, deposit via `.zenodo.json` (M1); add DOI badge to README (Findability)
- [ ] **Secret-hardening follow-up** — gitleaks pre-commit confirmed, scanned history
- [ ] **Re-run EVERSE scan** at end of M5 to measure dimension improvements (Reproducibility/Maintainability/Findability/Trustworthiness/Reusability)

**Acceptance**
- Re-scan report shows no ❌ and a majority of ✅; README carries DOI badge

**Scan refs**: §3.31 Archiving ⚠️, §3.33 Sustainability ⚠️, §3.8 Docs, §2 Long-Term

---

## Overview — scan item → milestone mapping

| Scan item | Status | Milestone |
|---|---|---|
| LICENSE | ⚠️ (stale: file exists) | M0 (fix pyproject mismatch) |
| CITATION.cff | ❌ | M1 |
| codemeta.json | ❌ | M1 |
| Authorship / ORCID | ⚠️ | M1 |
| Software identifiers | ⚠️ | M1 + M6 (DOI badge) |
| Contribution guidelines / CoC / Issue templates / PR template | ⚠️ | M2 |
| Security (Dependabot, CODEOWNERS, SECURITY.md) | ⚠️ | M2 + M3 |
| CI/CD | ❌ | M3 |
| Tests (coverage) | ⚠️ | M3 |
| Readable code (formatter/.editorconfig) | ⚠️ | M3 |
| Dependency management | ⚠️ | M3 |
| Releasing / Changelog / Tags | ⚠️ | M4 |
| API documentation | ⚠️ | M5 |
| Reproducibility checklist / DMP | ⚠️ | M5 |
| Archiving / Sustainability / Doc site | ⚠️ | M6 (optional) |
| README / Structure / VCS / Packaging / Static analysis / Env / Containerization / Future proofing | ✅ (passed) | — no action (README badges → M4) |

## Suggested execution order

M0 → M1 → M2 → M3 → M4 → M5 → (M6 follow-ups). Milestones are sequential in dependency but M2 files can be created in parallel with M1.
