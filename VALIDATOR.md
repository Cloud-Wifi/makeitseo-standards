# AI Visibility Audit Standard — Validator Specification v0.1

**Conformance validator for the AI Visibility Audit Standard**

Cloud WiFi Limited · Published 23 April 2026 · Licensed under CC-BY 4.0

This document specifies the behaviour of a conformant validator for the AI Visibility Audit Standard. It is a companion document to STANDARD.md and is published alongside it at `standard.makeitseo.io/validator`. Source is maintained at `github.com/cloud-wifi/makeitseo-standard`.

---

## 1. Purpose and scope

### 1.1 Purpose

This document specifies the behaviour of a conformant validator — the executable layer of the AI Visibility Audit Standard. Where STANDARD.md defines what an audit report must contain, this document defines how conformance is mechanically determined. The two documents together constitute the executable specification of the standard.

The validator exists because claims of standard conformance must be testable. A document alone — no matter how well written — permits rhetorical conformance: vendors citing the standard in marketing while shipping audits that diverge from it. The validator turns claims into facts. A tool that passes the validator conforms; a tool that fails does not; there is no third category.

### 1.2 Scope

This document specifies:

- The validator's command-line interface, including all commands, flags, and stdin/stdout behaviour.
- The ten lint rules that determine conformance, each with exact trigger conditions, severities, and finding shapes.
- The JSON output format emitted by the validator, including the finding schema and summary block.
- Exit codes and their semantics.
- Version pinning behaviour — how a validator handles audit reports declaring a different standard version.
- The public HTTP endpoint at `validate.makeitseo.io`, including rate limits, error responses, and the badge-issuance protocol.
- What it means to claim conformance as a validator (third-party validators are permitted; the standard does not require use of the reference validator published by Cloud WiFi Limited).

### 1.3 Non-goals

This document does not:

- Specify the internal code structure, language, or architecture of any implementation. A conformant validator may be written in any language.
- Prescribe user-interface conventions for tools that wrap the validator. A GUI audit tool that embeds the validator is free to present findings however it wishes, provided the underlying finding set is unmodified.
- Define validation rules beyond those required for conformance. A validator may emit additional warnings or info-level findings outside the ten named rules, provided such findings are clearly distinguished from the named rules and do not affect the conformance determination.

### 1.4 Relationship to STANDARD.md

The validator is subordinate to STANDARD.md. Where the two documents diverge on the meaning of conformance, STANDARD.md governs. This document specifies the mechanics of checking conformance; it does not define conformance itself.

Each lint rule in §3 cites the specific section of STANDARD.md that the rule enforces. When STANDARD.md is revised, lint rules that enforce revised sections are updated in lockstep.

---

## 2. Command-line interface

### 2.1 Distribution

The reference validator is published as an npm package at `@makeitseo/standard`. It is runnable via `npx` without prior installation and has no required configuration. A conformant validator published by a third party MAY use any distribution mechanism appropriate to its implementation language.

All examples in this document use the `npx @makeitseo/standard` invocation for concreteness. The commands, flags, and behaviour they specify apply equally to any conformant validator, regardless of distribution.

### 2.2 Commands

A conformant validator MUST implement the following four commands:

| Command | Purpose |
| --- | --- |
| `lint` | Validate a single audit report against the standard. |
| `diff` | Compare two audit reports and report structural differences. |
| `export` | Emit a derivative artifact (JSON Schema, OpenAPI, TypeScript, etc.) from the spec. |
| `version` | Print the standard version supported and the validator's own version. |

A validator MAY implement additional commands beyond this set. Additional commands MUST NOT reuse any of the four command names above with divergent semantics.

### 2.3 The `lint` command

#### 2.3.1 Synopsis

```
lint [--level <level>] [--rules <list>] [--format <format>] [--strict] <file> | -
```

#### 2.3.2 Arguments and flags

**`<file>`** — path to a JSON file containing the audit report. Exactly one of `<file>` or `-` (stdin) MUST be provided. The file MUST be encoded in UTF-8.

**`-`** — read the audit report from standard input. Stdin MUST be consumed until EOF and parsed as a single JSON document. Streaming or line-delimited JSON is not supported in v0.1.

