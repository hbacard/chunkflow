# Sustainability plan

This document records how ChunkFlow is maintained and how its long-term
sustainability is handled.

## Maintenance

- **Maintainer(s):** Hugo Bacard (`hbacard@pm.me`).
- **Versioning:** Semantic Versioning; releases are tagged (e.g. `v0.1.0`) and
  tracked in [`CHANGELOG.md`](CHANGELOG.md).
- **Dependency upkeep:** Dependabot opens weekly PRs for Python, Docker, and
  GitHub Actions dependencies (see `.github/dependabot.yml`).
- **Quality gates:** CI runs lint, formatting, and tests with a coverage floor
  on every pull request (see `.github/workflows/ci.yml`).

## Contribution & bus factor

- Contributions are documented in [`CONTRIBUTING.md`](CONTRIBUTING.md) and
  governed by the [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- The project currently has a bus factor of **1 maintainer**. Backup
  maintainership is open for adoption — reach out via the issue tracker.

## Recognition

- Citation and credit are provided via [`CITATION.cff`](CITATION.cff),
  [`codemeta.json`](codemeta.json), and [`AUTHORS`](AUTHORS).
- Run `cffconvert` / pre-commit checks to keep metadata in sync.

## Funding & support

- No external funding is currently attached to this project. Development is
  funded by the maintainers' time and institutional support (IJCLab, IN2P3/CNRS).
