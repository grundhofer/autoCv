"""Fill a corporate DOCX template with extracted CV data."""

from __future__ import annotations

from pathlib import Path

from docxtpl import DocxTemplate

from .schema import CVData


def render(cv: CVData, template_path: Path, output_path: Path) -> Path:
    """Render *cv* into the corporate template and write to *output_path*."""
    tpl = DocxTemplate(str(template_path))

    context = cv.model_dump()

    # Convenience: date ranges for experience entries
    for job in context.get("experience", []):
        end = job.get("end_date") or "Present"
        start = job.get("start_date") or ""
        job["date_range"] = f"{start} – {end}" if start else end

    # Convenience: date ranges for education entries
    for edu in context.get("education", []):
        end = edu.get("end_date") or ""
        start = edu.get("start_date") or ""
        if start and end:
            edu["date_range"] = f"{start} – {end}"
        else:
            edu["date_range"] = start or end or ""

    # Convenience: joined skills per category
    for cat in context.get("skills", []):
        cat["skills_joined"] = ", ".join(cat.get("skills", []))

    # Flat skills list for bullet rendering (one skill per line)
    skills_flat = []
    for cat in context.get("skills", []):
        skills_flat.extend(cat.get("skills", []))
    context["skills_flat"] = skills_flat

    tpl.render(context, autoescape=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tpl.save(str(output_path))
    return output_path
