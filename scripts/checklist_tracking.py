#!/usr/bin/env python3
"""Issue/PR tracking on checklist lines in APPLICATION.md and README.md."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

CHECKLIST_LINE = re.compile(
    r"^- \[[ xX]\].*<!-- checklist:[a-z0-9-]+ -->.*$"
)
CHECKLIST_SLUG = re.compile(r"<!-- checklist:([a-z0-9-]+) -->")
TRACKING_SUFFIX = re.compile(r" \((Issue|PR):.*\)\s*$")

START_DASHBOARD = "<!-- application-dashboard:start -->"
END_DASHBOARD = "<!-- application-dashboard:end -->"


def issue_token_placeholder(slug: str) -> str:
    token = f"#ISSUE_{slug.upper().replace('-', '_')}"
    return f"(Issue: {token})"


def issue_token_linked(repo: str, issue_number: int) -> str:
    return (
        f"(Issue: [#{issue_number}]"
        f"(https://github.com/{repo}/issues/{issue_number}))"
    )


def pr_token_linked(repo: str, pr_number: int) -> str:
    return (
        f"(PR: [#{pr_number}]"
        f"(https://github.com/{repo}/pull/{pr_number}))"
    )


def strip_tracking_suffix(line: str) -> str:
    return TRACKING_SUFFIX.sub("", line.rstrip())


def set_checklist_line_tracking(line: str, slug: str, tracking: str) -> str:
    marker = f"<!-- checklist:{slug} -->"
    if marker not in line or not CHECKLIST_LINE.match(line):
        return line
    base = strip_tracking_suffix(line)
    return f"{base} {tracking}"


def apply_issue_link(content: str, slug: str, issue_number: int, repo: str) -> str:
    placeholder = issue_token_placeholder(slug)
    linked = issue_token_linked(repo, issue_number)
    lines = []
    for line in content.splitlines():
        if f"<!-- checklist:{slug} -->" in line and placeholder in line:
            lines.append(line.replace(placeholder, linked))
        else:
            lines.append(line)
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def apply_pr_link(content: str, slug: str, pr_number: int, repo: str) -> str:
    tracking = pr_token_linked(repo, pr_number)
    lines = [
        set_checklist_line_tracking(line, slug, tracking)
        if f"<!-- checklist:{slug} -->" in line
        else line
        for line in content.splitlines()
    ]
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


def mark_checkbox_complete(content: str, slug: str) -> str:
    marker = f"<!-- checklist:{slug} -->"
    pattern = re.compile(
        rf"^- \[ \] (.+?{re.escape(marker)})( .*)?$",
        re.MULTILINE,
    )

    def repl(match: re.Match[str]) -> str:
        suffix = match.group(2) or ""
        return f"- [x] {match.group(1)}{suffix}"

    return pattern.sub(repl, content, count=1)


def slug_for_issue(registry: Dict[str, int], issue_number: int) -> Optional[str]:
    for slug, num in registry.items():
        if int(num) == int(issue_number):
            return slug
    return None


def load_issue_registry(path: Path) -> Dict[str, int]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: int(v) for k, v in data.get("issues", {}).items()}


def parse_closing_issues(text: str) -> List[int]:
    pattern = re.compile(
        r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)",
        re.IGNORECASE,
    )
    return [int(m.group(1)) for m in pattern.finditer(text or "")]


def build_application_dashboard(application: str) -> str:
    lines: List[str] = []
    current_heading: Optional[str] = None
    section_lines: List[str] = []

    def flush_section() -> None:
        nonlocal section_lines, current_heading
        if not current_heading:
            section_lines = []
            return
        anchor = current_heading
        lines.append(f"### [{anchor}](APPLICATION.md#{anchor})")
        lines.append("")
        for row in section_lines:
            if CHECKLIST_LINE.match(row):
                lines.append(row)
        if any(CHECKLIST_LINE.match(r) for r in section_lines):
            lines.append("")
        section_lines = []

    in_guide = False
    for raw in application.splitlines():
        heading = re.match(r"^## ([a-z0-9_]+)\s*$", raw)
        if heading:
            flush_section()
            current_heading = heading.group(1)
            in_guide = False
            continue
        if current_heading is None:
            continue
        if raw.strip() == "<!-- field-guide:start -->":
            in_guide = True
            continue
        if raw.strip() == "<!-- field-guide:end -->":
            in_guide = False
            continue
        if in_guide:
            continue
        if raw.startswith("**Your answer"):
            continue
        if CHECKLIST_LINE.match(raw):
            section_lines.append(raw)

    flush_section()
    return "\n".join(lines).rstrip() + "\n"


def sync_readme_dashboard(root: Path) -> bool:
    readme = root / "README.md"
    application = root / "APPLICATION.md"
    if not readme.is_file() or not application.is_file():
        return False
    content = readme.read_text(encoding="utf-8")
    if START_DASHBOARD not in content or END_DASHBOARD not in content:
        return False
    dashboard = build_application_dashboard(application.read_text(encoding="utf-8"))
    pattern = re.compile(
        rf"{re.escape(START_DASHBOARD)}.*?{re.escape(END_DASHBOARD)}",
        re.DOTALL,
    )
    replacement = f"{START_DASHBOARD}\n{dashboard}{END_DASHBOARD}"
    new_content = pattern.sub(replacement, content, count=1)
    if new_content == content:
        return False
    readme.write_text(new_content, encoding="utf-8")
    return True


def update_files_for_pr(root: Path, repo: str, pr_number: int, issue_numbers: List[int]) -> Tuple[bool, List[str]]:
    registry_path = root / ".github" / "issue-registry.json"
    registry = load_issue_registry(registry_path)
    application_path = root / "APPLICATION.md"
    before = application_path.read_text(encoding="utf-8")
    application = before
    changed_slugs: List[str] = []

    for issue_number in issue_numbers:
        slug = slug_for_issue(registry, issue_number)
        if not slug:
            continue
        # Closes #N is enough: swap Issue→PR and check the box. README mirrors APPLICATION.md.
        application = apply_pr_link(application, slug, pr_number, repo)
        application = mark_checkbox_complete(application, slug)
        changed_slugs.append(slug)

    if not changed_slugs or application == before:
        return False, []

    application_path.write_text(application, encoding="utf-8")
    sync_readme_dashboard(root)
    return True, changed_slugs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    sub = parser.add_subparsers(dest="command", required=True)

    link_issue = sub.add_parser("link-issue")
    link_issue.add_argument("--slug", required=True)
    link_issue.add_argument("--number", type=int, required=True)
    link_issue.add_argument("--repo", required=True)

    link_pr = sub.add_parser("link-pr")
    link_pr.add_argument("--repo", required=True)
    link_pr.add_argument("--pr-number", type=int, required=True)
    link_pr.add_argument("--issue-numbers", nargs="+", type=int, required=True)

    sub.add_parser("sync-readme")

    complete = sub.add_parser("complete-checkbox")
    complete.add_argument("--slug", required=True)

    args = parser.parse_args()
    root = args.root
    application_path = root / "APPLICATION.md"

    if args.command == "link-issue":
        text = application_path.read_text(encoding="utf-8")
        text = apply_issue_link(text, args.slug, args.number, args.repo)
        application_path.write_text(text, encoding="utf-8")
        sync_readme_dashboard(root)
        return 0

    if args.command == "link-pr":
        changed, slugs = update_files_for_pr(
            root, args.repo, args.pr_number, args.issue_numbers
        )
        if not changed:
            print("No checklist lines updated for PR", file=sys.stderr)
            return 0
        print(f"Updated PR links and checked boxes for: {', '.join(slugs)}")
        return 0

    if args.command == "sync-readme":
        sync_readme_dashboard(root)
        return 0

    if args.command == "complete-checkbox":
        text = application_path.read_text(encoding="utf-8")
        text = mark_checkbox_complete(text, args.slug)
        application_path.write_text(text, encoding="utf-8")
        sync_readme_dashboard(root)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
