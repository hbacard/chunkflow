from chunkflow.chunker.chunk import CHUNK_TOKENS, chunk_sections
from chunkflow.chunker.parse import parse_file


def test_md_section_detection(sample_md):
    sections = parse_file(sample_md)
    assert [s.heading_path for s in sections] == ["Doc > Installation", "Doc > Advanced"]
    assert "More installation text." in sections[0].text
    assert sections[0].page_number is None


def test_pdf_section_detection(sample_pdf):
    sections = parse_file(sample_pdf)
    assert len(sections) == 1
    assert sections[0].heading_path == "Doc > Installation"
    assert sections[0].page_number == 0
    assert "Body paragraph number 3" in sections[0].text


def test_chunk_sizes_and_overlap(sample_md):
    from chunkflow.chunker.chunk import OVERLAP_RATIO, _split

    records = chunk_sections(parse_file(sample_md))
    children = [r for r in records if r["chunk_type"] == "child"]
    assert children, "expected children chunks"
    assert all(r["token_count"] <= CHUNK_TOKENS for r in children)
    step = CHUNK_TOKENS - int(CHUNK_TOKENS * OVERLAP_RATIO)
    shared = CHUNK_TOKENS - step
    chunks = _split(list(range(3000)))
    for a, b in zip(chunks, chunks[1:]):
        if len(a) == CHUNK_TOKENS and len(b) == CHUNK_TOKENS:
            assert a[-shared:] == b[:shared]
            assert 0.10 <= shared / CHUNK_TOKENS <= 0.15
            break


def test_parent_linkage(sample_md):
    records = chunk_sections(parse_file(sample_md))
    parents = [r for r in records if r["chunk_type"] == "parent"]
    children = [r for r in records if r["chunk_type"] == "child"]
    by_id = {r["id"]: r for r in parents}
    for child in children:
        parent = by_id[child["parent_id"]]
        assert parent["heading_path"] == child["heading_path"]
        assert parent["token_count"] >= child["token_count"]
    assert all(r["parent_id"] is None for r in parents)
    from collections import defaultdict

    per_parent = defaultdict(list)
    for c in children:
        per_parent[c["parent_id"]].append(c["child_index"])
    for indexes in per_parent.values():
        assert indexes == list(range(len(indexes)))


def test_url_mapping():
    from chunkflow.common.records import Section

    sections = [
        Section("alpha text", "A", None, "known.md"),
        Section("beta text", "B", None, "unknown.md"),
    ]
    records = chunk_sections(sections, {"known.md": "https://example.com/known"})
    by_file = {r["source_file"]: r["source_url"] for r in records if r["chunk_type"] == "parent"}
    assert by_file["known.md"] == "https://example.com/known"
    assert by_file["unknown.md"] is None
