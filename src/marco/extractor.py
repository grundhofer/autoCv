"""Extract text from DOCX and PDF files as Markdown."""

from __future__ import annotations

import warnings
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
import pdfplumber


def extract(path: Path) -> str:
    """Auto-detect file type and extract text as Markdown."""
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    raise ValueError(f"Unsupported file type: {suffix}")


# ---------------------------------------------------------------------------
# DOCX extraction
# ---------------------------------------------------------------------------

def extract_docx(path: Path) -> str:
    """Read a DOCX file and convert its content to Markdown."""
    doc = docx.Document(str(path))
    lines: list[str] = []

    for block in doc.iter_inner_content():
        if isinstance(block, Paragraph):
            lines.append(_paragraph_to_md(block))
        elif isinstance(block, Table):
            lines.append(_table_to_md(block))

    return "\n".join(lines)


def _paragraph_to_md(para: Paragraph) -> str:
    """Convert a single paragraph to a Markdown line."""
    text = para.text.strip()
    if not text:
        return ""

    style_name = (para.style.name or "").lower()

    # Headings
    if style_name.startswith("heading"):
        try:
            level = int(style_name.replace("heading", "").strip())
        except ValueError:
            level = 1
        return f"{'#' * level} {text}"

    # Bullet / list items
    num_pr = para._element.find(qn("w:pPr"))
    if num_pr is not None and num_pr.find(qn("w:numPr")) is not None:
        ilvl_el = num_pr.find(qn("w:numPr")).find(qn("w:ilvl"))
        indent = int(ilvl_el.get(qn("w:val"))) if ilvl_el is not None else 0
        return f"{'  ' * indent}- {text}"

    return text


def _table_to_md(table: Table) -> str:
    """Convert a DOCX table to a Markdown table."""
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
        rows.append("| " + " | ".join(cells) + " |")

    if len(rows) >= 1:
        # Add separator after header row
        col_count = len(table.rows[0].cells)
        sep = "| " + " | ".join(["---"] * col_count) + " |"
        rows.insert(1, sep)

    return "\n".join(rows)


# ---------------------------------------------------------------------------
# PDF extraction
# ---------------------------------------------------------------------------

def extract_pdf(path: Path) -> str:
    """Read a PDF file and extract text as Markdown."""
    pages: list[str] = []

    with pdfplumber.open(str(path)) as pdf:
        if not pdf.pages:
            warnings.warn(f"PDF has no pages: {path}")
            return ""

        for i, page in enumerate(pdf.pages):
            parts: list[str] = []

            text = page.extract_text(use_text_flow=True)
            if text:
                parts.append(text)

            tables = page.extract_tables()
            for table in tables:
                parts.append(_pdf_table_to_md(table))

            if not parts:
                warnings.warn(
                    f"Page {i + 1} of {path.name} has no extractable text "
                    "(may be image-based/scanned)."
                )

            pages.append("\n".join(parts))

    return "\n\n".join(pages)


def _pdf_table_to_md(table: list[list[str | None]]) -> str:
    """Convert a pdfplumber table to a Markdown table."""
    rows = []
    for row in table:
        cells = [(cell or "").strip().replace("\n", " ") for cell in row]
        rows.append("| " + " | ".join(cells) + " |")

    if len(rows) >= 1:
        col_count = len(table[0])
        sep = "| " + " | ".join(["---"] * col_count) + " |"
        rows.insert(1, sep)

    return "\n".join(rows)
