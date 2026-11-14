# ChunkFlow

[![CI](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml/badge.svg)](https://github.com/hbacard/chunkflow/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/tag/hbacard/chunkflow)](https://github.com/hbacard/chunkflow/tags)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue.svg)](pyproject.toml)

A 3-stage parent-child chunking pipeline for Markdown/PDF documents, backed by
Qdrant hybrid search.

- **Stage 1 (chunk):** split docs into parent (section) + child (token-windowed chunk) records → `chunks.json`
- **Stage 2 (embed):** embed child texts via an OpenAI-compatible `/v1/embeddings` API → `embedded_chunks.json`
- **Stage 3 (ingest):** upsert records into Qdrant; parents stored once with zero vectors, children with dense + sparse (BM25, computed client-side via fastembed) vectors

Retrieval is hybrid (dense + sparse BM25 with Reciprocal Rank Fusion) over children,
then parents are fetched by ID — see `chunkflow/ingester/retrieve.py`.

## Setup

```bash
pdm install          # Python >=3.12,<3.14
docker compose up -d # Qdrant on localhost:6333
```

This is the local development install (Qdrant in a container, pipeline run with
`pdm`). To run the whole stack — including the MCP server — in containers, see
[Docker](#docker).

## Docker

### Run the full stack

```bash
docker compose up -d --build
```

This starts two services:

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

```bash
cp env.example .env   # then edit as needed
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

## Usage

```bash
chunkflow chunk  --input samples --output chunks.json --url-mapping url_mapping.json
chunkflow embed  --input chunks.json --output embedded_chunks.json
chunkflow ingest --input embedded_chunks.json
```

## Environment variables

| Variable | Default | Used by |
|---|---|---|
| `EMBEDDING_BASE_URL` | `http://localhost:11434` | embed, MCP server |
| `EMBEDDING_MODEL` | `embeddinggemma-2:440m` | embed |
| `EMBEDDING_DIM` | `768` | ingest |
| `QDRANT_URL` | `http://localhost:6333` | ingest, MCP server |
| `COLLECTION_NAME` | `docs_rag` | ingest, MCP server |

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