**`--level <level>`** — the conformance level to validate against. One of `minimal`, `standard`, `full`. When omitted, the validator uses the `level` field declared in the audit report itself. When both are omitted, the default is `standard`. An explicit `--level` flag overrides the audit's declared level; this is the correct behaviour for "can this audit claim level X?" queries.

**`--rules <list>`** — a comma-separated list of rule IDs to enable, or `all` (the default). A rule ID may be prefixed with `-` to disable a specific rule from the `all` set (e.g., `--rules all,-evidence-complete`). Rules disabled by this flag MUST NOT appear in the output. An audit that would have failed due to a disabled rule MUST be reported as conformant with a single `info`-level finding noting which rules were disabled.

**`--format <format>`** — output format. One of `json` (the default), `text`, or `junit`. See §4.

**`--strict`** — treat all `warning`-severity findings as `error`-severity for the purpose of determining conformance and exit code. Default is off.

#### 2.3.3 Execution order

A conformant `lint` invocation MUST proceed in the following order. Each stage blocks on completion of the previous stage:

1. **Read input.** Parse the file path or stdin into a UTF-8 byte stream.
2. **Parse JSON.** If JSON parsing fails, emit a single `error`-severity finding with rule ID `schema-conformance` and terminate with exit code 2.
3. **Resolve spec version.** Read `standard_version` from the audit. If the field is absent, emit an `error`-severity finding with rule ID `schema-conformance` and continue. If the version does not match the validator's declared supported version, apply the version-mismatch protocol in §5.
4. **Resolve conformance level.** Apply the `--level` flag if present; otherwise use the `level` field from the audit; otherwise default to `standard`.
5. **Run rules.** Execute each enabled rule against the audit. Rules MUST execute deterministically — a single audit produces a single finding set per validator version.
6. **Aggregate findings.** Combine all findings into the output structure specified in §4.
7. **Emit output.** Write the finding set to stdout in the requested format.
8. **Exit.** Apply the exit-code protocol in §6.

A validator MAY parallelise rule execution internally provided the output finding set is identical to what a sequential execution would produce. Ordering within the finding set is specified in §4.2.

#### 2.3.4 Determinism

Given the same validator version, the same audit report input, and the same flag set, the output MUST be byte-identical across invocations. This is the lint-level analogue of the schema determinism requirement in STANDARD.md §5.2. A validator that produces non-deterministic output — for example, because findings are ordered by wall-clock timing of internal checks — is non-conformant.

### 2.4 The `diff` command

#### 2.4.1 Synopsis

```
diff [--format <format>] <before> <after>
```

#### 2.4.2 Arguments

**`<before>`** and **`<after>`** — paths to two audit report JSON files. Both MUST be parseable as conformant audits at the `minimal` level or higher; if either fails to parse, the validator terminates with exit code 2 and a single `error` finding identifying the malformed input.

#### 2.4.3 Output

The `diff` command emits a structured comparison of the two audits. The output MUST distinguish:

- **Check-level differences.** Checks present in one audit but not the other; checks present in both but with different verdicts; checks present in both with the same verdict but different evidence.
- **Score differences.** Per-pillar score changes and overall score change. When either audit lacks scoring, that axis MUST be reported as `null`.
- **Metadata differences.** Differences in `implementation`, `timestamp`, or `methodology.engine_version` that indicate the audits were produced by different tools or different versions of the same tool. These differences are informational, not conformance findings.

The `diff` command is informational and does not produce conformance findings. Exit code is 0 on successful diff computation regardless of whether the two audits differ, and 2 on parse failure.

#### 2.4.4 Example output

```json
{
  "before": { "audited_url": "https://example.com", "timestamp": "2026-04-23T10:30:00Z" },
  "after":  { "audited_url": "https://example.com", "timestamp": "2026-04-30T10:30:00Z" },
  "checks": {
    "added": [],
    "removed": [],
    "verdict_changed": [
      { "id": "seo.title_tag", "before": "warning", "after": "pass" }
    ],
    "evidence_changed": [
      { "id": "geo.directory_presence" }
    ]
  },
  "scoring": {
    "pillar_scores": {
      "seo": { "before": 75, "after": 87, "delta": 12 },
      "aeo": { "before": 60, "after": 60, "delta": 0 },
      "geo": { "before": 50, "after": 55, "delta": 5 }
    },
    "overall_score": { "before": 62, "after": 67, "delta": 5 }
  }
}
```

### 2.5 The `export` command

