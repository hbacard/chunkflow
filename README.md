# ChunkFlow

[![CI](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml/badge.svg)](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/tag/hbacard/chunkflow)](https://github.com/hbacard/chunkflow/tags)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](pyproject.toml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24350590.svg)](https://doi.org/10.5281/zenodo.24350590)

A 3-stage parent-child chunking pipeline for Markdown/PDF documents, backed by
Qdrant hybrid search.

- **Stage 1 (chunk):** split docs into parent (section) + child (token-windowed chunk) records → `chunks.json`
- **Stage 2 (embed):** embed child texts via an OpenAI-compatible `/v1/embeddings` API → `embedded_chunks.json`
- **Stage 3 (ingest):** upsert records into Qdrant; parents stored once with zero vectors, children with dense + sparse (BM25, computed client-side via fastembed) vectors

Retrieval is hybrid (dense + sparse BM25 with Reciprocal Rank Fusion) over children,
then parents are fetched by ID — see `chunkflow/ingester/retrieve.py`.

ChunkFlow can then be used in two ways, both backed by the same Qdrant
collection:

- **Ingest documents (CLI):** run the 3-stage pipeline to chunk, embed, and
  upsert documents into the collection.
- **Agentic RAG (MCP server):** a second container deployed alongside Qdrant in
  the same compose stack, exposing MCP tools that let AI agents retrieve and
  store documents in that same collection.

## Requirements

- **Python** >=3.12,<3.14 with [PDM](https://pdm-project.org/)
- **Docker + Docker Compose** — to run Qdrant
- (Stage 2 only) an OpenAI-compatible embeddings endpoint (e.g. Ollama) reachable
  at `EMBEDDING_BASE_URL`

## Install & start the database

Qdrant is the only external dependency and is shared by **both** the ingestion
CLI and the MCP server.

```bash
pdm install                  # Python >=3.12,<3.14
docker compose up -d qdrant  # Qdrant on localhost:6333
```

No `.env` is required — Compose falls back to the defaults in
[Environment variables](#environment-variables). Copy `.env.example` to `.env`
only to override them.

## Ingest documents via the CLI (3 stages)

The pipeline runs locally with PDM and ingests documents into the shared Qdrant
collection in three stages:

```bash
chunkflow chunk  --input samples --output chunks.json --url-mapping url_mapping.json
chunkflow embed  --input chunks.json --output embedded_chunks.json
chunkflow ingest --input embedded_chunks.json
```

Everything ingested here lands in the same collection the MCP server reads, so
it is immediately retrievable by agents — see
[Agentic RAG: MCP server alongside Qdrant](#agentic-rag-mcp-server-alongside-qdrant-docker).

## Agentic RAG: MCP server alongside Qdrant (Docker)

The MCP server turns the shared Qdrant collection into an agentic RAG backend.
Compose starts a second container, `ragmcp`, alongside the Qdrant container in
the same stack — both services share the same database the CLI pipeline
ingested into. The server exposes MCP tools — currently `qdrant_find` (hybrid
dense + BM25 retrieval) and `qdrant_store` (store text as a parent/child pair) —
so an MCP client / AI agent can retrieve and store documents at runtime; see
[`docs/api.md`](docs/api.md) for the full tool list. One Compose command brings
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
cp .env.example .env   # optional, then edit as needed
```

Within the compose stack:

- `QDRANT_URL` is set automatically to `http://qdrant:6333` (Docker service-name
  resolution), so the MCP server reaches the Qdrant container.
- `EMBEDDING_BASE_URL` reaches your host's Ollama by default: the host CLI
  defaults to `http://localhost:11434`, while Compose defaults the container to
  `http://host.docker.internal:11434` (mapped to the host via `extra_hosts`),
  because inside a container `localhost` is the container itself.
- If you set `EMBEDDING_BASE_URL` in `.env` (or the shell) to any **other** URL —
  a remote embeddings API, your LAN IP — Compose passes it to the container
  unchanged, so the CLI and the MCP server share the same endpoint. Just never
  put `localhost` in `.env`: the container would inherit it and lose Ollama.
  See [`.env.example`](.env.example) for the full rule.

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
| `EMBEDDING_BASE_URL` | host: `http://localhost:11434` · container: `http://host.docker.internal:11434` | embed, MCP server |
| `EMBEDDING_MODEL` | `embeddinggemma-2:440m` | embed |
| `EMBEDDING_DIM` | `768` | ingest |
| `QDRANT_URL` | `http://localhost:6333` | ingest, MCP server |
| `COLLECTION_NAME` | `docs_rag` | ingest, MCP server |

> Inside the compose stack, `EMBEDDING_BASE_URL` defaults to
> `http://host.docker.internal:11434` (to reach your host's Ollama from a
> container) and `QDRANT_URL` to `http://qdrant:6333` (Docker service-name
> resolution) — see [Agentic RAG: MCP server alongside Qdrant](#agentic-rag-mcp-server-alongside-qdrant-docker).
> Any value set in `.env`/shell overrides both sides uniformly — see
> [`.env.example`](.env.example).

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
