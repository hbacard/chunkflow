# Chunkflow — Implementation Milestones

Build of the pipeline from [_docs/plan.md](./plan.md), split into independently runnable/testable milestones. Each stage in the plan maps to one milestone.

Decisions locked: **pdm** (package manager), **argparse** (CLI), **pytest** (tests per milestone).

## M0 — Scaffold & infra

- `pdm add markdown-it-py pymupdf tiktoken qdrant-client httpx pytest`
- `src/chunkflow/{chunker,embedder,ingester,common}/__init__.py`, `cli.py` (argparse, subcommands `chunk|embed|ingest`)
- `docker-compose.yml` (qdrant image, 6333/6334, `qdrant_data` volume)
- `docker compose up -d` to verify Qdrant responds on `localhost:6333`

## M1 — Stage 1: chunker → `chunks.json`

- `common/records.py`: `Section(text, heading_path, page_number, source_file)` + parent/child record dicts (id, text, chunk_type, source_file, source_url, page_number, heading_path, parent_id, child_index, token_count)
- `chunker/parse.py`: MD via `markdown-it-py` (`heading_open` walk); PDF via `pymupdf` block font-size vs. document median → H1/H2… ; both emit `Section`
- `chunker/chunk.py`: sliding window, ≤1024 tokens, 10-15% overlap (`tiktoken`), parent + children with `parent_id`; `--url-mapping` sets `source_url` (null fallback)
- `chunker/__main__.py` for `chunkflow chunk --input --output --url-mapping`
- Tests: sample `.md` + `.pdf` fixtures → assert section detection, chunk sizes, overlap, parent linkage, URL mapping

## M2 — Stage 2: embedder → `embedded_chunks.json`

- `embedder/embed.py`: batch child texts via httpx → `/v1/embeddings` (`EMBEDDING_BASE_URL`, `EMBEDDING_MODEL` env); add `dense_vector` to children only; parents pass through
- Tests: mock HTTP endpoint (no real model needed)

## M3 — Stage 3: ingester → Qdrant

- `ingester/ingest.py`: `AsyncQdrantClient`; create collection (`dense` + `sparse` named vectors, size via env `EMBEDDING_DIM`) if absent; upsert parent points (zero dense vector, full text payload) + child points (client-side fastembed BM25 `SparseVector`)
- `ingester/retrieve.py`: hybrid query helper (RRF prefetch, `chunk_type="child"` filter → collect `parent_id` → `retrieve()`)
- Tests: against a test collection on local Qdrant (skip if not running) + payload shape asserts

## M4 — E2E + docs

- Run full pipeline on sample docs → verify hybrid search returns correct parents
- `README.md`: setup, Docker, env vars, CLI usage, JSON contract

## Sequencing

M0 → M1 → M2 → M3 are strict (each stage consumes the previous output); M4 last. Each milestone ends green on pytest + a runnable CLI.

## Ask me to commit after each milestone 

## Deferred / risks

- No retrieval API/server (not in plan — query helper only)
- No embedding-model fallback beyond env vars
- No Qdrant auth/SSL config
- Risk: PDF heading heuristics need real-doc calibration
- Risk: embedding dims must match the chosen embedding model
