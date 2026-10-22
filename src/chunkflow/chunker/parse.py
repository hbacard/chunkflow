import statistics
from pathlib import Path

import pymupdf
from markdown_it import MarkdownIt

from chunkflow.common.records import Section

_MD = MarkdownIt("commonmark")


def parse_file(path: str | Path) -> list[Section]:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".md":
        return _parse_md(p)
    if suffix == ".pdf":
        return _parse_pdf(p)
    raise ValueError(f"unsupported file type: {p.suffix}")


def _parse_md(path: Path) -> list[Section]:
    tokens = _MD.parse(path.read_text(encoding="utf-8"))
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    buf: list[str] = []
    pending: int | None = None

    def flush() -> None:
        text = "".join(buf).strip()
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


def _parse_pdf(path: Path) -> list[Section]:
    doc = pymupdf.open(path)
    blocks: list[tuple[int, float, str]] = []
    for page in doc:
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            size = max(s["size"] for l in b["lines"] for s in l["spans"])
            text = "".join(s["text"] for l in b["lines"] for s in l["spans"]).strip()
            if text:
                blocks.append((page.number, size, text))
    doc.close()
    if not blocks:
        return []

    sizes = {s for _, s, _ in blocks}
    median = statistics.median(s for _, s, _ in blocks)
    levels = {s: i + 1 for i, s in enumerate(sorted((s for s in sizes if s > median * 1.05), reverse=True))}

    sections: list[Section] = []
    stack: list[tuple[int, str]] = []
    buf: list[str] = []
    page_no: int | None = None

    def flush() -> None:
        text = "".join(buf).strip()
        if text:
            sections.append(Section(text, " > ".join(h for _, h in stack), page_no, path.name))
        buf.clear()

    for page, size, text in blocks:
        level = levels.get(size)
        if level is not None:
            flush()
            page_no = page
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, text))
        else:
            buf.append(text)
    flush()
    return sections
