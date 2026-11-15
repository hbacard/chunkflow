# EVERSE Scan Report

- **Repository**: chunkflow
- **Date**: 2026-11-15
- **Language(s) detected**: Python
- **Software tier**: Infrastructure (tier 3)
- **Lifecycle stage**: Active dev
- **AI Intensity Profile**: Not found

---

## 1. Executive Summary

### Strengths
- **README**: README found: README.md, quality score 4/4
- **LICENSE**: License file found: LICENSE (Apache-2.0)
- **CITATION.cff**: CITATION.cff found with all required fields
- **codemeta.json**: codemeta.json valid with all required fields
- **Structure**: Well-structured project with src/, tests/, and docs/
- **Version control**: Git repository with good .gitignore and 1 release(s)
- **Tests**: Tests found (3 files, framework: pytest)
- **Documentation**: Good documentation coverage
- **CI/CD**: CI/CD well configured (GitHub Actions)
- **Packaging**: Packaging well configured (pyproject.toml, Dockerfile)
- **Static analysis**: Static analysis tools configured (ruff)
- **Security**: Good security practices
- **Reproducible environments**: Reproducible environment configured (uv.lock, pdm.lock, Dockerfile, docker-compose.yml)
- **Code review**: Good code review practices
- **Software identifiers**: Software identifiers present
- **Releasing**: Good releasing practices (1 tags, semver, changelog)
- **Readable code**: Code formatting configured (ruff)
- **Authorship**: Authorship information found
- **ORCID**: ORCID references found in: CITATION.cff, codemeta.json, AUTHORS
- **Dependency management**: Dependency management configured: Dependabot
- **Containerization**: Container support: Dockerfile, docker-compose
- **API documentation**: API documentation found: docs/api.md
- **Changelog**: Changelog found: CHANGELOG.md
- **Contribution guidelines**: Contribution guide found: CONTRIBUTING.md
- **Code of conduct**: Code of conduct found: CODE_OF_CONDUCT.md
- **Issue templates**: Issue templates found: 3
- **Secret management**: Good secret management practices (2 indicators)
- **Data management plan**: Data management plan found: DMP.md
- **Reproducibility checklist**: Reproducibility checklist found: REPRODUCIBILITY.md
- **Archiving**: Archiving indicators found: Zenodo, Zenodo DOI in README
- **Future proofing**: Good future proofing (3/3 indicators)
- **Software sustainability plan**: Sustainability plan found: SUSTAINABILITY.md

### Weaknesses
- **Environmental sustainability**: Environmental practices: 1 indicator(s)

### Overall Compliance

| Check | Status |
|-------|--------|
| README | ✅ Pass |
| LICENSE | ✅ Pass |
| CITATION.cff | ✅ Pass |
| codemeta.json | ✅ Pass |
| Structure | ✅ Pass |
| Version control | ✅ Pass |
| Tests | ✅ Pass |
| Documentation | ✅ Pass |
| CI/CD | ✅ Pass |
| Packaging | ✅ Pass |
| Static analysis | ✅ Pass |
| Security | ✅ Pass |
| Reproducible environments | ✅ Pass |
| Code review | ✅ Pass |
| Software identifiers | ✅ Pass |
| Releasing | ✅ Pass |
| Readable code | ✅ Pass |
| Authorship | ✅ Pass |
| ORCID | ✅ Pass |
| Dependency management | ✅ Pass |
| Containerization | ✅ Pass |
| Computational workflows | ⬜ N/A |
| API documentation | ✅ Pass |
| Changelog | ✅ Pass |
| Contribution guidelines | ✅ Pass |
| Code of conduct | ✅ Pass |
| Issue templates | ✅ Pass |
| Secret management | ✅ Pass |
| Data management plan | ✅ Pass |
| Reproducibility checklist | ✅ Pass |
| Archiving | ✅ Pass |
| Future proofing | ✅ Pass |
| Software sustainability plan | ✅ Pass |
| Environmental sustainability | ⚠️ Warn |
| Software peer review | ⬜ N/A |
| Software quality model | ⬜ N/A |

### Quality Dimensions (RSQKit mapping)

> Source: https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks involved |
|---|---|---|
| Reproducibility | ✅ | Packaging, Tests, CI/CD |
| Maintainability | ✅ | Structure, Documentation, Readable code |
| Findability | ✅ | CITATION.cff, codemeta.json, Software identifiers |
| Trustworthiness | ✅ | Tests, CI/CD, Version control, Security |
| Reusability | ✅ | LICENSE, README, Documentation |

### Detected Software Tier
**Tier**: Infrastructure (tier 3)
**Justification**: Multi-package or complex CI, Docker=yes, docs=extensive, contributors=3, releases=1

### Detected Lifecycle Stage
**Stage**: Active dev
**Justification**: Regular commits (23 in last 3 months, 23 total), active development

### Non-evaluated Tasks

