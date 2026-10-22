import json

import httpx

from chunkflow.embedder.embed import BATCH_SIZE, _embed_batch, embed_records, run


def _mock_client(requests_log=None):
    def handler(request):
        if requests_log is not None:
            requests_log.append(request)
        body = json.loads(request.content)
        n = len(body["input"])
        return httpx.Response(200, json={"data": [{"embedding": [0.5] * 8} for _ in range(n)]})

    return httpx.Client(base_url="http://test", transport=httpx.MockTransport(handler))


def _records(n_children=3):
    records = [{"id": "p", "chunk_type": "parent", "text": "x"}]
    for i in range(n_children):
        records.append({"id": f"c{i}", "chunk_type": "child", "text": f"text {i}"})
    return records


def test_embed_batch_shape():
    vectors = _embed_batch(_mock_client(), ["a", "b"])
    assert vectors == [[0.5] * 8, [0.5] * 8]


def test_embed_records_only_children():
    records = _records()
    embed_records(records, _mock_client())
    assert "dense_vector" not in records[0]
    for rec in records[1:]:
        assert rec["dense_vector"] == [0.5] * 8


def test_embed_batches_children():
    log = []
    records = _records(n_children=BATCH_SIZE + 3)
    embed_records(records, _mock_client(log))
    assert len(log) == 2
    assert len(log[0].content and json.loads(log[0].content)["input"]) == BATCH_SIZE


def test_run(monkeypatch, tmp_path):
    monkeypatch.setattr("chunkflow.embedder.embed.make_client", _mock_client)
    inp = tmp_path / "chunks.json"
    inp.write_text(json.dumps(_records()))
    out = tmp_path / "embedded.json"
    run(str(inp), str(out))
    data = json.loads(out.read_text())
    assert data[0] == {"id": "p", "chunk_type": "parent", "text": "x"}
    assert data[1]["dense_vector"] == [0.5] * 8
