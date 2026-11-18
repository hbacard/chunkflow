# ChunkFlow

[![CI](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml/badge.svg)](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/tag/hbacard/chunkflow)](https://github.com/hbacard/chunkflow/tags)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](pyproject.toml)
<!-- TODO: replace XXXXXXX with the real Zenodo DOI after the first release
     is deposited (see SUSTAINABILITY.md → Releasing & archiving). -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

A 3-stage parent-child chunking pipeline for Markdown/PDF documents, backed by
Qdrant hybrid search.

- **Stage 1 (chunk):** split docs into parent (section) + child (token-windowed chunk) records → `chunks.json`
- **Stage 2 (embed):** embed child texts via an OpenAI-compatible `/v1/embeddings` API → `embedded_chunks.json`
- **Stage 3 (ingest):** upsert records into Qdrant; parents stored once with zero vectors, children with dense + sparse (BM25, computed client-side via fastembed) vectors

Retrieval is hybrid (dense + sparse BM25 with Reciprocal Rank Fusion) over children,
then parents are fetched by ID — see `chunkflow/ingester/retrieve.py`.

## Requirements

- **Python** >=3.12,<3.14 with [PDM](https://pdm-project.org/)
- **Docker + Docker Compose** — to run Qdrant
- (Stage 2 only) an OpenAI-compatible embeddings endpoint (e.g. Ollama) reachable
  at `EMBEDDING_BASE_URL`

## Install & start the database

Qdrant is the only external dependency and is shared by **both** the CLI and the
MCP server.

```bash
pdm install                  # Python >=3.12,<3.14
docker compose up -d qdrant  # Qdrant on localhost:6333
```

No `.env` is required — Compose falls back to the defaults in
[Environment variables](#environment-variables). Copy `env.example` to `.env`
only to override them.

## Use via the CLI

The pipeline runs locally with PDM and talks to the Qdrant container above:

```bash
chunkflow chunk  --input samples --output chunks.json --url-mapping url_mapping.json
chunkflow embed  --input chunks.json --output embedded_chunks.json
chunkflow ingest --input embedded_chunks.json
```

## Use via the MCP server (optional, Docker)

The MCP server runs in containers on top of Qdrant. One Compose command brings
up **both** services:

```bash
docker compose up -d --build
```

| Service  | Image / build          | Ports                              | Notes                                  |
|----------|------------------------|------------------------------------|----------------------------------------|
| `qdrant` | `qdrant/qdrant:v1.20.0` | REST `6333`, gRPC `6334`           | Data persisted in the `qdrant_data` volume |
| `ragmcp` | local `Dockerfile`     | streamable HTTP `8001`             | MCP server, waits for Qdrant to be healthy |

Ports are exposed on all interfaces so the stack can be reached over the LAN.
Both services run with resource limits and reduced privileges (`cap_drop: ALL`,
`no-new-privileges`).

### Connect to the MCP server

The MCP server speaks **streamable HTTP** — point your MCP client at
`http://<host>:8001/mcp`.

### Environment

Defaults are baked in; use a `.env` file only to override them:

```bash
cp env.example .env   # optional, then edit as needed
```

Within the compose stack:

- `QDRANT_URL` is set automatically to `http://qdrant:6333` (Docker service-name
  resolution), so the MCP server reaches the Qdrant container.
- `EMBEDDING_BASE_URL` must reach your host's Ollama. Inside a container
  `localhost` points to the container itself, so use
  `http://host.docker.internal:11434` — the compose file maps
  `host.docker.internal` to the host.

### Smoke test

```bash
./scripts/smoke_test.sh
```

Builds the image, runs it on a free port, and verifies the MCP `initialize`
handshake.

### Build the image on its own

```bash
docker build -t chunkflow .
```

## Environment variables

All variables have sensible defaults and can be overridden via environment
variables or an optional `.env` file (see [Install & start the database](#install--start-the-database)).

| Variable | Default | Used by |
|---|---|---|
| `EMBEDDING_BASE_URL` | `http://localhost:11434` | embed, MCP server |
| `EMBEDDING_MODEL` | `embeddinggemma-2:440m` | embed |
| `EMBEDDING_DIM` | `768` | ingest |
| `QDRANT_URL` | `http://localhost:6333` | ingest, MCP server |
| `COLLECTION_NAME` | `docs_rag` | ingest, MCP server |

> Inside the compose stack, `EMBEDDING_BASE_URL` defaults to
> `http://host.docker.internal:11434` (to reach your host's Ollama from a
> container) and `QDRANT_URL` to `http://qdrant:6333` (Docker service-name
> resolution) — see [Use via the MCP server](#use-via-the-mcp-server-optional-docker).

## Tests

```bash
pdm run python -m pytest
```

Ingester tests skip when Qdrant is not running.

## Docs

- [`docs/plan.md`](docs/plan.md) — architecture, JSON contract, retrieval flow
- [`docs/implementation_milestones.md`](docs/implementation_milestones.md) — build milestones
- [`docs/api.md`](docs/api.md) — API reference (CLI, modules, MCP tools)
- [`samples/installation-guide.md`](samples/installation-guide.md) — sample input

## Citation

If you use ChunkFlow in your research, please cite it (see
[`CITATION.cff`](CITATION.cff)).

## License

Distributed under the Apache License, Version 2.0. See [`LICENSE`](LICENSE).
