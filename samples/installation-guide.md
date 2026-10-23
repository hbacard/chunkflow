# ChunkFlow Documentation

## Installation

Install the package with PDM:

```bash
pdm install
```

Then start Qdrant with Docker:

```bash
docker compose up -d
```

## Configuration

The pipeline is configured through environment variables:

| Variable | Default | Used by |
|---|---|---|
| `EMBEDDING_BASE_URL` | `http://localhost:11434` | embed |
| `EMBEDDING_MODEL` | `embeddinggemma-2:440m` | embed |
| `EMBEDDING_DIM` | `768` | ingest |

## CLI usage

The pipeline runs as three independent stages, each consuming the previous stage's JSON output:

```bash
chunkflow chunk  --input path/to/files --output chunks.json --url-mapping url_mapping.json
chunkflow embed  --input chunks.json --output embedded_chunks.json
chunkflow ingest --input embedded_chunks.json --collection chunkflow
```

## JSON contract

Stage 1 produces a list of parent and child records. Parents are document sections
(defined by headings); children are overlapping token-windowed chunks within each
section, capped at 1024 tokens with ~12.5% overlap.

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
    "dense_vector": [0.012, -0.034]
  }
]
```

Parents carry the full section text and are stored once per section (deduplicated).
Only children are embedded for search; `dense_vector` is added at stage 2. The sparse
BM25 vector is computed server-side by Qdrant at ingest time.

## Hybrid retrieval

Children are searched with a hybrid query (dense + sparse BM25 fused with Reciprocal
Rank Fusion). The unique parent IDs of the top children are then fetched directly:

```python
import asyncio
from qdrant_client import AsyncQdrantClient
from chunkflow.ingester.retrieve import hybrid_query


async def main():
    client = AsyncQdrantClient(url="http://localhost:6333")
    parents = await hybrid_query(
        client,
        "chunkflow",
        query_text="how do I install chunkflow",
        query_vector=[0.0] * 768,
        top_k=5,
    )
    await client.close()


asyncio.run(main())
```

## Development

```bash
pdm run python -m pytest
```

The ingester tests skip automatically when Qdrant is not running on `localhost:6333`.
