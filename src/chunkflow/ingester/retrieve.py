"""Hybrid retrieval: RRF-fuse dense + BM25 sparse searches, then return parent records."""

import asyncio

from qdrant_client import AsyncQdrantClient, models

from chunkflow.ingester.ingest import _sparse_embedder


async def hybrid_query(
    client: AsyncQdrantClient,
    collection: str,
    query_text: str,
    query_vector: list[float],
    top_k: int = 10,
    prefetch_k: int = 20,
    source: str | None = None,
) -> list[dict]:
    """Search child chunks with hybrid (dense + BM25) retrieval and map to parents.

    Logic flow: RRF-fuse dense and sparse prefetches over child chunks -> collect the
    matched children's ``parent_id`` -> retrieve the parent records and return them in
    fused-score order (best-matching child per parent).

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
    source : str | None
        If given, only match children from this source (filtered server-side).

    Returns
    -------
    list[dict]
        Payloads of the matched parent records, best first.
    """
    sparse = next(
        iter(
            await asyncio.to_thread(
                lambda: _sparse_embedder().query_embed([query_text])
            )
        )
    )
    sparse_vector = models.SparseVector(
        indices=sparse.indices.tolist(), values=sparse.values.tolist()
    )
    query_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="chunk_type", match=models.MatchValue(value="child")
            )
        ]
    )
    if source:
        # filter server-side, not after limiting to top_k (avoids dropping valid hits)
        query_filter.must.append(
            models.FieldCondition(key="source", match=models.MatchValue(value=source))
        )
    results = await client.query_points(
        collection_name=collection,
        query=models.FusionQuery(fusion=models.Fusion.RRF),
        prefetch=[
            models.Prefetch(query=query_vector, using="dense", limit=prefetch_k),
            models.Prefetch(
                query=sparse_vector,
                using="sparse",
                limit=prefetch_k,
            ),
        ],
        query_filter=query_filter,
        limit=top_k,
    )
    score_by_parent: dict[str, float] = {}
    for p in results.points:
        pid = p.payload.get("parent_id")
        if pid and (pid not in score_by_parent or p.score > score_by_parent[pid]):
            score_by_parent[pid] = p.score
    if not score_by_parent:
        return []
    parents = await client.retrieve(collection, ids=list(score_by_parent))
    parents.sort(key=lambda p: -score_by_parent.get(p.id, 0.0))
    return [p.payload for p in parents]
