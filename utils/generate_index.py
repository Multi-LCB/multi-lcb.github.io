#!/usr/bin/env python3
"""
Generate index.json for each dataset (lcb, lcb_pro, lcb_agentic).

Scans subdirectories inside data/<dataset>/ and builds a manifest of models
and their available .jsonl language files.

Usage:
    python utils/generate_index.py
"""

import os
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(SCRIPT_DIR, "..", "data")

# Datasets to process
DATASETS = ["lcb", "lcb_pro", "lcb_agentic"]


def extract_language(filename):
    """Extract language name from filename like cpp_cot.jsonl, python_2025-04-06.jsonl, etc."""
    name = filename.replace('.jsonl', '')
    match = re.match(r'^([a-z]+)', name)
    if match:
        return match.group(1)
    return None


def generate_index_for_dataset(dataset_path):
    """Generate index.json content for a single dataset directory."""
    models = []

    if not os.path.isdir(dataset_path):
        print(f"  Skipping (not a directory): {dataset_path}")
        return None

    items = sorted(os.listdir(dataset_path))

    for item in items:
        model_path = os.path.join(dataset_path, item)

        # Skip non-directories and special files
        if not os.path.isdir(model_path):
            continue

        # Get all .jsonl files in the folder
        try:
            files = [f for f in os.listdir(model_path) if f.endswith('.jsonl')]
        except Exception as e:
            print(f"  Error reading folder {item}: {e}")
            continue

        if not files:
            continue

        # Build files dictionary
        files_dict = {}
        for file in sorted(files):
            lang = extract_language(file)
            if lang:
                files_dict[lang] = file

        if files_dict:
            models.append({
                "name": item,
                "files": files_dict
            })

    return {"models": models}


def main():
    print(f"Data root: {DATA_ROOT}\n")

    for dataset in DATASETS:
        dataset_path = os.path.join(DATA_ROOT, dataset)
        output_path = os.path.join(dataset_path, "index.json")

        print(f"Processing: {dataset}")
        index = generate_index_for_dataset(dataset_path)

        if index is None:
            continue

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Generated {output_path}")
            print(f"    Models: {len(index['models'])}")
        except Exception as e:
            print(f"  ✗ Error writing {output_path}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
