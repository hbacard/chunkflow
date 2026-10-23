"""File parsing: turn .md/.pdf files into ordered Section objects with heading paths.

Logic flow:
    - Markdown: walk CommonMark tokens; every heading starts a new section and builds
      a " > "-joined heading path; body inline tokens accumulate until the next heading.
    - PDF: extract text blocks per page, drop page numbers/repeated headers, use font
      size to detect headings and reconstruct the same section/heading structure.
"""

import statistics
from collections import Counter
from pathlib import Path

import pymupdf
from markdown_it import MarkdownIt

from chunkflow.common.records import Section

_MD = MarkdownIt("commonmark")
_HEADING_MAX_LEN = 80


def parse_file(path: str | Path) -> list[Section]:
    """Parse a single .md or .pdf file into sections.

    Parameters
    ----------
    path : str | Path
        Path to the input file.

    Returns
    -------
    list[Section]
        Sections in reading order with heading paths and page numbers.

    Raises
    ------
    ValueError
        If the file suffix is not ``.md`` or ``.pdf``.
    """
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".md":
        return _parse_md(p)
    if suffix == ".pdf":
        return _parse_pdf(p)
    raise ValueError(f"unsupported file type: {p.suffix}")


def _parse_md(path: Path) -> list[Section]:
    """Parse a Markdown file into sections using the heading structure.

    Parameters
    ----------
    path : Path
        Path to the .md file.

    Returns
    -------
    list[Section]
        Sections ordered as they appear, heading path reflects nesting level.
    """
    tokens = _MD.parse(path.read_text(encoding="utf-8"))
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    buf: list[str] = []
    pending: int | None = None

    def flush() -> None:
        text = " ".join(buf).strip()
        if text:
            sections.append(Section(text, " > ".join(h for _, h in stack), None, path.name))
        buf.clear()

    for tok in tokens:
        if tok.type == "heading_open":
            flush()
            pending = int(tok.tag[1])
        elif tok.type == "inline":
            if pending is not None:
                while stack and stack[-1][0] >= pending:
                    stack.pop()
                stack.append((pending, tok.content.strip()))
                pending = None
            else:
                buf.append(tok.content)
        elif tok.type == "heading_close":
            pending = None
    flush()
    return sections


def _block_lines(b: dict) -> list[str]:
    """Extract non-empty text lines from a PyMuPDF text block.

    Parameters
    ----------
    b : dict
        A PyMuPDF ``dict`` text block containing ``lines`` with ``spans``.

    Returns
    -------
    list[str]
        Joined span text per line, right-stripped.
    """
    lines: list[str] = []
    for l in b["lines"]:
        spans = [s["text"] for s in l["spans"] if s["text"]]
        if spans:
            lines.append("".join(spans).rstrip())
    return lines


def _dehyphenate(lines: list[str]) -> list[str]:
    """Join lines broken by a trailing hyphen (hyphenated word wraps).

    Parameters
    ----------
    lines : list[str]
        Text lines from a PDF block.

    Returns
    -------
    list[str]
        Lines with trailing-hyphen wraps merged into the following line.
    """
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].endswith("-") and i + 1 < len(lines):
            out.append(lines[i][:-1] + lines[i + 1].lstrip())
            i += 2
        else:
            out.append(lines[i])
            i += 1
    return out


def _is_page_number(text: str) -> bool:
    """Heuristic: is this text a PDF page number?

    Parameters
    ----------
    text : str
        Candidate text.

    Returns
    -------
    bool
        True if the text is short and only digits (optionally slash-separated).
    """
    t = text.strip()
    return len(t) <= 8 and bool(t) and all(p.isdigit() for p in t.replace("/", " ").split())


def _parse_pdf(path: Path) -> list[Section]:
    """Parse a PDF file into sections using font size to detect headings.

    Logic flow: extract text blocks -> drop page numbers and repeated headers ->
    group blocks by detected heading size to rebuild the section/heading structure.

    Parameters
    ----------
    path : Path
        Path to the .pdf file.

    Returns
    -------
    list[Section]
        Sections ordered as they appear, with page numbers.
    """
    doc = pymupdf.open(path)
    n_pages = doc.page_count
    raw: list[tuple[int, float, str]] = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0 or not b["lines"]:
                continue
            lines = _dehyphenate(_block_lines(b))
            text = " ".join(lines).strip()
            if not text:
                continue
            size = max(s["size"] for l in b["lines"] for s in l["spans"])
            raw.append((page.number, size, text))
    doc.close()
    if not raw:
        return []

    counts = Counter(t for _, _, t in raw)
    repeated = {t for t, c in counts.items() if c > max(1, int(n_pages * 0.6)) and len(t) < 80}

    blocks: list[tuple[int, float, str]] = []
    for page, size, text in raw:
        if _is_page_number(text) or text in repeated:
            continue
        blocks.append((page, size, text))
    if not blocks:
        return []

    median = statistics.median(s for _, s, _ in blocks)

    def is_heading(text: str, size: float) -> bool:
        if size <= median * 1.05 or len(text) > _HEADING_MAX_LEN:
            return False
        return not text.endswith((".", ",", ";"))

    levels = {s: i + 1 for i, s in enumerate(sorted({s for _, s, t in blocks if is_heading(t, s)}, reverse=True))}

    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    buf: list[str] = []
    page_no: int | None = None

    def flush() -> None:
        text = " ".join(buf).strip()
        if text:
            sections.append(Section(text, " > ".join(h for _, h in stack), page_no, path.name))
        buf.clear()

    for page, size, text in blocks:
        if is_heading(text, size):
            flush()
            page_no = page
            level = levels[size]
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, text))
        else:
            buf.append(text)
    flush()
    return sections
