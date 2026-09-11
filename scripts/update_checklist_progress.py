#!/usr/bin/env python3
"""Update the checklist progress indicator in README.md."""

import re
import sys
from pathlib import Path


START_MARKER = "<!-- checklist-progress:start -->"
END_MARKER = "<!-- checklist-progress:end -->"
BAR_WIDTH = 20


def slug_complete(content: str, slug: str) -> bool:
    marker = f"<!-- checklist:{slug} -->"
    for line in content.splitlines():
        if marker not in line:
            continue
        if re.match(r"^- \[[xX]\]", line):
            return True
    return False


def compute_progress(content: str) -> tuple[int, int]:
    slugs = sorted(set(re.findall(r"<!-- checklist:([a-z0-9-]+) -->", content)))
    completed = sum(1 for slug in slugs if slug_complete(content, slug))
    return completed, len(slugs)


def render_progress(completed: int, total: int) -> str:
    if total == 0:
        percent = 0
    else:
        percent = round((completed / total) * 100)

    filled = round((completed / total) * BAR_WIDTH) if total else 0
    bar = ("█" * filled) + ("░" * (BAR_WIDTH - filled))

    return (
        f"> **Application progress:** **{completed} / {total}** items complete ({percent}%)  \n"
        f"> `{bar}` {percent}%"
    )


def update_readme(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(f"Error: progress markers not found in {path}", file=sys.stderr)
        return False

    completed, total = compute_progress(content)
    progress_block = render_progress(completed, total)

    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )
    replacement = f"{START_MARKER}\n{progress_block}\n{END_MARKER}"
    new_content = pattern.sub(replacement, content, count=1)

    if new_content == content:
        return False

    path.write_text(new_content, encoding="utf-8")
    print(f"Checklist progress: {completed}/{total} ({round((completed / total) * 100) if total else 0}%)")
    return True


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    readme = root / "README.md"
    if not readme.is_file():
        print(f"Error: {readme} not found", file=sys.stderr)
        return 1
    update_readme(readme)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