#### 2.5.1 Synopsis

```
export --format <format> [--version <version>]
```

#### 2.5.2 Arguments

**`--format <format>`** — required. One of: `json-schema`, `openapi`, `typescript`, `python`, `postman`. A conformant validator MUST support at least `json-schema`; the other four SHOULD be supported.

**`--version <version>`** — optional. The standard version to export. When omitted, the validator exports the version it natively supports.

#### 2.5.3 Determinism

Every export invocation with the same validator version and the same `--format` and `--version` arguments MUST produce byte-identical output. This matches STANDARD.md §5.2.

#### 2.5.4 Output destination

The `export` command writes to stdout by default. A validator MAY accept an `--out` flag to write to a file. When writing to stdout, no trailing newline or byte-order mark may be added to otherwise-deterministic formats.

### 2.6 The `version` command

#### 2.6.1 Synopsis

```
version [--format <format>]
```

#### 2.6.2 Output

The `version` command emits a small JSON object identifying the validator and the standard version it supports:

```json
{
  "validator": "@makeitseo/standard",
  "validator_version": "1.0.0",
  "standard_version": "0.1",
  "supported_export_formats": ["json-schema", "openapi", "typescript"]
}
```

A validator supporting multiple standard versions MUST list them as an array under `supported_standard_versions` instead of the singular `standard_version`.

---

## 3. Lint rules

A conformant validator MUST implement the ten lint rules specified in this section. Each rule is identified by a stable rule ID that MUST NOT change between patch versions of the standard. Rule IDs are lowercase, hyphen-separated ASCII strings.

Each rule specification below contains:
- **ID** — the stable identifier.
- **Severity** — `error`, `warning`, or `info`. A rule's severity MAY be overridden by `--strict` (which promotes `warning` to `error`) but not otherwise modified.
- **Enforces** — the STANDARD.md section(s) the rule enforces.
- **Trigger** — the precise condition under which the rule emits a finding.
- **Finding message template** — the shape of the `message` field emitted.

### 3.1 schema-conformance

**ID.** `schema-conformance`

**Severity.** `error`

**Enforces.** STANDARD.md §7 (Audit report format) and the exported JSON Schema at `standard.makeitseo.io/v0.1/audit-report.schema.json`.

**Trigger.** The audit report does not validate against the JSON Schema for the resolved conformance level. This includes: missing required fields, fields of the wrong type, and violations of conditional requirements (for example, a `full`-level audit missing its `scoring` block).

**Finding message template.** `Schema violation at <path>: <details>` — where `<path>` is a JSON Pointer to the offending field and `<details>` is the JSON Schema validator's error message.

**Note.** A single audit may trigger multiple `schema-conformance` findings. The validator MUST emit one finding per distinct violation rather than aggregating them into a single message. This is the rule that makes machine-readable lint output useful for automated remediation.

### 3.2 check-id-valid

**ID.** `check-id-valid`

**Severity.** `error`

**Enforces.** STANDARD.md §5 (Check specifications) and §7.3 (Non-standard check extensions).

**Trigger.** A check ID in the audit report is prefixed with one of the three pillar namespaces (`seo.`, `aeo.`, `geo.`) but does not appear in the spec's check set for the resolved version. Counterfeit checks within the core namespaces are rejected; legitimate extensions outside them are permitted (see `unknown-check`).

**Finding message template.** `Unknown check ID '<check_id>'. Check IDs in the core pillar namespaces (seo., aeo., geo.) must be defined in the spec. Non-standard checks MUST be namespaced outside the core (e.g., 'ext.vendor.custom').`

### 3.3 verdict-valid

**ID.** `verdict-valid`

**Severity.** `error`

**Enforces.** STANDARD.md §5 (per-check `verdicts` declaration) and §3.3 (Verdict semantics).

**Trigger.** A check's verdict is either not in the universal verdict set `{pass, warning, fail, not_checked}`, OR is in the universal set but not in the specific check's declared verdict set. For example, `seo.https` declares only `{pass, fail, not_checked}`; a verdict of `warning` for `seo.https` triggers this rule even though `warning` is a valid verdict for other checks.

**Finding message template.** `Verdict '<verdict>' is not valid for check '<check_id>'. Allowed verdicts for this check: <allowed_set>.`

### 3.4 duplicate-check

