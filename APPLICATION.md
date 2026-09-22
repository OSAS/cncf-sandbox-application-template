# CNCF Sandbox Application

Single source of truth for the CNCF sandbox application. Each `## field_id` section maps to the [official CNCF application form](https://github.com/cncf/sandbox/blob/main/.github/ISSUE_TEMPLATE/application.yml).

**Work here only:** Each checklist line shows `(Issue: …)` until you open a PR; automation then shows `(PR: …)` in this file and in [README.md](README.md). Edit answers below; do not edit README for application content.

Run `./scripts/generate-submission.sh` when ready to submit to CNCF.

> **Privacy note:** If this repository is public, do not commit private contact emails. Store sensitive contact details locally and fill them in only when generating or submitting the final issue.

---

## read_prerequisites

<!-- field-guide:start -->
Thank you for applying to join the CNCF Sandbox. Read and understand:

- CNCF [Sandbox README](https://github.com/cncf/sandbox/blob/main/README.md)
- CNCF [Project Lifecycle & Process](https://github.com/cncf/toc/blob/main/process/README.md#cncf-project-lifecycle--process)
- CNCF IP Policy, from [section 11 of the CNCF Charter](https://github.com/cncf/foundation/blob/main/charter.md#11-ip-policy), particularly Apache 2.0
- CNCF [Allowlist License Policy](https://github.com/cncf/foundation/blob/main/policies-guidance/allowed-third-party-license-policy.md) for dependencies
- CNCF [minimal support and marketing expectations for Sandbox projects](https://contribute.cncf.io/resources/project-services/maturity-levels/#sandbox)

Based on this form, a Contribution Agreement is sent to your contacts. **It must be signed before the TOC can vote.** Linux Foundation countersigns only after a successful vote.

> [!CAUTION]
> The TOC must approve your application and a Contribution Agreement must be signed before the project is an official CNCF project. Do not represent the project as "donated" or "contributed" until those steps complete.

When finished, add review notes or links under **Your answer** below and open a PR with `Closes` and the issue number on the checklist line.
<!-- field-guide:end -->

- [ ] Reviewed all prerequisite documentation <!-- checklist:read-prerequisites --> (Issue: #ISSUE_READ_PREREQUISITES)

**Your answer:**

_Link to prerequisite review notes or existing project docs._

## project_summary

<!-- field-guide:start -->
Draft the CNCF form fields in the sections below:

- `project_summary` — one-line summary
- `project_description` — 100–300 words on what the project does, why it is needed, and gaps it fills

Open one PR covering both fields; use `Closes` with the issue on the checklist line.
<!-- field-guide:end -->

- [ ] Project summary and description drafted <!-- checklist:project-summary --> (Issue: #ISSUE_PROJECT_SUMMARY)

**Your answer:**

_One-line summary of the project._

## project_description

_100–300 word description of what the project does, why it's needed, and what gaps it fills in the cloud native ecosystem._

## not_reference_architecture

<!-- field-guide:start -->
Confirm this is a **reusable open source project** for broad adoption—not a reference architecture, reference implementation, or demo of patterns.

If this is a reference architecture, apply via [CNCF Reference Architectures](https://architecture.cncf.io/) instead.

Check the box below when confirmed.
<!-- field-guide:end -->

- [ ] This is a reusable open source project designed for broad adoption, not a reference architecture, reference implementation, or demonstration of patterns <!-- checklist:reusable-project --> (Issue: #ISSUE_REUSABLE_PROJECT)

**Your answer:** (check the box above; add notes below if needed)

_Optional notes._

## org_repo_url

<!-- field-guide:start -->
Document URLs for this application:

- `org_repo_url` — org repo if all repos under the org are in scope, or N/A
- `project_repo_url` — primary project repository
- `additional_repos` — other in-scope repos, or leave blank
<!-- field-guide:end -->

- [ ] Org and repository URLs documented <!-- checklist:org-and-repo-urls --> (Issue: #ISSUE_ORG_AND_REPO_URLS)

**Your answer:**

_Org repo URL, or N/A._

## project_repo_url

_Primary project repository URL._

## additional_repos

_Additional repository URLs in scope, or leave blank._

## parent_separation_vote

<!-- field-guide:start -->
If separating from a parent project, link a **public issue** in the parent repo showing maintainer consensus to split. Otherwise document **N/A** in `parent_separation_vote`.
<!-- field-guide:end -->

- [ ] Parent project separation vote linked (or N/A documented) <!-- checklist:parent-separation-vote --> (Issue: #ISSUE_PARENT_SEPARATION_VOTE)

**Your answer:**

_If separating from a parent project, link to the public maintainer vote issue. Otherwise write N/A._

## website_url

<!-- field-guide:start -->
Provide the project website URL, or the primary repo URL if there is no dedicated site.
<!-- field-guide:end -->

- [ ] Website URL documented <!-- checklist:website-url --> (Issue: #ISSUE_WEBSITE_URL)

**Your answer:**

_Project website URL, or primary repo URL if no website._

## roadmap

<!-- field-guide:start -->
Provide a publicly accessible roadmap URL in `roadmap` and optional direction in `roadmap_context`.
<!-- field-guide:end -->

- [ ] Roadmap and context documented <!-- checklist:roadmap --> (Issue: #ISSUE_ROADMAP)

**Your answer:**

_Roadmap URL._

## roadmap_context

_Optional details about roadmap direction._

## contributing_guide

<!-- field-guide:start -->
Link directly to the project's contributing guide (not a promise to add one later).
<!-- field-guide:end -->

- [ ] Contributing guide linked <!-- checklist:contributing-guide --> (Issue: #ISSUE_CONTRIBUTING_GUIDE)

**Your answer:**

_Direct link to the contributing guide._

## code_of_conduct

<!-- field-guide:start -->
Link directly to the project's Code of Conduct.
<!-- field-guide:end -->

- [ ] Code of Conduct linked <!-- checklist:code-of-conduct --> (Issue: #ISSUE_CODE_OF_CONDUCT)

**Your answer:**

_Direct link to the Code of Conduct._

## adopters

<!-- field-guide:start -->
Link to an adopters file or explain why one does not exist yet.
<!-- field-guide:end -->

- [ ] Adopters list linked or rationale documented <!-- checklist:adopters --> (Issue: #ISSUE_ADOPTERS)

**Your answer:**

_Link to adopters file, or leave blank._

## maintainers_file

<!-- field-guide:start -->
Create or verify `MAINTAINERS.md` with **Name**, **GitHub ID**, and **Company/Organization** columns. Use a direct GitHub `/blob/` link—not the contributors graph.

Example:

| Maintainer | GitHub ID | Company/Organization |
| ---------- | --------- | -------------------- |
| Jane Doe   | @janedoe  | Acme Corp            |

> [!NOTE]
> Organization diversity is not required for Sandbox, but the TOC considers it. A Company/Organization column helps reviewers understand your contributor base.
<!-- field-guide:end -->

- [ ] MAINTAINERS file created with required columns <!-- checklist:maintainers-file --> (Issue: #ISSUE_MAINTAINERS_FILE)

**Your answer:**

_Direct GitHub `/blob/` link to MAINTAINERS.md with Name, GitHub ID, and Company/Organization columns._

## security_policy

<!-- field-guide:start -->
Link to `SECURITY.md` or your security policy. See [CNCF security guidelines](https://contribute.cncf.io/maintainers/security/security-guidelines/#3-securitymd) and [templates](https://github.com/cncf/tag-security/tree/main/community/resources/project-resources/templates).
<!-- field-guide:end -->

- [ ] Security policy linked <!-- checklist:security-policy --> (Issue: #ISSUE_SECURITY_POLICY)

**Your answer:**

_Direct link to SECURITY.md or security policy._

## standard_or_spec

<!-- field-guide:start -->
If the project is or includes a standard or specification, describe it. Otherwise write **N/A**.
<!-- field-guide:end -->

- [ ] Standard/specification details documented <!-- checklist:standard-or-spec --> (Issue: #ISSUE_STANDARD_OR_SPEC)

**Your answer:**

_If this project is or includes a standard or specification, provide details. Otherwise write N/A._

## product_separation

<!-- field-guide:start -->
Explain separation from related commercial products or services, or state: "This project is unrelated to any product or service."
<!-- field-guide:end -->

- [ ] Business product/service separation documented <!-- checklist:product-separation --> (Issue: #ISSUE_PRODUCT_SEPARATION)

**Your answer:**

_Explain separation from commercial products/services, or write: "This project is unrelated to any product or service."_

## why_cncf

<!-- field-guide:start -->
Why contribute the project to CNCF? What value does CNCF membership provide?
<!-- field-guide:end -->

- [ ] Why CNCF drafted <!-- checklist:why-cncf --> (Issue: #ISSUE_WHY_CNCF)

**Your answer:**

_Why contribute the project to CNCF? What value does CNCF membership provide?_

## landscape_benefit

<!-- field-guide:start -->
How will adding this project benefit the Cloud Native Landscape?
<!-- field-guide:end -->

- [ ] Landscape benefit drafted <!-- checklist:landscape-benefit --> (Issue: #ISSUE_LANDSCAPE_BENEFIT)

**Your answer:**

_How will adding this project benefit the Cloud Native Landscape?_

## cloud_native_fit

<!-- field-guide:start -->
Where does the project fit in the cloud native landscape?
<!-- field-guide:end -->

- [ ] Cloud native fit drafted <!-- checklist:cloud-native-fit --> (Issue: #ISSUE_CLOUD_NATIVE_FIT)

**Your answer:**

_Where does the project fit in the cloud native landscape?_

## cloud_native_integration

<!-- field-guide:start -->
Which CNCF projects does this complement or depend on?
<!-- field-guide:end -->

- [ ] Cloud native integration drafted <!-- checklist:cloud-native-integration --> (Issue: #ISSUE_CLOUD_NATIVE_INTEGRATION)

**Your answer:**

_What CNCF projects does this complement or depend on?_

## cloud_native_overlap

<!-- field-guide:start -->
Which CNCF projects overlap, and how do you differentiate?
<!-- field-guide:end -->

- [ ] Cloud native overlap drafted <!-- checklist:cloud-native-overlap --> (Issue: #ISSUE_CLOUD_NATIVE_OVERLAP)

**Your answer:**

_What CNCF projects does this overlap with, and how?_

## similar_projects

<!-- field-guide:start -->
List similar projects in CNCF or elsewhere, or write **N/A**.
<!-- field-guide:end -->

- [ ] Similar projects documented <!-- checklist:similar-projects --> (Issue: #ISSUE_SIMILAR_PROJECTS)

**Your answer:**

_Similar projects in CNCF or elsewhere. Write N/A if none._

## landscape

<!-- field-guide:start -->
Are you listed on [landscape.cncf.io](https://landscape.cncf.io/)? Document status and link if applicable.
<!-- field-guide:end -->

- [ ] Landscape listing status documented <!-- checklist:landscape-listing --> (Issue: #ISSUE_LANDSCAPE_LISTING)

**Your answer:**

_Are you listed on [landscape.cncf.io](https://landscape.cncf.io/)?_

## insights

<!-- field-guide:start -->
Are you listed on [LFX Insights](https://insights.linuxfoundation.org/)? Document status.
<!-- field-guide:end -->

- [ ] LFX Insights status documented <!-- checklist:lfx-insights --> (Issue: #ISSUE_LFX_INSIGHTS)

**Your answer:**

_Are you listed on [LFX Insights](https://insights.linuxfoundation.org/)?_

## trademark_agreement

<!-- field-guide:start -->
If accepted, you agree to donate project trademarks and accounts to the CNCF. Check the box when you accept.
<!-- field-guide:end -->

- [ ] If the project is accepted, I agree to donate all project trademarks and accounts to the CNCF <!-- checklist:trademark-agreement --> (Issue: #ISSUE_TRADEMARK_AGREEMENT)

**Your answer:** (check the box above; add notes below if needed)

_Optional notes._

## ip_policy_agreement

<!-- field-guide:start -->
If accepted, the project will follow the CNCF IP Policy. Check the box when you accept.
<!-- field-guide:end -->

- [ ] If the project is accepted, I agree the project will follow the CNCF IP Policy <!-- checklist:ip-policy-agreement --> (Issue: #ISSUE_IP_POLICY_AGREEMENT)

**Your answer:** (check the box above; add notes below if needed)

_Optional notes._

## license

<!-- field-guide:start -->
**Critical:** License must be Apache 2.0 (or an approved exception documented separately) **before** acceptance—not after.

Document the license and link to the `LICENSE` file in the project repo.

Common auto-closure mistakes: BSL/GPL, or promising to relicense later.
<!-- field-guide:end -->

- [ ] Apache 2.0 license compliance documented <!-- checklist:apache-2-license --> (Issue: #ISSUE_APACHE_2_LICENSE)

**Your answer:**

_Project license (must be Apache 2.0) and link to LICENSE file._

## license_exception

<!-- field-guide:start -->
Document whether a CNCF license exception is needed. Write **N/A** if using Apache 2.0 with no exception.
<!-- field-guide:end -->

- [ ] License exception review completed <!-- checklist:license-exception --> (Issue: #ISSUE_LICENSE_EXCEPTION)

**Your answer:**

_Write N/A if using Apache 2.0 with no exception needed._

## dependency_licenses

<!-- field-guide:start -->
Verify dependency licenses are on the [CNCF allowlist](https://github.com/cncf/foundation/blob/main/policies-guidance/allowed-third-party-license-policy.md) or have approved exceptions. Write **N/A** if fully compliant.
<!-- field-guide:end -->

- [ ] Dependency license compliance verified <!-- checklist:dependency-licenses --> (Issue: #ISSUE_DEPENDENCY_LICENSES)

**Your answer:**

_Write N/A if all dependency licenses are on the CNCF allowlist or an approved exception._

## domain_technical_review

<!-- field-guide:start -->
Optional: link TAG engagement, presentations, or a completed General Technical Review questionnaire. Leave blank if not applicable.
<!-- field-guide:end -->

- [ ] Domain Technical Review linked (if applicable) <!-- checklist:domain-technical-review --> (Issue: #ISSUE_DOMAIN_TECHNICAL_REVIEW)

**Your answer:**

_TAG engagement, presentations, or General Technical Review links. Leave blank if not applicable._

## repo_age_evidence

<!-- field-guide:start -->
**Critical:** Repository must be at least **6 months** old with evidence of active development (recent commits, releases, etc.).

Document creation date and activity below.

Common mistake: submitting a repo younger than six months.
<!-- field-guide:end -->

- [ ] Repository age and active development verified <!-- checklist:repo-age-and-activity --> (Issue: #ISSUE_REPO_AGE_AND_ACTIVITY)

**Your answer:**

_Repository creation date and evidence of active development (recent commits, releases, etc.)._

## maintainer_diversity

<!-- field-guide:start -->
Document maintainer **employer** diversity. Different GitHub org memberships do **not** count as organization diversity.
<!-- field-guide:end -->

- [ ] Maintainer organization diversity documented <!-- checklist:maintainer-diversity --> (Issue: #ISSUE_MAINTAINER_DIVERSITY)

**Your answer:**

_Maintainer employers. Different GitHub org memberships do not count as organization diversity._

## application_contact_emails

<!-- field-guide:start -->
Add application contact emails in `application_contact_emails` and Contribution Agreement signatory details in `signatory_information` (table format from the CNCF form).

> [!WARNING]
> If this repo is public, avoid committing private emails. Use a private fork or fill contacts only when generating the submission locally.
<!-- field-guide:end -->

- [ ] Application contact emails and signatory information completed <!-- checklist:contact-information --> (Issue: #ISSUE_CONTACT_INFORMATION)

**Your answer:**

_Comma-separated application contact email addresses._

## signatory_information

_Contribution Agreement signatory details. Use the table format from the CNCF form._

## cncf_contacts

<!-- field-guide:start -->
Add CNCF leadership contacts familiar with the project (TOC, TAGs, etc.) in `cncf_contacts` and any extra TOC context in `additional_information`.
<!-- field-guide:end -->

- [ ] CNCF contacts and additional information completed <!-- checklist:additional-information --> (Issue: #ISSUE_ADDITIONAL_INFORMATION)

**Your answer:**

_CNCF leadership contacts familiar with the project (TOC, TAGs, etc.)._

## additional_information

_Any additional context for the TOC._

## final_review

<!-- field-guide:start -->
When every checklist item above is complete:

```bash
./scripts/generate-submission.sh --validate
./scripts/generate-submission.sh --create-issue --project-name "YourProject"
```

Or copy `CNCF-SUBMISSION.md` into a [new CNCF sandbox issue](https://github.com/cncf/sandbox/issues/new?assignees=&labels=New&projects=&template=application.yml&title=%5BSandbox%5D+%3CProject+Name%3E).

`--create-issue` records the CNCF issue link in this section and in README automatically. Then open a PR with `Closes` and the final-review issue number.
<!-- field-guide:end -->

- [ ] Final review complete and application submitted to CNCF <!-- checklist:final-review --> (Issue: #ISSUE_FINAL_REVIEW)

**Your answer:**

_Link to the submitted CNCF sandbox issue after submission._
