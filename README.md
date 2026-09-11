# CNCF Sandbox Application

> **Project name:** _Replace with your project name_
>
> **Official CNCF application issue:** _Link after submission_
>
> **Checklist issues created:** Run `./scripts/bootstrap-issues.sh` after creating your repo from this template.

Prepare a comprehensive [CNCF Sandbox application](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E) before submitting to the TOC.

Application answers live in **[APPLICATION.md](APPLICATION.md)**. This README tracks checklist progress. When complete, run `./scripts/generate-submission.sh` to produce a ready-to-submit `CNCF-SUBMISSION.md`.

## Quick start

1. Click **Use this template** to create your own copy of this repository.
2. Clone and bootstrap checklist issues:

   ```bash
   git clone git@github.com:YOUR_ORG/YOUR_REPO.git
   cd YOUR_REPO
   ./scripts/bootstrap-issues.sh
   ```

3. The bootstrap script prompts for your project name, repo URLs, and optional one-line summary, then commits-ready updates to `README.md` and `APPLICATION.md`.
4. Commit the updated files and push.
5. Work through checklist issues—update fields in [APPLICATION.md](APPLICATION.md), one PR per item, with `Closes #N` in the PR description.
6. When all items are complete:

   ```bash
   ./scripts/generate-submission.sh --validate
   ./scripts/generate-submission.sh --create-issue
   ```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

---

## Application checklist

<!-- checklist-progress:start -->
> **Application progress:** **0 / 33** items complete (0%)  
> `░░░░░░░░░░░░░░░░░░░░` 0%
<!-- checklist-progress:end -->

### Read before proceeding

Thank you for applying to join the CNCF Sandbox. Please familiarize yourself with the:

