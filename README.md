# ChunkFlow

A 3-stage parent-child chunking pipeline for Markdown/PDF documents, backed by
Qdrant hybrid search.

- **Stage 1 (chunk):** split docs into parent (section) + child (token-windowed chunk) records → `chunks.json`
- **Stage 2 (embed):** embed child texts via an OpenAI-compatible `/v1/embeddings` API → `embedded_chunks.json`
- **Stage 3 (ingest):** upsert records into Qdrant; parents stored once with zero vectors, children with dense + sparse (BM25) vectors

Retrieval is hybrid (dense + sparse BM25 with Reciprocal Rank Fusion) over children,
then parents are fetched by ID — see `chunkflow/ingester/retrieve.py`.

## Setup

```bash
pdm install          # Python >=3.12
docker compose up -d # Qdrant on localhost:6333
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
| `EMBEDDING_BASE_URL` | `http://localhost:11434` | embed |
| `EMBEDDING_MODEL` | `embeddinggemma-2:440m` | embed |
| `EMBEDDING_DIM` | `768` | ingest |

## Tests

```bash
pdm run python -m pytest
```

Ingester tests skip when Qdrant is not running.

## Docs

- [`_docs/plan.md`](_docs/plan.md) — architecture, JSON contract, retrieval flow
- [`_docs/implementation_milestones.md`](_docs/implementation_milestones.md) — build milestones
- [`samples/installation-guide.md`](samples/installation-guide.md) — sample input
