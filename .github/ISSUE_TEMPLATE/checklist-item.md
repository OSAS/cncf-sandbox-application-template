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
        1. Complete the work described in the linked checklist item in `APPLICATION.md`.
        2. Open a pull request with your changes.
        3. Include `Closes #ISSUE_NUMBER` in the PR description (replace with this issue's number).
        4. When the PR merges, this issue closes automatically and the checklist in `APPLICATION.md` is updated.

  - type: textarea
    attributes:
      label: Work to complete
      description: Describe what needs to be done for this checklist item.
      placeholder: Add the specific deliverable, file path, or link required.
    validations:
      required: true

  - type: input
    attributes:
      label: Application file
      description: Which file in the application/ directory should be updated?
      placeholder: application/02-project-details.md
    validations:
      required: false
