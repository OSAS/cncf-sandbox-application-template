#!/usr/bin/env python3
"""Rewrite APPLICATION.md from the current form while preserving answers."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist_tracking import (  # noqa: E402
    CHECKLIST_LINE,
    CHECKLIST_SLUG,
    TRACKING_SUFFIX,
    issue_token_placeholder,
)
from generate_submission import FIELD_GUIDE, is_empty  # noqa: E402
from render_application_template import render  # noqa: E402
from sync_readme_from_application import main as sync_readme  # noqa: E402
from update_checklist_progress import main as update_progress  # noqa: E402

HEADING = re.compile(r"^## ([a-z0-9_]+)\s*$")


def parse_sections(text: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None
    for line in text.splitlines():
        match = HEADING.match(line)
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {key: "\n".join(lines) for key, lines in sections.items()}


def extract_checklist_state(body: str) -> Dict[str, Tuple[bool, str]]:
    state: Dict[str, Tuple[bool, str]] = {}
    for line in body.splitlines():
        if not CHECKLIST_LINE.match(line.strip()):
            continue
        slug_match = CHECKLIST_SLUG.search(line)
        if not slug_match:
            continue
        slug = slug_match.group(1)
        checked = bool(re.match(r"^- \[[xX]\]", line.strip()))
        tracking_match = TRACKING_SUFFIX.search(line)
        tracking = tracking_match.group(0).strip() if tracking_match else ""
        state[slug] = (checked, tracking)
    return state


def extract_answer(body: str) -> str:
    body = FIELD_GUIDE.sub("", body)
    lines: List[str] = []
    for line in body.splitlines():
        if CHECKLIST_LINE.match(line.strip()) or "<!-- checklist:" in line:
            continue
        if line.strip().startswith("**Your answer"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def apply_checklist_state(text: str, state: Dict[str, Tuple[bool, str]]) -> str:
    lines: List[str] = []
    for line in text.splitlines():
        slug_match = CHECKLIST_SLUG.search(line)
        if not slug_match or not CHECKLIST_LINE.match(line.strip()):
            lines.append(line)
            continue
        slug = slug_match.group(1)
        if slug not in state:
            lines.append(line)
            continue
        checked, tracking = state[slug]
        mark = "x" if checked else " "
        stripped = TRACKING_SUFFIX.sub("", line).rstrip()
        stripped = re.sub(r"^- \[[ xX]\]", f"- [{mark}]", stripped, count=1)
        if tracking:
            stripped = f"{stripped} {tracking}"
        elif "(Issue:" not in stripped and "(PR:" not in stripped:
            stripped = f"{stripped} {issue_token_placeholder(slug)}"
        lines.append(stripped)
    return "\n".join(lines) + "\n"


def inject_answer(section_body: str, field_id: str, answer: str, checkbox: bool) -> str:
    if is_empty(answer):
        return section_body
    lines = section_body.splitlines()
    prefix: List[str] = []
    idx = 0
    while idx < len(lines) and lines[idx].strip() == "":
        prefix.append(lines[idx])
        idx += 1
    if idx < len(lines) and lines[idx].strip() == "<!-- field-guide:start -->":
        while idx < len(lines):
            prefix.append(lines[idx])
            if lines[idx].strip() == "<!-- field-guide:end -->":
                idx += 1
                break
            idx += 1
    while idx < len(lines) and lines[idx].strip() == "":
        prefix.append(lines[idx])
        idx += 1
    while idx < len(lines) and CHECKLIST_LINE.match(lines[idx]):
        prefix.append(lines[idx])
        idx += 1
    while idx < len(lines) and lines[idx].strip() == "":
        prefix.append(lines[idx])
        idx += 1

    out = list(prefix)
    if checkbox:
        out.append("**Your answer:** (check the box above; add notes below if needed)")
        out.append("")
        out.append(answer)
        out.append("")
    else:
        out.append("**Your answer:**")
        out.append("")
        out.append(answer)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def replace_section(text: str, field_id: str, new_body: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(field_id)}\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    body = new_body if new_body.endswith("\n") else new_body + "\n"
    return pattern.sub(lambda match: f"{match.group(1)}{body}", text, count=1)


def checkbox_ids(form: Dict) -> set[str]:
    return {
        field["id"]
        for section in form["sections"]
        for field in section["fields"]
        if field.get("type") == "checkbox"
    }


def merge_application(root: Path, orphan_path: Optional[Path] = None) -> None:
    application_path = root / "APPLICATION.md"
    form = json.loads((root / ".github" / "cncf-form.json").read_text(encoding="utf-8"))
    existing = application_path.read_text(encoding="utf-8") if application_path.is_file() else ""
    sections = parse_sections(existing)
    checklist_state: Dict[str, Tuple[bool, str]] = {}
    answers: Dict[str, str] = {}
    for field_id, body in sections.items():
        checklist_state.update(extract_checklist_state(body))
        answers[field_id] = extract_answer(body)

    keep_ids = {"read_prerequisites", "final_review"} | {
        field["id"] for section in form["sections"] for field in section["fields"]
    }
    orphans = {
        field_id: answer
        for field_id, answer in answers.items()
        if field_id not in keep_ids and not is_empty(answer)
    }
    if orphans and orphan_path is not None:
        lines = ["# Orphaned APPLICATION.md answers", ""]
        for field_id, answer in orphans.items():
            lines.append(f"## {field_id}")
            lines.append("")
            lines.append(answer)
            lines.append("")
        orphan_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        print(f"Wrote orphaned answers to {orphan_path}")

    rendered = render(root)
    rendered = apply_checklist_state(rendered, checklist_state)
    boxes = checkbox_ids(form)
    for field_id in keep_ids:
        if field_id not in answers:
            continue
        match = re.search(
            rf"(^## {re.escape(field_id)}\n)(.*?)(?=\n## |\Z)",
            rendered,
            re.MULTILINE | re.DOTALL,
        )
        if not match:
            continue
        new_body = inject_answer(
            match.group(2),
            field_id,
            answers[field_id],
            field_id in boxes,
        )
        rendered = replace_section(rendered, field_id, new_body)

    application_path.write_text(rendered if rendered.endswith("\n") else rendered + "\n")
    update_progress()
    sync_readme()


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    merge_application(root, root / "APPLICATION-orphaned-answers.md")
    print(f"Wrote {root / 'APPLICATION.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
