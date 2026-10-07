#!/usr/bin/env python3
"""Render APPLICATION.md with checklist checkboxes (template maintenance)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checklist_tracking import issue_token_placeholder

ROOT = Path(__file__).resolve().parent.parent


def load_artifacts(root: Path = ROOT):
    form = json.loads((root / ".github/cncf-form.json").read_text())
    labels = json.loads((root / "scripts/checklist_checkbox_labels.json").read_text())
    placeholders = json.loads((root / "scripts/application_field_placeholders.json").read_text())
    guides = json.loads((root / "scripts/application_field_guides.json").read_text())
    return form, labels, placeholders, guides


def slug_primary_field(form: dict) -> dict[str, str]:
    primary: dict[str, str] = {}
    for section in form["sections"]:
        for field in section["fields"]:
            for slug in field.get("checklist", []):
                primary.setdefault(slug, field["id"])
    return primary


def checkbox_field_ids(form: dict) -> set[str]:
    return {
        field["id"]
        for section in form["sections"]
        for field in section["fields"]
        if field.get("type") == "checkbox"
    }


def checklist_line(slug: str, labels: dict[str, str]) -> str:
    label = labels[slug]
    return f"- [ ] {label} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"


def emit_guide(lines: list[str], field_id: str, guides: dict[str, str]) -> None:
    guide = guides.get(field_id, "").strip()
    if not guide:
        return
    lines.append("<!-- field-guide:start -->")
    lines.extend(guide.splitlines())
    lines.append("<!-- field-guide:end -->")
    lines.append("")


def form_option_label(form: dict, field_id: str) -> str:
    for section in form["sections"]:
        for field in section["fields"]:
            if field["id"] == field_id:
                return field.get("option_label") or field.get("label") or field_id
    return field_id


def render(root: Path = ROOT) -> str:
    form, labels, placeholders, guides = load_artifacts(root)
    primary = slug_primary_field(form)
    checkboxes = checkbox_field_ids(form)
    lines = [
        "# CNCF Sandbox Application",
        "",
        "Single source of truth for the CNCF sandbox application. Each `## field_id` section maps to the [official CNCF application form](https://github.com/cncf/sandbox/blob/main/.github/ISSUE_TEMPLATE/application.yml).",
        "",
        "**Work here only:** Each checklist line shows `(Issue: …)` until you open a PR with `Closes #N`; automation then checks the box and shows `(PR: …)` here and in [README.md](README.md). Edit answers below; do not edit README or toggle checklist boxes yourself.",
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
            emit_guide(lines, field_id, guides)
            if field_id in checkboxes:
                text = placeholders.get(field_id) or form_option_label(form, field_id)
                lines.append(
                    f"- [ ] {text} <!-- checklist:{slug} --> {issue_token_placeholder(slug)}"
                )
            else:
                lines.append(checklist_line(slug, labels))
            lines.append("")
            emitted_slugs.add(slug)
        if field_id in checkboxes:
            if show_slug:
                lines.append(
                    "**Your answer:** (check the box above; add notes below if needed)"
                )
                lines.append("")
                lines.append("_Optional notes._")
                lines.append("")
            return

        body = placeholders.get(field_id, "")
        if not body:
            return
        if show_slug and body.startswith("_"):
            lines.append("**Your answer:**")
            lines.append("")
        lines.append(body)
        lines.append("")

    add_section("read_prerequisites", "read-prerequisites")

    for section in form["sections"]:
        for field in section["fields"]:
            field_id = field["id"]
            slugs = field.get("checklist", [])
            slug = slugs[0] if slugs and primary.get(slugs[0]) == field_id else None
            add_section(field_id, slug)

    add_section("final_review", "final-review")
    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    out = ROOT / "APPLICATION.md"
    out.write_text(render())
    print(f"Wrote {out}")
    print(
        "Warning: this overwrites APPLICATION.md. Prefer "
        "`./scripts/sync-cncf-form.sh --write --merge-application`.",
        file=sys.stderr,
    )
