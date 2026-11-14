# EVERSE Scan Report

**Repository**: chunkflow
**Date**: 2026-11-13
**Language(s) detected**: Python
**Software tier**: Tool/Library (tier 2)
**Lifecycle stage**: Active dev
**AI Intensity Profile**: Not found

---

## 1. Executive Summary

### Strengths
- **README**: README found: README.md, quality score 4/4
- **Structure**: Well-structured project with src/, tests/, and docs/
- **Version control**: Git repository (19 commits, 2 authors, 0 tags)
- **Tests**: Tests found (3 files, framework: pytest)
- **Documentation**: Good documentation coverage
- **Packaging**: Packaging well configured (pyproject.toml, Dockerfile)
- **Static analysis**: Static analysis tools configured (ruff)
- **Reproducible environments**: Reproducible environment configured (uv.lock, Dockerfile, docker-compose.yml)
- **Containerization**: Container support: Dockerfile, docker-compose
- **Future proofing**: Good future proofing (3/3 indicators)

### Weaknesses
- **LICENSE**: License mentioned in pyproject.toml but no dedicated LICENSE file
- **CITATION.cff**: No CITATION.cff found
- **codemeta.json**: No codemeta.json found
- **CI/CD**: No CI/CD configuration found
- **Security**: No security tools or policies found
- **Code review**: No code review practices found
- **Software identifiers**: No software identifiers (DOI, Zenodo) found
- **Releasing**: No releasing practices found
- **Readable code**: No code formatting configuration found
- **Authorship**: No authorship metadata found (CITATION.cff, codemeta.json, or AUTHORS)
- **ORCID**: No ORCID references found in metadata files
- **Dependency management**: No dependency management tool found (Dependabot, Renovate)
- **API documentation**: No API documentation found (OpenAPI/Swagger or docs/api)
- **Changelog**: No changelog file found
- **Contribution guidelines**: No CONTRIBUTING.md found
- **Code of conduct**: No CODE_OF_CONDUCT.md found
- **Issue templates**: No issue templates found
- **Secret management**: Partial secret management (1 indicator(s))
- **Data management plan**: No data management plan found
- **Reproducibility checklist**: No reproducibility checklist found
- **Archiving**: No software archiving indicators found
- **Software sustainability plan**: No sustainability plan found

### Overall Compliance

| Check | Status |
|-------|--------|
| README | ✅ Pass |
| LICENSE | ⚠️ Warn |
| CITATION.cff | ❌ Fail |
| codemeta.json | ❌ Fail |
| Structure | ✅ Pass |
| Version control | ✅ Pass |
| Tests | ✅ Pass |
| Documentation | ✅ Pass |
| CI/CD | ❌ Fail |
| Packaging | ✅ Pass |
| Static analysis | ✅ Pass |
| Security | ⚠️ Warn |
| Reproducible environments | ✅ Pass |
| Code review | ⚠️ Warn |
| Software identifiers | ⚠️ Warn |
| Releasing | ⚠️ Warn |
| Readable code | ⚠️ Warn |
| Authorship | ⚠️ Warn |
| ORCID | ⚠️ Warn |
| Dependency management | ⚠️ Warn |
| Containerization | ✅ Pass |
| Computational workflows | ⬜ N/A |
| API documentation | ⚠️ Warn |
| Changelog | ⚠️ Warn |
| Contribution guidelines | ⚠️ Warn |
| Code of conduct | ⚠️ Warn |
| Issue templates | ⚠️ Warn |
| Secret management | ⚠️ Warn |
| Data management plan | ⚠️ Warn |
| Reproducibility checklist | ⚠️ Warn |
| Archiving | ⚠️ Warn |
| Future proofing | ✅ Pass |
| Software sustainability plan | ⚠️ Warn |
| Software quality model | ⬜ N/A |

### Quality Dimensions (RSQKit mapping)

> Source: https://everse.software/RSQKit/all_indicators

| Dimension | Score | Checks involved |
|---|---|---|
| Reproducibility | ❌ | Packaging, Tests, CI/CD |
| Maintainability | ⚠️ | Structure, Documentation, Readable code |
| Findability | ❌ | CITATION.cff, codemeta.json, Software identifiers |
| Trustworthiness | ❌ | Tests, CI/CD, Version control, Security |
| Reusability | ⚠️ | LICENSE, README, Documentation |

