"""Serveur MCP pour ChunkFlow : outils `qdrant_store` et `qdrant_find` (hybride dense + BM25)."""

import asyncio
import os
import uuid

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from qdrant_client import AsyncQdrantClient, models

from chunkflow.embedder.embed import _embed, make_client
from chunkflow.ingester.ingest import _dim, _ensure_collection, _sparse_embedder
from chunkflow.ingester.retrieve import hybrid_query

load_dotenv()
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.environ.get("COLLECTION_NAME", "docs_rag")

qdrant = AsyncQdrantClient(url=QDRANT_URL)
embedder = make_client()

mcp = MCPServer("qdrant")


@mcp.tool()
async def qdrant_store(
    text: str,
    source: str = "",
    page: int | None = None,
    metadata: dict | None = None,
) -> str:
    """Stocke un texte dans Qdrant sous forme d'un couple parent/enfant (recherche hybride).

    Args:
        text: contenu à mémoriser.
        source: origine du texte (nom de fichier, URL...), filtrable côté recherche.
        page: numéro de page éventuel.
        metadata: métadonnées supplémentaires (dict JSON).
    """
    dim = _dim()
    await _ensure_collection(qdrant, COLLECTION, dim)

    # differs from the CLI pipeline: stores the whole text as one parent/child pair,
    # no token-window chunking - fine for short notes, limit input length for long text
    parent_id = str(uuid.uuid4())
    child_id = str(uuid.uuid4())

    extra = metadata or {}
    parent_payload = {"chunk_type": "parent", "text": text, "source": source, **extra}
    if page is not None:
        parent_payload["page"] = page
    child_payload = {
        "chunk_type": "child",
        "parent_id": parent_id,
        "text": text,
        "source": source,
        **extra,
    }
    if page is not None:
        child_payload["page"] = page

    dense = await asyncio.to_thread(_embed, embedder, text)
    sparse = next(iter(await asyncio.to_thread(_sparse_embedder().embed, [text])))

    await qdrant.upsert(
        COLLECTION,
        points=[
            models.PointStruct(
                id=parent_id,
                vector={"dense": [0.0] * dim},
                payload=parent_payload,
            ),
            models.PointStruct(
                id=child_id,
                vector={
                    "dense": dense,
                    "sparse": models.SparseVector(
                        indices=sparse.indices.tolist(), values=sparse.values.tolist()
                    ),
                },
                payload=child_payload,
            ),
        ],
    )
    return f"Stocké (parent={parent_id}, child={child_id}) dans '{COLLECTION}'."


@mcp.tool()
async def qdrant_find(
    query: str, source: str | None = None, limit: int = 5
) -> list[dict]:
    """Recherche hybride (dense + BM25) dans Qdrant, retourne les parents correspondants.

    Args:
        query: question ou description en langage naturel.
        source: si fourni, ne garde que les résultats de cette source.
        limit: nombre maximum de résultats.
    """
    if not await qdrant.collection_exists(COLLECTION):
        return []

    query_vector = await asyncio.to_thread(_embed, embedder, query)
    results = await hybrid_query(
        qdrant, COLLECTION, query, query_vector, top_k=limit, source=source
    )
    return results[:limit]


if __name__ == "__main__":
    transport = "streamable-http"
    # default 0.0.0.0 keeps the documented LAN setup; bind MCP_HOST=127.0.0.1 to restrict.
    # shortcut: no auth on this server - LAN clients can read all docs and insert text;
    # add a token header check before exposing beyond a trusted network.
    port = int(os.environ.get("MCP_PORT", "8001"))
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    mcp.run(transport=transport, port=port, host=host)
