import json
import os
from pathlib import Path

import httpx

BATCH_SIZE = 32
DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "embeddinggemma-2:440m"


def make_client() -> httpx.Client:
    return httpx.Client(
        base_url=os.environ.get("EMBEDDING_BASE_URL", DEFAULT_BASE_URL),
        timeout=httpx.Timeout(60.0),
    )


def _embed_batch(client: httpx.Client, texts: list[str]) -> list[list[float]]:
    resp = client.post(
        "/v1/embeddings",
        json={"model": os.environ.get("EMBEDDING_MODEL", DEFAULT_MODEL), "input": texts},
    )
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]


def embed_records(records: list[dict], client: httpx.Client) -> list[dict]:
    children = [r for r in records if r["chunk_type"] == "child"]
    for i in range(0, len(children), BATCH_SIZE):
        batch = children[i : i + BATCH_SIZE]
        vectors = _embed_batch(client, [r["text"] for r in batch])
        for rec, vec in zip(batch, vectors):
            rec["dense_vector"] = vec
    return records


def run(input_path: str, output_path: str) -> None:
    records = json.loads(Path(input_path).read_text(encoding="utf-8"))
    with make_client() as client:
        embed_records(records, client)
    Path(output_path).write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
