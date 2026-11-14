# Chunkflow — Plan

## Overview

A 3-stage pipeline that creates a parent-child hierarchy from Markdown and PDF documents. Parents are document sections (defined by headings); children are overlapping token-windowed chunks within each section. Only children are embedded for vector search — using **hybrid search** (dense + sparse/BM25 with Reciprocal Rank Fusion). Parents are stored as separate points in the same Qdrant collection with zero vectors — deduplicating parent text across children and keeping retrieval to a fast O(1) ID lookup.

Each stage is independently runnable, testable, and re-runnable. The contract between stages is a JSON file.

## Architecture

```
Document (MD/PDF)
  └── Section (PARENT) — identified by headings
        ├── Child chunk 1 (≤1024 tokens, 10-15% overlap)
        ├── Child chunk 2
        └── Child chunk N

Qdrant Collection (two point types, named vectors)
  ├── Parent points (zero "dense" vector, payload has full section text)
  └── Child points  ("dense" embedding + "sparse" BM25, payload references parent_id)
```

## Stack

| Component | Choice |
|---|---|
| Language | Python >=3.12,<3.14 |
| PDF parsing | pymupdf (fitz) — font size heuristics for heading detection |
| MD parsing | `markdown-it-py` for heading hierarchy |
| Chunking | Custom Python, no framework |
| Embedding model | OpenAI-compatible API (e.g. Ollama `embeddinggemma-2:440m` via `/v1/embeddings`) |
| Sparse vectors | Client-side BM25 via fastembed `SparseTextEmbedding("Qdrant/bm25")` → `SparseVector` |
| Vector DB | Qdrant — single collection, named vectors ("dense" + "sparse"), hybrid search with RRF |
| Qdrant client | `AsyncQdrantClient` (async throughout) |
| Qdrant deployment | Docker container with persisted volume (`docker-compose.yml`) |
| URL mapping | `a path to a file will be given ` |

## Repository Structure

```
chunkflow/
├── src/
│   ├── chunker/        # parse.py + chunk.py → outputs chunks.json
│   ├── embedder/       # embed.py → outputs embedded_chunks.json
│   ├── ingester/       # ingest.py (AsyncQdrantClient, Qdrant-specific)
│   └── common/         # shared dataclasses (Section, ChildChunk, schemas)
├── _docs/
│   ├── plan.md
│   └── url_mapping.json
├── docker-compose.yml  # Qdrant service with persisted volume
├── pyproject.toml
└── README.md
```

## CLI

```bash
chunkflow chunk   --input path/to/files --output chunks.json --url-mapping path/to/url_mapping_file.json
chunkflow embed   --input chunks.json --output embedded_chunks.json
chunkflow ingest  --input embedded_chunks.json
```

## 3-Stage Pipeline

### Stage 1: Chunk (`chunker/`)

**Input:** directory of MD/PDF files + optional `--url-mapping` JSON file
**Output:** `chunks.json`

Modules:
- `parse.py` — MD: `markdown-it-py` to walk tokens, detect `heading_open`, build heading hierarchy. Text between headings becomes a section's `parent_text`. PDF: `pymupdf` (`fitz`) to extract text blocks with font metadata. Classify blocks as headings/body based on font size relative to document median. Largest fonts → H1, next → H2, etc. Both parsers output a uniform `Section` dataclass: `(parent_text, heading_path, page_number, source_file)`.
- `chunk.py` — Takes a `Section`, splits `parent_text` into child chunks of ≤1024 tokens with 10-15% overlap (sliding window). Token counting via `tiktoken`. Outputs both parent and child records: parents carry the full section text, children carry only their own chunk text + `parent_id` reference. If `--url-mapping` is provided, loads the JSON and attaches `source_url` to each record based on `source_file`. Files not in the mapping get `source_url: null`.

No dependency on Qdrant or embedding model.

### Stage 2: Embed (`embedder/`)

**Input:** `chunks.json`
**Output:** `embedded_chunks.json`

