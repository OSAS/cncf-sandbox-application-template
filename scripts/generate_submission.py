#!/usr/bin/env python3
"""Generate CNCF-SUBMISSION.md from APPLICATION.md."""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List


CHECKLIST_LINE = re.compile(r"^- \[[ xX]\].*<!-- checklist:[a-z0-9-]+ -->.*$")
FIELD_GUIDE = re.compile(
    r"<!-- field-guide:start -->.*?<!-- field-guide:end -->\n*",
    re.DOTALL,
)
YOUR_ANSWER = re.compile(r"^\*\*Your answer:\*\*.*\n*", re.MULTILINE)


TRACKING_SUFFIX = re.compile(r" \((Issue|PR):.*\)\s*$")


def strip_template_lines(body: str) -> str:
    body = FIELD_GUIDE.sub("", body)
    body = YOUR_ANSWER.sub("", body)
    lines = []
    for line in body.splitlines():
        if CHECKLIST_LINE.match(line.strip()):
            continue
        if line.strip() == "_Optional notes._":
            continue
        lines.append(TRACKING_SUFFIX.sub("", line))
    return "\n".join(lines).strip()


def strip_checklist_lines(body: str) -> str:
    lines = [
        line
        for line in body.splitlines()
        if not CHECKLIST_LINE.match(line.strip())
    ]
    return "\n".join(lines).strip()


def parse_answers(text: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {}
    current = None
    for line in text.splitlines():
        match = re.match(r"^## ([a-z0-9_]+)\s*$", line)
        if match:
            current = match.group(1)
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {
        field_id: strip_template_lines("\n".join(lines))
        for field_id, lines in sections.items()
    }


def is_checkbox_checked(value: str) -> bool:
    return bool(re.search(r"^\s*-\s*\[[xX]\]", value, re.MULTILINE))


def is_empty(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    if stripped.startswith("_") and stripped.endswith("_"):
        return True
    non_checkbox_lines = [
        line
        for line in stripped.splitlines()
        if not re.match(r"^\s*-\s*\[[ xX]\]", line)
    ]
    if not non_checkbox_lines:
        return not is_checkbox_checked(stripped)
    return all(
        line.strip().startswith("_") and line.strip().endswith("_")
        for line in non_checkbox_lines
        if line.strip()
    )


def main() -> int:
    form_file = Path(os.environ["FORM_FILE"])
    answers_file = Path(os.environ["ANSWERS_FILE"])
    output_file = Path(os.environ["OUTPUT_FILE"])
    validate = os.environ.get("VALIDATE", "false") == "true"

    form = json.loads(form_file.read_text())
    answers = parse_answers(answers_file.read_text())

    missing: List[str] = []
    out: List[str] = [
        "# Sandbox Application form",
        "",
        (
            "Please fill out the form below as completely as possible. "
            "This information will help facilitate the review by the CNCF TOC "
            "and a Technical Advisory Group (TAG) by minimizing follow-up questions."
        ),
        "",
    ]

    for section in form["sections"]:
        out.append(section["heading"])
        out.append("")
        if section.get("intro"):
            out.append(section["intro"])
            out.append("")
        for field in section["fields"]:
            field_id = field["id"]
            label = field["label"]
            value = answers.get(field_id, "").strip()
            field_type = field.get("type", "text")

            if field.get("required") and is_empty(value):
                missing.append(field_id)

            out.append(f"### {label}")
            out.append("")
            if field_type == "checkbox":
                if is_checkbox_checked(value):
                    out.append(f"- [x] {label}")
                else:
                    out.append(f"- [ ] {label}")
                    if validate and field.get("required"):
                        missing.append(field_id)
            else:
                out.append(value if value else "_Not provided_")
            out.append("")

    output_file.write_text("\n".join(out).rstrip() + "\n")

    if validate and missing:
        unique_missing = sorted(set(missing))
        print("Error: required fields are missing or still contain placeholders:", file=sys.stderr)
        for field_id in unique_missing:
            print(f"  - {field_id} (see APPLICATION.md)", file=sys.stderr)
        return 1

    print(f"Wrote {output_file}")
    return 0


def record_submission_links(root: Path, issue_url: str) -> None:
    readme = root / "README.md"
    if readme.is_file():
        content = readme.read_text(encoding="utf-8")
        content = re.sub(
            r"> \*\*Official CNCF application issue:\*\*[^\n]*",
            f"> **Official CNCF application issue:** {issue_url}",
            content,
            count=1,
        )
        readme.write_text(content, encoding="utf-8")

    application = root / "APPLICATION.md"
    if application.is_file():
        sys.path.insert(0, str(root / "scripts"))
        from apply_project_info import set_application_field  # noqa: WPS433

        application.write_text(
            set_application_field(
                application.read_text(encoding="utf-8"),
                "final_review",
                f"CNCF sandbox application submitted: {issue_url}",
            ),
            encoding="utf-8",
        )
        sys.path.insert(0, str(root / "scripts"))
        from checklist_tracking import sync_readme_dashboard  # noqa: WPS433

        sync_readme_dashboard(root)


if __name__ == "__main__":
    raise SystemExit(main())
