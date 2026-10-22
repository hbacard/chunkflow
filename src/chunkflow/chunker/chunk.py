import tiktoken

from chunkflow.common.records import Section, child_record, parent_record

CHUNK_TOKENS = 1024
OVERLAP_RATIO = 0.125
_ENC = tiktoken.get_encoding("cl100k_base")


def chunk_sections(sections: list[Section], url_map: dict[str, str] | None = None) -> list[dict]:
    url_map = url_map or {}
    records: list[dict] = []
    for section in sections:
        tokens = _ENC.encode(section.text)
        if not tokens:
            continue
        parent = parent_record(section, url_map.get(section.source_file), len(tokens))
        records.append(parent)
        for index, chunk in enumerate(_split(tokens)):
            records.append(child_record(parent, _ENC.decode(chunk), index, len(chunk)))
    return records


def _split(tokens: list[int]) -> list[list[int]]:
    step = CHUNK_TOKENS - int(CHUNK_TOKENS * OVERLAP_RATIO)
    chunks: list[list[int]] = []
    start = 0
    n = len(tokens)
    while start < n:
        end = min(start + CHUNK_TOKENS, n)
        chunks.append(tokens[start:end])
        if end == n:
            break
        start += step
    return chunks
