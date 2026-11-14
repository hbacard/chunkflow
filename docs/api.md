# ChunkFlow API reference

ChunkFlow is a 3-stage pipeline exposed both as a CLI (`chunkflow`) and as an
MCP server. This document describes the public interface of each stage, the
shared data model, and the MCP tools.

## Installation

```bash
pdm install          # Python >=3.12,<3.14
docker compose up -d # Qdrant on localhost:6333
```

## Environment variables

| Variable             | Default                  | Used by      |
|----------------------|--------------------------|--------------|
| `EMBEDDING_BASE_URL` | `http://localhost:11434` | embed, MCP   |
| `EMBEDDING_MODEL`    | `embeddinggemma-2:440m`  | embed        |
| `EMBEDDING_DIM`      | `768`                    | ingest       |
| `QDRANT_URL`         | `http://localhost:6333`  | ingest, MCP  |
| `COLLECTION_NAME`    | `chunkflow` / `docs_rag` | ingest, MCP  |

## CLI

`chunkflow {chunk|embed|ingest}` — entry point defined in `pyproject.toml`
(`chunkflow.cli:main`).

### `chunkflow chunk`

Stage 1 — split a directory of `.md`/`.pdf` files into parent (section group) +
child (token-windowed chunk) records.

| Argument       | Required | Description                                     |
|----------------|----------|-------------------------------------------------|
| `--input`      | yes      | Directory of `.md`/`.pdf` files                 |
| `--output`     | yes      | Output `chunks.json` path                       |
| `--url-mapping`| no       | JSON file mapping `source_file` → `source_url`  |

```bash
chunkflow chunk --input samples --output chunks.json
```

### `chunkflow embed`

Stage 2 — embed child texts via an OpenAI-compatible `POST /v1/embeddings`.

| Argument   | Required | Description                     |
|------------|----------|---------------------------------|
| `--input`  | yes      | Input `chunks.json` path        |
| `--output` | yes      | Output `embedded_chunks.json`   |

```bash
chunkflow embed --input chunks.json --output embedded_chunks.json
```

### `chunkflow ingest`

Stage 3 — upsert records into Qdrant (parents stored once with zero vectors;
children with dense + sparse BM25 vectors).

| Argument      | Required | Description                      |
|---------------|----------|----------------------------------|
| `--input`     | yes      | Input `embedded_chunks.json`     |
| `--collection`| no       | Qdrant collection name           |
| `--url`       | no       | Qdrant REST URL (default `http://localhost:6333`) |

```bash
chunkflow ingest --input embedded_chunks.json
```

## Data model (`chunkflow.common.records`)

### `Section` (dataclass)

`text: str` · `heading_path: str` (e.g. `"Doc > Installation"`) ·
`page_number: int | None` · `source_file: str` — a contiguous block of document
text under one heading path.

### Records (dicts)

Parent record:

```json
{
  "id": "uuid",
  "text": "merged parent text",
  "chunk_type": "parent",
  "source_file": "doc.md",
  "source_url": null,
  "page_number": null,
  "heading_path": "Doc > Installation",
  "parent_id": null,
  "token_count": 200
}
```

Child record: same shape plus `chunk_type: "child"`, `parent_id` pointing to its
parent's `id`, and a `child_index` within the parent. After Stage 2, embedded
children also carry `dense_vector`.

## Pipeline modules

### `chunkflow.chunker`

- `parse_file(path) -> list[Section]` — parse a `.md`/`.pdf` file into sections.
- `chunk_sections(sections, url_map=None) -> list[dict]` — group sections into
  parent groups (≤ `PARENT_TOKENS`, default 2000) and split text into
  sentence-aligned child chunks (≤ `CHILD_TOKENS`, default 1000).
- `chunker.__main__.run(input_dir, output, url_mapping=None)` — orchestrate
  Stage 1.

### `chunkflow.embedder.embed`

- `make_client() -> httpx.Client` — client for the embeddings endpoint.
- `embed_records(records, client) -> list[dict]` — add `dense_vector` to every
  child record in batches of `BATCH_SIZE` (32).
- `run(input_path, output_path)` — orchestrate Stage 2.

### `chunkflow.ingester.ingest`

- `_ensure_collection(client, collection, dim)` — create the collection (dense
  COSINE vector space + sparse vector space) if missing.
- `_points(records, dim) -> list[PointStruct]` — build Qdrant points; children
  get dense + BM25 sparse vectors, parents get a zero dense vector.
- `ingest(records, client, collection, dim)` / `run(input_path, collection, url)`
  — upsert records.

### `chunkflow.ingester.retrieve`

- `hybrid_query(client, collection, query_text, query_vector, top_k=10,
  prefetch_k=20) -> list[dict]` — RRF-fuse dense and BM25 sparse prefetches over
  child chunks, then fetch and return the parent records.

## MCP server (`mcp/server.py`)

Streamable-HTTP MCP server (default port `8001`, endpoint `/mcp`) exposing two
tools backed by a Qdrant collection:

### `qdrant_store(text, source="", page=None, metadata=None) -> str`

Store a text as a parent/child pair in Qdrant with hybrid vectors; returns the
generated parent/child ids.

### `qdrant_find(query, source=None, limit=5) -> list[dict]`

Hybrid (dense + BM25) retrieval over children; returns the matching parent
records. Optional `source` filters on `source` field.

```bash
docker compose up -d --build   # start Qdrant + MCP server
# Point an MCP client at http://<host>:8001/mcp
```
