# Changelog

All notable changes to ChunkFlow are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-11-18

### Added
- `aidecl.yaml` — AI declaration for the OpenCode coding agent.
- Locked dependency files (`pdm.lock`, `uv.lock`) now tracked for reproducible
  installs.

### Changed
- README reframed around three-stage CLI ingestion and agentic RAG via the MCP
  server, deployed as a container alongside Qdrant.
- Email address normalization in `AUTHORS`, `CITATION.cff`, `codemeta.json`.

### Fixed
- Audit findings: retrieval/ID handling, dependency cleanup, and hardening in
  the chunker, embedder, ingester, and MCP server.

## [0.2.0] - 2026-11-15

### Added
- FAIR metadata: `CITATION.cff`, `codemeta.json`, `.zenodo.json`, `AUTHORS`.
- Community & governance files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `CODEOWNERS`, issue templates, PR template.
- CI/CD: GitHub Actions workflow (lint + tests with coverage across Python
  3.12/3.13), Dependabot for dependency updates.
- Quality gates: `pytest-cov` coverage with a regression floor, `ruff` format
  enforcement, `.editorconfig`, optional pre-commit hooks (see
  `.pre-commit-config.yaml`).
- Docs: `docs/api.md` API reference, `REPRODUCIBILITY.md`, `SUSTAINABILITY.md`.

### Changed
- License metadata aligned to Apache-2.0 (SPDX) in `pyproject.toml`; keywords
  and classifiers added.

## [0.1.0] - 2026-11-14

### Added
- 3-stage parent-child chunking pipeline.
  - **Stage 1 (chunk)**: parse Markdown/PDF into sections (`chunker/`) and
    produce parent + child records in `chunks.json`.
  - **Stage 2 (embed)**: embed child texts via an OpenAI-compatible
    `/v1/embeddings` endpoint (`embedder/`).
  - **Stage 3 (ingest)**: upsert records into Qdrant with hybrid dense + BM25
    sparse vectors; parents stored once with zero vectors (`ingester/`).
- CLI entry point `chunkflow {chunk|embed|ingest}`.
- MCP server (`mcp/server.py`) exposing `qdrant_store` and `qdrant_find` tools
  over streamable HTTP.
- Hybrid retrieval with Reciprocal Rank Fusion (`ingester/retrieve.py`).
- Docker support: `Dockerfile`, `docker-compose.yml` (Qdrant + MCP server),
  smoke test script `scripts/smoke_test.sh`.
- Test suite (pytest) covering chunking, embedding and ingestion.

[Unreleased]: https://github.com/hbacard/chunkflow/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/hbacard/chunkflow/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/hbacard/chunkflow/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/hbacard/chunkflow/releases/tag/v0.1.0
