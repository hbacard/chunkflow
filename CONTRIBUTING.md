# Contributing to ChunkFlow

Thanks for your interest in contributing! This document describes how to set up
the project for development and how to contribute changes.

## Development setup

Requirements: Python `>=3.12,<3.14`, [PDM](https://pdm-project.org) (the lockfile
is `pdm.lock`) and optionally [Docker](https://www.docker.com/) for Qdrant.

```bash
git clone git@github.com:hbacard/chunkflow.git
cd chunkflow

# Install the package with dev dependencies
pdm install -G dev

# Optional: start Qdrant for the ingester integration tests
python -m pip install pdm
docker compose up -d            # or: docker compose up -d qdrant
```

## Development workflow

1. **Create a branch** off `main`: `git checkout -b feat/your-feature`
2. **Make your change** and add tests under `tests/` (pytest).
3. **Run the checks** before pushing:

   ```bash
   pdm run ruff check .
   pdm run ruff format --check .
   pdm run python -m pytest
   ```

   The CI workflow runs exactly these commands (see `.github/workflows/ci.yml`).
4. **Keep the changelog updated**: add a bullet under the appropriate section of
   `CHANGELOG.md`.
5. **Open a pull request** against `main`, filling in the PR template.

## Code style

- **Formatting/linting**: [ruff](https://docs.astral.sh/ruff/) — format with
  `pdm run ruff format .` and lint with `pdm run ruff check .`
- **Type hints**: modern Python (`X | None`, built-in generics).
- **Docstrings**: NumPy style on public functions/classes.

## Commit messages

Use conventional prefixes, e.g. `feat:`, `fix:`, `docs:`, `chore:`,
`test:`, `refactor:`.

## Reporting issues / vulnerabilities

- Bugs and feature requests: open an issue using the issue templates.
- Security vulnerabilities: see `SECURITY.md` for the private reporting process.
