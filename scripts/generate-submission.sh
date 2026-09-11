#!/usr/bin/env bash
set -euo pipefail

# Generates CNCF-SUBMISSION.md from APPLICATION.md for one-step CNCF submission.
#
# Prerequisites:
#   - jq installed
#   - python3 installed
#
# Usage:
#   ./scripts/generate-submission.sh              # generate CNCF-SUBMISSION.md
#   ./scripts/generate-submission.sh --validate   # fail if required fields are empty
#   ./scripts/generate-submission.sh --create-issue --project-name "MyProject"
#                                                 # submit to cncf/sandbox via gh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORM_FILE="${ROOT_DIR}/.github/cncf-form.json"
ANSWERS_FILE="${ROOT_DIR}/APPLICATION.md"
OUTPUT_FILE="${ROOT_DIR}/CNCF-SUBMISSION.md"
METADATA_FILE="${ROOT_DIR}/.github/project-metadata.json"
GENERATOR="${ROOT_DIR}/scripts/generate_submission.py"
VALIDATE=false
CREATE_ISSUE=false
PROJECT_NAME=""

while [[ $# -gt 0 ]]; do
  case "${1}" in
    --validate)
      VALIDATE=true
      ;;
    --create-issue)
      CREATE_ISSUE=true
      VALIDATE=true
      ;;
    --project-name)
      PROJECT_NAME="${2:-}"
      shift
      ;;
    -h|--help)
      sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: ${1}" >&2
      exit 1
      ;;
  esac
  shift
done

for cmd in jq python3; do
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    echo "Error: ${cmd} is required." >&2
    exit 1
  fi
done

if [[ ! -f "${FORM_FILE}" || ! -f "${ANSWERS_FILE}" || ! -f "${GENERATOR}" ]]; then
  echo "Error: required files missing. Run from repository root." >&2
  exit 1
fi

export FORM_FILE ANSWERS_FILE OUTPUT_FILE VALIDATE
python3 "${GENERATOR}"

if [[ "${CREATE_ISSUE}" == true ]]; then
  if ! command -v gh >/dev/null 2>&1; then
    echo "Error: gh is required for --create-issue." >&2
    exit 1
  fi
  if ! gh api user -q .login >/dev/null 2>&1; then
    echo "Error: gh is not authenticated. Run: gh auth login" >&2
    exit 1
  fi
  if [[ -z "${PROJECT_NAME}" && -f "${METADATA_FILE}" ]]; then
    PROJECT_NAME="$(jq -r '.project_name // ""' "${METADATA_FILE}")"
  fi
  if [[ -z "${PROJECT_NAME}" ]]; then
    echo "Error: --project-name is required with --create-issue (or run bootstrap-issues.sh first)." >&2
    exit 1
  fi

  title_prefix="$(jq -r '.title_prefix' "${FORM_FILE}")"
  labels="$(jq -r '.issue_labels | join(",")' "${FORM_FILE}")"
  echo "Creating CNCF sandbox application issue..."
  issue_url="$(gh issue create \
    -R cncf/sandbox \
    --title "${title_prefix} ${PROJECT_NAME}" \
    --label "${labels}" \
    --body-file "${OUTPUT_FILE}")"
  echo "Created: ${issue_url}"
  echo "Add this link to README.md under 'Official CNCF application issue'."
fi
