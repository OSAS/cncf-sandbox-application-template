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
        1. Complete the work described in the linked checklist item in `README.md`.
        2. Update the relevant field(s) in `APPLICATION.md`.
        3. Open a pull request with your changes.
        4. Include `Closes #ISSUE_NUMBER` in the PR description (replace with this issue's number).
        5. When the PR merges, this issue closes automatically and the checklist in `README.md` is updated.

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
