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

## Releasing & archiving

ChunkFlow is archived on [Zenodo](https://zenodo.org/) through the GitHub
integration, which mints a new DOI for each tagged release.

Release / archive checklist:

1. Update [`CHANGELOG.md`](CHANGELOG.md) and the package version
   (`pyproject.toml`, `codemeta.json`, `CITATION.cff`).
2. Tag and push the release (`git tag -a vX.Y.Z`, then push the tag).
3. Publish the GitHub release from the tag; Zenodo automatically archives it
   (the repository must be linked in your Zenodo account → GitHub settings).
4. From the Zenodo record, copy the **new release DOI** and refresh:
   - the DOI badge in [`README.md`](README.md), and
   - the `doi:` field in [`CITATION.cff`](CITATION.cff)
   (currently placeholders — `10.5281/zenodo.XXXXXXX`).

## Environmental impact

ChunkFlow follows energy-conscious practices where practical:

- **Containers run with resource limits** — Qdrant and the MCP server declare
  memory/CPU limits and run with reduced privileges (`cap_drop: ALL`,
  `no-new-privileges`) in `docker-compose.yml`.
- **Efficient CI** — jobs use a concurrency group with `cancel-in-progress`,
  dependency caching (`setup-pdm cache: true`), and per-job timeouts so stale
  or hung runs don't waste compute (`.github/workflows/ci.yml`).
- **Embedding footprint** — the default embedding model
  (`embeddinggemma-2:440m`, int4) is small by design; BM25 sparse vectors are
  computed client-side, avoiding an extra model dependency.
- **Future work** — measure energy use of the embed/ingest steps (e.g.
  CodeCarbon) and report it alongside performance benchmarks.

## Funding & support

- No external funding is currently attached to this project. Development is
  funded by the maintainers' time and institutional support (IJCLab, IN2P3/CNRS).
