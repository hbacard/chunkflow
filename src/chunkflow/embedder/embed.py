"""Stage 2: embed child chunk texts via an OpenAI-compatible /v1/embeddings endpoint."""

import json
import os
from pathlib import Path

import httpx

BATCH_SIZE = 32
DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "embeddinggemma-2:440m"


def make_client() -> httpx.Client:
    """Build an HTTP client for the embedding endpoint.

    The base URL comes from the ``EMBEDDING_BASE_URL`` env var, defaulting to
    ``http://localhost:11434`` with a 60s timeout.

    Returns
    -------
    httpx.Client
        Configured client for embedding requests.
    """
    return httpx.Client(
        base_url=os.environ.get("EMBEDDING_BASE_URL", DEFAULT_BASE_URL),
        timeout=httpx.Timeout(60.0),
    )


def _embed_batch(client: httpx.Client, texts: list[str]) -> list[list[float]]:
    """Embed one batch of texts via the embeddings endpoint.

    Parameters
    ----------
    client : httpx.Client
        Client for embedding requests.
    texts : list[str]
        Texts to embed.

    Returns
    -------
    list[list[float]]
        One embedding vector per input text, in the same order.
    """
    resp = client.post(
        "/v1/embeddings",
        json={
            "model": os.environ.get("EMBEDDING_MODEL", DEFAULT_MODEL),
            "input": texts,
        },
    )
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]


def embed_records(records: list[dict], client: httpx.Client) -> list[dict]:
    """Add a ``dense_vector`` to every child record, in batches.

    Parameters
    ----------
    records : list[dict]
        Chunk records; only ``chunk_type == "child"`` are embedded.
    client : httpx.Client
        Client for embedding requests.

    Returns
    -------
    list[dict]
        The same records list, mutated with dense vectors added.
    """
    children = [r for r in records if r["chunk_type"] == "child"]
    for i in range(0, len(children), BATCH_SIZE):
        batch = children[i : i + BATCH_SIZE]
        vectors = _embed_batch(client, [r["text"] for r in batch])
        for rec, vec in zip(batch, vectors):
            rec["dense_vector"] = vec
    return records


def run(input_path: str, output_path: str) -> None:
    """Embed all child chunks in a chunks.json file and write the result.

    Parameters
    ----------
    input_path : str
        Path of the input chunks.json file.
    output_path : str
        Path of the output embedded_chunks.json file.
    """
    records = json.loads(Path(input_path).read_text(encoding="utf-8"))
    with make_client() as client:
        embed_records(records, client)
    Path(output_path).write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
