# Changelog — MakeitSEO Standards Programme

All notable changes to this standards programme are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).  
Specifications use a `v{major}.{minor}` version scheme (see GOVERNANCE.md §3).

---

## [v0.1] — 2026-05-12

### Initial publication of the MakeitSEO Standards Programme

This release publishes the first set of normative specifications for measuring website visibility across traditional search, answer engines, and AI-generated responses.

#### Specifications published

| Specification | Path | Summary |
|---------------|------|---------|
| MakeitSEO Standard | `STANDARD.md` | Three-pillar framework (SEO / AEO / GEO) with overall score = arithmetic mean |
| SEO Scoring | `seo-scoring/v0.1.md` | 6 sub-scores: content quality (30%), technical health (25%), authority signals (22%), content freshness (10%), runtime compatibility (8%), brand mentions (3%) |
| AEO Scoring | `aeo-scoring/v0.1.md` | 5 sub-scores: AIO presence (40%), featured snippet (25%), knowledge panel (15%), PAA (10%), runtime compatibility (10%) |
| GEO Scoring | `geo-scoring/v0.1.md` | 8 sub-scores: citation rate (20%), brand mentions (15%), mention share (10%), content freshness (10%), platform affinity (10%), structured content (10%), AI crawler (10%), runtime compatibility (15%) |
| Methodology ADR | `methodology-adr/v0.1.md` | 15 Architectural Decision Records covering pillar design, scoring formulae, and measurement protocols |
| Methodology Overview | `methodology-overview/v0.1.md` | Readable guide to all three pillars + Retrievability derived view |
| Agent Runtime Compatibility | `agent-runtime-compatibility/v0.1.md` | ARC protocol — machine-readable runtime capability declarations |
| AI Crawler Accessibility | `ai-crawler-accessibility/v0.1.md` | robots.txt, sitemap, structured-data crawlability signals |
| Brand Web Mentions | `brand-web-mentions/v0.1.md` | Off-domain brand mention measurement (weighted mention score) |
| Cascade Monitoring | `cascade-monitoring/v0.1.md` | Event-based threshold anomaly detection |
| Content Freshness | `content-freshness/v0.1.md` | Per-page freshness multiplier (0.4–1.0) derivation |
| Local SEO Signals | `local-seo-signals/v0.1.md` | GBP/NAP completeness (v0.2 active measurement milestone) |
| Per-Platform Source Affinity | `per-platform-source-affinity/v0.1.md` | Platform-level citation affinity score |
| Structured Content Density | Not yet published | Schema type coverage × field completeness × multi-schema diversity |

#### Structural artefacts published

- `audit-report.schema.json` — JSON Schema for conformant audit output
- `STANDARD.md` — human-readable overview of the MakeitSEO Standard
- `VALIDATOR.md` — documentation for the `@makeitseo/standard` CLI validator
- `README.md` — programme introduction and quick-start
- `CONTRIBUTING.md` — contribution guide (editor-led model at v0.1)
- `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1
- `GOVERNANCE.md` — governance model, versioning policy, Stage 2 transition path
- `CHANGELOG.md` — this file

#### Key architectural decisions (from methodology-adr/v0.1)

| Decision | ADR | Summary |
|----------|-----|---------|
| Three outcome pillars only (no composite pillar) | #1 | SEO / AEO / GEO; no "AI visibility" meta-pillar |
| Overall = arithmetic mean | #6 | (SEO + AEO + GEO) / 3; no pillar weighting |
| FAQ/HowTo schema removed from AEO | #2 | Schema annotation ≠ answer-engine surface; moved to SEO content proxy |
| ARC findings route to pillars | #3 | Per `relevant_outcome_pillar` with even distribution for multi-pillar runtimes |
| Retrievability = derived view | #15 | (agent_runtime_readiness + geo_ai_crawler) / 2; NOT a fourth pillar |
| Freshness multiplier approach | #9 | Multiplier-as-modifier (0.4–1.0) over freshness as an additive signal |

#### Reference implementation

The MakeitSEO audit engine at [makeitseo.com](https://makeitseo.com) is the designated reference implementation of this standard as of v0.1.

---

## Notes on pre-v1.0 versioning

- Versions `v0.x` are pre-stable. Normative text may change between minor versions.
- Implementations conformant with `v0.1` should be re-validated when `v0.2` is published.
- `v1.0` marks the first stable release; breaking changes from that point require TAB approval and 90 days notice.
