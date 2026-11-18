"""Parent-child chunking: group sections into parent records, split text into child records.

Logic flow:
    1. Group consecutive sections into parent groups bounded by PARENT_TOKENS.
    2. Emit one parent record per group with its token count.
    3. Split each parent text into sentence-aligned child chunks bounded by CHILD_TOKENS
       and emit one child record per chunk.
"""

import tiktoken
from pysbd import Segmenter

from chunkflow.common.records import Section, child_record, parent_record

PARENT_TOKENS = 2000
CHILD_TOKENS = 1000
_ENC = tiktoken.get_encoding("cl100k_base")
_SEG = Segmenter(language="en", clean=False)


def chunk_sections(
    sections: list[Section], url_map: dict[str, str] | None = None
) -> list[dict]:
    """Turn document sections into parent/child chunk records.

    Parameters
    ----------
    sections : list[Section]
        Sections of a single document, in reading order.
    url_map : dict[str, str] | None
        Optional mapping of source file name to source URL.

    Returns
    -------
    list[dict]
        Parent records followed by their child records, ready to persist.
    """
    url_map = url_map or {}
    records: list[dict] = []
    for group in _parent_groups(sections):
        text = " ".join(s.text for s in group).strip()
        tokens = _ENC.encode(text)
        if not tokens:
            continue
        first = group[0]
        parent = parent_record(first, text, url_map.get(first.source_file), len(tokens))
        records.append(parent)
        for index, chunk in enumerate(_split_sentences(text)):
            records.append(child_record(parent, chunk, index, len(_ENC.encode(chunk))))
    return records


def _parent_groups(sections: list[Section]) -> list[list[Section]]:
    """Group consecutive sections into token-bounded parent groups.

    A section that has no page number or already exceeds PARENT_TOKENS forms its own
    group. Otherwise sections accumulate until adding the next would exceed PARENT_TOKENS.

    Parameters
    ----------
    sections : list[Section]
        Sections of a single document, in reading order.

    Returns
    -------
    list[list[Section]]
        Groups of sections, each to become one parent record.
    """
    counts = [(s, len(_ENC.encode(s.text))) for s in sections]
    groups: list[list[Section]] = []
    current: list[Section] = []
    current_tokens = 0
    for section, tokens in counts:
        if section.page_number is None or tokens >= PARENT_TOKENS:
            if current:
                groups.append(current)
                current, current_tokens = [], 0
            groups.append([section])
        elif not current:
            current = [section]
            current_tokens = tokens
        elif current_tokens + tokens > PARENT_TOKENS:
            groups.append(current)
            current = [section]
            current_tokens = tokens
        else:
            current.append(section)
            current_tokens += tokens
    if current:
        groups.append(current)
    return groups


def _split_sentences(text: str) -> list[str]:
    """Split text into sentence-aligned chunks bounded by CHILD_TOKENS.

    When a chunk is full, the next chunk starts with the previous chunk's last
    sentence to preserve sentence boundaries across chunks.

    Parameters
    ----------
    text : str
        Text to split into child chunks.

    Returns
    -------
    list[str]
        Child chunks, each within CHILD_TOKENS tokens.
    """
    sentences = [s.strip() for s in _SEG.segment(text) if s.strip()]
    chunks: list[str] = []
    buf: list[str] = []
    buf_tokens = 0
    for sentence in sentences:
        n = len(_ENC.encode(sentence))
        # shortcut: a single sentence longer than CHILD_TOKENS is kept whole (chunk
        # exceeds the budget); hard-split it when over-budget run-ons matter
        if buf and buf_tokens + n > CHILD_TOKENS:
            chunks.append(" ".join(buf))
            buf = [buf[-1]]
            buf_tokens = len(_ENC.encode(buf[0]))
        buf.append(sentence)
        buf_tokens += n
    if buf:
        chunks.append(" ".join(buf))
    return chunks
