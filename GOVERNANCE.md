# Governance — MakeitSEO Standards Programme

## Current governance model: Editor-led (v0.1)

The MakeitSEO Standards Programme uses an **editor-led** model during the v0.1 cycle. This document defines how decisions are made, how the programme will transition to Stage 2 open governance, and the roles and processes that apply at each stage.

---

## 1. Roles

| Role | Holder | Scope |
|------|--------|-------|
| **Editor** | Daniel Titton (Cloud WiFi Limited) | Normative authority for all specifications during Stage 1 (v0.1) |
| **Contributor** | Anyone | Permitted to submit issues and advisory pull requests (see CONTRIBUTING.md) |
| **Implementor** | Any organisation that ships a conformant product | Listed in `implementations/` after passing the validator |
| **Technical Advisor** | TBD (Stage 2) | Will form the Technical Advisory Board (TAB) |

The editor role will pass to the Technical Advisory Board at Stage 2 (target: v1.0 publication).

---

## 2. Decision-making at Stage 1 (v0.1)

### What the editor decides unilaterally

- All changes to normative specification text
- The version numbering and release timeline
- Which issues are in scope vs out of scope
- Which pull requests are merged, modified, or declined

### What the editor must document

- All rejections of pull requests that change normative text (a written reason must be added to the PR within 30 days)
- All changes classified as "breaking" under the versioning policy (§4)
- ADR-level decisions (via `methodology-adr/` entries)

### Appeal process

During Stage 1 there is no formal appeal process. The editor's decision is final. If you believe a decision is inconsistent with the programme's stated principles, you may fork the repository under the CC-BY 4.0 licence (specification text) or the MIT licence (validator code).

---

## 3. Versioning policy

Versions follow a `v{major}.{minor}` scheme (e.g. `v0.1`, `v0.2`, `v1.0`).

| Change type | Effect on version |
|-------------|------------------|
| Clarification (non-normative, no behavioural change) | Patch note; no version increment |
| Normative extension (new MUST/SHOULD rules; backwards-compatible) | Minor increment (e.g. `v0.1` → `v0.2`) |
| Breaking change (removes, renames, or tightens existing rules in a way that could break conformant implementations) | Major increment (e.g. `v0.x` → `v1.0`) |

Version `v0.x` is explicitly a pre-stable series. Breaking changes are permitted with appropriate notice.

Version `v1.0` marks the first stable release. From v1.0 onwards, breaking changes require TAB approval and a minimum 90-day notice period.

---

## 4. Stage 2 transition

**Target:** When the MakeitSEO Standard reaches `v1.0`.

Stage 2 opens the following:

1. **Technical Advisory Board (TAB)** formed — minimum 5 members from at least 3 independent organisations
2. **TAB controls** all breaking changes and the release roadmap
3. **Editor becomes TAB secretary** (drafts specs, manages repo operations)
4. **Working Groups** may be chartered by the TAB for specific topic areas
5. **Implementors list** becomes a voting constituency for version proposals

Stage 2 governance will be documented in a revised version of this file prior to its activation.

---

## 5. Conflicts of interest

The editor (Cloud WiFi Limited / MakeitSEO) is also the publisher of the designated reference implementation. This creates a structural conflict that is acknowledged and managed through:

1. The `fabricated-verdict` lint rule: no conformant tool may report a passing result for a check it did not perform — this prevents the reference implementation from gaining scoring advantages by silently skipping checks
2. The open validator: all conformance checks are implemented in the public validator; no private pass/fail criteria exist
3. The ADR process: all scoring decisions are recorded with decision rationale in `methodology-adr/`

---

## 6. Contact

For governance questions: open a GitHub Issue with the label `governance`.

For legal or licensing questions: contact legal@makeitseo.com