- Sends **child texts only** in batches to an OpenAI-compatible `/v1/embeddings` endpoint (e.g. Ollama serving `embeddinggemma-2:440m`).
- Parent records pass through unchanged (no embedding).
- Configurable via env vars: `EMBEDDING_BASE_URL`, `EMBEDDING_MODEL`.
- Returns the same JSON with an added `dense_vector` field per child chunk.

No dependency on Qdrant or document parsing.

### Stage 3: Ingest (`ingester/`)

**Input:** `embedded_chunks.json`
**Output:** Qdrant collection

- Uses `AsyncQdrantClient` for all operations:
  ```python
  from qdrant_client import AsyncQdrantClient, models

  client = AsyncQdrantClient(url="http://localhost:6333")
  ```
- Creates collection with named vectors if it doesn't exist:
  ```python
  await client.create_collection(
      "chunkflow",
      vectors_config={
          "dense": models.VectorParams(size=DIM, distance=models.Distance.COSINE)
      },
      sparse_vectors_config={"sparse": models.SparseVectorParams()},
  )
  ```
- Builds two types of `PointStruct` with named vectors:
  - **Parent points**: `vector={"dense": [0.0, ...]}` (zero vector, same dims), `chunk_type="parent"`, payload includes full section text. No sparse vector — parents are never searched.
  - **Child points**: `vector={"dense": [embedding], "sparse": SparseVector(indices, values)}` (BM25 computed client-side via fastembed), `chunk_type="child"`, payload includes chunk text + `parent_id` reference.
- `source_url` already present in `embedded_chunks.json` (injected at stage 1) — passed through to payload as-is.
- Upserts all points to a single Qdrant collection via `await client.upsert(...)`.

Only stage that depends on Qdrant. Swappable without touching stages 1-2.

## JSON Contract Between Stages

### `chunks.json` (stage 1 → 2)

Contains both parent and child records:

```json
[
  {
    "id": "parent-uuid",
    "text": "full parent section text...",
    "chunk_type": "parent",
    "source_file": "doc.md",
    "source_url": "https://example.com/docs/install",
    "page_number": null,
    "heading_path": "Doc > Installation",
    "parent_id": null,
    "token_count": 3800
  },
  {
    "id": "child-uuid",
    "text": "child chunk text...",
    "chunk_type": "child",
    "source_file": "doc.md",
    "source_url": "https://example.com/docs/install",
    "page_number": null,
    "heading_path": "Doc > Installation",
    "parent_id": "parent-uuid",
    "child_index": 0,
    "token_count": 980
  }
]
```

### `embedded_chunks.json` (stage 2 → 3)

Same as above, but child records have an added `dense_vector` field. Parent records pass through unchanged. (Sparse/BM25 vector is computed client-side via fastembed at ingest time, not stored in the JSON contract.)

```json
[
  {
    "id": "parent-uuid",
    "text": "full parent section text...",
    "chunk_type": "parent",
    "source_file": "doc.md",
    "source_url": "https://example.com/docs/install",
    "page_number": null,
    "heading_path": "Doc > Installation",
    "parent_id": null,
    "token_count": 3800
  },
  {
    "id": "child-uuid",
    "text": "child chunk text...",
    "chunk_type": "child",
    "source_file": "doc.md",
    "source_url": "https://example.com/docs/install",
    "page_number": null,
    "heading_path": "Doc > Installation",
    "parent_id": "parent-uuid",
    "child_index": 0,
    "token_count": 980,
    "dense_vector": [0.012, -0.034, ...]
  }
]
```

## Qdrant Payloads (final, after `source_url` injection)

### Parent point

```python
PointStruct(
    id="parent-uuid",
    vector={"dense": [0.0, 0.0, ...]},  # zero vector, required by Qdrant
    payload={
        "text": "full parent section text...",
        "chunk_type": "parent",
        "source_file": "doc.md",
        "source_url": "https://...",  # from url_mapping.json, null if not web-origin
        "page_number": null,  # null for MD
        "heading_path": "Doc > Installation",
        "token_count": 3800,
    },
)
```

### Child point

