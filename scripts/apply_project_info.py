#!/usr/bin/env python3
"""Apply bootstrap project metadata to README.md and APPLICATION.md."""

import json
import os
import re
from pathlib import Path
from typing import Dict, List


CHECKLIST_LINE = re.compile(r"^- \[[ xX]\].*<!-- checklist:[a-z0-9-]+ -->.*$")
FIELD_GUIDE = re.compile(
    r"<!-- field-guide:start -->.*?<!-- field-guide:end -->\n*",
    re.DOTALL,
)


def section_prefix_lines(section_lines: List[str]) -> List[str]:
    """Preserve static guide blocks and checklist lines at the top of a section."""
    idx = 0
    preserved: List[str] = []

    # Sections usually start with a blank line after the ## heading.
    while idx < len(section_lines) and section_lines[idx].strip() == "":
        preserved.append(section_lines[idx])
        idx += 1

    if idx < len(section_lines) and section_lines[idx].strip() == "<!-- field-guide:start -->":
        while idx < len(section_lines):
            preserved.append(section_lines[idx])
            if section_lines[idx].strip() == "<!-- field-guide:end -->":
                idx += 1
                break
            idx += 1

    while idx < len(section_lines) and section_lines[idx].strip() == "":
        preserved.append(section_lines[idx])
        idx += 1

    while idx < len(section_lines) and CHECKLIST_LINE.match(section_lines[idx]):
        preserved.append(section_lines[idx])
        idx += 1

    if idx < len(section_lines) and section_lines[idx].strip() == "":
        preserved.append(section_lines[idx])
    return preserved


def set_application_field(content: str, field_id: str, value: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(field_id)}\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        body = value.strip()
        if not body:
            return match.group(0)

        section_lines = match.group(2).splitlines()
        preserved = section_prefix_lines(section_lines)

        new_section = "\n".join(preserved)
        if new_section and not new_section.endswith("\n"):
            new_section += "\n"
        if new_section:
            new_section += "\n"
        new_section += body + "\n"
        return f"{match.group(1)}{new_section}"

    return pattern.sub(repl, content, count=1)


def update_readme(content: str, metadata: Dict[str, str]) -> str:
    project_name = metadata["project_name"]
    content = content.replace(
        "> **Project name:** _Replace with your project name_",
        f"> **Project name:** {project_name}",
    )
    content = content.replace(
        "> **Checklist issues:** Run `./scripts/bootstrap-issues.sh` after creating your repo from this template.",
        "> **Checklist issues:** Bootstrapped",
    )
    content = re.sub(
        r"^# CNCF Sandbox Application\s*$",
        f"# {project_name} — CNCF Sandbox Application",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    return content


def main() -> int:
    root = Path(os.environ["ROOT_DIR"])
    metadata = json.loads(os.environ["PROJECT_METADATA_JSON"])

    readme_path = root / "README.md"
    application_path = root / "APPLICATION.md"
    metadata_path = root / ".github" / "project-metadata.json"

    readme_path.write_text(update_readme(readme_path.read_text(), metadata))

    application = application_path.read_text()
    field_map = {
        "project_summary": metadata.get("project_summary", ""),
        "org_repo_url": metadata.get("org_repo_url", ""),
        "project_repo_url": metadata.get("project_repo_url", ""),
        "website_url": metadata.get("website_url", ""),
    }
    for field_id, value in field_map.items():
        if value:
            application = set_application_field(application, field_id, value)
    application_path.write_text(application)

    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"Updated {readme_path.name}, {application_path.name}, and {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
