# MakeitSEO Standards Programme

Open specifications for measuring and improving website visibility in traditional search engines, answer engines, and AI-generated responses.

[![Licence: CC-BY 4.0](https://img.shields.io/badge/Licence-CC--BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Validator: MIT](https://img.shields.io/badge/Validator-MIT-blue.svg)](./LICENSE-MIT.txt)
[![npm: @makeitseo/standard](https://img.shields.io/npm/v/@makeitseo/standard.svg)](https://www.npmjs.com/package/@makeitseo/standard)

---

## What this is

The MakeitSEO Standards Programme is a set of vendor-neutral, openly licensed specifications that define:

- **What to measure** when auditing a website for search engine, answer engine, and AI visibility.
- **How to score** findings consistently across implementations, so that two conformant tools produce comparable results from the same input.
- **How AI agents** should signal their capabilities, limitations, and operating context to downstream consumers.

Specifications are normative documents. They can be cited, forked, translated, and implemented by anyone — including commercial competitors to MakeitSEO — without permission or licence fees.

---

## Specifications

### MakeitSEO Standard

> Current version: **v0.1** (draft)

The MakeitSEO Standard defines a structured methodology for auditing and scoring website visibility across three dimensions:

| Dimension | Definition |
|-----------|------------|
| **SEO** | Discoverability in traditional web search (Google, Bing, etc.) |
| **AEO** | Answer Engine Optimisation — appearing in featured snippets, knowledge panels, and structured answer surfaces |
| **GEO** | Generative Engine Optimisation — being cited and quoted in LLM-generated responses (ChatGPT, Gemini, Claude, Perplexity, etc.) |

The three scores are independent. The overall score is their mean. No weighting is applied.

→ [`makeitseo-standard/STANDARD.md`](./makeitseo-standard/STANDARD.md)

### Agent Runtime Compatibility (ARC)

> Current version: **v0.1** (draft)

ARC defines a lightweight protocol for AI agents to declare their runtime capabilities, tool availability, and operating constraints in a machine-readable format — enabling orchestrators, pipelines, and downstream consumers to make accurate routing decisions without probing or hallucinating capabilities.

→ [`agent-runtime-compatibility/ARC.md`](./agent-runtime-compatibility/ARC.md)

---

## Four-pillar platform

Each specification ships as four artefacts, not just a document:

| Pillar | What it is |
|--------|------------|
| **Specification document** | The normative `.md` file — the human-readable source of truth |
| **Conformance validator** | CLI + Node.js library (`@makeitseo/standard`) for programmatic compliance checking |
| **Schema and type exports** | JSON Schema, OpenAPI fragment, TypeScript `.d.ts`, and Pydantic model — for embedding in any language and toolchain |
| **Reference implementation** | The MakeitSEO audit engine, which is the designated reference implementation of the MakeitSEO Standard |

The **fabricated-verdict lint rule** is the single most important rule in the validator. It enforces the programme's zero-fabricated-verdicts principle: no conformant tool may report a passing result for a check it did not actually perform.

---

## Validator quick start

```bash
npm install -g @makeitseo/standard
makeitseo-validate ./my-audit-output.json
```

Or programmatically:

```js
import { validate } from '@makeitseo/standard';

const result = validate(auditPayload);
if (!result.valid) {
  console.error(result.errors);
}
```

→ Full API reference in [`makeitseo-standard/VALIDATOR.md`](./makeitseo-standard/VALIDATOR.md)

---

## Public validator

A hosted version of the validator is available at:

**[validate.makeitseo.io](https://validate.makeitseo.io)**

Paste or upload an audit payload and receive a conformance report with line-level diagnostics.

---

## Implementations directory

Conformant implementations — including third-party tools — are listed in:

→ [`makeitseo-standard/IMPLEMENTATIONS.md`](./makeitseo-standard/IMPLEMENTATIONS.md)

To list your implementation, open an issue using the **Implementation listing request** template. There is no fee and no exclusivity requirement. The conformance bar is defined in `STANDARD.md §8`.

---

## Design philosophy

**Measurement before fixes.** The standard defines how to measure. What to do about findings is outside scope. This keeps the spec vendor-neutral and allows any fix methodology to be evaluated against a common baseline.

**No fabricated verdicts.** A conformant implementation must not report a result for a check it did not perform. Absence of data is surfaced as `status: not-checked`, never as a pass.

**LLM-native from v0.1.** GEO is a first-class dimension, not an afterthought. The spec accounts for the reality that a significant and growing share of search queries are now resolved by language models rather than traditional SERPs.

**Non-coercive adoption.** A specification someone *can* adopt is more credible than a methodology someone *must* license. The Programme commits to maintaining specs as open assets that any product or methodology can implement, with no obligation to use MakeitSEO's platform.

The Programme is maintained by [Cloud WiFi Limited](https://cloudwifi.io) (UK Co. No. 13521157), the company behind [MakeitSEO](https://makeitseo.io). Its governance is documented in [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Contributing

Contributions are welcome. The full process is in [CONTRIBUTING.md](./CONTRIBUTING.md). The short version:

- Substantive changes are proposed via GitHub Issues. Discussion happens in the issue thread before any pull request.
- New specifications start as a `v0.1.md` draft and progress to `v1.0` as feedback accumulates.
- Existing specifications evolve via minor version bumps for clarifications and major version bumps for semantic breaks.
- The maintainer (Daniel Titton, Cloud WiFi Limited) holds the editorial decision on what ships at what version, but the discussion is public.

We're particularly interested in:

- Implementation feedback from products that adopt these specs
- Edge cases the current spec doesn't handle clearly
- New runtimes, platforms, and AI engines the spec should account for
- Translations, derivative works, and academic references (no permission required under CC-BY 4.0; we'd love to know they exist)

By contributing, you agree that your contributions are licensed under CC-BY 4.0 (consistent with the rest of the repository). All contributors are bound by the [Code of Conduct](./CODE_OF_CONDUCT.md).

For governance details — decision-making process, versioning policy, and the Stage 2 TAB transition — see [GOVERNANCE.md](./GOVERNANCE.md).

---

## Licensing

The contents of this repository are dual-licensed. See [LICENSE](./LICENSE) for the full notice.

| File type | Licence |
|-----------|---------|
| Specification documents, schema exports, governance docs | [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| Validator code, test fixtures, build scripts, npm package | [MIT](./LICENSE-MIT.txt) |

You may share and adapt the material in any medium or format, for any purpose, including commercially, provided you give appropriate credit, link to the licence, and indicate if changes were made.

**Recommended attribution:**
> Based on the MakeitSEO Standards Programme by Cloud WiFi Limited, licensed under CC-BY 4.0. https://github.com/Cloud-Wifi/makeitseo-standards

---

## Contact

| Channel | Details |
|---------|---------|
| Issues and specification proposals | [GitHub Issues](https://github.com/Cloud-Wifi/makeitseo-standards/issues) |
| Maintainer | Daniel Titton, Cloud WiFi Limited — `daniel@makeitseo.io` |
| Programme home | https://github.com/Cloud-Wifi/makeitseo-standards |
| Platform | https://makeitseo.io |
| Defensive governance domain | https://aivisibilitystandard.com |

---

*MakeitSEO Standards Programme · CC-BY 4.0 (docs) / MIT (code) · Cloud WiFi Limited (UK Co. No. 13521157)*
