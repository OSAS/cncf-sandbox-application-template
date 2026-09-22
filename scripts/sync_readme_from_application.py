#!/usr/bin/env python3
"""Refresh README application dashboard from APPLICATION.md."""

from pathlib import Path

from checklist_tracking import sync_readme_dashboard


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    sync_readme_dashboard(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
