# Sandbox Application Template

A GitHub template repository for preparing a comprehensive [CNCF Sandbox application](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E).

Use this repo to track each requirement from the [CNCF sandbox application form](https://github.com/cncf/sandbox/blob/main/.github/ISSUE_TEMPLATE/application.yml) as an individual GitHub issue. Complete work via pull requests; when a PR merges with `Closes #N`, the linked issue closes and the checklist in [APPLICATION.md](APPLICATION.md) updates automatically.

## Quick start

1. Click **Use this template** to create your own copy of this repository.
2. Clone your new repository and run the bootstrap script:

   ```bash
   git clone git@github.com:YOUR_ORG/YOUR_REPO.git
   cd YOUR_REPO
   ./scripts/bootstrap-issues.sh
   ```

3. Commit the updated `APPLICATION.md` and push.
4. Work through checklist issues—one PR per item, with `Closes #N` in the PR description.
5. When all items are complete, copy content from `application/*.md` into the [official CNCF application form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E) and submit.

## Repository structure

```
.
├── APPLICATION.md              # Main checklist mirroring the CNCF application form
├── application/                  # Draft answers for each application section
│   ├── 01-basic-information.md
│   ├── 02-project-details.md
│   ├── 03-cloud-native-context.md
│   ├── 04-cncf-policies.md
│   ├── 05-pre-submission.md
│   ├── 06-contact-information.md
│   └── 07-additional-information.md
├── scripts/
│   └── bootstrap-issues.sh     # Creates one GitHub issue per checklist item
└── .github/
    ├── checklist-map.json      # Issue definitions and labels
    ├── issue-registry.json     # Generated mapping of slugs to issue numbers
    └── workflows/
        ├── sync-checklist.yml  # Updates APPLICATION.md when issues close
        └── validate-pr-closes-issues.yml
```

## How it works

### Checklist → Issue mapping

[APPLICATION.md](APPLICATION.md) mirrors the [CNCF sandbox application issue form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E), including:

- Basic project information
- Project details (repos, roadmap, community files)
- Cloud native context
- CNCF policies
- Pre-submission critical requirements and recommendations
- Contact and additional information

Each checklist item maps to a GitHub issue created by `./scripts/bootstrap-issues.sh`.

### PR-driven issue closure

1. Pick a checklist issue.
2. Complete the work (update files under `application/` or your project repos).
3. Open a PR with `Closes #123` in the description.
4. On merge, GitHub closes issue #123.
5. The [sync-checklist workflow](.github/workflows/sync-checklist.yml) checks the corresponding box in `APPLICATION.md`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Critical requirements tracked

These items from the CNCF pre-submission checklist are marked `critical` and will cause application closure if missing:

- Apache 2.0 license
- MAINTAINERS file with Name, GitHub ID, and Company/Organization columns
- Direct link to MAINTAINERS file (not contributors graph)
- Repository 6+ months old with active development
- Parent project separation vote (if applicable)
- Reusable project (not reference architecture)

## References

- [CNCF Sandbox repository](https://github.com/cncf/sandbox)
- [CNCF Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md)
- [CNCF Sandbox Application Form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E)
- [Sandbox support expectations](https://contribute.cncf.io/resources/project-services/maturity-levels/#sandbox)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
