#!/usr/bin/env bash
set -euo pipefail

# Creates GitHub issues for each CNCF sandbox application checklist item and
# updates APPLICATION.md with the issue numbers.
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - jq installed
#   - Run from the repository root after creating a repo from this template
#
# Usage:
#   ./scripts/bootstrap-issues.sh [--dry-run]

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAP_FILE="${ROOT_DIR}/.github/checklist-map.json"
APPLICATION_FILE="${ROOT_DIR}/APPLICATION.md"
REGISTRY_FILE="${ROOT_DIR}/.github/issue-registry.json"
DRY_RUN=false
SLUGS_FILE="$(mktemp)"
SLUGS_ORDERED_FILE="$(mktemp)"
REGISTRY_TMP="$(mktemp)"
LABELS_FILE="$(mktemp)"
EXISTING_LABELS_FILE="$(mktemp)"

cleanup() {
  rm -f "${SLUGS_FILE}" "${SLUGS_ORDERED_FILE}" "${REGISTRY_TMP}" \
    "${LABELS_FILE}" "${EXISTING_LABELS_FILE}" "${APPLICATION_FILE}.tmp"
}
trap cleanup EXIT

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
  echo "Dry run mode: issues will not be created."
fi

for cmd in gh jq; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: ${cmd} is required." >&2
    exit 1
  fi
done

# gh auth status exits non-zero when any configured host has a stale token
# (e.g. legacy github_com in hosts.yml), even if github.com auth works.
# Verify API access instead — that's what this script actually needs.
if ! gh api user -q .login >/dev/null 2>&1; then
  echo "Error: gh is not authenticated or the token is invalid." >&2
  echo "Run: gh auth login" >&2
  echo >&2
  gh auth status 2>&1 || true
  exit 1
fi

if [[ ! -f "${MAP_FILE}" || ! -f "${APPLICATION_FILE}" ]]; then
  echo "Error: required files missing. Run from repository root." >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
if [[ -z "${REPO}" ]]; then
  echo "Error: not inside a GitHub repository. Push this template to GitHub first." >&2
  exit 1
fi

label_color() {
  case "${1}" in
    checklist-item) echo "0E8A16" ;;
    critical) echo "B60205" ;;
    recommended) echo "FBCA04" ;;
    phase:*) echo "5319E7" ;;
    checklist:*) echo "1D76DB" ;;
    *) echo "BFD4F2" ;;
  esac
}

label_description() {
  case "${1}" in
    checklist-item) echo "Part of the CNCF sandbox application preparation checklist" ;;
    critical) echo "Required before CNCF submission" ;;
    recommended) echo "Improves review experience" ;;
    phase:*) echo "Application section: ${1#phase:}" ;;
    checklist:*) echo "Checklist item: ${1#checklist:}" ;;
    *) echo "" ;;
  esac
}

reverse_lines() {
  if command -v tac >/dev/null 2>&1; then
    tac "$1"
  else
    tail -r "$1"
  fi
}

build_checklist_order() {
  grep -oE 'checklist:[a-z0-9-]+' "${APPLICATION_FILE}" \
    | sed 's/checklist://' \
    | awk '!seen[$0]++' > "${SLUGS_ORDERED_FILE}"
}

validate_checklist_order() {
  local map_slugs app_slugs
  map_slugs="$(jq -r 'keys[]' "${MAP_FILE}" | sort)"
  app_slugs="$(sort "${SLUGS_ORDERED_FILE}")"
  if [[ "${map_slugs}" != "${app_slugs}" ]]; then
    echo "Error: checklist slugs in APPLICATION.md do not match checklist-map.json" >&2
    comm -3 <<< "${map_slugs}" <<< "${app_slugs}" | sed 's/^/  /' >&2
    exit 1
  fi
}

ensure_labels() {
  local label color description

  # Use temp files instead of pipes/here-strings so grep never reads the same
  # stdin as the while loop (that deadlock shows up as a hang on grep).
  echo "Fetching existing repository labels..."
  gh label list --limit 500 --json name -q '.[].name' | sort > "${EXISTING_LABELS_FILE}"
  jq -r '[.[].labels[]] | unique | sort | .[]' "${MAP_FILE}" > "${LABELS_FILE}"

  while IFS= read -r label; do
    [[ -z "${label}" ]] && continue
    if grep -qxF "${label}" "${EXISTING_LABELS_FILE}"; then
      continue
    fi

    color="$(label_color "${label}")"
    description="$(label_description "${label}")"

    if [[ "${DRY_RUN}" == true ]]; then
      echo "[dry-run] Would create label: ${label}"
      continue
    fi

    echo "Creating label: ${label}"
    gh label create "${label}" --color "${color}" --description "${description}"
  done < "${LABELS_FILE}"
}

