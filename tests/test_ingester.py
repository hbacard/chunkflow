import asyncio

import httpx
import pytest
from qdrant_client import AsyncQdrantClient

from chunkflow.ingester.ingest import _points, ingest
from chunkflow.ingester.retrieve import hybrid_query

COLLECTION = "test_chunkflow"
URL = "http://localhost:6333"


def _is_up() -> bool:
    try:
        return httpx.get(f"{URL}/healthz", timeout=2).status_code == 200
    except httpx.RequestError:
        return False


pytestmark = pytest.mark.skipif(
    not _is_up(),
    reason="Qdrant not running on localhost:6333 (docker compose up -d)",
)


def _sample_records():
    parent = {
        "id": "11111111-1111-1111-1111-111111111111",
        "text": "Full installation section text about setup and configuration.",
        "chunk_type": "parent",
        "source_file": "doc.md",
        "source_url": "https://example.com/doc",
        "page_number": None,
        "heading_path": "Doc > Install",
        "parent_id": None,
        "token_count": 12,
    }
    child = dict(parent)
    child.update(
        id="22222222-2222-2222-2222-222222222222",
        text="Run the setup command to install and configure.",
        chunk_type="child",
        parent_id="11111111-1111-1111-1111-111111111111",
        child_index=0,
        token_count=6,
        dense_vector=[0.1] * 8,
    )
    return [parent, child]


def _run_with_client(coro_factory):
    client = AsyncQdrantClient(url=URL)
    try:
        return asyncio.run(coro_factory(client))
    finally:
        asyncio.run(client.close())


def test_points_payload_shape():
    points = _points(_sample_records(), dim=8)
    parent, child = points
    assert parent.vector == {"dense": [0.0] * 8}
    assert child.vector["sparse"].model == "Qdrant/bm25"
    assert child.vector["dense"] == [0.1] * 8
    assert child.payload["parent_id"] == "11111111-1111-1111-1111-111111111111"
    assert "id" not in child.payload and "dense_vector" not in child.payload
    assert parent.payload["chunk_type"] == "parent"


def _ingested():
    async def scenario(client):
        await client.delete_collection(COLLECTION)
        await ingest(_sample_records(), client, COLLECTION, dim=8)

    _run_with_client(scenario)


def test_ingest_creates_collection_and_upserts():
    _ingested()

    async def scenario(client):
        assert await client.collection_exists(COLLECTION)
        got = await client.retrieve(
            COLLECTION,
            ids=[
                "11111111-1111-1111-1111-111111111111",
                "22222222-2222-2222-2222-222222222222",
            ],
            with_vectors=True,
        )
        by_id = {p.id: p for p in got}
        assert (
            by_id["11111111-1111-1111-1111-111111111111"]
            .payload["text"]
            .startswith("Full installation")
        )
        assert (
            by_id["22222222-2222-2222-2222-222222222222"].payload["chunk_type"]
            == "child"
        )

    _run_with_client(scenario)


def test_hybrid_query_returns_parent():
    _ingested()

    async def scenario(client):
        parents = await hybrid_query(
            client, COLLECTION, "setup and configure", [0.1] * 8, top_k=2
        )
        assert parents
        assert parents[0]["chunk_type"] == "parent"
        assert "Install" in parents[0]["heading_path"]

    _run_with_client(scenario)
