import json
import os
from pathlib import Path

from qdrant_client import AsyncQdrantClient, models

DEFAULT_COLLECTION = "chunkflow"
DEFAULT_DIM = 768


def _dim() -> int:
    return int(os.environ.get("EMBEDDING_DIM", str(DEFAULT_DIM)))


async def _ensure_collection(client: AsyncQdrantClient, collection: str, dim: int) -> None:
    if not await client.collection_exists(collection):
        await client.create_collection(
            collection,
            vectors_config={"dense": models.VectorParams(size=dim, distance=models.Distance.COSINE)},
            sparse_vectors_config={"sparse": models.SparseVectorParams()},
        )


def _points(records: list[dict], dim: int) -> list[models.PointStruct]:
    points = []
    for r in records:
        vector = {"dense": r["dense_vector"]} if r["chunk_type"] == "child" else {"dense": [0.0] * dim}
        if r["chunk_type"] == "child":
            vector["sparse"] = models.Document(text=r["text"], model="Qdrant/bm25")
        payload = {k: v for k, v in r.items() if k not in ("id", "dense_vector")}
        points.append(models.PointStruct(id=r["id"], vector=vector, payload=payload))
    return points


async def ingest(records: list[dict], client: AsyncQdrantClient, collection: str, dim: int) -> None:
    await _ensure_collection(client, collection, dim)
    await client.upsert(collection, points=_points(records, dim))


async def run(input_path: str, collection: str = DEFAULT_COLLECTION, url: str = "http://localhost:6333") -> None:
    records = json.loads(Path(input_path).read_text(encoding="utf-8"))
    client = AsyncQdrantClient(url=url)
    try:
        await ingest(records, client, collection, _dim())
    finally:
        await client.close()
