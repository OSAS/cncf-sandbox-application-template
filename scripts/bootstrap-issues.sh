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
REGISTRY_TMP="$(mktemp)"

cleanup() {
  rm -f "${SLUGS_FILE}" "${REGISTRY_TMP}" "${APPLICATION_FILE}.tmp"
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

if ! gh auth status >/dev/null 2>&1; then
  echo "Error: gh is not authenticated. Run: gh auth login" >&2
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

jq -r 'keys[]' "${MAP_FILE}" | sort > "${SLUGS_FILE}"
total="$(wc -l < "${SLUGS_FILE}" | tr -d ' ')"

echo "Bootstrapping ${total} checklist issues for ${REPO}..."
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