**ID.** `duplicate-check`

**Severity.** `error`

**Enforces.** STANDARD.md §3.4 (Graceful-unknown handling — duplicate check ID is explicitly listed as a hard error).

**Trigger.** A check ID appears more than once in the `checks` object. In well-formed JSON this condition cannot arise from standard parsing (duplicate keys are rejected or silently deduplicated by most parsers), but the validator MUST detect it when the source JSON uses a parser that preserves duplicates, and MUST emit a finding when it does.

**Finding message template.** `Check ID '<check_id>' appears <n> times. Each check ID MUST appear exactly once.`

### 3.5 evidence-complete

**ID.** `evidence-complete`

**Severity.** `warning`

**Enforces.** STANDARD.md §7.2 (Field requirements by level), specifically the `full`-level requirement that every check include its declared `evidence_required` fields.

**Trigger.** At the `full` conformance level, a check's `evidence` object is missing one or more fields named in that check's `evidence_required` list. At the `minimal` or `standard` levels, this rule does not fire — evidence is optional at those levels.

**Finding message template.** `Check '<check_id>' is missing required evidence field(s): <missing_fields>. Required by the 'full' conformance level.`

**Note.** This rule is `warning`-severity, not `error`-severity, because the conformance level itself is determined by `schema-conformance`. If a full-level audit is missing evidence, `schema-conformance` will already have emitted an `error` — this rule adds a human-readable clarification of which specific fields are missing and on which checks.

### 3.6 scoring-consistent

**ID.** `scoring-consistent`

**Severity.** `warning`

**Enforces.** STANDARD.md §6 (Scoring methodology), specifically the formula `pillar_score = sum(earned) / sum(possible) * 95` and `overall_score = mean(pillar_scores)`.

**Trigger.** A claimed score in the audit report cannot be reproduced from the verdicts using the standard's scoring formulas within ±1 (accounting for rounding per STANDARD.md §6.6). The validator computes the expected score independently from the verdicts and compares against the reported score.

**Finding message template.** `Claimed <score_field> = <claimed>, but verdicts reconcile to <expected>. Delta of <delta> exceeds the ±1 rounding tolerance.`

**Note.** This rule is `warning`-severity rather than `error`-severity to accommodate implementations that apply bespoke rounding or display transformations. The rule exists primarily to catch implementations that apply custom weightings, silently drop `not_checked` verdicts incorrectly, or exceed the pillar cap of 95. A consistently-failing `scoring-consistent` finding is strong evidence of a non-conformant scoring implementation.

### 3.7 level-complete

**ID.** `level-complete`

**Severity.** `info`

**Enforces.** STANDARD.md §2.3 (Conformance levels).

**Trigger.** The audit declares or is validated at the `standard` or `full` level but does not contain all 17 core checks. When this rule fires at the `standard` level or higher, `schema-conformance` will also have fired; this rule provides a human-readable summary.

**Finding message template.** `Audit declares level '<level>' but contains <count> of 17 required core checks. Missing: <comma_separated_list>.`

### 3.8 unknown-check

**ID.** `unknown-check`

**Severity.** `info`

**Enforces.** STANDARD.md §7.3 (Non-standard check extensions) and §3.4 (Graceful-unknown handling).

**Trigger.** The audit contains a check ID outside the three core pillar namespaces (`seo.`, `aeo.`, `geo.`) — that is, a legitimate namespaced extension. The rule emits an `info` finding acknowledging the extension was preserved. This rule does NOT fire for counterfeit core-namespace checks; those trigger `check-id-valid` at `error` severity.

**Finding message template.** `Non-standard check '<check_id>' preserved but excluded from scoring. Extensions are permitted outside the core pillar namespaces (spec §7.3).`

### 3.9 source-attribution

**ID.** `source-attribution`

**Severity.** `warning`

**Enforces.** STANDARD.md §3.2 (Source transparency).

**Trigger.** A check whose `detection` method is `external_lookup` has a verdict of `pass`, `warning`, or `fail` (not `not_checked`) at the `full` level, but its evidence does not include a source name and timestamp for the external lookup. Currently the only `external_lookup` check in v0.1 is `geo.directory_presence`; the rule is written to generalise to any future external-lookup check.

**Finding message template.** `Check '<check_id>' used an external data source but did not declare it in evidence. Required fields: source name(s), lookup timestamp(s).`

