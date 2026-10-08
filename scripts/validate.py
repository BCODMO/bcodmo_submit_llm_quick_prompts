#!/usr/bin/env python3
"""Checks quick-prompts.json and the prompts/ folder the same way the
submission API does, so a mistake is caught by the GitHub Action before a data
manager presses Refresh. Run it from the repository root."""
import json
import re
import sys
from pathlib import Path

PROMPTS = Path("prompts")
FILE_SELECTIONS = ("none", "parameterFiles", "keep")


def fail(message):
    sys.exit(f"ERROR: {message}")


try:
    with open("quick-prompts.json") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    fail(f"quick-prompts.json is not valid JSON: {e}")

prompts = data.get("quickPrompts")
if not isinstance(prompts, list) or not prompts:
    fail('quick-prompts.json must have a non-empty "quickPrompts" list')

seen = set()
for i, p in enumerate(prompts):
    where = f"quickPrompts[{i}]"
    if not isinstance(p, dict):
        fail(f"{where}: must be an object")
    if "id" in p:
        where = f'quick prompt "{p["id"]}"'
    for key in ("id", "label"):
        if not isinstance(p.get(key), str) or not p[key].strip():
            fail(f"{where}: {key} is required")
    if not re.fullmatch(r"[a-z0-9_]+", p["id"]):
        fail(f"{where}: id must be lowercase letters, numbers and underscores")
    if p["id"] in seen:
        fail(f"{where}: duplicate id")
    seen.add(p["id"])
    if "prompt" in p:
        fail(f"{where}: the prompt text belongs in prompts/{p['id']}.txt, not in the JSON")
    if p.get("fileSelection", "none") not in FILE_SELECTIONS:
        fail(f"{where}: fileSelection must be one of {', '.join(FILE_SELECTIONS)}")
    for option in ("includePublications", "includePeople", "includeChecklist", "includeRedmineTicket"):
        if option in p and not isinstance(p[option], bool):
            fail(f"{where}: {option} must be true or false")
    text_file = PROMPTS / f"{p['id']}.txt"
    if not text_file.is_file():
        fail(f"{where}: {text_file} is missing")
    if not text_file.read_text(encoding="utf-8").strip():
        fail(f"{where}: {text_file} is empty")

orphans = sorted(f.name for f in PROMPTS.glob("*.txt") if f.stem not in seen)
if orphans:
    fail(f"prompts/ has files with no entry in quick-prompts.json: {', '.join(orphans)}. "
         "Add an entry for each, or delete them.")

print(f"{len(prompts)} quick prompts OK")