```python
PointStruct(
    id="child-uuid",
    vector={
        "dense": [0.012, -0.034, ...],  # real embedding
        "sparse": models.SparseVector(
            indices=..., values=...
        ),  # client-side fastembed BM25
    },
    payload={
        "text": "child chunk text...",
        "chunk_type": "child",
        "source_file": "doc.md",
        "source_url": "https://...",  # from url_mapping.json, null if not web-origin
        "page_number": null,  # null for MD
        "heading_path": "Doc > Installation",
        "parent_id": "parent-uuid",
        "child_index": 0,
        "token_count": 980,
    },
)
```

## Retrieval Flow (hybrid search + O(1) parent fetch)

```
Query (text)
  → Embed query via same embedding model → dense query vector
  → Qdrant query_points with two prefetches:
      1. Dense:  query=<dense_vector>,  using="dense",  limit=K
      2. Sparse: query=SparseVector (fastembed BM25), using="sparse", limit=K
  → Server-side Reciprocal Rank Fusion (RRF) merges both result sets
  → Filter: chunk_type="child" (parents excluded from search)
  → Top-K fused child results
  → Collect unique parent_id values
  → Qdrant retrieve(parent_ids) — O(1) direct lookup, no vector search
  → Return parent text(s) as context to LLM
```

### Hybrid search query example

```python
from qdrant_client import AsyncQdrantClient, models

client = AsyncQdrantClient(url="http://localhost:6333")

results = await client.query_points(
    collection_name="my-collection-name",
    query=models.FusionQuery(fusion=models.Fusion.RRF),
    prefetch=[
        models.Prefetch(
            query=dense_query_vector,  # from embedding model
            using="dense",
            limit=20,
        ),
        models.Prefetch(
            query=models.SparseVector(
                indices=..., values=...
            ),  # client-side fastembed BM25
            using="sparse",
            limit=20,
        ),
    ],
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="chunk_type", match=models.MatchValue(value="child")
            )
        ]
    ),
    limit=10,
)

# Fetch parent texts by ID
parent_ids = {
    p.payload["parent_id"] for p in results.points if p.payload.get("parent_id")
}
parents = await client.retrieve("my-collection-name", ids=list(parent_ids))
```

Parent text is stored once per section, not duplicated across children. `retrieve()` is a direct ID lookup — negligible cost compared to the hybrid vector search.

## Infrastructure — Qdrant via Docker

`docker-compose.yml`:

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"   # REST
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

volumes:
  qdrant_data:
```

- Start: `docker compose up -d`
- Data persists across container restarts via the named volume `qdrant_data`.
- Async client connects to `http://localhost:6333` (REST) — for gRPC use `localhost:6334`.

## URL Mapping (`_docs/url_mapping.json`)

```json
{
    "installation-guide.md": "https://example.com/docs/install",
    "api-reference.md": "https://example.com/docs/api"
}
```

- Loaded at chunk time by stage 1 (`--url-mapping` flag).
- Files not in the mapping get `source_url: null`.
- Applies to any source file (MD or PDF) — keyed by filename.
- `source_url` flows through stages 2 and 3 unchanged.

## Key Decisions Summary

| Aspect | Choice |
|---|---|
| Base unit | Semantic blocks by headings |
| Parent | Section-level (content under a heading) |
| Child | Sub-sections within a section, ~1024 tokens |
| Overlap | 10-15% between children |
| Embeddings | Children only |
| Search mode | Hybrid (dense + sparse/BM25 with RRF fusion) |
| Parent storage | Separate Qdrant points with zero vectors — deduplicated |
| PDF parsing | pymupdf font size heuristics |
| MD parsing | markdown-it-py |
| Vector DB | Qdrant (single collection, named vectors "dense" + "sparse") |
| Retrieval | Hybrid search children (RRF) → retrieve parents by ID (O(1)) |
| Framework | Custom Python (no LlamaIndex/LangChain) |
| Embedding model | OpenAI-compatible API (Ollama `embeddinggemma-2:440m`) |
| URL mapping | JSON file |
| Pipeline separation | 3 stages: chunk → embed → ingest |

## Remarks

- [x] Qdrant collection name and vector size will be set manually.
