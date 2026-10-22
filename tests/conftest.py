import pytest

LONG_PARA = ("This is a test paragraph with enough words to generate a reasonable number of tokens. " * 100)

MD_CONTENT = f"""# Doc

## Installation

{LONG_PARA}

More installation text.

## Advanced

Short advanced body.
"""


@pytest.fixture
def sample_md(tmp_path):
    p = tmp_path / "sample.md"
    p.write_text(MD_CONTENT, encoding="utf-8")
    return p


@pytest.fixture
def sample_pdf(tmp_path):
    import pymupdf

    p = tmp_path / "sample.pdf"
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Doc", fontsize=30)
    page.insert_text((72, 130), "Installation", fontsize=24)
    y = 180
    for i in range(4):
        page.insert_text((72, y), f"Body paragraph number {i} with some installation details.", fontsize=12)
        y += 30
    doc.save(p)
    doc.close()
    return p