build_checklist_order
validate_checklist_order
# GitHub's default issue list sort is Newest (created descending). Create the
# last checklist item first so the first item appears at the top of the list.
reverse_lines "${SLUGS_ORDERED_FILE}" > "${SLUGS_FILE}"
total="$(wc -l < "${SLUGS_ORDERED_FILE}" | tr -d ' ')"

echo "Bootstrapping ${total} checklist issues for ${REPO}..."
echo "Completion order (top to bottom in the issues list):"
while IFS= read -r slug; do
  echo "  - $(jq -r --arg s "${slug}" '.[$s].title' "${MAP_FILE}")"
done < "${SLUGS_ORDERED_FILE}"
echo

ensure_labels
echo

echo "{" > "${REGISTRY_TMP}"
echo "  \"repository\": \"${REPO}\"," >> "${REGISTRY_TMP}"
echo "  \"created_at\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "${REGISTRY_TMP}"
echo "  \"issues\": {" >> "${REGISTRY_TMP}"

first_entry=true
while IFS= read -r slug; do
  title="$(jq -r --arg s "${slug}" '.[$s].title' "${MAP_FILE}")"
  labels="$(jq -r --arg s "${slug}" '.[$s].labels | join(",")' "${MAP_FILE}")"
  body="$(jq -r --arg s "${slug}" '.[$s].body' "${MAP_FILE}")"
  placeholder="#ISSUE_$(echo "${slug}" | tr '[:lower:]-' '[:upper:]_')"
  body="${body//\#ISSUE_NUMBER/${placeholder}}"
  footer=$'\n\n---\n**Checklist slug:** `'"${slug}"'`\n**Checklist marker:** `<!-- checklist:'"${slug}"' -->`\n**Application checklist:** See [APPLICATION.md](APPLICATION.md)'

  if [[ "${DRY_RUN}" == true ]]; then
    echo "[dry-run] Would create: ${title}"
    issue_number="0"
  else
    existing="$(gh issue list --label "checklist:${slug}" --state all --json number -q '.[0].number' 2>/dev/null || true)"
    if [[ -n "${existing}" && "${existing}" != "null" ]]; then
      echo "Issue already exists for ${slug}: #${existing}"
      issue_number="${existing}"
    else
      echo "Creating issue: ${title}"
      issue_url="$(gh issue create --title "${title}" --label "${labels}" --body "${body}${footer}")"
      issue_number="${issue_url##*/}"
      echo "  -> #${issue_number}"
    fi
  fi

  if [[ "${first_entry}" == true ]]; then
    first_entry=false
  else
    echo "," >> "${REGISTRY_TMP}"
  fi
  printf '    "%s": %s' "${slug}" "${issue_number}" >> "${REGISTRY_TMP}"

  if [[ "${DRY_RUN}" == false ]]; then
    cp "${APPLICATION_FILE}" "${APPLICATION_FILE}.tmp"
    if sed --version >/dev/null 2>&1; then
      sed -i "s/${placeholder}/#${issue_number}/g" "${APPLICATION_FILE}.tmp"
    else
      sed -i '' "s/${placeholder}/#${issue_number}/g" "${APPLICATION_FILE}.tmp"
    fi
    mv "${APPLICATION_FILE}.tmp" "${APPLICATION_FILE}"
  fi
done < "${SLUGS_FILE}"

echo >> "${REGISTRY_TMP}"
echo "  }" >> "${REGISTRY_TMP}"
echo "}" >> "${REGISTRY_TMP}"

if [[ "${DRY_RUN}" == true ]]; then
  echo
  echo "Dry run complete. No files modified."
  exit 0
fi

mv "${REGISTRY_TMP}" "${REGISTRY_FILE}"
trap - EXIT

echo
echo "Updated APPLICATION.md and wrote ${REGISTRY_FILE}"
echo
echo "Next steps:"
echo "  git add APPLICATION.md .github/issue-registry.json"
echo "  git commit -m 'Bootstrap CNCF sandbox checklist issues'"
echo "  git push"