### 3.10 fabricated-verdict

**ID.** `fabricated-verdict`

**Severity.** `error`

**Enforces.** STANDARD.md §3.1 (Honest measurement) — the principle that verdicts MUST NOT be inferred from proxy signals.

**Trigger.** A check has measurement_type `field` (as declared in the spec front matter) and has a verdict of `pass`, `warning`, or `fail`, but its evidence does not include a measurement timestamp from the field source the check declares. This rule has no effect in v0.1 because all v0.1 checks are `lab` type; it exists in the v0.1 validator so that v0.2 implementations can be mechanically prevented from fabricating field-measurement results.

**Finding message template.** `Check '<check_id>' is a field-measurement check and reports a non-'not_checked' verdict, but evidence is missing a measurement timestamp from the declared field source. Field verdicts MUST be derived from actual measurement, not inferred from proxy signals (spec §3.1).`

**Note.** This is the single most important rule in the validator. The standard exists in part to prevent vendors from claiming AI-platform citation rates without actually measuring them. Once field checks ship in v0.2, this rule is the mechanism that blocks such claims at the validator layer. A vendor cannot pass `fabricated-verdict` while inferring Perplexity citation from "the site has FAQ schema" — the rule requires an actual Perplexity query timestamp in evidence.

### 3.11 Rule summary table

| Rule ID | Severity | Enforces | Blocks conformance? |
| --- | --- | --- | --- |
| `schema-conformance` | error | §7 + JSON Schema | Yes |
| `check-id-valid` | error | §5, §7.3 | Yes |
| `verdict-valid` | error | §5, §3.3 | Yes |
| `duplicate-check` | error | §3.4 | Yes |
| `evidence-complete` | warning | §7.2 | No (unless `--strict`) |
| `scoring-consistent` | warning | §6 | No (unless `--strict`) |
| `level-complete` | info | §2.3 | No |
| `unknown-check` | info | §7.3 | No |
| `source-attribution` | warning | §3.2 | No (unless `--strict`) |
| `fabricated-verdict` | error | §3.1 | Yes |

---

## 4. Output format

### 4.1 The JSON output shape

When `--format json` (the default), the validator MUST emit a single JSON document to stdout with the following top-level structure:

```json
{
  "validator": "@makeitseo/standard",
  "validator_version": "1.0.0",
  "standard_version": "0.1",
  "audit_file": "my-audit.json",
  "level": "standard",
  "conformant": true,
  "findings": [
    {
      "rule": "unknown-check",
      "severity": "info",
      "path": "checks.ext.vendor.custom_check",
      "message": "Non-standard check 'ext.vendor.custom_check' preserved but excluded from scoring."
    }
  ],
  "summary": {
    "errors": 0,
    "warnings": 0,
    "infos": 1,
    "rules_run": 10,
    "rules_disabled": []
  }
}
```

### 4.2 Finding ordering

Findings within the `findings` array MUST be ordered deterministically, in this order:

1. By `severity`, with `error` first, then `warning`, then `info`.
2. Within the same severity, by `rule` ID in lexicographic order.
3. Within the same rule, by `path` in lexicographic order.

This ordering guarantees byte-identical output across invocations with the same input.

### 4.3 The `conformant` field

The top-level `conformant` field is a boolean. It is `true` if and only if the `summary.errors` count is zero **and** (when `--strict` is set) the `summary.warnings` count is also zero. This field is the authoritative machine-readable conformance verdict; downstream tools that need a single yes/no answer should read this field rather than computing it from `summary`.

### 4.4 The `text` format

When `--format text`, the validator emits human-readable output to stdout. The format is not normatively specified — implementations MAY style output for legibility. However, each finding MUST include, at minimum: the severity, the rule ID, the path (when applicable), and the message. A recommended layout:

```
my-audit.json → standard level

error   schema-conformance  checks.seo.https.verdict    Verdict 'unknown' is not valid for check 'seo.https'.
warning evidence-complete   checks.aeo.faq_schema       Missing required evidence field: question_count.
info    unknown-check       checks.ext.vendor.custom    Non-standard check preserved but excluded from scoring.

Summary: 1 error, 1 warning, 1 info. NOT CONFORMANT.
```

### 4.5 The `junit` format

