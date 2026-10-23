"""Hybrid retrieval: RRF-fuse dense + BM25 sparse searches, then return parent records."""

from qdrant_client import AsyncQdrantClient, models


async def hybrid_query(
    client: AsyncQdrantClient,
    collection: str,
    query_text: str,
    query_vector: list[float],
    top_k: int = 10,
    prefetch_k: int = 20,
) -> list[dict]:
    """Search child chunks with hybrid (dense + BM25) retrieval and map to parents.

    Logic flow: RRF-fuse dense and sparse prefetches over child chunks -> collect the
    matched children's ``parent_id`` -> retrieve the parent records and return them.

    Parameters
    ----------
    client : AsyncQdrantClient
        Qdrant client.
    collection : str
        Collection name.
    query_text : str
        Raw query text used for the BM25 sparse search.
    query_vector : list[float]
        Dense query vector.
    top_k : int
        Number of parent results to return (default 10).
    prefetch_k : int
        Per-vector-space candidate count before fusion (default 20).

    Returns
    -------
    list[dict]
        Payloads of the matched parent records.
    """
    results = await client.query_points(
        collection_name=collection,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        prefetch=[
            models.Prefetch(query=query_vector, using="dense", limit=prefetch_k),
            models.Prefetch(query=models.Document(text=query_text, model="Qdrant/bm25"), using="sparse", limit=prefetch_k),
        ],
        query_filter=models.Filter(
            must=[models.FieldCondition(key="chunk_type", match=models.MatchValue(value="child"))]
        ),
        limit=top_k,
    )
    parent_ids = list({p.payload["parent_id"] for p in results.points if p.payload.get("parent_id")})
    if not parent_ids:
        return []
    parents = await client.retrieve(collection, ids=parent_ids)
    return [p.payload for p in parents]