- CNCF [Sandbox README](https://github.com/cncf/sandbox/blob/main/README.md)
- CNCF [Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md#cncf-project-lifecycle--process)
- CNCF IP Policy, from [section 11 of the CNCF Charter](https://github.com/cncf/foundation/blob/main/charter.md#11-ip-policy), particularly about using the Apache 2.0 License
- CNCF [Allowlist License Policy](https://github.com/cncf/foundation/blob/main/policies-guidance/allowed-third-party-license-policy.md) for dependencies (not core project code)
- CNCF [minimal support and marketing expectations for Sandbox projects](https://contribute.cncf.io/resources/project-services/maturity-levels/#sandbox)

- [ ] Reviewed all prerequisite documentation <!-- checklist:read-prerequisites --> (#ISSUE_READ_PREREQUISITES)

Based on the information in this form, a Contribution Agreement will be sent to the contacts provided. **This must be signed before the Technical Oversight Committee (TOC) can complete a vote on whether to accept the project.** It will be countersigned by the Linux Foundation only after a successful vote.

> [!CAUTION]
> The TOC MUST vote to approve your application and a Contribution Agreement MUST be signed before your project can be considered an official CNCF project. You can not represent your project as "donated" or "contributed" until those steps are completed.

### Basic project information

| Field | Status | Issue | Answer field |
| --- | --- | --- | --- |
| Project summary | ⬜ | #ISSUE_PROJECT_SUMMARY | [project_summary](APPLICATION.md#project_summary) |
| Project description | ⬜ | #ISSUE_PROJECT_SUMMARY | [project_description](APPLICATION.md#project_description) |
| Reusable project (not reference architecture) | ⬜ | #ISSUE_REUSABLE_PROJECT | [not_reference_architecture](APPLICATION.md#not_reference_architecture) |

- [ ] Project summary and description drafted <!-- checklist:project-summary --> (#ISSUE_PROJECT_SUMMARY)
- [ ] Confirmed this is a reusable open source project, not a reference architecture <!-- checklist:reusable-project --> (#ISSUE_REUSABLE_PROJECT)

### Project details

| Field | Status | Issue | Answer field |
| --- | --- | --- | --- |
| Org repo URL | ⬜ | #ISSUE_ORG_AND_REPO_URLS | [org_repo_url](APPLICATION.md#org_repo_url) |
| Project repo URL | ⬜ | #ISSUE_ORG_AND_REPO_URLS | [project_repo_url](APPLICATION.md#project_repo_url) |
| Additional repos | ⬜ | #ISSUE_ORG_AND_REPO_URLS | [additional_repos](APPLICATION.md#additional_repos) |
| Website URL | ⬜ | #ISSUE_WEBSITE_URL | [website_url](APPLICATION.md#website_url) |
| Roadmap | ⬜ | #ISSUE_ROADMAP | [roadmap](APPLICATION.md#roadmap) |
| Roadmap context | ⬜ | #ISSUE_ROADMAP | [roadmap_context](APPLICATION.md#roadmap_context) |
| Contributing guide | ⬜ | #ISSUE_CONTRIBUTING_GUIDE | [contributing_guide](APPLICATION.md#contributing_guide) |
| Code of Conduct | ⬜ | #ISSUE_CODE_OF_CONDUCT | [code_of_conduct](APPLICATION.md#code_of_conduct) |
| Adopters | ⬜ | #ISSUE_ADOPTERS | [adopters](APPLICATION.md#adopters) |
| Maintainers file | ⬜ | #ISSUE_MAINTAINERS_FILE | [maintainers_file](APPLICATION.md#maintainers_file) |
| Security policy | ⬜ | #ISSUE_SECURITY_POLICY | [security_policy](APPLICATION.md#security_policy) |
| Standard or specification | ⬜ | #ISSUE_STANDARD_OR_SPEC | [standard_or_spec](APPLICATION.md#standard_or_spec) |
| Business product separation | ⬜ | #ISSUE_PRODUCT_SEPARATION | [product_separation](APPLICATION.md#product_separation) |

- [ ] Org and repository URLs documented <!-- checklist:org-and-repo-urls --> (#ISSUE_ORG_AND_REPO_URLS)
- [ ] Parent project separation vote linked (or N/A documented) <!-- checklist:parent-separation-vote --> (#ISSUE_PARENT_SEPARATION_VOTE)
- [ ] Website URL documented <!-- checklist:website-url --> (#ISSUE_WEBSITE_URL)
- [ ] Roadmap and context documented <!-- checklist:roadmap --> (#ISSUE_ROADMAP)
- [ ] Contributing guide linked <!-- checklist:contributing-guide --> (#ISSUE_CONTRIBUTING_GUIDE)
- [ ] Code of Conduct linked <!-- checklist:code-of-conduct --> (#ISSUE_CODE_OF_CONDUCT)
- [ ] Adopters list linked or rationale documented <!-- checklist:adopters --> (#ISSUE_ADOPTERS)
- [ ] MAINTAINERS file created with required columns <!-- checklist:maintainers-file --> (#ISSUE_MAINTAINERS_FILE)
- [ ] Security policy linked <!-- checklist:security-policy --> (#ISSUE_SECURITY_POLICY)
- [ ] Standard/specification details documented <!-- checklist:standard-or-spec --> (#ISSUE_STANDARD_OR_SPEC)
- [ ] Business product/service separation documented <!-- checklist:product-separation --> (#ISSUE_PRODUCT_SEPARATION)

> [!NOTE]
> **Organization Diversity**
>
> Organization diversity is not a requirement for Sandbox, but the TOC does consider it during review. Including a "Company" or "Organization" column in your MAINTAINERS file helps the TOC understand the project's contributor base.

### Cloud native context

| Field | Status | Issue | Answer field |
| --- | --- | --- | --- |
| Why CNCF? | ⬜ | #ISSUE_WHY_CNCF | [why_cncf](APPLICATION.md#why_cncf) |
| Benefit to the landscape | ⬜ | #ISSUE_LANDSCAPE_BENEFIT | [landscape_benefit](APPLICATION.md#landscape_benefit) |
| Cloud native fit | ⬜ | #ISSUE_CLOUD_NATIVE_FIT | [cloud_native_fit](APPLICATION.md#cloud_native_fit) |
| Cloud native integration | ⬜ | #ISSUE_CLOUD_NATIVE_INTEGRATION | [cloud_native_integration](APPLICATION.md#cloud_native_integration) |
| Cloud native overlap | ⬜ | #ISSUE_CLOUD_NATIVE_OVERLAP | [cloud_native_overlap](APPLICATION.md#cloud_native_overlap) |
| Similar projects | ⬜ | #ISSUE_SIMILAR_PROJECTS | [similar_projects](APPLICATION.md#similar_projects) |
| Landscape listing | ⬜ | #ISSUE_LANDSCAPE_LISTING | [landscape](APPLICATION.md#landscape) |
| LFX Insights | ⬜ | #ISSUE_LFX_INSIGHTS | [insights](APPLICATION.md#insights) |

- [ ] Why CNCF drafted <!-- checklist:why-cncf --> (#ISSUE_WHY_CNCF)
- [ ] Landscape benefit drafted <!-- checklist:landscape-benefit --> (#ISSUE_LANDSCAPE_BENEFIT)
- [ ] Cloud native fit drafted <!-- checklist:cloud-native-fit --> (#ISSUE_CLOUD_NATIVE_FIT)
- [ ] Cloud native integration drafted <!-- checklist:cloud-native-integration --> (#ISSUE_CLOUD_NATIVE_INTEGRATION)
- [ ] Cloud native overlap drafted <!-- checklist:cloud-native-overlap --> (#ISSUE_CLOUD_NATIVE_OVERLAP)
- [ ] Similar projects documented <!-- checklist:similar-projects --> (#ISSUE_SIMILAR_PROJECTS)
- [ ] Landscape listing status documented <!-- checklist:landscape-listing --> (#ISSUE_LANDSCAPE_LISTING)
- [ ] LFX Insights status documented <!-- checklist:lfx-insights --> (#ISSUE_LFX_INSIGHTS)

### CNCF policies

| Field | Status | Issue | Answer field |
| --- | --- | --- | --- |
| Trademark and accounts | ⬜ | #ISSUE_TRADEMARK_AGREEMENT | [trademark_agreement](APPLICATION.md#trademark_agreement) |
| IP policy | ⬜ | #ISSUE_IP_POLICY_AGREEMENT | [ip_policy_agreement](APPLICATION.md#ip_policy_agreement) |
| License (Apache 2.0) | ⬜ | #ISSUE_APACHE_2_LICENSE | [license](APPLICATION.md#license) |
| License exception | ⬜ | #ISSUE_LICENSE_EXCEPTION | [license_exception](APPLICATION.md#license_exception) |
| Dependency licenses | ⬜ | #ISSUE_DEPENDENCY_LICENSES | [dependency_licenses](APPLICATION.md#dependency_licenses) |
| Domain Technical Review | ⬜ | #ISSUE_DOMAIN_TECHNICAL_REVIEW | [domain_technical_review](APPLICATION.md#domain_technical_review) |

- [ ] Trademark and accounts agreement confirmed <!-- checklist:trademark-agreement --> (#ISSUE_TRADEMARK_AGREEMENT)
- [ ] CNCF IP policy agreement confirmed <!-- checklist:ip-policy-agreement --> (#ISSUE_IP_POLICY_AGREEMENT)
- [ ] License exception review completed <!-- checklist:license-exception --> (#ISSUE_LICENSE_EXCEPTION)
- [ ] Dependency license compliance verified <!-- checklist:dependency-licenses --> (#ISSUE_DEPENDENCY_LICENSES)
- [ ] Domain Technical Review linked (if applicable) <!-- checklist:domain-technical-review --> (#ISSUE_DOMAIN_TECHNICAL_REVIEW)

### Pre-submission checklist

#### Critical requirements (application will be closed if any are missing)

- [ ] Project uses the **Apache 2.0** license <!-- checklist:apache-2-license --> (#ISSUE_APACHE_2_LICENSE)
- [ ] **MAINTAINERS file** exists with Name, GitHub ID, and **Company/Organization** columns <!-- checklist:maintainers-file --> (#ISSUE_MAINTAINERS_FILE)
- [ ] Direct link to MAINTAINERS file provided (not contributors graph, not "N/A") <!-- checklist:maintainers-file --> (#ISSUE_MAINTAINERS_FILE)
- [ ] Repository is **6+ months old** with active development <!-- checklist:repo-age-and-activity --> (#ISSUE_REPO_AGE_AND_ACTIVITY)
- [ ] If separating from a parent project: public vote issue from parent project maintainers linked <!-- checklist:parent-separation-vote --> (#ISSUE_PARENT_SEPARATION_VOTE)
- [ ] Project is **reusable**, not a reference architecture, reference implementation, or company-specific platform <!-- checklist:reusable-project --> (#ISSUE_REUSABLE_PROJECT)

#### Recommended (improves review experience)

- [ ] Code of Conduct, Contributing guide, Security policy properly documented <!-- checklist:code-of-conduct --> (#ISSUE_CODE_OF_CONDUCT) <!-- checklist:contributing-guide --> (#ISSUE_CONTRIBUTING_GUIDE) <!-- checklist:security-policy --> (#ISSUE_SECURITY_POLICY)
- [ ] Adopters list with production users <!-- checklist:adopters --> (#ISSUE_ADOPTERS)
- [ ] Roadmap shows future direction and is publicly accessible <!-- checklist:roadmap --> (#ISSUE_ROADMAP)
- [ ] Similar projects section addresses overlap and differentiation <!-- checklist:similar-projects --> (#ISSUE_SIMILAR_PROJECTS)
- [ ] Maintainers from multiple organizations (employers, not GitHub orgs) <!-- checklist:maintainer-diversity --> (#ISSUE_MAINTAINER_DIVERSITY)

**Common mistakes that result in auto-closure:**

- Linking to contributors graph instead of MAINTAINERS.md file
- License not compliant (BSL, GPL, or promise to convert later)
- Repository younger than 6 months
- Saying "will add [required file] after acceptance"
- Reference architecture or reference implementation submitted as a project

- [ ] Repository age and active development verified <!-- checklist:repo-age-and-activity --> (#ISSUE_REPO_AGE_AND_ACTIVITY)
- [ ] Maintainer organization diversity documented <!-- checklist:maintainer-diversity --> (#ISSUE_MAINTAINER_DIVERSITY)

See [repo_age_evidence](APPLICATION.md#repo_age_evidence) and [maintainer_diversity](APPLICATION.md#maintainer_diversity).

### Contact information

- [ ] Application contact emails and signatory information completed <!-- checklist:contact-information --> (#ISSUE_CONTACT_INFORMATION)

See [application_contact_emails](APPLICATION.md#application_contact_emails) and [signatory_information](APPLICATION.md#signatory_information).

### Additional information

- [ ] CNCF contacts and additional information completed <!-- checklist:additional-information --> (#ISSUE_ADDITIONAL_INFORMATION)

See [cncf_contacts](APPLICATION.md#cncf_contacts) and [additional_information](APPLICATION.md#additional_information).

### Submit to CNCF

When all checklist items above are complete:

1. Generate the submission document: `./scripts/generate-submission.sh --validate`
2. Submit via `./scripts/generate-submission.sh --create-issue --project-name "YourProject"`, or copy [CNCF-SUBMISSION.md](CNCF-SUBMISSION.md) into a [new CNCF sandbox issue](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E).
3. Link the submitted CNCF issue at the top of this README.

- [ ] Final review complete and application submitted to CNCF <!-- checklist:final-review --> (#ISSUE_FINAL_REVIEW)

---

## How checklist tracking works

Each checklist item maps to a GitHub issue created by `./scripts/bootstrap-issues.sh`.

1. Assign the issue to a contributor.
2. Update the relevant field(s) in [APPLICATION.md](APPLICATION.md).
3. Open a pull request with `Closes #123` in the PR description.
4. When the PR merges, GitHub closes the issue automatically.
5. The [sync-checklist workflow](.github/workflows/sync-checklist.yml) checks the corresponding box in this README.

## References

- [CNCF Sandbox repository](https://github.com/cncf/sandbox)
- [CNCF Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md)
- [CNCF Sandbox Application Form](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E)
- [Sandbox support expectations](https://contribute.cncf.io/resources/project-services/maturity-levels/#sandbox)

## License

Apache License 2.0 — see [LICENSE](LICENSE).
