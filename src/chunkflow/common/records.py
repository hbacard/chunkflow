from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Section:
    text: str
    heading_path: str
    page_number: int | None
    source_file: str


def parent_record(section: Section, source_url: str | None, token_count: int) -> dict:
    return {
        "id": str(uuid4()),
        "text": section.text,
        "chunk_type": "parent",
        "source_file": section.source_file,
        "source_url": source_url,
        "page_number": section.page_number,
        "heading_path": section.heading_path,
        "parent_id": None,
        "token_count": token_count,
    }


def child_record(parent: dict, text: str, child_index: int, token_count: int) -> dict:
    return {
        "id": str(uuid4()),
        "text": text,
        "chunk_type": "child",
        "source_file": parent["source_file"],
        "source_url": parent["source_url"],
        "page_number": parent["page_number"],
        "heading_path": parent["heading_path"],
        "parent_id": parent["id"],
        "child_index": child_index,
        "token_count": token_count,
    }
