from qdrant_client import AsyncQdrantClient, models


async def hybrid_query(
    client: AsyncQdrantClient,
    collection: str,
    query_text: str,
    query_vector: list[float],
    top_k: int = 10,
    prefetch_k: int = 20,
) -> list[dict]:
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
