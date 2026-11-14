"""Stage 1 runner: parse all .md/.pdf files in a directory and write chunk records."""

import json
from pathlib import Path

from chunkflow.chunker.chunk import chunk_sections
from chunkflow.chunker.parse import parse_file


def run(input_dir: str, output: str, url_mapping: str | None = None) -> None:
    """Chunk every supported file in ``input_dir`` and write the records to JSON.

    Parameters
    ----------
    input_dir : str
        Directory containing .md/.pdf files.
    output : str
        Path of the chunks.json file to write.
    url_mapping : str | None
        Optional path to a JSON file mapping source_file -> source_url.
    """
    mapping: dict[str, str] = {}
    if url_mapping:
        mapping = json.loads(Path(url_mapping).read_text(encoding="utf-8"))
    records: list[dict] = []
    for p in sorted(Path(input_dir).iterdir()):
        if p.suffix.lower() in (".md", ".pdf"):
            records.extend(chunk_sections(parse_file(p), mapping))
    Path(output).write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
