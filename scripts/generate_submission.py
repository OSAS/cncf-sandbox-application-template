#!/usr/bin/env python3
"""Generate CNCF-SUBMISSION.md from APPLICATION.md.

By default prefers the live CNCF sandbox application.yml so submission matches
the current official form. Applicants do not need to sync their worksheet.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def parse_raw_sections(text: str) -> Dict[str, str]:
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
    return {field_id: "\n".join(lines) for field_id, lines in sections.items()}


def parse_answers(text: str) -> Dict[str, str]:
    return {
        field_id: strip_template_lines(body)
        for field_id, body in parse_raw_sections(text).items()
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


def load_form(
    root: Path,
    local_form_path: Path,
    prefer_live: bool,
    require_live: bool,
) -> Tuple[dict, Optional[str]]:
    """Return (form, status_message)."""
    local_form = json.loads(local_form_path.read_text(encoding="utf-8"))
    if not prefer_live and not require_live:
        return local_form, None

    scripts = str(root / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)

    try:
        from sync_cncf_form import DEFAULT_URL, fetch_compiled_form
    except ImportError as exc:
        if require_live:
            print(
                "Error: could not load live CNCF form helper "
                f"({exc}). Install deps with: pip install -r requirements-dev.txt",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return local_form, "Using local form snapshot (live form helper unavailable)."

    try:
        compiled, unmatched, diff = fetch_compiled_form(root, DEFAULT_URL)
    except Exception as exc:  # noqa: BLE001
        if require_live:
            print(
                "Error: could not fetch the live CNCF application form.\n"
                f"  {exc}\n"
                "Check your network connection and re-run.",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return local_form, f"Using local form snapshot (live fetch failed: {exc})."

    if unmatched:
        print(
            "Error: the live CNCF form has fields this repository does not recognize yet:",
            file=sys.stderr,
        )
        for item in unmatched:
            print(f"  - {item}", file=sys.stderr)
        print(
            "\nAdd a mapping in scripts/cncf_field_aliases.json, or pull the latest "
            "template updates, then re-run.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    added = diff.get("added") or []
    notice_parts = ["Using live CNCF application form."]
    if added:
        notice_parts.append(
            "New upstream fields: " + ", ".join(added) + "."
        )
    return compiled, " ".join(notice_parts)


def render_submission(
    form: dict,
    answers: Dict[str, str],
    raw_sections: Dict[str, str],
    validate: bool,
) -> Tuple[str, List[str], List[str]]:
    missing: List[str] = []
    unknown_required: List[str] = []
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
            in_application = field_id in raw_sections

            if field.get("required") and field_type != "checkbox" and is_empty(value):
                missing.append(field_id)
                if not in_application:
                    unknown_required.append(field_id)

            out.append(f"### {label}")
            out.append("")
            if field_type == "checkbox":
                box_label = field.get("option_label") or label
                raw_value = raw_sections.get(field_id, value)
                if is_checkbox_checked(raw_value) or is_checkbox_checked(value):
                    out.append(f"- [x] {box_label}")
                else:
                    out.append(f"- [ ] {box_label}")
                    if validate and field.get("required"):
                        missing.append(field_id)
                        if not in_application:
                            unknown_required.append(field_id)
            else:
                out.append(value if value else "_Not provided_")
            out.append("")

    return "\n".join(out).rstrip() + "\n", missing, unknown_required


def main() -> int:
    form_file = Path(os.environ["FORM_FILE"])
    answers_file = Path(os.environ["ANSWERS_FILE"])
    output_file = Path(os.environ["OUTPUT_FILE"])
    meta_file = Path(
        os.environ.get("FORM_META_FILE", str(output_file) + ".meta.json")
    )
    validate = os.environ.get("VALIDATE", "false") == "true"
    prefer_live = os.environ.get("PREFER_LIVE_FORM", "true") == "true"
    require_live = os.environ.get("REQUIRE_LIVE_FORM", "false") == "true"
    root = Path(os.environ.get("ROOT_DIR", form_file.resolve().parent.parent))

    form, notice = load_form(root, form_file, prefer_live, require_live)
    if notice:
        print(notice, file=sys.stderr, flush=True)

    raw_answers = answers_file.read_text(encoding="utf-8")
    answers = parse_answers(raw_answers)
    raw_sections = parse_raw_sections(raw_answers)

    body, missing, unknown_required = render_submission(
        form, answers, raw_sections, validate
    )
    output_file.write_text(body, encoding="utf-8")
    meta_file.write_text(
        json.dumps(
            {
                "title_prefix": form.get("title_prefix", "[Sandbox]"),
                "issue_labels": form.get("issue_labels", ["New"]),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if validate and missing:
        unique_missing = sorted(set(missing))
        unique_unknown = sorted(set(unknown_required))
        print(
            "Error: required fields are missing or still contain placeholders:",
            file=sys.stderr,
        )
        for field_id in unique_missing:
            if field_id in unique_unknown:
                print(
                    f"  - {field_id} — new on the live CNCF form; "
                    f"add a `## {field_id}` section in APPLICATION.md and fill it in",
                    file=sys.stderr,
                )
            else:
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
