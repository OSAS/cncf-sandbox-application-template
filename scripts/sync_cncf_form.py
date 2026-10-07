#!/usr/bin/env python3
"""Fetch the live CNCF sandbox application.yml and compile local form artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError:  # pragma: no cover
    print(
        "Error: PyYAML is required. Install with: pip install -r requirements-dev.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REF = "main"
DEFAULT_URL = (
    "https://raw.githubusercontent.com/cncf/sandbox/"
    f"{DEFAULT_REF}/.github/ISSUE_TEMPLATE/application.yml"
)

LOCAL_ONLY_SLUGS = ("read-prerequisites", "final-review")
SKIP_SECTION_HEADINGS = (
    "pre-submission checklist",
    "✅ pre-submission checklist",
)

PHASE_BY_HEADING = {
    "basic project information": "phase:basic-info",
    "project details": "phase:project-details",
    "cloud native context": "phase:cloud-native",
    "cncf policies": "phase:cncf-policies",
    "contact information": "phase:contact",
    "additional information": "phase:contact",
}

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
EMOJI_PREFIX_RE = re.compile(r"^[\W_]+", re.UNICODE)


def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "cncf-sandbox-application-sync"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def title_prefix(title: str) -> str:
    cleaned = title.replace("<Project Name>", "").strip()
    return cleaned.rstrip()


def heading_key(heading: str) -> str:
    text = heading.strip()
    text = re.sub(r"^:[a-z0-9_+-]+:\s*", "", text)
    text = EMOJI_PREFIX_RE.sub("", text)
    return text.strip().lower()


def parse_section_markdown(value: str) -> Optional[Tuple[str, str]]:
    match = HEADING_RE.search(value)
    if not match:
        return None
    heading = match.group(1).strip()
    if heading_key(heading) in SKIP_SECTION_HEADINGS:
        return None
    after = value[match.end() :].strip()
    after = re.sub(r"<br\s*/?>", "", after, flags=re.IGNORECASE).strip()
    intro = after.split("\n\n")[0].strip() if after else ""
    intro = " ".join(intro.split())
    return f"## {heading}", intro


def field_ids_from_form(form: Dict[str, Any]) -> List[str]:
    ids: List[str] = []
    for section in form.get("sections", []):
        for field in section.get("fields", []):
            ids.append(field["id"])
    return ids


def fields_by_id(form: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for section in form.get("sections", []):
        for field in section.get("fields", []):
            out[field["id"]] = field
    return out


def checklist_slugs_from_form(form: Dict[str, Any]) -> List[str]:
    slugs: List[str] = []
    seen: set[str] = set()
    for section in form.get("sections", []):
        for field in section.get("fields", []):
            for slug in field.get("checklist", []):
                if slug not in seen:
                    slugs.append(slug)
                    seen.add(slug)
    return slugs


def id_to_slug(field_id: str) -> str:
    return field_id.replace("_", "-")


def resolve_field_id(
    item: Dict[str, Any],
    aliases: Dict[str, Any],
) -> Optional[str]:
    by_id = aliases.get("by_id") or {}
    by_label = aliases.get("by_label") or {}
    upstream_id = item.get("id")
    if upstream_id and upstream_id in by_id:
        return by_id[upstream_id]
    attrs = item.get("attributes") or {}
    label = (attrs.get("label") or "").strip()
    if label in by_label:
        return by_label[label]
    if item.get("type") == "checkboxes":
        options = attrs.get("options") or []
        if options:
            option_label = (options[0].get("label") or "").strip()
            if option_label in by_label:
                return by_label[option_label]
    return None


def map_field_type(item_type: str) -> str:
    if item_type == "input":
        return "text"
    if item_type == "textarea":
        return "textarea"
    if item_type == "checkboxes":
        return "checkbox"
    return item_type


def field_required(item: Dict[str, Any]) -> bool:
    validations = item.get("validations") or {}
    if validations.get("required"):
        return True
    if item.get("type") == "checkboxes":
        options = (item.get("attributes") or {}).get("options") or []
        return any(opt.get("required") for opt in options)
    return False


def seed_placeholder(item: Dict[str, Any]) -> str:
    attrs = item.get("attributes") or {}
    if item.get("type") == "checkboxes":
        options = attrs.get("options") or []
        if options:
            return (options[0].get("label") or "").strip()
        return (attrs.get("label") or "").strip()
    placeholder = (attrs.get("placeholder") or "").strip()
    if placeholder:
        return f"_{placeholder}_"
    description = (attrs.get("description") or "").strip()
    if description:
        first = description.splitlines()[0].strip()
        return f"_{first}_"
    return "_Not provided._"


def seed_guide(item: Dict[str, Any]) -> str:
    attrs = item.get("attributes") or {}
    description = attrs.get("description")
    if not description:
        return ""
    return str(description).strip()


def compile_form(
    template: Dict[str, Any],
    aliases: Dict[str, Any],
    previous: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str], Dict[str, Dict[str, Any]]]:
    previous_fields = fields_by_id(previous)
    unmatched: List[str] = []
    compiled_meta: Dict[str, Dict[str, Any]] = {}
    sections: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    labels = template.get("labels") or ["New"]
    if isinstance(labels, str):
        labels = [labels]

    form: Dict[str, Any] = {
        "title_prefix": title_prefix(template.get("title") or "[Sandbox]"),
        "issue_labels": labels,
        "sections": sections,
    }

    for item in template.get("body") or []:
        item_type = item.get("type")
        if item_type == "markdown":
            parsed = parse_section_markdown((item.get("attributes") or {}).get("value") or "")
            if parsed:
                heading, intro = parsed
                current = {"heading": heading}
                if intro:
                    current["intro"] = intro
                current["fields"] = []
                sections.append(current)
            continue
        if item_type not in {"input", "textarea", "checkboxes"}:
            continue
        if current is None:
            current = {"heading": "## Application", "fields": []}
            sections.append(current)

        field_id = resolve_field_id(item, aliases)
        attrs = item.get("attributes") or {}
        label = (attrs.get("label") or "").strip()
        if not field_id:
            unmatched.append(f"{item.get('id') or '(no id)'}: {label or item_type}")
            continue

        previous_field = previous_fields.get(field_id, {})
        checklist = list(previous_field.get("checklist") or [id_to_slug(field_id)])
        field: Dict[str, Any] = {
            "id": field_id,
            "label": label,
            "type": map_field_type(item_type),
            "required": field_required(item),
            "checklist": checklist,
        }
        if item_type == "checkboxes":
            options = attrs.get("options") or []
            if options:
                field["option_label"] = (options[0].get("label") or "").strip()
        current["fields"].append(field)
        compiled_meta[field_id] = {
            "placeholder": seed_placeholder(item),
            "guide": seed_guide(item),
            "label": label,
            "heading": current["heading"],
            "checklist": checklist,
        }

    form["sections"] = [section for section in sections if section.get("fields")]
    return form, unmatched, compiled_meta


def diff_forms(previous: Dict[str, Any], compiled: Dict[str, Any]) -> Dict[str, List[str]]:
    old = fields_by_id(previous)
    new = fields_by_id(compiled)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    renamed: List[str] = []
    required_changed: List[str] = []
    for field_id in sorted(set(old) & set(new)):
        if old[field_id].get("label") != new[field_id].get("label"):
            renamed.append(
                f"{field_id}: {old[field_id].get('label')!r} -> {new[field_id].get('label')!r}"
            )
        if bool(old[field_id].get("required")) != bool(new[field_id].get("required")):
            required_changed.append(
                f"{field_id}: required {old[field_id].get('required')} -> {new[field_id].get('required')}"
            )
    return {
        "added": added,
        "removed": removed,
        "renamed": renamed,
        "required_changed": required_changed,
    }


def format_report(diff: Dict[str, List[str]], stale_slugs: Iterable[str] = ()) -> str:
    lines = ["CNCF application form sync report", ""]
    for key, title in (
        ("added", "Added fields"),
        ("removed", "Removed fields"),
        ("renamed", "Renamed labels"),
        ("required_changed", "Required-flag changes"),
    ):
        items = diff.get(key) or []
        lines.append(f"## {title}")
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- (none)")
        lines.append("")
    stale = list(stale_slugs)
    lines.append("## Stale checklist slugs (existing GitHub issues are not updated)")
    if stale:
        lines.extend(f"- {slug}" for slug in stale)
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def upsert_placeholders(
    path: Path,
    compiled_ids: List[str],
    meta: Dict[str, Dict[str, Any]],
    local_field_ids: Iterable[str],
) -> None:
    data = load_json(path)
    keep = set(compiled_ids) | set(local_field_ids)
    for field_id in list(data):
        if field_id not in keep:
            del data[field_id]
    for field_id in compiled_ids:
        if field_id not in data:
            data[field_id] = meta[field_id]["placeholder"]
    ordered: Dict[str, str] = {}
    if "read_prerequisites" in data:
        ordered["read_prerequisites"] = data["read_prerequisites"]
    for field_id in compiled_ids:
        if field_id in data:
            ordered[field_id] = data[field_id]
    if "final_review" in data:
        ordered["final_review"] = data["final_review"]
    dump_json(path, ordered)


def upsert_guides(
    path: Path,
    compiled_ids: List[str],
    meta: Dict[str, Dict[str, Any]],
    local_field_ids: Iterable[str],
    force: bool,
) -> None:
    data = load_json(path)
    keep = set(compiled_ids) | set(local_field_ids)
    for field_id in list(data):
        if field_id not in keep:
            del data[field_id]
    for field_id in compiled_ids:
        guide = meta[field_id].get("guide") or ""
        if not guide:
            continue
        if field_id not in data or force:
            data[field_id] = guide
    dump_json(path, data)


def phase_for_heading(heading: str) -> str:
    key = heading_key(heading.replace("## ", ""))
    return PHASE_BY_HEADING.get(key, "phase:prepare")


def stub_map_entry(slug: str, field_id: str, label: str, heading: str) -> Dict[str, Any]:
    return {
        "title": f"[Application] {label}",
        "labels": ["checklist-item", f"checklist:{slug}", phase_for_heading(heading)],
        "template": "checklist-item.md",
        "body": (
            f"Update `{field_id}` in [APPLICATION.md](../APPLICATION.md).\n\n"
            "When complete, open a PR with `Closes #ISSUE_NUMBER`."
        ),
    }


def upsert_checklist_artifacts(
    labels_path: Path,
    map_path: Path,
    form: Dict[str, Any],
    meta: Dict[str, Dict[str, Any]],
    force_map_bodies: bool,
) -> List[str]:
    labels = load_json(labels_path)
    checklist_map = load_json(map_path)
    form_slugs = checklist_slugs_from_form(form)
    keep_slugs = list(LOCAL_ONLY_SLUGS[:1]) + form_slugs + list(LOCAL_ONLY_SLUGS[1:])

    slug_primary: Dict[str, str] = {}
    for section in form["sections"]:
        for field in section["fields"]:
            for slug in field.get("checklist", []):
                slug_primary.setdefault(slug, field["id"])

    stale = sorted(set(checklist_map) - set(keep_slugs))
    new_map: Dict[str, Any] = {}
    new_labels: Dict[str, str] = {}
    for slug in keep_slugs:
        if slug in checklist_map and not force_map_bodies:
            new_map[slug] = checklist_map[slug]
        elif slug in checklist_map and force_map_bodies and slug in LOCAL_ONLY_SLUGS:
            new_map[slug] = checklist_map[slug]
        elif slug in LOCAL_ONLY_SLUGS and slug in checklist_map:
            new_map[slug] = checklist_map[slug]
        else:
            field_id = slug_primary.get(slug, slug.replace("-", "_"))
            info = meta.get(field_id, {})
            new_map[slug] = stub_map_entry(
                slug,
                field_id,
                info.get("label") or field_id.replace("_", " "),
                info.get("heading") or "## Application",
            )
        if slug in labels:
            new_labels[slug] = labels[slug]
        else:
            field_id = slug_primary.get(slug, slug.replace("-", "_"))
            info = meta.get(field_id, {})
            new_labels[slug] = info.get("label") or slug.replace("-", " ").capitalize()

    dump_json(map_path, new_map)
    dump_json(labels_path, new_labels)
    return stale


def canonical(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync local CNCF form snapshot from cncf/sandbox application.yml"
    )
    parser.add_argument("--url", help="Override application.yml URL")
    parser.add_argument(
        "--ref",
        default=DEFAULT_REF,
        help="cncf/sandbox git ref (default: main). Ignored if --url is set.",
    )
    parser.add_argument("--check", action="store_true", help="Exit 1 if committed form differs")
    parser.add_argument("--write", action="store_true", help="Write compiled artifacts")
    parser.add_argument("--report", action="store_true", help="Print a field-change report")
    parser.add_argument(
        "--merge-application",
        action="store_true",
        help="Rewrite APPLICATION.md while preserving answers",
    )
    parser.add_argument("--force-guides", action="store_true")
    parser.add_argument("--force-map-bodies", action="store_true")
    return parser.parse_args()


def template_url(args: argparse.Namespace) -> str:
    if args.url:
        return args.url
    if args.ref != DEFAULT_REF:
        return (
            "https://raw.githubusercontent.com/cncf/sandbox/"
            f"{args.ref}/.github/ISSUE_TEMPLATE/application.yml"
        )
    return DEFAULT_URL


def fetch_compiled_form(
    root: Path = ROOT,
    url: str = DEFAULT_URL,
) -> Tuple[Dict[str, Any], List[str], Dict[str, List[str]]]:
    """Fetch and compile the live CNCF form against local aliases/snapshot.

    Returns (compiled_form, unmatched_field_descriptions, diff_vs_local).
    """
    form_path = root / ".github" / "cncf-form.json"
    aliases = load_json(root / "scripts" / "cncf_field_aliases.json")
    previous = load_json(form_path) if form_path.is_file() else {"sections": []}
    raw = fetch_text(url)
    template = yaml.safe_load(raw)
    compiled, unmatched, _meta = compile_form(template, aliases, previous)
    return compiled, unmatched, diff_forms(previous, compiled)


def main() -> int:
    args = parse_args()
    if not (args.check or args.write or args.report or args.merge_application):
        args.report = True

    form_path = ROOT / ".github" / "cncf-form.json"
    aliases = load_json(ROOT / "scripts" / "cncf_field_aliases.json")
    previous = load_json(form_path) if form_path.is_file() else {"sections": []}

    url = template_url(args)
    try:
        raw = fetch_text(url)
    except Exception as exc:  # noqa: BLE001
        print(f"Error: failed to fetch {url}: {exc}", file=sys.stderr)
        return 1

    template = yaml.safe_load(raw)
    compiled, unmatched, meta = compile_form(template, aliases, previous)
    if unmatched:
        print("Error: unmatched CNCF form fields. Add aliases in scripts/cncf_field_aliases.json:", file=sys.stderr)
        for item in unmatched:
            print(f"  - {item}", file=sys.stderr)
        return 1

    diff = diff_forms(previous, compiled)
    stale_preview: List[str] = []
    previous_slugs = set()
    if (ROOT / ".github" / "checklist-map.json").is_file():
        previous_slugs = set(load_json(ROOT / ".github" / "checklist-map.json"))
    keep_slugs = set(LOCAL_ONLY_SLUGS) | set(checklist_slugs_from_form(compiled))
    stale_preview = sorted(previous_slugs - keep_slugs)
    report = format_report(diff, stale_preview)

    if args.report or args.check or args.write:
        print(report)

    form_changed = canonical(previous) != canonical(compiled)
    if args.check and not args.write:
        if form_changed:
            print("Committed .github/cncf-form.json is out of date with upstream.", file=sys.stderr)
            return 1
        print("cncf-form.json matches upstream.")
        return 0

    if args.write:
        dump_json(form_path, compiled)
        compiled_ids = field_ids_from_form(compiled)
        upsert_placeholders(
            ROOT / "scripts" / "application_field_placeholders.json",
            compiled_ids,
            meta,
            ("read_prerequisites", "final_review"),
        )
        upsert_guides(
            ROOT / "scripts" / "application_field_guides.json",
            compiled_ids,
            meta,
            ("read_prerequisites", "final_review"),
            args.force_guides,
        )
        stale = upsert_checklist_artifacts(
            ROOT / "scripts" / "checklist_checkbox_labels.json",
            ROOT / ".github" / "checklist-map.json",
            compiled,
            meta,
            args.force_map_bodies,
        )
        print(f"Wrote {form_path}")
        if stale:
            print("Removed checklist slugs (close or retitle related issues manually):")
            for slug in stale:
                print(f"  - {slug}")

    if args.merge_application:
        sys.path.insert(0, str(ROOT / "scripts"))
        from merge_application import merge_application

        orphan_path = ROOT / f"APPLICATION-orphaned-answers-{date.today().isoformat()}.md"
        merge_application(ROOT, orphan_path)
        print(f"Merged APPLICATION.md")

    if args.check and args.write:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
