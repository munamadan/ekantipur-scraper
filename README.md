# Ekantipur Scraper

This project scrapes data from `https://ekantipur.com` using Python and Playwright.

It extracts:
- Top 5 entertainment news items
- Cartoon of the day

The script writes the result to `output.json`.

## Requirements

- Python 3.11 or newer
- `uv` package manager

## Setup

1. Clone the repository and go into the project folder.
2. Install `uv` (if not installed):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

3. Install project dependencies:

```bash
uv sync
```

4. Install Playwright Chromium browser:

```bash
uv run playwright install chromium
```

## Run

Run the scraper:

```bash
uv run python scraper.py
```

After running, check `output.json` in the project root.

## Notes

- If some fields are missing on the website, the script writes `null` for those values.
- If scraping fails, the script still writes valid JSON with fallback empty values.
