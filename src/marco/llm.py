"""Claude Code CLI structured extraction of CV data."""

from __future__ import annotations

import json
import os
import subprocess

from .schema import CVData

DEFAULT_MODEL = "sonnet"

SYSTEM_PROMPT = """\
You are a CV data extraction specialist. Your task is to extract ALL information \
from the provided CV text into a structured format.

Rules:
- Extract every piece of information present — do not omit anything.
- Use reverse chronological order for experience and education (most recent first).
- Normalize date formats to "Month YYYY" where possible (e.g., "January 2020"). \
  If only a year is given, keep it as "YYYY". Keep "Present" or "current" for ongoing roles.
- If the CV is in a language other than English, translate all content to English.
- For skills, group them into logical categories (e.g., "Programming Languages", \
  "Frameworks", "Tools", "Soft Skills"). If the CV already groups them, preserve those groups.
- The summary should be the professional summary/profile from the CV. If none exists, \
  generate a brief one based on the CV content.
- For personal_info, split the full name into first_name and last_name if possible.
- Include ALL work experience entries, even short ones.
- For responsibilities, use concise bullet points. Each bullet should be a single \
  actionable statement.
"""


def extract_cv_data(
    markdown: str,
    *,
    model: str = DEFAULT_MODEL,
) -> CVData:
    """Send CV markdown to Claude Code CLI and get structured CVData back."""
    schema = json.dumps(CVData.model_json_schema())

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    result = subprocess.run(
        [
            "claude", "-p",
            "--output-format", "json",
            "--json-schema", schema,
            "--model", model,
            "--system-prompt", SYSTEM_PROMPT,
        ],
        input=f"Extract all data from this CV:\n\n{markdown}",
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )

    messages = json.loads(result.stdout)
    # --output-format json returns a conversation array;
    # the last entry (type=result) holds structured_output.
    data = messages[-1]["structured_output"]
    return CVData.model_validate(data)
