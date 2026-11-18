"""Shared data model and record builders for the chunk pipeline."""

import hashlib
from dataclasses import dataclass


def _stable_id(*parts: str) -> str:
    # deterministic id so re-ingesting the same doc upserts instead of duplicating
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()


@dataclass
class Section:
    """A contiguous block of document text under one heading path.

    Parameters
    ----------
    text : str
        Body text of the section.
    heading_path : str
        " > "-joined heading path from the document root.
    page_number : int | None
        Source page number (PDF only), else None.
    source_file : str
        File name the section was parsed from.
    """

    text: str
    heading_path: str
    page_number: int | None
    source_file: str


def parent_record(
    section: Section, text: str, source_url: str | None, token_count: int
) -> dict:
    """Build a parent chunk record from a section.

    Parameters
    ----------
    section : Section
        Section providing the parent's metadata (file, heading path, page).
    text : str
        Full merged text of the parent's sections.
    source_url : str | None
        Optional URL of the source file.
    token_count : int
        Number of tokens in the parent text.

    Returns
    -------
    dict
        Parent chunk record with a fresh id and ``chunk_type="parent"``.
    """
    return {
        "id": _stable_id(
            "parent",
            section.source_file,
            section.heading_path,
            str(section.page_number),
            text,
        ),
        "text": text,
        "chunk_type": "parent",
        "source_file": section.source_file,
        "source_url": source_url,
        "page_number": section.page_number,
        "heading_path": section.heading_path,
        "parent_id": None,
        "token_count": token_count,
    }


def child_record(parent: dict, text: str, child_index: int, token_count: int) -> dict:
    """Build a child chunk record linked to its parent record.

    Parameters
    ----------
    parent : dict
        Parent record the child belongs to.
    text : str
        Child chunk text.
    child_index : int
        Zero-based index of the child within its parent.
    token_count : int
        Number of tokens in the child text.

    Returns
    -------
    dict
        Child chunk record inheriting the parent's metadata with ``chunk_type="child"``.
    """
    return {
        "id": _stable_id("child", parent["id"], str(child_index), text),
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
