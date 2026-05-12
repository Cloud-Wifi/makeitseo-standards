# Contributing to the MakeitSEO Standards Programme

Thank you for considering a contribution. This document explains how the programme is governed at v0.1, the three contribution types we accept, the conformance bar for implementations directory entries, and the planned Stage 2 transition that will formally open governance.

This is a working document. It will be revised at Stage 2 (§6) to reflect the broader contribution model that takes effect once a technical advisory board is in place.

---

## 1. Governance posture at v0.1

The MakeitSEO Standards Programme is **editor-led** during the v0.1 cycle of both the MakeitSEO Standard and Agent Runtime Compatibility (ARC).

This means:

- **Daniel Titton** (Cloud WiFi Limited) is the sole editor and merge authority for both specifications until Stage 2.
- **Issues are welcome and triaged.** No issue is closed without a reasoned response — even if that response is "deferred to Stage 2" or "out of scope."
- **Pull requests are welcome but advisory.** Acceptance is at editor discretion, with decision criteria set out in §3.
- **The implementations directory has its own lighter path.** See §4.

The editor-led model is a deliberate choice during the bootstrapping phase, not a signal of closed governance. The standard must reach internal coherence before it is stable enough to govern by committee.

---

## 2. What we're looking for

Contributions that will be prioritised:

| Type | Examples |
|------|---------|
| **Implementation feedback** | "We implemented the MakeitSEO Standard and §4.4 was ambiguous in this edge case..." |
| **Coverage gaps** | New AI engines, new answer surfaces, new runtime types not yet in scope |
| **Spec clarifications** | Places where the normative text is unclear, contradictory, or underspecified |
| **Validator issues** | False positives/negatives, missing lint rules, performance issues |
| **Schema improvements** | Type accuracy, completeness, forward compatibility |
| **Translations** | No permission required under CC-BY 4.0; open an issue so we can link to your fork |

Contributions that are out of scope at v0.1:

- Recommendations for what to *do* about findings (the standard measures; it does not prescribe fixes)
- Backlink-related metrics of any kind
- Proprietary or non-verifiable signals

---

## 3. How to contribute

### Step 1 — Open an issue first

For any substantive change (anything that would alter normative text, validator behaviour, or schema shape), open a GitHub Issue before writing code or a pull request. Use the relevant template:

- **Specification change proposal** — for changes to `STANDARD.md` or `ARC.md`
- **Validator bug report** — for bugs in the `@makeitseo/standard` npm package
- **Validator feature request** — for new lint rules or validator capabilities
- **Implementation listing request** — to list a conformant implementation (see §4)
- **General question / discussion** — for anything else

Discussion happens in the issue thread. The editor will indicate whether a PR is invited, deferred, or out of scope before you invest time writing one.

### Step 2 — Fork and branch

```bash
git clone https://github.com/Cloud-Wifi/makeitseo-standards.git
cd makeitseo-standards
git checkout -b fix/your-descriptive-branch-name
```

Branch naming conventions:

| Prefix | Use for |
|--------|---------|
| `fix/` | Corrections to existing normative text or validator behaviour |
| `feat/` | New rules, new schema fields, new spec sections |
| `docs/` | Non-normative improvements (examples, editorial, governance docs) |
| `impl/` | Implementations directory additions |

### Step 3 — Make your changes

For **specification changes:**

- Edit the relevant `.md` file directly.
- Update the version line and changelog entry in the same commit.
- If the change alters validation behaviour, update or add test fixtures in `validator-tests/`.

For **validator changes:**

- Changes to `packages/validator/` must include passing tests.
- Run `npm test` before opening a PR.
- The fabricated-verdict lint rule must not be weakened or bypassed under any circumstances.

For **schema changes:**

- JSON Schema, TypeScript `.d.ts`, and any other type exports must be updated in sync.
- Do not break existing conformant payloads without a major version bump.

### Step 4 — Open a pull request

Reference the issue number in your PR description. PRs without a linked issue will be asked to open one first.

The editor will review, may request changes, and will merge or close with a written reason.

### Commit style

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(standard): add GEO citation-depth field to §4.3
fix(validator): fabricated-verdict rule false-positive on status:not-checked
docs(arc): clarify tool-availability declaration for stateless agents
```

---

## 4. Implementations directory

Any conformant implementation — including products that compete with MakeitSEO — may request a listing in the implementations directory of the relevant specification.

**Requirements:**

1. Your implementation must pass the `@makeitseo/standard` validator at the current major version.
2. You must be able to provide a conformance report (output of `makeitseo-validate`) or equivalent evidence.
3. You must agree to update or remove your listing within 30 days if a new major version is released and your implementation no longer conforms.

**Process:**

Open an issue using the **Implementation listing request** template. Include:

- Product name and URL
- Specification(s) and version(s) you conform to
- A conformance report or link to one

There is no fee, no exclusivity requirement, and no obligation to use MakeitSEO's platform. The implementations directory is the official record of conformant implementations. Listing is a factual statement, not an endorsement.

---

## 5. Licence agreement

By submitting a contribution to this repository, you agree that:

- Your contribution is your own original work, or you have the right to submit it.
- Your contribution is licensed under **CC-BY 4.0** (for documentation, schema, and governance material) or **MIT** (for validator code and test fixtures), consistent with the file types set out in [LICENSE](./LICENSE).
- You grant Cloud WiFi Limited the right to include your contribution in the repository under those terms.

No contributor licence agreement (CLA) signature is required. Your pull request submission constitutes agreement.

---

## 6. Stage 2 — planned governance transition

Approximately 6–8 weeks after the v1.0 release of the MakeitSEO Standard, this programme is expected to transition to Stage 2 governance. Stage 2 will introduce:

- A **technical advisory board** (TAB) — a small group of external experts with formal roles in the specification process. TAB members will be compensated; terms are deferred and will be published when the board is constituted.
- **Formal RFC process** — substantive changes will require an RFC document, comment period, and TAB vote rather than editor discretion alone.
- **Revised CONTRIBUTING.md** — this document will be updated to reflect the Stage 2 process at the time of transition.

The Stage 2 transition will be announced via the repository, `makeitseo.io`, and the newsletter. No existing contributions or conformance claims will be invalidated by the transition.

---

## 7. Questions

If something in this document is unclear, open a **General question / discussion** issue. We'd rather answer a question than have a potential contributor give up.

---

*MakeitSEO Standards Programme · CC-BY 4.0 · Cloud WiFi Limited (UK Co. No. 13521157)*
