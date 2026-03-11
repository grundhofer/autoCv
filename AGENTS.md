# Marco — CV Format Converter

## Overview

Marco converts candidate CVs (PDF or DOCX) into professionally formatted corporate Word documents. It uses Claude AI for structured data extraction and docxtpl for template rendering.

## Setup

```bash
pip install -e .
```

Requires Python 3.10+ and the `claude` CLI (Claude Code) on PATH.

## Usage

```bash
marco <input_file> <template> <output> [--json <path>] [--model <model>]
```

Example:

```bash
marco input/CV_MatheusAlves.pdf template/corporate.docx output/matheus_alves.docx --json output/matheus_alves.json
```

- `--json` saves the extracted structured data as JSON
- `--model` selects the Claude model (default: `sonnet`)

## Project Structure

```
src/marco/
  cli.py        # Typer CLI entry point
  extractor.py  # PDF/DOCX → Markdown text extraction
  llm.py        # Claude Code CLI structured extraction
  renderer.py   # docxtpl template rendering
  schema.py     # Pydantic models (CVData, WorkExperience, etc.)
template/       # Corporate DOCX templates with Jinja2 tags
input/          # Input CV files (gitignored)
output/         # Generated documents (gitignored)
```

## Architecture

Three-step pipeline in `cli.py`:

1. **Extract text** (`extractor.py`) — converts PDF/DOCX to Markdown using pdfplumber / python-docx.
2. **LLM extraction** (`llm.py`) — sends Markdown to Claude via `claude -p` with `--json-schema` for structured output. Returns a validated `CVData` Pydantic model.
3. **Render template** (`renderer.py`) — fills a corporate DOCX template via docxtpl with the extracted data.

## Key Implementation Details

### CLAUDECODE env stripping

`llm.py` strips the `CLAUDECODE` env var before calling `claude -p` as a subprocess. This prevents the subprocess from detecting it is running inside Claude Code, which would change its behavior. Do not remove this.

```python
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
```

### Computed template fields

`renderer.py` enriches the context dict with computed fields before rendering:

- `date_range` on experience and education entries (e.g., "August 2020 – Present")
- `skills_joined` — comma-separated skills per category
- `skills_flat` — flat list of all skills for bullet rendering

### Structured output parsing

The `claude -p --output-format json` call returns a conversation array. The structured data lives in `messages[-1]["structured_output"]`. This is validated against the Pydantic schema.

## Conventions

- Python 3.10+, type hints throughout (`from __future__ import annotations`)
- Pydantic v2 for data models
- snake_case functions, PascalCase classes
- pathlib.Path for all file paths
- Each module has a docstring; functions have docstrings
- No tests yet — `tests/` directory exists but is empty

## Dependencies

- `python-docx` — DOCX reading
- `pdfplumber` — PDF text extraction
- `docxtpl` — Jinja2-based DOCX templating
- `pydantic` — data validation and schemas
- `typer` — CLI framework
- `hatchling` — build backend
