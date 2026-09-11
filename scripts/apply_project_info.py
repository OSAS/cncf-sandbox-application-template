#!/usr/bin/env python3
"""Apply bootstrap project metadata to README.md and APPLICATION.md."""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict


def set_application_field(content: str, field_id: str, value: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(field_id)}\n)(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def repl(match: re.Match[str]) -> str:
        body = value.strip()
        if not body:
            return match.group(0)
        return f"{match.group(1)}{body}\n"

    return pattern.sub(repl, content, count=1)


def update_readme(content: str, metadata: Dict[str, str]) -> str:
    project_name = metadata["project_name"]
    content = content.replace(
        "> **Project name:** _Replace with your project name_",
        f"> **Project name:** {project_name}",
    )
    content = content.replace(
        "> **Checklist issues created:** Run `./scripts/bootstrap-issues.sh` after creating your repo from this template.",
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
