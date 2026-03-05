"""CLI entry point for Marco CV converter."""

import json
from pathlib import Path
from typing import Annotated, Optional

import typer

from .extractor import extract
from .llm import DEFAULT_MODEL, extract_cv_data
from .renderer import render

app = typer.Typer(help="Marco — CV format converter")


@app.command()
def convert(
    input_file: Annotated[
        Path,
        typer.Argument(help="Input CV file (.docx or .pdf)"),
    ],
    template: Annotated[
        Path,
        typer.Argument(help="Corporate DOCX template with Jinja2 tags"),
    ],
    output: Annotated[
        Path,
        typer.Argument(help="Output DOCX path"),
    ],
    json_out: Annotated[
        Optional[Path],
        typer.Option("--json", help="Save extracted JSON to this path"),
    ] = None,
    model: Annotated[
        str,
        typer.Option("--model", help="Claude model to use"),
    ] = DEFAULT_MODEL,
) -> None:
    """Convert a CV into the corporate template format."""
    # 1. Extract text
    typer.echo(f"Extracting text from {input_file.name} ...")
    markdown = extract(input_file)

    if not markdown.strip():
        typer.echo("Error: no text could be extracted from the input file.", err=True)
        raise typer.Exit(code=1)

    # 2. LLM structured extraction
    typer.echo(f"Extracting CV data via Claude ({model}) ...")
    cv_data = extract_cv_data(markdown, model=model)

    # 3. Optionally dump JSON
    if json_out is not None:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(
            json.dumps(cv_data.model_dump(), indent=2, ensure_ascii=False)
        )
        typer.echo(f"Saved extracted data to {json_out}")

    # 4. Render template
    typer.echo(f"Rendering template {template.name} ...")
    render(cv_data, template, output)
    typer.echo(f"Done! Output saved to {output}")
