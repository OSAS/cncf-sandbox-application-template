#!/usr/bin/env bash
set -euo pipefail

# Creates GitHub issues for each CNCF sandbox application checklist item and
# updates APPLICATION.md with GitHub issue numbers.
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - jq installed
#   - Run from the repository root after creating a repo from this template
#
# Usage:
#   ./scripts/bootstrap-issues.sh [--dry-run]
#   ./scripts/bootstrap-issues.sh --project-name "MyProject" [--non-interactive]
#
# Options:
#   --project-name NAME       Project name (prompted if omitted)
#   --project-summary TEXT    One-line summary for APPLICATION.md
#   --org-repo-url URL        Org repo URL or N/A
#   --project-repo-url URL    Primary project repo URL (defaults to this GitHub repo)
#   --website-url URL         Project website (defaults to project repo URL)
#   --non-interactive         Fail if required values are missing instead of prompting

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAP_FILE="${ROOT_DIR}/.github/checklist-map.json"
CHECKLIST_FILE="${ROOT_DIR}/APPLICATION.md"
README_FILE="${ROOT_DIR}/README.md"
APPLICATION_FILE="${ROOT_DIR}/APPLICATION.md"
REGISTRY_FILE="${ROOT_DIR}/.github/issue-registry.json"
METADATA_FILE="${ROOT_DIR}/.github/project-metadata.json"
APPLY_PROJECT_INFO="${ROOT_DIR}/scripts/apply_project_info.py"
UPDATE_PROGRESS="${ROOT_DIR}/scripts/update_checklist_progress.py"
DRY_RUN=false
NON_INTERACTIVE=false
PROJECT_NAME=""
PROJECT_SUMMARY=""
ORG_REPO_URL=""
PROJECT_REPO_URL=""
WEBSITE_URL=""
SLUGS_FILE="$(mktemp)"
SLUGS_ORDERED_FILE="$(mktemp)"
REGISTRY_TMP="$(mktemp)"
LABELS_FILE="$(mktemp)"
EXISTING_LABELS_FILE="$(mktemp)"

cleanup() {
  rm -f "${SLUGS_FILE}" "${SLUGS_ORDERED_FILE}" "${REGISTRY_TMP}" \
    "${LABELS_FILE}" "${EXISTING_LABELS_FILE}" \
    "${CHECKLIST_FILE}.tmp" "${README_FILE}.tmp"
}
trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "${1}" in
    --dry-run)
      DRY_RUN=true
      ;;
    --non-interactive)
      NON_INTERACTIVE=true
      ;;
    --project-name)
      PROJECT_NAME="${2:-}"
      shift
      ;;
    --project-summary)
      PROJECT_SUMMARY="${2:-}"
      shift
      ;;
    --org-repo-url)
      ORG_REPO_URL="${2:-}"
      shift
      ;;
    --project-repo-url)
      PROJECT_REPO_URL="${2:-}"
      shift
      ;;
    --website-url)
      WEBSITE_URL="${2:-}"
      shift
      ;;
    -h|--help)
      sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: ${1}" >&2
      exit 1
      ;;
  esac
  shift
done

if [[ "${DRY_RUN}" == true ]]; then
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

if [[ ! -f "${MAP_FILE}" || ! -f "${CHECKLIST_FILE}" || ! -f "${APPLICATION_FILE}" ]]; then
  echo "Error: required files missing. Run from repository root." >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
if [[ -z "${REPO}" ]]; then
  echo "Error: not inside a GitHub repository. Push this template to GitHub first." >&2
  exit 1
fi

DEFAULT_REPO_URL="$(gh repo view --json url -q .url 2>/dev/null || true)"

prompt_value() {
  local var_name="${1}"
  local prompt_text="${2}"
  local default_value="${3}"
  local current_value="${!var_name}"

  if [[ -n "${current_value}" ]]; then
    return 0
  fi

  if [[ "${NON_INTERACTIVE}" == true ]]; then
    echo "Error: --${var_name//_/-} is required in non-interactive mode." >&2
    exit 1
  fi

  if [[ -n "${default_value}" ]]; then
    read -r -p "${prompt_text} [${default_value}]: " input
    if [[ -z "${input}" ]]; then
      input="${default_value}"
    fi
  else
    read -r -p "${prompt_text}: " input
    while [[ -z "${input}" ]]; do
      read -r -p "${prompt_text} (required): " input
    done
  fi

  printf -v "${var_name}" '%s' "${input}"
}

collect_project_info() {
  if [[ "${DRY_RUN}" == true ]]; then
    echo "Project setup (skipped in dry run):"
    echo "  Project name: ${PROJECT_NAME:-<prompted>}"
    echo "  Project summary: ${PROJECT_SUMMARY:-<optional>}"
    echo "  Org repo URL: ${ORG_REPO_URL:-N/A}"
    echo "  Project repo URL: ${PROJECT_REPO_URL:-${DEFAULT_REPO_URL}}"
    echo "  Website URL: ${WEBSITE_URL:-${DEFAULT_REPO_URL}}"
    echo
    return 0
  fi

  if [[ -f "${METADATA_FILE}" && -z "${PROJECT_NAME}" && "${NON_INTERACTIVE}" == true ]]; then
    PROJECT_NAME="$(jq -r '.project_name' "${METADATA_FILE}")"
  fi

  echo "Project setup"
  echo "Press Enter to accept [default] values."
  echo

  prompt_value PROJECT_NAME "Project name" ""
  prompt_value PROJECT_SUMMARY "One-line project summary (optional)" ""
  prompt_value ORG_REPO_URL "Org repo URL (or N/A if not applying for a whole org)" "N/A"
  prompt_value PROJECT_REPO_URL "Primary project repository URL" "${DEFAULT_REPO_URL}"
  prompt_value WEBSITE_URL "Website URL" "${PROJECT_REPO_URL}"

  local metadata
  metadata="$(jq -n \
    --arg project_name "${PROJECT_NAME}" \
    --arg project_summary "${PROJECT_SUMMARY}" \
    --arg org_repo_url "${ORG_REPO_URL}" \
    --arg project_repo_url "${PROJECT_REPO_URL}" \
    --arg website_url "${WEBSITE_URL}" \
    --arg repository "${REPO}" \
    --arg bootstrapped_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    '{
      project_name: $project_name,
      project_summary: $project_summary,
      org_repo_url: $org_repo_url,
      project_repo_url: $project_repo_url,
      website_url: $website_url,
      repository: $repository,
      bootstrapped_at: $bootstrapped_at
    }')"

  export ROOT_DIR PROJECT_METADATA_JSON="${metadata}"
  python3 "${APPLY_PROJECT_INFO}"
  echo
}

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
  grep -oE 'checklist:[a-z0-9-]+' "${CHECKLIST_FILE}" \
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

collect_project_info

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
    python3 "${ROOT_DIR}/scripts/checklist_tracking.py" \
      --root "${ROOT_DIR}" \
      link-issue \
      --slug "${slug}" \
      --number "${issue_number}" \
      --repo "${REPO}"
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

python3 "${UPDATE_PROGRESS}"

echo
python3 "${ROOT_DIR}/scripts/sync_readme_from_application.py"

echo "Updated APPLICATION.md, README.md, and wrote ${REGISTRY_FILE}"
echo
echo "Next steps:"
echo "  git add APPLICATION.md README.md .github/project-metadata.json .github/issue-registry.json"
echo "  git commit -m 'Bootstrap CNCF sandbox checklist issues'"
echo "  git push"