When `--format junit`, the validator emits JUnit XML suitable for CI-system consumption. Each finding becomes a test case; errors become failures, warnings become failures only when `--strict` is set, infos become skipped tests. This format is provided so that CI pipelines using off-the-shelf JUnit reporters can surface standard-conformance failures alongside unit test failures without custom tooling.

### 4.6 Stream separation

The validator writes its output to stdout. All diagnostic messages from the validator itself — tool errors, unrecognised flags, file-not-found messages — are written to stderr and never to stdout. This separation is load-bearing: it allows `lint` output to be piped into downstream tooling without contamination from tool errors.

---

## 5. Version pinning and compatibility

### 5.1 Declared version support

Every validator implementation MUST declare, via the `version` command, the set of standard versions it supports. A validator supporting only v0.1 returns `standard_version: "0.1"`. A validator supporting multiple versions returns `supported_standard_versions: ["0.1", "0.2"]`.

### 5.2 Version-mismatch protocol

When a validator receives an audit report declaring a `standard_version` that the validator does not support, it MUST:

1. Emit an `error`-severity finding with rule ID `schema-conformance`, message including the supported version(s) and the audit's declared version.
2. Terminate with exit code 1 (non-conformant), not exit code 2 (tool error). A version mismatch is a conformance failure for this validator, not a malformed invocation.

A validator MUST NOT attempt to validate an audit declared at an unsupported version by applying the rules of a different version. Such cross-version validation produces spurious findings and undermines the meaning of conformance.

### 5.3 Forward compatibility

A v0.1 validator encountering a v0.2 audit terminates with a version-mismatch error as specified above. A v0.2 validator encountering a v0.1 audit MAY validate it, provided the validator supports v0.1 in its `supported_standard_versions` list. Dual-version support is the recommended path for validators during a version transition.

### 5.4 Graceful handling of unknown fields within a supported version

Within a supported version, a validator MUST apply the graceful-unknown handling protocol from STANDARD.md §3.4. Specifically:

- Unknown check IDs outside the core pillar namespaces are preserved and reported via `unknown-check` (info).
- Unknown check IDs within core pillar namespaces trigger `check-id-valid` (error).
- Unknown verdict values for known checks trigger `verdict-valid` (error).
- Unknown fields within evidence blocks are preserved without warning — this permits implementations to record supplementary evidence beyond the declared required set.
- Unknown top-level fields in the audit report are preserved without warning.

---

## 6. Exit codes

| Code | Meaning | When returned |
| --- | --- | --- |
| 0 | Conformant | `conformant: true` in the output. Zero errors (and zero warnings if `--strict`). |
| 1 | Non-conformant | `conformant: false`. One or more errors present, or one or more warnings with `--strict`. |
| 2 | Tool error | The validator could not complete its operation. File not found, malformed JSON that prevents parsing at all, unrecognised command-line arguments, internal validator crash. |

### 6.1 The 1 vs 2 distinction

The distinction between exit code 1 and exit code 2 is load-bearing for CI integration. An exit code of 1 means "the validator ran successfully and found that your audit does not conform" — this is the expected exit code when a CI build should fail due to a conformance regression. An exit code of 2 means "the validator could not determine conformance" — this is a tool-level problem that should surface differently to a CI operator, typically as a build infrastructure alert rather than a code-quality alert.

A validator that conflates these two exit codes makes CI pipelines harder to operate. An audit reporter that silently returns 0 on malformed input is actively dangerous. The exit-code protocol exists to prevent both failure modes.

### 6.2 Signal-based termination

If the validator process is terminated by a signal (SIGINT, SIGTERM, etc.), the conventional exit code for that signal (128 + signal number on POSIX systems) MUST be returned. Validators MUST NOT intercept signals to return 0, 1, or 2 — signal-based termination indicates an externally imposed stop, not a conformance determination.

---

## 7. The public HTTP endpoint

### 7.1 Purpose and scope

Cloud WiFi Limited operates a hosted HTTP version of the reference validator at `validate.makeitseo.io`. The endpoint is provided as a public good, funded by Cloud WiFi Limited, and is not required for standard conformance — any organisation may operate its own validator, including its own HTTP endpoint, and produce equally valid conformance determinations.

The public endpoint exists primarily for two purposes: non-developer users who need to validate a single audit without installing a package, and third-party tools that wish to display the conformance badge issued by the endpoint.

