# Data management plan (DMP)

ChunkFlow processes Markdown/PDF documents into chunk records and embeddings,
and stores them in a Qdrant collection. It does not collect personal data.

## Data handled

| Data | Type | Producer | Stored where |
|------|------|----------|--------------|
| Input documents | `.md` / `.pdf` files | User | Source-controlled repo or local filesystem |
| Chunk records | JSON (`chunks.json`) | Stage 1 | Local filesystem (gitignored: `*chunks.json`) |
| Embedded records | JSON (`embedded_chunks.json`) | Stage 2 | Local filesystem (gitignored: `*_embeddings.json`) |
| Vector index | Qdrant points | Stage 3 | Qdrant `qdrant_data` volume |

## Preservation & retention

- Generated chunk/embedding files are intentionally **not** committed (see
  `.gitignore`) — they are derived data and can be regenerated from the input
  documents with the documented pipeline. If you need to redistribute them,
  archive them on a platform such as Zenodo together with the exact version
  (`pdm.lock`) used to produce them.
- Qdrant data persists in the `qdrant_data` Docker volume; back it up if the
  collection is authoritative.

## Provenance

- Every record carries `source_file`, `source_url` (when provided via
  `--url-mapping`) and `page_number`, so each chunk can be traced to its source.
- The pipeline version is tracked via version tags; combine the tag with
  `pdm.lock` to reproduce a given dataset.

## Compliance

- No personal/sensitive data is processed by default. Users embedding documents
  containing personal data are responsible for compliance (e.g. GDPR) with their
  own embedding/Qdrant deployments.
