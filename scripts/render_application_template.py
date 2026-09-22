#!/usr/bin/env python3
"""Render APPLICATION.md with checklist checkboxes (template maintenance)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist_tracking import issue_token_placeholder

ROOT = Path(__file__).resolve().parent.parent
FORM = json.loads((ROOT / ".github/cncf-form.json").read_text())
LABELS = json.loads((ROOT / "scripts/checklist_checkbox_labels.json").read_text())
PLACEHOLDERS = json.loads((ROOT / "scripts/application_field_placeholders.json").read_text())
GUIDES = json.loads((ROOT / "scripts/application_field_guides.json").read_text())

# First field id per checklist slug (form field order)
SLUG_PRIMARY_FIELD: dict[str, str] = {}
for section in FORM["sections"]:
    for field in section["fields"]:
        for slug in field.get("checklist", []):
            SLUG_PRIMARY_FIELD.setdefault(slug, field["id"])

CHECKBOX_FIELDS = {"not_reference_architecture", "trademark_agreement", "ip_policy_agreement"}


def checklist_line(slug: str) -> str:
    label = LABELS[slug]
    return f"- [ ] {label} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"


def emit_guide(lines: list[str], field_id: str) -> None:
    guide = GUIDES.get(field_id, "").strip()
    if not guide:
        return
    lines.append("<!-- field-guide:start -->")
    lines.extend(guide.splitlines())
    lines.append("<!-- field-guide:end -->")
    lines.append("")


def render() -> str:
    lines = [
        "# CNCF Sandbox Application",
        "",
        "Single source of truth for the CNCF sandbox application. Each `## field_id` section maps to the [official CNCF application form](https://github.com/cncf/sandbox/blob/main/.github/ISSUE_TEMPLATE/application.yml).",
        "",
        "**Work here only:** Each checklist line shows `(Issue: …)` until you open a PR; automation then shows `(PR: …)` in this file and in [README.md](README.md). Edit answers below; do not edit README for application content.",
        "",
        "Run `./scripts/generate-submission.sh` when ready to submit to CNCF.",
        "",
        "> **Privacy note:** If this repository is public, do not commit private contact emails. Store sensitive contact details locally and fill them in only when generating or submitting the final issue.",
        "",
        "---",
        "",
    ]

    emitted_slugs: set[str] = set()

    def add_section(field_id: str, slug: str | None = None) -> None:
        lines.append(f"## {field_id}")
        lines.append("")
        show_slug = slug and slug not in emitted_slugs
        if show_slug:
            emit_guide(lines, field_id)
            if field_id in CHECKBOX_FIELDS:
                text = PLACEHOLDERS[field_id]
                lines.append(
                    f"- [ ] {text} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"
                )
            else:
                lines.append(checklist_line(slug))
            lines.append("")
            emitted_slugs.add(slug)
        if field_id in CHECKBOX_FIELDS:
            if show_slug:
                lines.append(
                    "**Your answer:** (check the box above; add notes below if needed)"
                )
                lines.append("")
                lines.append("_Optional notes._")
                lines.append("")
            return

        body = PLACEHOLDERS.get(field_id, "")
        if not body:
            return
        if show_slug and body.startswith("_"):
            lines.append("**Your answer:**")
            lines.append("")
        lines.append(body)
        lines.append("")

    add_section("read_prerequisites", "read-prerequisites")

    for section in FORM["sections"]:
        for field in section["fields"]:
            field_id = field["id"]
            slugs = field.get("checklist", [])
            slug = slugs[0] if slugs and SLUG_PRIMARY_FIELD.get(slugs[0]) == field_id else None
            add_section(field_id, slug)

    add_section("final_review", "final-review")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    out = ROOT / "APPLICATION.md"
    out.write_text(render())
    print(f"Wrote {out}")
