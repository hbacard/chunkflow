# Reproducibility

This document describes how to reproduce the ChunkFlow installation, tests, and
end-to-end pipeline. Everything below was validated on a clean Ubuntu machine.

## Requirements

| Component          | Version / constraint                          |
|--------------------|-----------------------------------------------|
| Python             | `>=3.12,<3.14` (tested on 3.12 and 3.13)      |
| PDM                | any recent release (2.x)                      |
| Docker + Compose   | recent release (for Qdrant / containers)      |
| Qdrant             | `qdrant/qdrant:v1.20.0` (via compose)         |

Dependencies are pinned in the committed lockfiles: `pdm.lock` and `uv.lock`.

## 1. Create the environment

```bash
git clone git@github.com:hbacard/chunkflow.git
cd chunkflow

pdm install -G dev
# or, with uv:  uv sync --extra dev

# Start Qdrant (needed for the ingester integration tests and for ingest/retrieve)
docker compose up -d qdrant
```

Copy and edit the environment template:

```bash
cp .env.example .env
```

## 2. Run the tests

```bash
pdm run python -m pytest
```

- The chunker and embedder tests run without external dependencies.
- Ingester tests **skip** when Qdrant is not reachable at `QDRANT_URL`.

Coverage is reported with `pytest-cov`; the regression floor is configured in
`pyproject.toml` (`[tool.coverage.report]`).

```bash
pdm run ruff check . && pdm run ruff format --check .   # lint as in CI
```

## 3. Run the pipeline end-to-end

```bash
# Stage 1 — chunk a sample directory into records
chunkflow chunk --input samples --output chunks.json --url-mapping url_mapping.json

# Stage 2 — embed child texts (requires an OpenAI-compatible embeddings endpoint
# such as Ollama, configured via EMBEDDING_BASE_URL / EMBEDDING_MODEL)
chunkflow embed --input chunks.json --output embedded_chunks.json

# Stage 3 — ingest into Qdrant (requires Qdrant running)
chunkflow ingest --input embedded_chunks.json
```

Smoke-test the containerized MCP server:

```bash
./scripts/smoke_test.sh
```

## Reproduction checklist

- [ ] Python version within `>=3.12,<3.14`
- [ ] Dependencies from the committed lockfiles (`pdm.lock`)
- [ ] Qdrant running (compose) before ingester tests / ingest
- [ ] Embedding endpoint reachable for Stage 2
- [ ] `pdm run python -m pytest` passes (green CI: see
      [workflow](.github/workflows/ci.yml))

## Known environment notes

- Inside containers, `localhost` refers to the container itself; point
  `EMBEDDING_BASE_URL` at the host (e.g. `http://host.docker.internal:11434`).
- Qdrant data is persisted in the `qdrant_data` volume.

## Data management

When redistributing generated datasets (chunks/embeddings), see
[`DMP.md`](../DMP.md) for provenance and retention guidance.