### 7.2 API surface

The endpoint exposes two routes:

**`POST /v0.1/lint`** — accepts a JSON audit report as request body, returns the same JSON output as the CLI `lint` command.

**`GET /v0.1/badge/<audit_hash>`** — returns an SVG badge for a previously-validated audit. See §7.5.

### 7.3 Rate limits

The endpoint is free and does not require an account. It is rate-limited per source IP address. In v0.1, the rate limit is **1,000 `lint` requests per IP per 24-hour rolling window**. This threshold is deliberately generous — it accommodates routine CI usage, manual experimentation, and small-scale integrations without requiring signup. A requesting tool that exceeds this threshold receives HTTP 429 with a `Retry-After` header indicating when the window resets.

The rate limit threshold MAY be revised in minor releases of this specification. Any change MUST be announced at least 30 days before it takes effect, published in the change log, and reflected in the endpoint's `GET /v0.1/limits` response (when implemented).

Higher-volume users may operate their own validator using the npm package or any third-party conformant implementation. There is no commercial path to higher rate limits on the public endpoint in v0.1; the endpoint is not a commercial product.

### 7.4 CORS and authentication

The `POST /v0.1/lint` route MUST permit cross-origin requests. The `Access-Control-Allow-Origin` header is set to `*`. This is the correct choice for a standards validator: any origin should be able to validate against the standard, and there is no user data worth protecting in a POST body that contains only an audit report.

Authentication is not used in v0.1. Rate limiting is by IP. A future version MAY introduce optional API keys for attribution purposes (tracking which tools submit how many audits) but MUST NOT require them for access to the rate-limited free tier.

### 7.5 The conformance badge

A conformant audit report submitted to `POST /v0.1/lint` receives, in addition to the standard finding set, a `badge` field in the response:

```json
{
  "conformant": true,
  "level": "full",
  "badge": {
    "url": "https://validate.makeitseo.io/v0.1/badge/7a8b3c...",
    "svg_url": "https://validate.makeitseo.io/v0.1/badge/7a8b3c....svg",
    "expires_at": "2026-05-23T10:30:00Z"
  },
  "findings": [...]
}
```

The badge URL is stable for thirty days from issuance. Fetching the SVG returns an embeddable badge image with text: `"Validated against AI Visibility Audit Standard v0.1 (full)"` or `"Validated against AI Visibility Audit Standard v0.1 (standard)"`.

After the 30-day window, the badge URL returns HTTP 410 Gone. Implementations MUST re-validate their audit output to reissue a badge. This is deliberate: it enforces ongoing conformance rather than one-time claims. A tool that was conformant on 1 March and has since diverged should not continue to display the badge.

Non-conformant audits receive no badge. The `badge` field is absent from the response. There is no "partial" or "warning" badge variant in v0.1 — the badge communicates binary conformance at the declared level.

### 7.6 Error responses

Error responses from the public endpoint follow RFC 9457 (Problem Details for HTTP APIs):

```json
{
  "type": "https://validate.makeitseo.io/problems/rate-limited",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "This IP has exceeded 1000 lint requests in the preceding 24 hours.",
  "retry_after": "2026-04-24T10:30:00Z"
}
```

Problem types used by v0.1:

| Type | HTTP status | Cause |
| --- | --- | --- |
| `rate-limited` | 429 | IP-level rate limit exceeded. |
| `malformed-request` | 400 | Request body is not valid JSON, or missing. |
| `unsupported-version` | 400 | Audit declares a standard version this endpoint does not support. |
| `payload-too-large` | 413 | Request body exceeds 5 MB. |
| `internal-error` | 500 | Unexpected validator failure. |

### 7.7 Deprecation and stability

The URL `validate.makeitseo.io/v0.1/*` is stable for the lifetime of v0.1 of the standard. When v0.2 ships, a parallel path at `validate.makeitseo.io/v0.2/*` will be added; the v0.1 path remains operational for at least one year after v0.2 release to give implementers time to migrate.

---

## 8. Conformance for validators

### 8.1 What makes a validator conformant

A validator implementation is conformant with this specification if and only if:

1. It implements all four commands (`lint`, `diff`, `export`, `version`) with the semantics specified in §2.
2. It implements all ten lint rules with the triggers, severities, and finding shapes specified in §3.
3. Its JSON output matches the shape specified in §4.
4. Its exit codes follow the protocol specified in §6.
5. Its version-pinning behaviour follows §5.
6. Given the reference audit test suite (§8.3), it produces the reference finding set byte-for-byte.

