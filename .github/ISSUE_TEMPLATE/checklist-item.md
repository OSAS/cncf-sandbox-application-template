---
name: Sandbox checklist item
description: Track one item of the CNCF sandbox application preparation checklist
title: "[Checklist] "
labels:
  - checklist-item
body:
  - type: markdown
    attributes:
      value: |
        Use this template when creating a custom checklist item. For standard items, run `./scripts/bootstrap-issues.sh` instead—it creates all predefined checklist issues automatically.

        **Workflow**
        1. Open the matching section in `APPLICATION.md` (instructions and issue link are on the checklist line).
        2. Complete **Your answer** and open a pull request that only changes `APPLICATION.md`.
        3. Include `Closes #ISSUE_NUMBER` in the PR description (replace with this issue's number).
        4. When the PR merges, this issue closes and the checkbox in `APPLICATION.md` is updated automatically.

  - type: textarea
    attributes:
      label: Work to complete
      description: Describe what needs to be done for this checklist item.
      placeholder: Add the specific deliverable, file path, or link required.
    validations:
      required: true

  - type: input
    attributes:
      label: Application field
      description: Which field in APPLICATION.md should be updated?
      placeholder: maintainers_file
    validations:
      required: false
