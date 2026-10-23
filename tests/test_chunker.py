from chunkflow.chunker.chunk import CHILD_TOKENS, chunk_sections
from chunkflow.chunker.parse import parse_file


def test_md_section_detection(sample_md):
    sections = parse_file(sample_md)
    assert [s.heading_path for s in sections] == [
        "Doc > Installation",
        "Doc > Advanced",
    ]
    assert "More installation text." in sections[0].text
    assert sections[0].page_number is None


def test_pdf_section_detection(sample_pdf):
    sections = parse_file(sample_pdf)
    assert len(sections) == 1
    assert sections[0].heading_path == "Doc > Installation"
    assert sections[0].page_number == 0
    assert "Body paragraph number 3" in sections[0].text


def test_children_preserve_sentences(sample_md):
    records = chunk_sections(parse_file(sample_md))
    parents = {r["id"]: r for r in records if r["chunk_type"] == "parent"}
    children = [r for r in records if r["chunk_type"] == "child"]
    assert children, "expected children chunks"
    assert all(r["token_count"] <= CHILD_TOKENS for r in children)
    from pysbd import Segmenter

    seg = Segmenter(language="en", clean=False)
    for child in children:
        parent_text = parents[child["parent_id"]]["text"]
        for sentence in seg.segment(child["text"]):
            assert sentence.strip() in parent_text, "child cuts a sentence in half"


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
    by_file = {
        r["source_file"]: r["source_url"]
        for r in records
        if r["chunk_type"] == "parent"
    }
    assert by_file["known.md"] == "https://example.com/known"
    assert by_file["unknown.md"] is None


def test_pdf_filters_page_numbers_and_headers(tmp_path):
    import pymupdf

    p = tmp_path / "garbage.pdf"
    doc = pymupdf.open()
    for i in range(4):
        page = doc.new_page()
        page.insert_text((72, 40), "Running Header", fontsize=10)
        page.insert_text((72, 100), f"Body sentence {i}.", fontsize=12)
        page.insert_text((300, 800), "7", fontsize=10)
    doc.save(p)
    doc.close()

    text = " ".join(s.text for s in parse_file(p))
    assert "Running Header" not in text
    assert "7" not in text
    assert "Body sentence 0." in text
