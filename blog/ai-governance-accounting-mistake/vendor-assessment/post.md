- **Date:** 2026-05-27
- **Author:** Jake Joyner, AILedger, PBC
- **Companion piece:** Essay "AI governance is repeating accounting's biggest mistake" at [jakejoyner.com/blog/ai-governance-accounting-mistake/](https://jakejoyner.com/blog/ai-governance-accounting-mistake/)
- **Contact:** [help@ailedger.dev](mailto:help@ailedger.dev)

---

## Purpose

This document records the evidence underlying claims about Credo AI and Holistic AI made in the companion essay above. The claims at issue:

1. Both companies' platforms allow customer-configured audit thresholds
2. Both companies automate remediation through their own AI agents
3. (Holistic AI specifically) Holistic AI's founders advise on the regulations the platform sells compliance with

This is a public research note, not legal advice. Every claim below is sourced to the company's own marketing, press releases, product documentation, or third-party catalogs such as OECD's AI Tools listing. URLs are inline so readers can verify each finding independently.

For context, the AILedger Charter v1.3 publicly refuses three feature categories that map directly to the patterns documented below:

> "Configurable detection thresholds that allow suppression below standards-aligned defaults. 'Compliance mode' that generates reports without underlying detection. Removal of required-action workflows for detected events."
>
> Source: [ailedger.dev/charter](https://ailedger.dev/charter)

Charter v1.3 (ratified 2026-05-27) also adds a Scope section that separates detection and reporting (AILedger's role) from remediation (the customer's responsibility), structurally refusing the audit-substrate-as-remediator pattern.

---

## Credo AI

### At a glance

- Headquarters: Palo Alto, California
- Founded: pre-2020 (per their own product page, the company "pioneered" AI governance ahead of the ChatGPT era)
- Funding: $21M raised in 2024 ([credo.ai/resources](https://www.credo.ai/resources))
- Recent recognition: Ranked No. 6 in Applied AI on Fast Company's World's Most Innovative Companies of 2026 ([credo.ai](https://www.credo.ai/))
- Notable customers (per their own marketing): Mastercard, Principal, AdeptID
- Open-source artifact: Credo AI Lens at [github.com/credo-ai/credoai_lens](https://github.com/credo-ai/credoai_lens), Apache 2.0
- Platform URL: [credo.ai](https://www.credo.ai)

### Finding 1: Customer-configured audit thresholds

Credo AI's documented workflow places threshold setting in the customer's hands:

> "Define Governance Requirements: Organizations input internal policies, risk thresholds, and external compliance needs into Credo AI."
>
> Source: [trendingaitools.com/ai-tools/credo-ai/](https://www.trendingaitools.com/ai-tools/credo-ai/)

Credo AI's own blog confirms the pattern as a marketed feature:

> "By aligning policies, risk thresholds, and responsibilities across teams, Credo AI ensures AI risk is managed consistently and without silos."
>
> Source: [credo.ai/blog/third-party-risk-management-for-ai-a-governance-first-approach](https://www.credo.ai/blog/third-party-risk-management-for-ai-a-governance-first-approach)

**Charter conflict:** AILedger Charter v1.3 explicitly refuses "configurable detection thresholds that allow suppression below standards-aligned defaults."

### Finding 2: Automated remediation by Credo AI's own agents

From Credo AI's product page describing what their AI agents do:

> "Specialized AI agents that automate the most time-consuming governance tasks. They retrieve evidence, assess risk, generate governance plans, and remediate incidents, reducing weeks of manual work to minutes while maintaining human oversight for critical decisions."
>
> Source: [credo.ai/product](https://www.credo.ai/product)

The same vendor that performs the audit also generates the governance plan and remediates the incident. The customer remains nominally human-in-the-loop, but the surfacing-to-resolution loop is internal to the audit vendor.

**Charter conflict:** This is the structural pattern the AILedger Charter v1.3 Scope section refuses for AILedger. Detection and reporting must be separated from remediation, because an audit substrate that also remediates can pre-resolve findings before a regulator or affected party sees them.

### Finding 3: AI-powered control recommendations from the audit vendor

Credo AI's "Credo AI Assist" feature is documented as:

> "AI-Powered Control Recommendations: Credo AI Assist improves the recommendations that the Credo AI platform provides for specific risk-mitigating controls that are relevant to a given risk scenario."
>
> Source: [credo.ai/blog/introducing-credo-ai-assist-ai-powered-assistance-to-streamline-ai-governance-workflows](https://www.credo.ai/blog/introducing-credo-ai-assist-ai-powered-assistance-to-streamline-ai-governance-workflows)

An LLM operated by the audit vendor recommends which controls the customer should apply to the AI being audited. There is no reviewer-independent ground truth in this loop.

### Note on Credo AI Lens (open source)

Credo AI's open-source assessment framework, Credo AI Lens, is published under Apache 2.0 at [github.com/credo-ai/credoai_lens](https://github.com/credo-ai/credoai_lens), and a recent SDK release was published in January 2026 ([credo.ai/blog/introducing-the-credo-ai-sdk-build-ai-governance-into-your-existing-workflows](https://www.credo.ai/blog/introducing-the-credo-ai-sdk-build-ai-governance-into-your-existing-workflows)). The open-source artifact is in a more legitimate maintenance state than several competitors in the category. This finding is included for fairness: the closed-source SaaS platform's structural conflicts documented above do not extend to the open-source assessment library.

---

## Holistic AI

### At a glance

- Headquarters: U.S. (Palo Alto and London)
- Founded: 2020
- Co-founders: Adriano Koshiyama (Co-CEO), Emre Kazim (Co-CEO)
- Notable investors: Mozilla Ventures ([aiexpert.network/holistic-ai-ai-governance-for-enterprises](https://aiexpert.network/holistic-ai-ai-governance-for-enterprises/))
- Open-source artifact: [github.com/holistic-ai/holisticai](https://github.com/holistic-ai/holisticai), launched October 2024
- Platform URL: [holisticai.com](https://www.holisticai.com)
- OECD AI Tools catalog entry: [oecd.ai/en/catalogue/tools/holistic-ai-governance,-risk-and-compliance-platform](https://oecd.ai/en/catalogue/tools/holistic-ai-governance,-risk-and-compliance-platform)

### Finding 1: Pre-defined (customer-configured) thresholds

From Holistic AI's Guardian Agents product page:

> "When risk crosses a pre-defined threshold, Operative Agents step in automatically. They block, redirect, quarantine, or remediate unsafe AI behavior in real time."
>
> Source: [holisticai.com/guardian-agents](https://www.holisticai.com/guardian-agents)

"Pre-defined" thresholds are customer-configured thresholds, dressed as runtime enforcement. The substantive feature is identical to the configurable-thresholds pattern documented above for Credo AI.

**Charter conflict:** AILedger Charter v1.3 refuses configurable detection thresholds regardless of how the threshold is labeled.

### Finding 2: Real-time autonomous remediation by the same vendor

From Holistic AI's main governance platform page, describing Operative Agents:

> "When risks are detected, Operative Agents intervene in real time, activating kill switches, blocking unsafe requests, revoking privileges, and remediating violations before harm occurs."
>
> Source: [holisticai.com/ai-governance-platform](https://www.holisticai.com/ai-governance-platform)

The audit substrate is the remediator. Detection and remediation are unified in the same vendor's autonomous agents.

**Charter conflict:** Same as Credo AI Finding 2. This is the substrate-as-remediator pattern the AILedger Charter v1.3 Scope section refuses.

### Finding 3: Holistic AI's founders advise on the regulations Holistic AI sells compliance for

Holistic AI's own press releases describe their founders' regulatory advisory roles directly:

> "Holistic AI's founders are active members, experts, and/or collaborators in the following organizations and initiatives: the National Institute of Standards and Technology (NIST) AI Safety Institute, the UN AI Advisory Body, the OECD's Network of Experts on AI, the Alan Turing Institute, the Assessment and Mitigation working groups for the EU AI Act GPAI Code of Practice, the EU AI Act, the Council of Europe, and the first international convention on AI."
>
Sources — this exact passage appears across multiple Holistic AI press releases:

[holisticai.com/press-release/announcing-holistic-ai-tracker-2-0](https://www.holisticai.com/press-release/announcing-holistic-ai-tracker-2-0)

[holisticai.com/press-release/caseware-aida-evaluation-ai-risk-assurance-safety-protocols-holistic-ai-governance-platform](https://www.holisticai.com/press-release/caseware-aida-evaluation-ai-risk-assurance-safety-protocols-holistic-ai-governance-platform)

[holisticai.com/press-release/holistic-ai-launches-open-source-library-advance-responsible-ai](https://www.holisticai.com/press-release/holistic-ai-launches-open-source-library-advance-responsible-ai)

Co-founder Adriano Koshiyama's own bio on the Holistic AI website confirms his ongoing OECD advisory role:

> "Adriano is an active advisory member on the AI Risks and Accountability group at the OECD AI / Global Partnership on AI."
>
> Source: [holisticai.com/executive-bios/adriano-koshiyama](https://www.holisticai.com/executive-bios/adriano-koshiyama)

The OECD's own AI expert directory lists him independently in the same capacity:

> Source: [oecd.ai/en/community/adriano-koshiyama](https://oecd.ai/en/community/adriano-koshiyama)

**Why this matters for the essay:** the same individuals who advise governments on what AI auditing standards should require also operate the company whose products satisfy those requirements for paying enterprise customers. In financial auditing, this conflict was addressed structurally by Sarbanes-Oxley, which separates the standards-setting body (the Public Company Accounting Oversight Board, independent) from the audit firms that comply with the standards. AI governance has no equivalent separation today.

This is not a claim that any named individual is acting in bad faith. It is a structural observation about the configuration of the field. Independence in fact and independence in appearance, as codified by Sarbanes-Oxley, are violated by this configuration regardless of any individual's intent.

---

## Methodology note

- All citations link to public sources, primarily the named companies' own marketing pages, press releases, and product documentation. Where third-party sources are used (OECD AI Tools catalog, OECD expert directory, third-party AI tools listing sites), the third-party source is named and linked.
- Quoted material is reproduced for purposes of comment, criticism, and reporting on matters of public concern.
- Findings reflect the state of the named platforms and their public marketing as of the date above. Specific features and language may change. If you are reading this document at a later date and the linked URLs return different content, the document should be considered as evidence of what those URLs displayed on the publication date.
- This document is not legal advice and does not constitute a legal opinion about the named companies or individuals.
- Corrections, additions, or disputes from the named companies will be considered in good faith. Contact: [help@ailedger.dev](mailto:help@ailedger.dev).

---

## What this document is not

- This is not an exhaustive competitive review of either company. The findings address specific marketed patterns relevant to the essay's argument about auditor independence.
- This is not a claim that the named companies provide no value. The criticism is structural, applying to the architecture of the audit-vendor-as-remediator pattern, not to the technical competence of the platforms or their staff.
- This is not a claim about the personal motivations of any named individual.

---

## Maintenance

Last updated: 2026-05-27 by Jake Joyner, AILedger, PBC.

If the named platforms substantively change the patterns documented above, this document will be updated. Corrections welcome at [help@ailedger.dev](mailto:help@ailedger.dev).
