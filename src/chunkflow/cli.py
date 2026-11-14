"""Command-line entrypoint exposing the 3-stage chunkflow pipeline (chunk/embed/ingest)."""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()

COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "docs_rag")


def main(argv=None) -> None:
    """Parse CLI arguments and dispatch to the matching stage runner.

    Parameters
    ----------
    argv : list[str] | None
        Optional argument list; defaults to ``sys.argv[1:]``.
    """
    parser = argparse.ArgumentParser(
        prog="chunkflow", description="3-stage parent-child chunking pipeline"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_chunk = sub.add_parser(
        "chunk", help="Stage 1: split docs into parent/child chunks"
    )
    p_chunk.add_argument("--input", required=True, help="directory of .md/.pdf files")
    p_chunk.add_argument("--output", required=True, help="output chunks.json path")
    p_chunk.add_argument(
        "--url-mapping",
        default=None,
        help="JSON file mapping source_file -> source_url",
    )
    p_chunk.set_defaults(run=_run_chunk)

    p_embed = sub.add_parser("embed", help="Stage 2: embed child chunks")
    p_embed.add_argument("--input", required=True, help="input chunks.json path")
    p_embed.add_argument(
        "--output", required=True, help="output embedded_chunks.json path"
    )
    p_embed.set_defaults(run=_run_embed)

    p_ingest = sub.add_parser("ingest", help="Stage 3: upsert into Qdrant")
    p_ingest.add_argument(
        "--input", required=True, help="input embedded_chunks.json path"
    )
    p_ingest.add_argument(
        "--collection", default=COLLECTION_NAME, help="Qdrant collection name"
    )
    p_ingest.add_argument(
        "--url",
        default=os.environ.get("QDRANT_URL", "http://localhost:6333"),
        help="Qdrant REST URL",
    )
    p_ingest.set_defaults(run=_run_ingest)

    args = parser.parse_args(argv)
    args.run(args)


def _run_chunk(args) -> None:
    """Run the chunk stage (Stage 1) from parsed CLI args.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments with ``input``, ``output`` and ``url_mapping``.
    """
    from chunkflow.chunker.__main__ import run

    run(input_dir=args.input, output=args.output, url_mapping=args.url_mapping)


def _run_embed(args) -> None:
    """Run the embed stage (Stage 2) from parsed CLI args.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments with ``input`` and ``output``.
    """
    from chunkflow.embedder.embed import run

    run(input_path=args.input, output_path=args.output)


def _run_ingest(args) -> None:
    """Run the ingest stage (Stage 3) from parsed CLI args.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments with ``input``, ``collection`` and ``url``.
    """
    import asyncio

    from chunkflow.ingester.ingest import run

    asyncio.run(run(input_path=args.input, collection=args.collection, url=args.url))


if __name__ == "__main__":
    main()
