# Multi-LCB (Multi LiveCodeBench)

A static leaderboard website for multilingual code generation benchmarks. Deployed on GitHub Pages.

## Project Structure

```
index.html          — Single-page app (HTML + JS + CSS)
data/
  lcb/              — Main benchmark dataset
  lcb_pro/          — LCB-PRO dataset
  lcb_agentic/      — LCB-PRO-AGENTIC dataset
content/            — Markdown content (multilingual: en, ru, cn, he)
utils/
  generate_index.py — Script to regenerate index.json manifests
```

## Adding a New Model

1. Create a folder: `data/<dataset>/<ModelName>/`
2. Place `.jsonl` files for each language (e.g. `python.jsonl`, `cpp.jsonl`, `rust.jsonl`, etc.)
3. Optionally add `meta.json` with model hyperparameters (shown as tooltip)
4. Run the index generator:

```bash
python utils/generate_index.py
```
5. Test it localy via 
```bash
python -m http.server 8000
```
6. Commit and push. GitHub Pages will deploy automatically.

## JSONL Format

Each `.jsonl` file contains one JSON object per line:

```json
{"task_id": "abc123", "date": "2025-04-01", "pass": 0.85, "difficulty": "M", "platform": "leetcode"}
```

## Deployment

The site is hosted via GitHub Pages from the `main` branch. No build step required — it's a static HTML file.

## Local Development

Just open `index.html` in a browser, or serve with any static server:

```bash
python -m http.server 8000
```