### Detected Software Tier
**Tier**: Tool/Library (tier 2)
**Justification**: Packaging=yes, 2 author(s), tests=yes, source files=18

### Detected Lifecycle Stage
**Stage**: Active dev
**Justification**: Regular commits (19 in last 3 months, 19 total), active development

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
1. Create a CITATION.cff to enable proper citation of your software (cf. https://everse.software/RSQKit/citing_software) — **impact: high**
1. Create a codemeta.json with software metadata (cf. https://everse.software/RSQKit/complete_software_metadata_codemeta) — **impact: high**

### Medium Term (moderate effort, moderate impact)
1. Add a dedicated LICENSE file at the repository root (cf. https://everse.software/RSQKit/licensing_software)
1. Add Dependabot for dependency vulnerability scanning (cf. https://everse.software/RSQKit/research_software_security)
1. Add a PR template (.github/pull_request_template.md) (cf. https://everse.software/RSQKit/code_review)
1. Add .zenodo.json to control Zenodo deposition metadata (cf. https://everse.software/RSQKit/software_identifiers)
1. Create version tags (git tag v0.1.0) (cf. https://everse.software/RSQKit/releasing_software)

### Long Term (high effort, structural impact)
1. Create a GitHub Actions workflow for automated testing (cf. https://everse.software/RSQKit/ci_cd)

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
- No badges found

**Recommendations**:
- Consider adding badges (CI, license, coverage)

---

### 3.2 LICENSE
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/licensing_software

**Findings**:
- Referenced in: pyproject.toml
- No dedicated LICENSE file at root

**Recommendations**:
- Add a dedicated LICENSE file at the repository root

---

### 3.3 CITATION.cff
**Status**: ❌ Fail
**RSQKit**: https://everse.software/RSQKit/citing_software

**Findings**:
- CITATION.cff not present at repository root

**Recommendations**:
- Create a CITATION.cff to enable proper citation of your software
- Fields can be pre-filled from git log (authors) and README (title)

---

### 3.4 codemeta.json
**Status**: ❌ Fail
**RSQKit**: https://everse.software/RSQKit/complete_software_metadata_codemeta

**Findings**:
- codemeta.json not present at repository root

**Recommendations**:
- Create a codemeta.json with software metadata
- Can be generated from CITATION.cff and packaging files

---

### 3.5 Structure
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_project_structure

**Findings**:
- Top-level directories: .pdm-build, docs, markdowns_support, mcp, samples, scripts, src, tests
- src/ layout: yes
- tests/ directory: yes
- docs/ directory: yes

---

### 3.6 Version control
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/using_version_control

**Findings**:
- Commits: 19
- Authors: 2
- Tags/releases: 0
- .gitignore: present (4/7 common entries)

**Recommendations**:
- Create tags for version releases (git tag v0.1.0)

---

### 3.7 Tests
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/testing_software

**Findings**:
- Test files found: 3
- Test framework: pytest
- Tests directory: yes
- Coverage tool: none

**Recommendations**:
- Add coverage measurement (pytest-cov for Python)

---

### 3.8 Documentation
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- docs/ directory: yes (2 files)
- Doc site configs: none
- Docstrings found: 82
- README: present (3473 chars)

**Recommendations**:
- Set up Sphinx or MkDocs for documentation generation

---

### 3.9 CI/CD
**Status**: ❌ Fail
**RSQKit**: https://everse.software/RSQKit/ci_cd

**Findings**:
- No .github/workflows/, .gitlab-ci.yml, Jenkinsfile, or other CI config found

**Recommendations**:
- Create a GitHub Actions workflow for automated testing

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
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- Secrets found: 0
- Dependabot: no
- CODEOWNERS: no
- Security policy: no

**Recommendations**:
- Add Dependabot for dependency vulnerability scanning
- Add a CODEOWNERS file for review accountability
- Add a SECURITY.md with vulnerability reporting instructions

---

### 3.13 Reproducible environments
**Status**: ✅ Pass
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- Lockfiles: uv.lock
- Container files: Dockerfile, docker-compose.yml
- Nix: no

---

### 3.14 Code review
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/code_review

**Findings**:
- PR template: no
- CODEOWNERS: no
- CONTRIBUTING.md: no
- Issue templates: no

**Recommendations**:
- Add a PR template (.github/pull_request_template.md)
- Add a CODEOWNERS file for review accountability
- Add a CONTRIBUTING.md with contribution guidelines

---

### 3.15 Software identifiers
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_identifiers

**Findings**:
- .zenodo.json: no
- DOI in README: no
- DOI in CITATION.cff: no

**Recommendations**:
- Add .zenodo.json to control Zenodo deposition metadata
- Add a DOI badge to README (from Zenodo after first release)

---

### 3.16 Releasing
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- Git tags: 0 (none)
- Semantic versioning: no
- CHANGELOG: no
- Release template: no

**Recommendations**:
- Create version tags (git tag v0.1.0)
- Add a CHANGELOG.md to track release changes

---

### 3.17 Readable code
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/writing_readable_code

**Findings**:
- Formatters configured: none
- .editorconfig: no

**Recommendations**:
- Configure ruff format or black
- Add an .editorconfig for consistent editor settings

---

### 3.18 Authorship
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/credit_recognition_research_software

**Findings**:

**Recommendations**:
- Add authorship info to CITATION.cff or codemeta.json

---

### 3.19 ORCID
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_metadata

**Findings**:
- ORCID pattern not found in any metadata file

**Recommendations**:
- Add ORCID to CITATION.cff authors or codemeta.json

---

### 3.20 Dependency management
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- No dependabot.yml, renovate.json, or .renovaterc found

**Recommendations**:
- Add Dependabot: .github/dependabot.yml
- Or add Renovate: renovate.json

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
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_documentation

**Findings**:
- No openapi.yaml/json, swagger.yaml/json, or docs/api.md found

**Recommendations**:
- Add API documentation (OpenAPI spec or docs/api.md)

---

### 3.24 Changelog
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/releasing_software

**Findings**:
- No CHANGELOG.md, CHANGES.md, or similar found

**Recommendations**:
- Add a CHANGELOG.md to track version history

---

### 3.25 Contribution guidelines
**Status**: ⚠️ Warn

**Findings**:
- No CONTRIBUTING.md or .github/CONTRIBUTING.md found

**Recommendations**:
- Add CONTRIBUTING.md with guidelines for contributors

---

### 3.26 Code of conduct
**Status**: ⚠️ Warn

**Findings**:
- No CODE_OF_CONDUCT.md found

**Recommendations**:
- Add CODE_OF_CONDUCT.md (see Contributor Covenant)

---

### 3.27 Issue templates
**Status**: ⚠️ Warn

**Findings**:
- No .github/ISSUE_TEMPLATE/ directory or templates

**Recommendations**:
- Add issue templates in .github/ISSUE_TEMPLATE/

---

### 3.28 Secret management
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/research_software_security

**Findings**:
- .env in .gitignore

**Recommendations**:
- Add .env to .gitignore
- Add gitleaks to pre-commit hooks

---

### 3.29 Data management plan
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_management_planning

**Findings**:
- No DMP.md or DATA_MANAGEMENT_PLAN.md found

**Recommendations**:
- Add a data management plan (DMP.md) if your software uses/produces data

---

### 3.30 Reproducibility checklist
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/reproducible_software_environments

**Findings**:
- No REPRODUCIBILITY.md or CHECKLIST.md found

**Recommendations**:
- Add a reproducibility checklist documenting how to reproduce results

---

### 3.31 Archiving
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/archiving_software

**Findings**:
- No .zenodo.json, no Zenodo DOI in README, no Software Heritage reference

**Recommendations**:
- Create .zenodo.json
- Archive on Zenodo after first release

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
**Status**: ⚠️ Warn
**RSQKit**: https://everse.software/RSQKit/software_maintenance

**Findings**:
- No SUSTAINABILITY.md or similar found

**Recommendations**:
- Add a sustainability plan (SUSTAINABILITY.md)

---

### 3.34 Software quality model
**Status**: ⬜ N/A
**RSQKit**: https://everse.software/RSQKit/fair_rs

**Findings**:
- No QUALITY.md or quality model references