> ⚠️ This scan evaluates 36 of the 35+ RSQKit tasks. The following tasks are **not** evaluated:
>
> - [Archiving software](https://everse.software/RSQKit/archiving_software)
> - [Future proofing](https://everse.software/RSQKit/future_proofing)
> - [Performance profiling](https://everse.software/RSQKit/performance_profiling_and_optimization)
> - [Environmental sustainability](https://everse.software/RSQKit/improving_environmental_sustainability)
> - [Computational workflows](https://everse.software/RSQKit/computational_workflows)
> - ... (see [complete list](https://everse.software/RSQKit/tasks))

---

## 2. Prioritized Action Plan

> Prioritization by effort × impact. Impact factors in risk, tier, lifecycle, and target role.

### Critical Risks (address first if detected)
- No critical risks detected

### Quick Wins (low effort, high impact)
1. Improve this check (cf. https://everse.software/RSQKit/improving_environmental_sustainability) — **impact: moderate**

### Medium Term (moderate effort, moderate impact)
- Nothing to report

### Long Term (high effort, structural impact)
- Nothing to report

---

## 3. Technical Details by Task

### 3.1 README
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/creating_good_readme

**Findings**:
- Description present
- Installation instructions present
- Usage examples present
- License mentioned
- Badges present

---

### 3.2 LICENSE
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/licensing_software

**Findings**:
- SPDX identifier: Apache-2.0
- File: LICENSE

---

### 3.3 CITATION.cff
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/citing_software

**Findings**:
- Found fields: title, authors, date-released, version

---

### 3.4 codemeta.json
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/complete_software_metadata_codemeta

**Findings**:
- All required fields present

---

### 3.5 Structure
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_project_structure

**Findings**:
- Top-level directories: .github, .pdm-build, docs, mcp, samples, scripts, src, tests
- src/ layout: yes
- tests/ directory: yes
- docs/ directory: yes

---

### 3.6 Version control
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/using_version_control

**Findings**:
- Commits: 23
- Authors: 3
- Tags/releases: 1
- .gitignore: present (4/7 common entries)

---

### 3.7 Tests
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/testing_software

**Findings**:
- Test files found: 3
- Test framework: pytest
- Tests directory: yes
- Coverage tool: coverage/pytest-cov

---

### 3.8 Documentation
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- docs/ directory: yes (3 files)
- Doc site configs: none
- Docstrings found: 82
- README: present (4438 chars)

**Recommendations**:
- Set up Sphinx or MkDocs for documentation generation

---

### 3.9 CI/CD
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/ci_cd

**Findings**:
- CI system: GitHub Actions
- Test job: yes
- Lint job: yes
- Matrix builds: yes
- Dependabot: yes

---

### 3.10 Packaging
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/packaging_software

**Findings**:
- pyproject.toml: build-system=True, name=True, version=True, scripts=True
- Dockerfile: present

---

### 3.11 Static analysis
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/static_analysis

**Findings**:
- Linting tools configured: ruff

---

### 3.12 Security
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- Secrets found: 0
- Dependabot: yes
- CODEOWNERS: yes
- Security policy: yes

---

### 3.13 Reproducible environments
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- Lockfiles: uv.lock, pdm.lock
- Container files: Dockerfile, docker-compose.yml
- Nix: no

---

### 3.14 Code review
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/code_review

**Findings**:
- PR template: yes
- CODEOWNERS: yes
- CONTRIBUTING.md: yes
- Issue templates: yes

---

### 3.15 Software identifiers
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_identifiers

**Findings**:
- .zenodo.json: yes
- DOI in README: yes
- DOI in CITATION.cff: yes

---

### 3.16 Releasing
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- Git tags: 1 (v0.1.0)
- Semantic versioning: yes
- CHANGELOG: yes
- Release template: no

---

### 3.17 Readable code
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/writing_readable_code

**Findings**:
- Formatters configured: ruff
- .editorconfig: yes

---

### 3.18 Authorship
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/credit_recognition_research_software

**Findings**:
- CITATION.cff found (authors field)
- codemeta.json found (author field)
- AUTHORS file found

---

### 3.19 ORCID
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_metadata

**Findings**:
- ORCID found in CITATION.cff
- ORCID found in codemeta.json
- ORCID found in AUTHORS

---

### 3.20 Dependency management
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- .github/dependabot.yml found

---

### 3.21 Containerization
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/using_containers

**Findings**:
- Dockerfile found at root
- docker-compose file found

---

### 3.22 Computational workflows
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/computational_workflows

**Findings**:
- No .smk, .nf, .cwl, .ga files found

---

### 3.23 API documentation
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- API docs: docs/api.md

---

### 3.24 Changelog
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- File: CHANGELOG.md
- Has entries: True

---

### 3.25 Contribution guidelines
**Status**: ✅ Pass

**Findings**:
- File: CONTRIBUTING.md

---

### 3.26 Code of conduct
**Status**: ✅ Pass

**Findings**:
- File: CODE_OF_CONDUCT.md

---

### 3.27 Issue templates
**Status**: ✅ Pass

**Findings**:
- Templates: config.yml, bug_report.yml, feature_request.yml

---

### 3.28 Secret management
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- .env in .gitignore
- Secret scanning in pre-commit hooks

---

### 3.29 Data management plan
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_management_planning

**Findings**:
- File: DMP.md

---

### 3.30 Reproducibility checklist
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- File: REPRODUCIBILITY.md

---

### 3.31 Archiving
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/archiving_software

**Findings**:
- .zenodo.json found
- Zenodo/DOI reference in README

---

### 3.32 Future proofing
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/future_proofing

**Findings**:
- Lockfiles: uv.lock, pdm.lock
- .gitignore present
- Tests directory present

---

### 3.33 Software sustainability plan
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- File: SUSTAINABILITY.md

---

### 3.34 Environmental sustainability
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/improving_environmental_sustainability

**Findings**:
- CI caching in ci.yml

---

### 3.35 Software peer review
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/publishing_software

**Findings**:
- No JOSS paper, rOpenSci badge, or peer review reference

---

### 3.36 Software quality model
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/fair_rs

**Findings**:
- No QUALITY.md or quality model references

---

## 4. AI Usage Determination

**Profile**: Not found

> No AI intensity profile (`ai-intensity.yaml`) found in this repository.
>
> The RSQKit AI spectrum is a **self-assessment framework** — it cannot be
> determined by scanning repository files. To determine your AI intensity,
> run the **AI Intensity Q&A skill**.
>
> See: https://everse.software/RSQKit/spectrum_of_intensity_of_ai_usage
