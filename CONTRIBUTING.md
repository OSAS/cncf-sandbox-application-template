# Contributing to Your Sandbox Application

This repository tracks preparation work for a [CNCF Sandbox application](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E).

## Workflow

### 1. Bootstrap checklist issues

After creating your repository from this template, run:

```bash
./scripts/bootstrap-issues.sh
```

This prompts for basic project info (name, repo URLs, optional summary), creates one GitHub issue per checklist item, and updates `README.md` and `APPLICATION.md`.

### 2. Work on checklist items

Each checklist item in [README.md](README.md) links to a GitHub issue. Pick an issue, update the relevant field(s) in [APPLICATION.md](APPLICATION.md), and open a pull request.

### 3. Close issues via pull requests

Reference the checklist issue in your PR description using GitHub's closing keywords:

```markdown
Closes #12
```

Supported keywords: `Closes`, `Fixes`, `Resolves` (case insensitive).

When the PR merges to the default branch, GitHub closes the linked issue automatically.

### 4. Checklist sync

The [sync-checklist workflow](.github/workflows/sync-checklist.yml) runs when an issue with a `checklist:*` label is closed. It checks the corresponding box in `README.md` and opens a PR (or commits directly if run by a maintainer).

### 5. Submit to CNCF

When all checklist items are complete, generate and submit the application:

```bash
# Validate all required fields are filled in
./scripts/generate-submission.sh --validate

# Option A: create the CNCF issue directly (requires gh auth)
./scripts/generate-submission.sh --create-issue --project-name "YourProject"

# Option B: copy CNCF-SUBMISSION.md into a new CNCF sandbox issue manually
./scripts/generate-submission.sh
```

## Branch naming

Use descriptive branch names:

- `application/project-summary`
- `application/maintainers-file`
- `checklist/apache-license`

## Pull request template

Pull requests should include:

- Which checklist item(s) they address
- `Closes #N` for each completed item
- Which field(s) in `APPLICATION.md` were updated
- A brief summary of changes

## Labels

Issues created by the bootstrap script use these labels:

| Label | Meaning |
| --- | --- |
| `checklist-item` | Part of the application preparation checklist |
| `checklist:<slug>` | Maps to a specific item in README.md |
| `critical` | Required before CNCF submission |
| `recommended` | Improves review experience |
| `phase:*` | Application section grouping |

## References

- [CNCF Sandbox README](https://github.com/cncf/sandbox/blob/main/README.md)
- [CNCF Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md)
- [CNCF Sandbox Application Form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E)
