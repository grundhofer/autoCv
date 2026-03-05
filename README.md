# Marco — CV Format Converter

Marco takes a CV (PDF or Word document) and converts it into a professionally formatted corporate Word document using AI.

**What it does:** You provide a candidate's CV in any format, and Marco reads it, extracts all the relevant information (work experience, skills, education, etc.), and fills it into a clean corporate template — ready to send to clients.

## Prerequisites

- **Python 3.10+** installed on your machine
- **Claude Code CLI** installed and authenticated (Marco uses Claude to read and understand the CV)
- An **Anthropic API key** set up in your Claude Code CLI

## Setup

Open a terminal in the project folder and run:

```bash
pip install -e .
```

This installs Marco and all its dependencies.

## How to Use

### Basic usage

```bash
marco input/candidate_cv.pdf template/corporate.docx output/candidate_name.docx
```

This takes three things:
1. **Input file** — the candidate's CV (`.pdf` or `.docx`)
2. **Template** — the corporate template to fill in (use `template/corporate.docx`)
3. **Output file** — where to save the result

### Save the extracted data as JSON

If you also want a JSON file with all the extracted data (useful for review or debugging):

```bash
marco input/candidate_cv.pdf template/corporate.docx output/candidate_name.docx --json output/candidate_name.json
```

### Example

```bash
marco input/CV_MatheusAlves.pdf template/corporate.docx output/matheus_alves.docx --json output/matheus_alves.json
```

After running this, open `output/matheus_alves.docx` in Word to review the result.

## Project Structure

```
input/          → Place candidate CVs here (not tracked in git)
output/         → Generated documents appear here (not tracked in git)
template/       → Corporate Word templates with placeholder tags
src/marco/      → Source code
```