### 8.2 Multiple conformant implementations are permitted

The standard permits and encourages multiple conformant validator implementations. The reference implementation published by Cloud WiFi Limited at `@makeitseo/standard` is the canonical reference; third-party implementations (in other languages, with other distribution mechanisms, integrated into other tools) are welcome provided they pass the reference audit test suite.

### 8.3 The reference audit test suite

A companion test suite will be published at `github.com/cloud-wifi/makeitseo-standard/tree/main/validator-tests`. The suite contains audit report fixtures paired with expected validator output. Any validator implementation claiming conformance with this specification MUST produce the expected output for every fixture in the suite.

The test suite is versioned alongside the standard. A validator claiming conformance with v0.1 passes the v0.1 fixture set; a validator claiming conformance with v0.2 passes the v0.2 fixture set (which includes v0.1's fixtures, plus new ones for v0.2 additions).

### 8.4 Declaring conformance

A validator implementation claiming conformance with this specification MUST:

1. Pass every fixture in the reference audit test suite for the version claimed.
2. Expose its validator version and supported standard version(s) via the `version` command.
3. State the claimed conformance in any public representation of the validator.
4. Re-verify conformance against the current fixture set within 30 days of any patch release of this specification.

---

## Appendix A — Rule ID stability policy

Rule IDs are the stable public identifiers for lint rules. Once shipped in a public release, a rule ID MUST NOT:

- Be renamed.
- Be reassigned to a different rule.
- Change its trigger condition in a way that a previously-passing audit would newly fail, without a major version bump of the standard.

A rule MAY be deprecated. A deprecated rule continues to run and report findings, but the findings are downgraded to `info` severity and the finding message is prefixed with `[deprecated]`. Deprecated rules are removed in the next major version after the deprecation announcement.

This policy exists because downstream tooling — CI pipelines, badge infrastructure, third-party reporters — pins to rule IDs. Renaming `fabricated-verdict` to `field-verdict-missing-timestamp` would silently disable every CI check that watches for `fabricated-verdict` findings. The cost of rule-ID instability is paid by every downstream consumer, not by the validator publisher.

---

## Appendix B — Relationship to design.md's `hatch lint`

The Platform Spec that governs this project cites Google's design.md as the architectural precedent. design.md's validator, `hatch lint`, is a closer precedent than ESLint or JSON Schema validators alone, because `hatch lint` validates AI-generated UIs against a standard and produces the same public-pressure dynamic described in STANDARD.md §8.1.

Specific parallels:

- **Rule IDs as stable identifiers.** `hatch lint` treats rule IDs as part of the public API. This specification follows the same discipline in §3 and Appendix A.
- **Severity as machine-readable policy.** `hatch lint` uses severity to distinguish blocking failures from advisory concerns. This specification uses the same model, with `--strict` as the escalation knob.
- **Public validator endpoint as market mechanism.** `hatch lint` is most effective when run in CI or as a public service, not just locally. The public endpoint at `validate.makeitseo.io` (§7) implements the same pattern.

These parallels are not citations in the RFC-2119 sense — design.md is a convention, not a normative reference — but they inform the design choices in this specification and are recorded here for transparency.

---

## Appendix C — Change log

### v0.1 — 2026-04-23

Initial release of the Validator Specification.

**Added.** Full CLI specification for `lint`, `diff`, `export`, `version` commands. Ten lint rules (`schema-conformance`, `check-id-valid`, `verdict-valid`, `duplicate-check`, `evidence-complete`, `scoring-consistent`, `level-complete`, `unknown-check`, `source-attribution`, `fabricated-verdict`). JSON, text, and JUnit output formats. Three-state exit code protocol. Version-pinning protocol. Public HTTP endpoint specification including rate limits (1,000/IP/24hr), CORS, error responses, badge issuance with 30-day TTL. Rule ID stability policy.

**Breaking changes.** Not applicable to initial release.

**Migration guide.** Not applicable to initial release.

---

*— End of document —*

*AI Visibility Audit Standard — Validator Specification v0.1 · Cloud WiFi Limited · CC-BY 4.0 · Published 2026-04-23*
