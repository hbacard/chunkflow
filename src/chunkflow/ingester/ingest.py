"""Stage 3: upsert chunk records into a Qdrant collection with hybrid (dense + BM25 sparse) vectors."""

import json
import os
from pathlib import Path

from fastembed import SparseTextEmbedding
from qdrant_client import AsyncQdrantClient, models

DEFAULT_COLLECTION = "chunkflow"
DEFAULT_DIM = 768
SPARSE_MODEL = "Qdrant/bm25"

_embedder: SparseTextEmbedding | None = None


def _sparse_embedder() -> SparseTextEmbedding:
    """Return a lazily-initialized BM25 sparse embedder (cached).

    Returns
    -------
    SparseTextEmbedding
        The fastembed sparse embedder for ``Qdrant/bm25``.
    """
    global _embedder
    if _embedder is None:
        _embedder = SparseTextEmbedding(SPARSE_MODEL)
    return _embedder


def _dim() -> int:
    """Read the embedding dimension from ``EMBEDDING_DIM`` (default 768).

    Returns
    -------
    int
        Embedding vector dimension.
    """
    return int(os.environ.get("EMBEDDING_DIM", str(DEFAULT_DIM)))


async def _ensure_collection(
    client: AsyncQdrantClient, collection: str, dim: int
) -> None:
    """Create the collection if it does not exist yet.

    Creates a collection with a ``dense`` (COSINE, ``dim``) vector space and a
    ``sparse`` vector space.

    Parameters
    ----------
    client : AsyncQdrantClient
        Qdrant client.
    collection : str
        Collection name.
    dim : int
        Dense vector dimension.
    """
    if not await client.collection_exists(collection):
        await client.create_collection(
            collection,
            vectors_config={
                "dense": models.VectorParams(size=dim, distance=models.Distance.COSINE)
            },
            sparse_vectors_config={"sparse": models.SparseVectorParams()},
        )


def _points(records: list[dict], dim: int) -> list[models.PointStruct]:
    """Convert records into Qdrant points with hybrid vectors and payloads.

    Child records get their dense vector plus a client-side BM25 sparse vector;
    parent records get a zero dense vector (parents are not searched directly).

    Parameters
    ----------
    records : list[dict]
        Chunk records.
    dim : int
        Dense vector dimension for the zero vector of parents.

    Returns
    -------
    list[models.PointStruct]
        Qdrant points ready for upsert.
    """
    children = [r for r in records if r["chunk_type"] == "child"]
    sparse_by_id = {}
    if children:
        embeddings = _sparse_embedder().embed([r["text"] for r in children])
        sparse_by_id = {
            r["id"]: models.SparseVector(
                indices=e.indices.tolist(), values=e.values.tolist()
            )
            for r, e in zip(children, embeddings)
        }
    points = []
    for r in records:
        if r["chunk_type"] == "child":
            vector = {"dense": r["dense_vector"], "sparse": sparse_by_id[r["id"]]}
        else:
            vector = {"dense": [0.0] * dim}
        payload = {k: v for k, v in r.items() if k not in ("id", "dense_vector")}
        points.append(models.PointStruct(id=r["id"], vector=vector, payload=payload))
    return points


async def ingest(
    records: list[dict], client: AsyncQdrantClient, collection: str, dim: int
) -> None:
    """Ensure the collection exists and upsert all records as points.

    Parameters
    ----------
    records : list[dict]
        Chunk records to upsert.
    client : AsyncQdrantClient
        Qdrant client.
    collection : str
        Collection name.
    dim : int
        Dense vector dimension.
    """
    await _ensure_collection(client, collection, dim)
    await client.upsert(collection, points=_points(records, dim))


async def run(
    input_path: str,
    collection: str = DEFAULT_COLLECTION,
    url: str = "http://localhost:6333",
) -> None:
    """Load records from JSON and upsert them into Qdrant.

    Parameters
    ----------
    input_path : str
        Path of the input embedded_chunks.json file.
    collection : str
        Qdrant collection name (default ``chunkflow``).
    url : str
        Qdrant REST URL (default ``http://localhost:6333``).
    """
    records = json.loads(Path(input_path).read_text(encoding="utf-8"))
    client = AsyncQdrantClient(url=url)
    try:
        await ingest(records, client, collection, _dim())
    finally:
        await client.close()
