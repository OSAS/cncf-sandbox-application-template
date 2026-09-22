# Contributing to Your Sandbox Application

This repository tracks preparation work for a [CNCF Sandbox application](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E).

## Workflow

### 1. Bootstrap checklist issues

After creating your repository from this template, run:

```bash
./scripts/bootstrap-issues.sh
```

This prompts for basic project info (name, repo URLs, optional summary), creates one GitHub issue per checklist item, and writes issue numbers onto the matching checklist lines in **[APPLICATION.md](APPLICATION.md)**. It also updates README metadata (project name only)—not checklist content.

### 2. Work on checklist items (APPLICATION.md only)

Open **[APPLICATION.md](APPLICATION.md)** and stay in that file for all application work.

Each section includes:

- Instructions for what to complete
- A checklist line with `(Issue: [#N](…))` (after bootstrap)
- A **Your answer** area for form content

Pick an issue, edit the relevant section(s) in `APPLICATION.md`, and open a pull request with `Closes #N`. Automation updates the checklist line to `(PR: [#…](…))` in **both** `APPLICATION.md` and [README.md](README.md). **Do not edit README** for answers or tracking.

Progress lives in README only; it updates when checklist boxes are checked after issues close.

### 3. Close issues via pull requests

Reference the checklist issue in your PR description:

```markdown
Closes #12
```

Supported keywords: `Closes`, `Fixes`, `Resolves` (case insensitive).

When the PR merges to the default branch, GitHub closes the linked issue automatically.

### 4. Checklist sync

The [sync-checklist-pr workflow](.github/workflows/sync-checklist-pr.yml) runs when you open or update a PR with `Closes #N`, replacing `(Issue: …)` with `(PR: …)` in `APPLICATION.md` and README.

The [sync-checklist workflow](.github/workflows/sync-checklist.yml) runs when a checklist issue is closed. It checks the box in `APPLICATION.md`, refreshes the README dashboard and progress bar, and opens a PR.

### 5. Submit to CNCF

When all checklist items are complete:

```bash
# Validate all required fields are filled in
./scripts/generate-submission.sh --validate

# Option A: create the CNCF issue directly (requires gh auth)
./scripts/generate-submission.sh --create-issue --project-name "YourProject"

# Option B: copy CNCF-SUBMISSION.md into a new CNCF sandbox issue manually
./scripts/generate-submission.sh
```

`--create-issue` records the CNCF issue URL in README metadata and in the `final_review` section of `APPLICATION.md`.

## Branch naming

Use descriptive branch names:

- `application/project-summary`
- `application/maintainers-file`
- `checklist/apache-license`

## Pull request template

Pull requests should include:

- Which checklist item(s) they address
- `Closes #N` for each completed item
- Which section(s) in `APPLICATION.md` were updated
- A brief summary of changes

## Labels

Issues created by the bootstrap script use these labels:

| Label | Meaning |
| --- | --- |
| `checklist-item` | Part of the application preparation checklist |
| `checklist:<slug>` | Maps to a specific checkbox in APPLICATION.md |
| `critical` | Required before CNCF submission |
| `recommended` | Improves review experience |
| `phase:*` | Application section grouping |

## References

- [CNCF Sandbox README](https://github.com/cncf/sandbox/blob/main/README.md)
- [CNCF Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md)
- [CNCF Sandbox Application Form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E)
