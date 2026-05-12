---
version: "0.1"
name: AI Visibility Audit Standard
description: >
  Open specification for producing conformant audits of AI search
  visibility across traditional search engines and generative AI platforms.
license: CC-BY-4.0
published: 2026-04-23
editor: Cloud WiFi Limited
repository: https://github.com/cloud-wifi/makeitseo-standard
canonical_url: https://standard.makeitseo.io

pillars:
  seo:
    name: Search Engine Optimisation
    description: Technical discoverability by traditional search engine crawlers.
  aeo:
    name: Answer Engine Optimisation
    description: Content structure for direct-answer retrieval and featured-snippet eligibility.
  geo:
    name: Generative Engine Optimisation
    description: Citation and reference by large-language-model-based search platforms.

scoring:
  impact_bands:
    high: 20
    medium: 10
    low: 5
  verdict_points:
    pass: 1.0
    warning: 0.5
    fail: 0.0
    not_checked: excluded
  pillar_formula: "sum(earned) / sum(possible) * 95"
  overall_formula: "mean(pillar_scores)"
  pillar_cap: 95
  rounding: "round-half-up to nearest integer"

checks:

  seo.https:
    pillar: seo
    measurement_type: lab
    impact: high
    detection: http_probe
    verdicts: [pass, fail, not_checked]
    evidence_required: [final_url, final_protocol]
    description: >
      The audited URL, after following redirects, MUST be served over HTTPS.

  seo.mobile_viewport:
    pillar: seo
    measurement_type: lab
    impact: medium
    detection: html_meta_tag
    verdicts: [pass, fail, not_checked]
    evidence_required: [viewport_value]
    description: >
      A <meta name="viewport"> element MUST be present in the document head
      with a content value that includes "width=device-width".

  seo.title_tag:
    pillar: seo
    measurement_type: lab
    impact: high
    detection: html_element
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [title_text, title_length]
    description: >
      A non-empty <title> element MUST be present. Length SHOULD be between
      10 and 70 characters inclusive.

  seo.meta_description:
    pillar: seo
    measurement_type: lab
    impact: medium
    detection: html_meta_tag
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [description_text, description_length]
    description: >
      A <meta name="description"> element SHOULD be present. Length SHOULD
      be between 50 and 160 characters inclusive.

  seo.canonical_url:
    pillar: seo
    measurement_type: lab
    impact: medium
    detection: html_link_tag
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [canonical_href, resolves_to_self]
    description: >
      A <link rel="canonical"> element SHOULD be present. Its href SHOULD
      resolve to the audited URL after normalisation.

  seo.robots_indexability:
    pillar: seo
    measurement_type: lab
    impact: high
    detection: composite
    verdicts: [pass, fail, not_checked]
    evidence_required: [robots_txt_disallows, meta_robots_directives, x_robots_tag]
    description: >
      The audited URL MUST NOT be blocked from indexing by any of the three
      robots signals: robots.txt Disallow, <meta name="robots"> noindex,
      or X-Robots-Tag header noindex.

  seo.sitemap_present:
    pillar: seo
    measurement_type: lab
    impact: low
    detection: http_probe
    verdicts: [pass, fail, not_checked]
    evidence_required: [sitemap_url, sitemap_reachable, sitemap_valid_xml]
    description: >
      An XML sitemap SHOULD be reachable at /sitemap.xml or declared in
      robots.txt via a "Sitemap:" directive.

  aeo.faq_schema:
    pillar: aeo
    measurement_type: lab
    impact: high
    detection: jsonld_parse
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [schema_found, question_count]
    description: >
      FAQPage schema (schema.org) SHOULD be present on pages whose content
      is structured as question-answer pairs. Warning is emitted when FAQ
      content is detected heuristically but no schema is attached.

  aeo.heading_hierarchy:
    pillar: aeo
    measurement_type: lab
    impact: medium
    detection: dom_structure
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [h1_count, skipped_levels, heading_outline]
    description: >
      The document SHOULD contain exactly one <h1>. Heading levels SHOULD
      NOT skip (e.g., <h2> directly followed by <h4>). Warning is emitted
      for skipped levels; fail is emitted for zero or multiple <h1>.

  aeo.direct_answer_opening:
    pillar: aeo
    measurement_type: lab
    impact: high
    detection: content_analysis
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [first_paragraph_text, word_count, contains_definition]
    description: >
      The first paragraph of primary content SHOULD directly answer the
      page's implicit question within 40 to 60 words and SHOULD contain
      at least one definitional statement.

  aeo.article_schema:
    pillar: aeo
    measurement_type: lab
    impact: medium
    detection: jsonld_parse
    verdicts: [pass, fail, not_checked]
    evidence_required: [schema_found, required_properties_present]
    description: >
      Pages whose primary content type is editorial (article, blog post,
      news item) SHOULD declare Article, NewsArticle, or BlogPosting
      schema with at least headline, author, and datePublished.

  aeo.organization_schema:
    pillar: aeo
    measurement_type: lab
    impact: low
    detection: jsonld_parse
    verdicts: [pass, fail, not_checked]
    evidence_required: [schema_found, has_name, has_url]
    description: >
      Organization or LocalBusiness schema SHOULD be present somewhere
      on the site (typically the homepage) with at least name and url.

  geo.llms_txt_present:
    pillar: geo
    measurement_type: lab
    impact: medium
    detection: http_probe
    verdicts: [pass, fail, not_checked]
    evidence_required: [llms_txt_reachable, llms_txt_valid]
    description: >
      An llms.txt file MAY be reachable at the site root. Presence is
      rewarded; absence is not penalised as fail, but reported as the
      relevant not_checked distinction requires deliberate author action.

  geo.sameas_authority:
    pillar: geo
    measurement_type: lab
    impact: high
    detection: jsonld_parse
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [sameas_count, authoritative_domains]
    description: >
      Organization or Person schema SHOULD include a sameAs array
      referencing at least two authoritative external domains from the
      informative reference list (Wikidata, Wikipedia, Crunchbase, LinkedIn,
      Companies House, verified social profiles).

  geo.directory_presence:
    pillar: geo
    measurement_type: lab
    impact: medium
    detection: external_lookup
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [directory_sources_checked, listings_found, sources_timestamp]
    description: >
      The audited entity SHOULD be findable in at least one authoritative
      structured directory (Wikidata, Crunchbase, OpenCorporates, or
      equivalent jurisdictional registry). Each directory source MUST
      declare the lookup timestamp.

  geo.about_page_depth:
    pillar: geo
    measurement_type: lab
    impact: low
    detection: content_analysis
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [about_page_url, word_count, entity_markers]
    description: >
      An identifiable About page SHOULD exist and SHOULD contain at least
      300 words of substantive entity-describing content (who, what, where,
      when, founding, purpose).

  geo.entity_consistency:
    pillar: geo
    measurement_type: lab
    impact: medium
    detection: cross_page
    verdicts: [pass, warning, fail, not_checked]
    evidence_required: [canonical_entity_name, name_variants, address_variants]
    description: >
      The primary entity name and primary address SHOULD be consistent
      across schema markup, visible copy, and any declared directory
      listings. Warning is emitted for minor variants (punctuation,
      abbreviation); fail is emitted for material divergence.

conformance_levels:
  minimal:
    description: One check, one valid verdict.
    required:
      - standard_version
      - audited_url
      - timestamp
      - checks
  standard:
    description: All 17 launch checks present with valid verdicts.
    required:
      - standard_version
      - audited_url
      - timestamp
      - checks.seo.https
      - checks.seo.mobile_viewport
      - checks.seo.title_tag
      - checks.seo.meta_description
      - checks.seo.canonical_url
      - checks.seo.robots_indexability
      - checks.seo.sitemap_present
      - checks.aeo.faq_schema
      - checks.aeo.heading_hierarchy
      - checks.aeo.direct_answer_opening
      - checks.aeo.article_schema
      - checks.aeo.organization_schema
      - checks.geo.llms_txt_present
      - checks.geo.sameas_authority
      - checks.geo.directory_presence
      - checks.geo.about_page_depth
      - checks.geo.entity_consistency
  full:
    description: Standard plus complete evidence, scoring, methodology metadata, and source attribution.
    required:
      - standard_version
      - audited_url
      - timestamp
      - checks.*
      - checks.*.evidence
      - scoring.pillar_scores
      - scoring.overall_score
      - scoring.overall_score_semantics
      - methodology.engine_version
      - methodology.data_sources
---

# AI Visibility Audit Standard v0.1

**An Open Specification for Measuring Visibility Across Search Engines and Generative AI Platforms**

Cloud WiFi Limited · Published 23 April 2026 · Licensed under CC-BY 4.0

---

## 1. Introduction

### 1.1 Purpose

This document specifies an open, implementable standard for measuring the visibility of a web property across three retrieval surfaces: traditional search engines, answer-engine features (featured snippets, direct answers, People-Also-Ask), and generative AI platforms. It defines a fixed set of conformance checks, a scoring methodology, and a report format that any tool may implement to produce comparable, reproducible audits.

The standard exists because the current state of AI visibility measurement is marketing. Commercial tools publish scores without disclosing what is measured, how it is measured, or whether the results are reproducible. The AI Visibility Audit Standard is an attempt to replace claims with conformance.

### 1.2 Scope

This standard covers:

- The machine-readable structure of a conformant audit report.
- Seventeen named checks grouped into three pillars — SEO, AEO, and GEO.
- The detection methods, verdict rules, and evidence requirements for each check.
- A scoring methodology that converts verdicts into per-pillar and overall scores.
- Three conformance levels: minimal, standard, and full.
- Versioning, deprecation, and change-control policy.

### 1.3 Non-goals

This standard does not:

- Prescribe the content strategy, editorial approach, or commercial positioning of audited sites.
- Rank the relative importance of the three pillars beyond the impact bands on individual checks.
- Define a methodology for directly querying generative AI platforms to measure citation rates. That measurement is valuable but depends on unstable third-party APIs and is deferred to a future version.
- Supersede existing web standards. It references W3C, WHATWG, IETF, and schema.org specifications; it does not replace them.

### 1.4 Relationship to other standards

This standard builds on and references, without modifying, the following:

- RFC 2119 and RFC 8174 for normative terminology.
- IETF RFC 9309 for robots.txt semantics.
- WHATWG HTML for document structure.
- schema.org for structured-data vocabularies.
- Google Search Central documentation for indexability signals.

Where the prose of this standard and any of the above diverge, the external standard governs for its own domain, and a clarifying note is added to this standard's change log.

---

## 2. Definitions and conformance

### 2.1 Normative terminology

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

### 2.2 Glossary

**Audit report.** A structured document, conformant to this standard, describing the outcome of running the defined checks against a single URL at a single point in time.

**Check.** A named, versioned unit of measurement defined in the front matter of this standard under the `checks` key. Each check produces a single verdict for a single URL.

**Conformance level.** One of three tiers — minimal, standard, full — that an audit report may claim. Each level defines a set of required fields.

**Detection method.** The category of technical operation used to evaluate a check. Enumerated values: `http_probe`, `html_meta_tag`, `html_link_tag`, `html_element`, `dom_structure`, `jsonld_parse`, `content_analysis`, `composite`, `cross_page`, `external_lookup`.

**Evidence.** The raw observations recorded by the implementation that support a verdict. Each check declares the evidence fields required at the `full` conformance level.

**Impact band.** The weight applied to a check when computing scores. One of `high` (20 points), `medium` (10 points), or `low` (5 points).

**Measurement type.** The category of observation a check produces. One of `lab` (synthetic, reproducible, derived from a single crawl or a single API call to a declared source) or `field` (aggregated from real-world signals over a declared time window). All checks in v0.1 are `lab`. This field exists to accommodate `field`-type checks — for example, citation-rate measurement across generative AI platforms — in future versions without restructuring the spec. A conformant implementation treats an unknown measurement_type value as `lab` for scoring purposes and emits a warning.

**Implementation.** A software tool that produces audit reports conformant to this standard.

**Pillar.** One of three fixed groupings — SEO, AEO, GEO — to which every check belongs. Pillars are enumerated in the front matter and are fixed within a version.

**Reference implementation.** The singular implementation designated as canonical by this standard. The reference implementation's behaviour is authoritative where the prose of this standard is ambiguous.

**Verdict.** The outcome of a single check for a single URL. One of `pass`, `warning`, `fail`, `not_checked`. The verdict set per check is declared in the front matter.

### 2.3 Conformance levels

An audit report that claims conformance MUST declare its level. The three levels are:

**Minimal.** The audit report parses against the JSON Schema, contains `standard_version`, `audited_url`, `timestamp`, and at least one valid check entry with a valid verdict.

**Standard.** All seventeen launch checks are present. Each check contains a valid verdict from its declared verdict set. The four `minimal`-level fields are present.

**Full.** The `standard` level, plus: every check contains the evidence fields declared as `evidence_required`; scoring is present and reproducible from the verdicts using the formulas defined in this document; methodology metadata (engine version, data sources, timestamps per external lookup) is present and complete.

An implementation MAY submit audits at any level. An implementation claiming `full` conformance MUST produce audits that reconcile against the validator with zero errors at the `full` level.

---

## 3. Measurement principles

### 3.1 Honest measurement

Every check in this standard is directly observable. A verdict MUST be derived from an actual observation of the audited URL (or, for `external_lookup` checks, the declared external source). Inferring a verdict from a proxy signal — for example, asserting that a page is cited by ChatGPT because the page contains FAQ schema — is prohibited. Proxy inference is the single most common failure mode of commercial AI-visibility tools, and this standard exists in part to make it mechanically refutable.

### 3.2 Source transparency

Every check whose verdict depends on an external data source MUST declare the source in its evidence block. For `external_lookup` checks, the source name, the lookup timestamp, and the matched identifier (if any) are required at the `full` conformance level.

### 3.3 Verdict semantics

Verdicts are defined as follows, and implementations MUST apply these definitions consistently:

- `pass` — the observation meets the check's criteria as defined in its `description`.
- `warning` — the observation meets the check's criteria in part, or meets them with a qualification that is material enough to report but not severe enough to fail.
- `fail` — the observation does not meet the check's criteria.
- `not_checked` — the implementation did not evaluate the check. The verdict MUST NOT be `not_checked` when the check was evaluated and returned no result; in that case, the verdict is `fail`.

The distinction between `fail` and `not_checked` is load-bearing. A check that was evaluated and produced no qualifying observation is `fail`. A check that was not evaluated — because the implementation does not support it, because the data source was unreachable, because the audited URL returned a non-200 response — is `not_checked`. Mixing these two states breaks score comparability across implementations.

### 3.4 Graceful-unknown handling

An implementation that encounters a check it does not recognise MUST preserve the check in the output and exclude it from scoring. An implementation that encounters an unknown verdict value for a known check MUST treat the verdict as `not_checked` and emit a warning. An implementation that encounters an unknown pillar MUST reject the audit report as malformed.

These rules are defined more fully in §8 and are cross-referenced from the JSON Schema exported alongside this document.

---

## 4. The three pillars

### 4.1 SEO — Search Engine Optimisation

The SEO pillar measures technical discoverability by traditional search-engine crawlers. It is the oldest and most settled of the three pillars, and its checks reflect stable, documented behaviours of major search engines. The SEO pillar is not sufficient for AI visibility on its own, but failure at the SEO pillar generally implies failure at the other two, because AI platforms typically ingest web content via crawling pipelines that share characteristics with search-engine crawlers.

### 4.2 AEO — Answer Engine Optimisation

The AEO pillar measures content structure for direct-answer retrieval. It covers the features that determine whether a page is eligible to appear as a featured snippet, a People-Also-Ask expansion, or an AI Overview extract. The AEO pillar is the bridge between SEO and GEO: the same structural signals that help a page win a featured snippet also help it be cited by a generative AI platform. Most AEO checks are content-structure checks (headings, direct-answer openings, question-answer schema) rather than technical-discoverability checks.

### 4.3 GEO — Generative Engine Optimisation

The GEO pillar measures citation-friendliness for generative AI platforms. Its checks reflect the features that correlate with being referenced or cited by ChatGPT, Perplexity, Claude, and other LLM-based search surfaces. The GEO pillar is the newest and least settled. This version of the standard deliberately limits GEO checks to verifiable, entity-authority signals (directory presence, sameAs authority, About-page depth, entity consistency) and excludes direct citation-rate measurement, because the latter depends on platform APIs that are unstable and not universally available.

### 4.4 How the pillars relate

A site that passes every SEO check but fails every AEO and GEO check is technically findable but structurally invisible to AI platforms. A site that passes every AEO and GEO check but fails SEO is unreachable. The three pillars are interdependent, and a well-optimised site scores comparably across all three.

The standard does not apply a weighting between pillars when computing the overall score. Each pillar score is computed independently and the overall score is the mean. This is deliberate: the relative importance of the three pillars will change over time as AI platforms evolve, and encoding a static weighting would embed a time-limited opinion into the standard.

---

## 5. Check specifications

This section is normative. Each check defines a detection method, a verdict rule, an evidence requirement, an impact band, and at least one informative reference.

### 5.1 SEO checks

#### 5.1.1 seo.https

**Detection.** HTTP probe. The implementation issues a GET request to the audited URL, follows redirects up to a reasonable limit (RECOMMENDED: 10), and observes the final URL.

**Verdict rules.**
- `pass` — the final URL scheme is `https:`.
- `fail` — the final URL scheme is `http:`, or the request failed with a scheme-related error (e.g., mixed-content blocking).
- `not_checked` — the implementation was unable to issue the request for non-scheme reasons (DNS failure, timeout).

**Evidence required at full level.**
- `final_url` — the URL after redirect resolution.
- `final_protocol` — `http` or `https`.

**Impact.** High.

**Informative references.** RFC 9110 §4.2.2; MDN Web Docs, "HTTPS"; Google Search Central, "Secure your site with HTTPS".

---

#### 5.1.2 seo.mobile_viewport

**Detection.** HTML meta tag. The implementation parses the audited document and inspects `<meta name="viewport">` in the `<head>`.

**Verdict rules.**
- `pass` — a viewport meta tag is present and its `content` attribute contains `width=device-width` (case-insensitive).
- `fail` — no viewport meta tag present, or present but missing `width=device-width`.
- `not_checked` — the document could not be parsed as HTML.

**Evidence required at full level.**
- `viewport_value` — the full content attribute of the viewport tag, or `null` if absent.

**Impact.** Medium.

**Informative references.** W3C, "CSS Device Adaptation"; Google Search Central, "Mobile-friendly test".

---

#### 5.1.3 seo.title_tag

**Detection.** HTML element. The implementation parses the audited document and inspects the `<title>` element in the `<head>`.

**Verdict rules.**
- `pass` — a single non-empty `<title>` is present whose text length is between 10 and 70 characters inclusive, after whitespace normalisation.
- `warning` — a non-empty `<title>` is present but its length is outside the 10–70 character band.
- `fail` — no `<title>` present, or `<title>` is empty after whitespace normalisation, or multiple `<title>` elements are present.
- `not_checked` — the document could not be parsed as HTML.

**Evidence required at full level.**
- `title_text` — the normalised title text.
- `title_length` — integer character count after normalisation.

**Impact.** High.

**Informative references.** WHATWG HTML §4.2.2; Google Search Central, "Influencing your title links in search".

---

#### 5.1.4 seo.meta_description

**Detection.** HTML meta tag.

**Verdict rules.**
- `pass` — a `<meta name="description">` is present whose `content` length is between 50 and 160 characters inclusive.
- `warning` — meta description is present but outside the 50–160 character band.
- `fail` — no meta description present.
- `not_checked` — the document could not be parsed as HTML.

**Evidence required at full level.**
- `description_text` — the description content.
- `description_length` — integer character count.

**Impact.** Medium.

**Informative references.** Google Search Central, "Meta descriptions".

---

#### 5.1.5 seo.canonical_url

**Detection.** HTML link tag.

**Verdict rules.**
- `pass` — a `<link rel="canonical">` is present and its `href`, after URL normalisation, equals the audited URL.
- `warning` — a canonical link is present but resolves to a different URL than the audited one. This is a legitimate configuration (e.g., deliberate self-canonical to a cleaned variant) but warrants review.
- `fail` — no canonical link present.
- `not_checked` — the document could not be parsed as HTML.

**Evidence required at full level.**
- `canonical_href` — the raw href attribute value.
- `resolves_to_self` — boolean.

**Impact.** Medium.

**Informative references.** Google Search Central, "Consolidate duplicate URLs"; RFC 6596.

---

#### 5.1.6 seo.robots_indexability

**Detection.** Composite. The implementation inspects three signals in order: robots.txt at the site root, `<meta name="robots">` in the audited document, and the `X-Robots-Tag` response header.

**Verdict rules.**
- `pass` — none of the three signals disallow indexing for the audited URL.
- `fail` — any of the three signals disallows indexing.
- `not_checked` — one or more signals could not be retrieved (network error, non-parseable robots.txt).

**Evidence required at full level.**
- `robots_txt_disallows` — boolean, with matched rule text if true.
- `meta_robots_directives` — array of directive strings from the meta tag.
- `x_robots_tag` — the raw header value, or `null`.

**Impact.** High.

**Informative references.** RFC 9309; Google Search Central, "Robots meta tag, data-nosnippet, and X-Robots-Tag specifications".

---

#### 5.1.7 seo.sitemap_present

**Detection.** HTTP probe. The implementation checks `/sitemap.xml` at the site root, and parses robots.txt for `Sitemap:` directives.

**Verdict rules.**
- `pass` — at least one reachable sitemap URL is found that returns HTTP 200 with valid sitemap XML.
- `fail` — no sitemap found via either discovery method.
- `not_checked` — robots.txt could not be retrieved AND the default sitemap URL returned a network error.

**Evidence required at full level.**
- `sitemap_url` — the discovered sitemap URL, or `null`.
- `sitemap_reachable` — boolean.
- `sitemap_valid_xml` — boolean.

**Impact.** Low.

**Informative references.** sitemaps.org protocol 0.9; RFC 9309.

---

### 5.2 AEO checks

#### 5.2.1 aeo.faq_schema

**Detection.** JSON-LD parse. The implementation extracts all `application/ld+json` blocks from the document and searches for objects whose `@type` is `FAQPage`.

**Verdict rules.**
- `pass` — at least one `FAQPage` object is present with two or more `mainEntity` questions, each with a non-empty `acceptedAnswer`.
- `warning` — FAQ-structured content is detected heuristically in the visible HTML (question-answer pairs, `<dt>/<dd>` or `<details>/<summary>` patterns) but no `FAQPage` schema is attached.
- `fail` — neither schema nor structured FAQ content is detected on a page whose heuristic classification suggests FAQ intent (URL contains "faq" or similar).
- `not_checked` — the page is not FAQ-oriented and therefore the check does not apply. This verdict is valid here; `not_checked` is not exclusively for implementation errors.

**Evidence required at full level.**
- `schema_found` — boolean.
- `question_count` — integer; count of mainEntity questions in schema if present, else count of detected heuristic questions.

**Impact.** High.

**Informative references.** schema.org FAQPage; Google Search Central, "FAQ structured data".

---

#### 5.2.2 aeo.heading_hierarchy

**Detection.** DOM structure.

**Verdict rules.**
- `pass` — exactly one `<h1>` is present, and no heading level is skipped when traversing the document in source order.
- `warning` — exactly one `<h1>` is present, but one or more heading levels are skipped.
- `fail` — zero `<h1>` or more than one `<h1>`.
- `not_checked` — the document could not be parsed as HTML.

**Evidence required at full level.**
- `h1_count` — integer.
- `skipped_levels` — array of parent-child pairs where a level was skipped, e.g., `[["h2", "h4"]]`.
- `heading_outline` — ordered array of heading levels in source order.

**Impact.** Medium.

**Informative references.** WHATWG HTML §4.3.6; WCAG 2.2 SC 1.3.1 and 2.4.6.

---

#### 5.2.3 aeo.direct_answer_opening

**Detection.** Content analysis. The implementation extracts the first paragraph of primary content (after heuristic removal of navigation, advertising, and boilerplate) and evaluates it against three criteria.

**Verdict rules.**
- `pass` — the first paragraph is 40–60 words inclusive AND contains at least one definitional statement (identified by presence of a form-of-be verb linking the page's apparent subject to a predicate, e.g., "X is a Y that…").
- `warning` — the first paragraph is present but either outside the word band OR lacking a definitional statement.
- `fail` — no identifiable first paragraph (body content is a list, a form, or purely navigational).
- `not_checked` — primary content could not be identified.

**Evidence required at full level.**
- `first_paragraph_text` — the extracted paragraph text.
- `word_count` — integer.
- `contains_definition` — boolean.

**Impact.** High.

**Informative references.** Liu et al. (2023), "GEO: Generative Engine Optimization", arXiv:2311.09735; BrightEdge, "Featured Snippet Research Report" (2022).

---

#### 5.2.4 aeo.article_schema

**Detection.** JSON-LD parse.

**Verdict rules.**
- `pass` — the document declares `Article`, `NewsArticle`, or `BlogPosting` schema containing at minimum `headline`, `author`, and `datePublished`.
- `fail` — the document's primary content is editorial (identified heuristically by presence of a single long-form body and byline-like structure) but no Article-family schema is declared.
- `not_checked` — the document's primary content is not editorial in nature.

**Evidence required at full level.**
- `schema_found` — boolean.
- `required_properties_present` — array of present properties from the required set.

**Impact.** Medium.

**Informative references.** schema.org Article; Google Search Central, "Article structured data".

---

#### 5.2.5 aeo.organization_schema

**Detection.** JSON-LD parse. The check applies site-wide; the implementation MAY satisfy this check by retrieving the site's homepage in addition to the audited URL.

**Verdict rules.**
- `pass` — `Organization` or `LocalBusiness` schema is declared on either the audited URL or the site homepage, containing at minimum `name` and `url`.
- `fail` — no Organization-family schema detected on either page.
- `not_checked` — the homepage could not be retrieved.

**Evidence required at full level.**
- `schema_found` — boolean.
- `has_name` — boolean.
- `has_url` — boolean.

**Impact.** Low.

**Informative references.** schema.org Organization; schema.org LocalBusiness.

---

### 5.3 GEO checks

#### 5.3.1 geo.llms_txt_present

**Detection.** HTTP probe against `/llms.txt` at the site root.

**Verdict rules.**
- `pass` — the URL returns HTTP 200 with a valid `text/markdown` or `text/plain` body whose structure matches the llms.txt convention (H1 site title, H2 section headers, markdown link lists).
- `fail` — the URL returns a non-200 response, or returns 200 with a body that does not match the convention.
- `not_checked` — the URL could not be reached due to network error.

**Evidence required at full level.**
- `llms_txt_reachable` — boolean.
- `llms_txt_valid` — boolean (structural validity).

**Impact.** Medium.

**Informative references.** Answer.AI, "The /llms.txt file" (2024).

**Note.** llms.txt is a proposed convention, not a ratified standard. Its inclusion here reflects observed adoption by AI platforms as of publication date. The check may be deprecated in a future version if the convention is superseded.

---

#### 5.3.2 geo.sameas_authority

**Detection.** JSON-LD parse. The implementation extracts `Organization` or `Person` schema and inspects the `sameAs` array.

**Verdict rules.**
- `pass` — `sameAs` is present and contains at least two URLs whose domains appear in the standard's authoritative-domain list (see Appendix A).
- `warning` — `sameAs` is present but contains fewer than two authoritative URLs, OR contains URLs but none match the authoritative list.
- `fail` — `sameAs` is not present on Organization or Person schema.
- `not_checked` — no Organization or Person schema is present (making `sameAs` inapplicable).

**Evidence required at full level.**
- `sameas_count` — integer; total count of URLs in `sameAs`.
- `authoritative_domains` — array of domains from the authoritative list that are matched.

**Impact.** High.

**Informative references.** schema.org `sameAs`; Wikidata, "Items about organizations".

---

#### 5.3.3 geo.directory_presence

**Detection.** External lookup. The implementation queries a declared set of authoritative directories (see Appendix A) using the entity name derived from Organization schema or from the site's primary title.

**Verdict rules.**
- `pass` — the entity is found in at least one declared directory with a matching name and matching URL (where URL is part of the directory record).
- `warning` — the entity is found in at least one directory by name, but the URL does not match or is not declared in the directory.
- `fail` — the entity is not found in any declared directory.
- `not_checked` — no directories were queried (implementation does not support this check) OR all directory queries failed due to source unavailability.

**Evidence required at full level.**
- `directory_sources_checked` — array of source names.
- `listings_found` — array of `{source, record_url, match_type}` objects.
- `sources_timestamp` — per-source ISO 8601 timestamp of the lookup.

**Impact.** Medium.

**Informative references.** Wikidata Query Service; Crunchbase API; OpenCorporates API.

---

#### 5.3.4 geo.about_page_depth

**Detection.** Content analysis. The implementation identifies the site's About page by conventional URL patterns (`/about`, `/about-us`, `/company`, `/who-we-are`) or by navigation-link text.

**Verdict rules.**
- `pass` — an About page is identified and contains at least 300 words of substantive text, with the majority of sentences describing the entity (who/what/where/when/founding/purpose).
- `warning` — an About page is identified but is under 300 words, or exceeds 300 words but consists primarily of mission-statement abstractions rather than entity description.
- `fail` — no About page can be identified on the site.
- `not_checked` — the homepage could not be retrieved to discover navigation links.

**Evidence required at full level.**
- `about_page_url` — the discovered URL, or `null`.
- `word_count` — integer.
- `entity_markers` — array of matched markers (`founded`, `headquartered`, `founders`, etc.).

**Impact.** Low.

**Informative references.** Google's "About this result" documentation; E-E-A-T guidelines (Search Quality Evaluator Guidelines, Google 2024).

---

#### 5.3.5 geo.entity_consistency

**Detection.** Cross-page. The implementation compares the canonical entity name and primary address across three sources: Organization schema (if present), visible page copy (About, Contact, Footer), and any directory listings returned by `geo.directory_presence`.

**Verdict rules.**
- `pass` — entity name is identical across all available sources after whitespace normalisation, and address matches to the street-and-locality level.
- `warning` — minor divergence only: differences in punctuation (e.g., "Ltd" vs "Ltd."), abbreviation (e.g., "Street" vs "St"), or trailing-slash URL differences.
- `fail` — material divergence: different names, different street addresses, different locality or country.
- `not_checked` — fewer than two of the three sources are available for comparison.

**Evidence required at full level.**
- `canonical_entity_name` — the selected canonical form.
- `name_variants` — array of `{source, value}`.
- `address_variants` — array of `{source, value}`.

**Impact.** Medium.

**Informative references.** Moz, "NAP Consistency for Local SEO"; Google Business Profile guidelines.

---

### 5.4 Threshold summary

This subsection is non-normative. It consolidates every numeric threshold declared in §5.1 through §5.3 into a single table so that implementers and reviewers may audit threshold decisions in one pass. The authoritative definitions remain in the individual check specifications; in the event of any divergence between the prose of §5.1–§5.3 and this summary, the check specification governs.

| Check | Threshold | Verdict boundary |
| --- | --- | --- |
| seo.https | Redirect limit | 10 (RECOMMENDED maximum) |
| seo.title_tag | Title length | 10–70 characters → `pass`; outside → `warning` |
| seo.meta_description | Description length | 50–160 characters → `pass`; outside → `warning` |
| aeo.faq_schema | FAQPage question count | ≥ 2 `mainEntity` questions → `pass` |
| aeo.heading_hierarchy | `<h1>` count | exactly 1 → `pass`; 0 or > 1 → `fail` |
| aeo.direct_answer_opening | First-paragraph word count | 40–60 words → `pass` (with definition); outside → `warning` |
| geo.sameas_authority | Authoritative `sameAs` URLs | ≥ 2 from the authoritative-domain list (Appendix A.3) → `pass`; 1 → `warning` |
| geo.about_page_depth | About-page word count | ≥ 300 words substantive → `pass`; < 300 → `warning` |

Thresholds MAY be revised in any minor version release. Any threshold change MUST be listed explicitly in the change log (Appendix B) with documented rationale. Implementations SHOULD NOT introduce thresholds that diverge from this summary; a local threshold override breaks score comparability across implementations and is incompatible with claiming conformance.

---

## 6. Scoring methodology

### 6.1 Impact bands

Each check is assigned an impact band in its specification. Band values are fixed for version 0.1:

- `high` — 20 points possible.
- `medium` — 10 points possible.
- `low` — 5 points possible.

### 6.2 Verdict points

Each verdict contributes a multiplier to the check's impact band:

- `pass` — 1.0
- `warning` — 0.5
- `fail` — 0.0
- `not_checked` — excluded from scoring entirely.

A check whose verdict is `not_checked` contributes zero to both the earned score and the possible score for its pillar.

### 6.3 Per-check score

For any check with a scored verdict (`pass`, `warning`, `fail`):

```
earned   = impact_band_value * verdict_multiplier
possible = impact_band_value
```

### 6.4 Pillar score

For each pillar P, the pillar score is:

```
pillar_score(P) = ( sum(earned for all checks in P with scored verdicts)
                  / sum(possible for all checks in P with scored verdicts) )
                  * 95
```

The multiplier 95 is the pillar cap. A pillar in which every check passes produces a pillar score of 95, not 100. This cap is deliberate and is discussed in §6.7.

If every check in a pillar has verdict `not_checked`, the pillar score is `null` and the pillar is excluded from the overall score calculation.

### 6.5 Overall score

The overall score is the arithmetic mean of the pillar scores that are not `null`:

```
overall_score = mean(pillar_score(P) for P in [seo, aeo, geo] where pillar_score(P) is not null)
```

The overall score uses the same pillar cap of 95 by virtue of inheriting it from the pillar scores.

### 6.6 Rounding

All displayed scores MUST be rounded to the nearest integer using round-half-up. Intermediate calculations MUST be performed at full precision. An implementation that rounds intermediates and then sums will produce reports that fail the `scoring-consistent` lint rule.

### 6.7 Why the pillar cap is 95

No implementation achieves 100 on this standard, by design. The pillar cap of 95 reflects the fact that the seventeen checks in v0.1 are necessary but not sufficient for any real site's AI visibility — a site that scores 95 across all three pillars has passed every measurable structural check, but there remain unmeasurable factors (content quality, editorial credibility, inbound reference velocity, platform-specific citation history) that this standard does not claim to capture.

The gap between 95 and 100 is the gap between this standard and the truth. It is not a flaw; it is an acknowledgement. Any tool that produces 100/100 scores is overclaiming.

---

## 7. Audit report format

The audit report is a single JSON document. Its canonical shape is defined by the JSON Schema exported from this specification at `standard.makeitseo.io/v0.1/audit-report.schema.json`. This section describes the shape informally.

### 7.1 Top-level structure

```json
{
  "standard_version": "0.1",
  "level": "full",
  "audited_url": "https://example.com/page",
  "timestamp": "2026-04-23T10:30:00Z",
  "implementation": {
    "name": "MakeitSEO Reference Engine",
    "version": "1.0.0"
  },
  "checks": {
    "seo.https": { "verdict": "pass", "evidence": { /* ... */ } },
    "seo.mobile_viewport": { "verdict": "pass", "evidence": { /* ... */ } }
    /* 15 more checks at standard or full level */
  },
  "scoring": {
    "pillar_scores": { "seo": 87, "aeo": 72, "geo": 54 },
    "overall_score": 71,
    "overall_score_semantics": "Structural conformance across 17 checks in three pillars. Does not measure actual citation rate on generative AI platforms."
  },
  "methodology": {
    "engine_version": "1.0.0",
    "data_sources": [
      { "name": "Wikidata", "queried_at": "2026-04-23T10:30:12Z" },
      { "name": "Crunchbase", "queried_at": "2026-04-23T10:30:14Z" }
    ]
  }
}
```

### 7.2 Field requirements by level

At the `minimal` level, `standard_version`, `audited_url`, `timestamp`, and at least one `checks.*` entry are required. Everything else is optional.

At the `standard` level, every check listed in the front matter `checks` map MUST be present with a valid verdict.

At the `full` level, every check MUST additionally include an `evidence` object containing its declared `evidence_required` fields. The `scoring` block is required and MUST include `overall_score_semantics` — a single-sentence plain-language statement of what the overall score measures and what it does not. The `methodology` block is required. Every external lookup MUST have a timestamp.

The `overall_score_semantics` requirement exists to prevent the score from being read as more than it is. An audit score is a structural indicator, not a measurement of real-world AI visibility outcomes. A conformant implementation at the `full` level exposes this distinction at the point of display, not in footnotes. An implementation MAY use the exact default sentence shown in §7.1; an implementation MAY provide its own wording, provided the wording is truthful about what the score does and does not measure.

### 7.3 Non-standard check extensions

Implementations MAY include additional checks beyond the seventeen defined here. Such checks MUST be namespaced outside the three pillar prefixes (for example, `ext.vendor.custom_check`). Non-standard checks MUST NOT contribute to pillar or overall scores. A validator encountering a non-standard check will emit an `info`-severity finding, not an error.

---

## 8. Truncation and confidence

### 8.1 When an audit is complete

An audit is **complete** when every check declared at its conformance level has a verdict of `pass`, `warning`, or `fail` — i.e., no `not_checked` verdicts for in-scope checks. A complete audit at the `standard` level is the default presentational form.

### 8.2 When an audit is partial

An audit is **partial** when at least one in-scope check has verdict `not_checked` for reasons other than inapplicability. A partial audit is still conformant, but the pillar or overall score it produces is computed over fewer checks than a complete audit, and the two are not directly comparable.

An implementation producing a partial audit SHOULD expose the partial nature in any presentation of the score — for example, displaying "72 (partial)" rather than "72" alone.

### 8.3 When an audit is truncated

An audit is **truncated** when the implementation terminated before evaluating all in-scope checks (crash, timeout, rate limit, interrupted network). A truncated audit MUST declare its truncation explicitly, either by including fewer checks than the conformance level requires (in which case the validator rejects it as non-conformant) or by including them with verdict `not_checked` and a `truncation_reason` field in the evidence block.

### 8.4 Minimum viable audit

The minimum data required to produce a meaningful score is:

- At least one pillar with at least 40 points of scored possible value.
- Coverage of at least one `high`-impact check.

An implementation SHOULD refuse to emit a score for audits below this threshold, and SHOULD emit only the individual check verdicts, with a note that the score is not computable.

---

## 9. Versioning and change control

### 9.1 Semantic versioning

This standard uses semantic versioning with the following semantics:

- **Major version bump** — a breaking change. Removes or fundamentally alters an existing check, verdict state, pillar definition, or scoring rule in a way that renders v(current) conformance invalid at v(next).
- **Minor version bump** — an additive change. Introduces new checks, new optional evidence fields, new conformance levels, or new informative references.
- **Patch version bump** — a clarification. Prose edits, corrections to informative references, or non-behavioural fixes.

### 9.2 Deprecation

A check may be deprecated in a minor or patch release by setting `deprecated: true` and `deprecation_reason: <string>` in its front-matter entry. Deprecated checks remain in the spec for at least two minor versions before removal. Removal requires a major version bump. The validator treats deprecated checks as valid but emits a warning in the output.

### 9.3 Change log

Every release — major, minor, or patch — MUST be accompanied by an entry in Appendix B. Each entry lists the version number, release date, every added/modified/removed item with a rationale, any breaking changes, and a migration guide if breaking changes are present.

### 9.4 Pinning

Implementations MUST declare the `standard_version` against which they produce audits. A validator invocation targets a specific version; mixing versions within a single audit is malformed. Exported schema URLs are versioned (`/v0.1/audit-report.schema.json`) and are immutable after publication.

---

## 10. Conformance testing

### 10.1 The validator

Conformance is established mechanically by the validator published at `@makeitseo/standard` on npm. The validator takes an audit report and produces a structured finding report. Zero errors at the declared level equals conformance at that level.

```bash
npx @makeitseo/standard lint --level standard my-audit.json
```

Exit code 0 indicates conformance. Exit code 1 indicates conformance failure. Exit code 2 indicates a tool error.

### 10.2 The public endpoint

A hosted HTTP version of the validator is available at `validate.makeitseo.io` for non-developer users and for third-party tools that want to display a conformance badge. The endpoint is free, rate-limited, and does not require an account.

### 10.3 Claiming conformance

An implementation claiming AI Visibility Audit Standard conformance MUST:

1. Run the validator against a representative audit output at the claimed level.
2. Achieve zero errors.
3. State the claimed level and the standard version in any public representation of conformance.
4. Re-verify conformance within thirty days of any spec version bump that affects the implementation.

An implementation MAY display the embeddable conformance badge served from `validate.makeitseo.io` if it has passed validation within the preceding thirty days. The badge links back to the validator, where anyone may re-verify the claim.

### 10.4 The implementations directory

A public directory of conformant implementations is maintained at `standard.makeitseo.io/implementations`. Listing is alphabetical and includes the conformance level and last-verified date. Inclusion is free. The reference implementation is listed with a marker indicating its canonical status. Competitors to the reference implementation are included on the same terms as any other implementer; this is what distinguishes a directory from a product page.

---

## Appendix A — Informative references

### A.1 Normative references (for RFC 2119 terminology and related)

- **BCP 14** — RFC 2119 and RFC 8174, "Key words for use in RFCs to Indicate Requirement Levels".
- **RFC 9110** — "HTTP Semantics".
- **RFC 9309** — "Robots Exclusion Protocol".
- **RFC 6596** — "The Canonical Link Relation".

### A.2 Informative references (background)

- WHATWG HTML Living Standard — https://html.spec.whatwg.org/
- schema.org vocabulary — https://schema.org/docs/full.html
- Google Search Central documentation — https://developers.google.com/search/docs
- Google Search Quality Rater Guidelines (2024) — E-E-A-T framework.
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- Liu, et al. (2023). "GEO: Generative Engine Optimization". arXiv:2311.09735.
- Answer.AI (2024). "The /llms.txt file". https://llmstxt.org
- sitemaps.org — Protocol 0.9. https://www.sitemaps.org/protocol.html

### A.3 Authoritative-domain list (for `geo.sameas_authority`)

The following domains qualify as authoritative for the purpose of the `geo.sameas_authority` check in v0.1:

- wikidata.org
- wikipedia.org (all language subdomains)
- crunchbase.com
- linkedin.com (company pages only)
- opencorporates.com
- companieshouse.gov.uk
- sec.gov (EDGAR)
- bloomberg.com (company profile pages)
- reuters.com (company profile pages)

This list is revisable in any minor release. Additions require documented rationale in the change log.

### A.4 Authoritative directories (for `geo.directory_presence`)

The following directories are queryable for the `geo.directory_presence` check in v0.1:

- Wikidata (via the SPARQL endpoint at query.wikidata.org)
- Crunchbase (via the Crunchbase Basic API)
- OpenCorporates (via the OpenCorporates API)
- Companies House (for UK-registered entities)

An implementation MAY declare additional directories and include them in evidence. The standard-defined set is the minimum for a conformant `geo.directory_presence` evaluation at the `full` level.

---

## Appendix B — Change log

### v0.1 — 2026-04-23

Initial release.

**Added.** All seventeen launch checks across SEO (7), AEO (5), and GEO (5) pillars, each carrying a `measurement_type: lab` declaration. Three conformance levels (minimal, standard, full). Scoring methodology with impact bands, verdict multipliers, and pillar cap of 95. `overall_score_semantics` requirement at the `full` level. Threshold summary (§5.4). Audit report JSON structure. Versioning and deprecation policy. Validator interface specification. Reference-implementation designation.

**Rationale.** Seventeen checks is a deliberate choice. Fewer than fifteen produces a standard too thin to be useful. More than twenty produces an implementation barrier too high for adoption. Seventeen balances coverage and practicality, with the understanding that minor versions will expand the set as new checks are validated.

**Breaking changes.** Not applicable to initial release.

**Migration guide.** Not applicable to initial release.

---

## Appendix C — Open questions and research agenda

This appendix is non-normative. It records what v0.1 does not answer, and flags items under consideration for v0.2 and beyond. An open question here is neither a commitment to address it nor a promise to leave it alone; it is a record of the editor's awareness.

### C.1 Lab measurement and the absent field layer

Every v0.1 check carries `measurement_type: lab` — every check is a synthetic observation derived from a single crawl or a single declared external lookup. A lab-only standard measures whether a site is structurally eligible for AI visibility; it does not measure whether AI visibility is actually achieved. The two are not the same, and the distinction will determine how v0.1 is read.

The gap matters. A site can pass every structural check in this standard and still fail to be cited by any generative AI platform, because citation depends on factors outside structure — content quality, editorial credibility, inbound reference velocity, platform-specific training data inclusion, topic competitiveness. Conversely, a site can fail several structural checks and still be routinely cited, because a platform's retrieval model happens to index it.

The intended future shape of the standard is a two-layer structure: lab checks (the current seventeen) plus a future field-measurement layer that queries generative AI platforms directly and records actual citation rates over a declared window. The two layers produce independent scores that sit side by side in the report. Divergence between them — high lab, low field — is diagnostic information, not a flaw in either measurement.

Introducing field measurement waits on three preconditions: (1) stable, documented, generally-available platform APIs or scraping-permission frameworks that do not depend on a single vendor's goodwill; (2) a statistically defensible methodology for selecting query sets per site, because citation rate is meaningful only relative to a defined question universe; (3) a privacy and attribution framework that lets implementations share field data without exposing their query sets to reverse engineering. None of the three is resolved as of publication.

Candidate v0.2 checks once preconditions are met: `geo.citation_rate_perplexity`, `geo.citation_rate_openai`, `geo.citation_rate_anthropic`, `geo.citation_rate_google_ai_overviews`. Each would carry `measurement_type: field`.

### C.2 CrUX-style enrichment of lab checks

Independent of the citation-rate question above, several SEO and AEO lab checks could be strengthened by incorporating existing field-data sources such as the Chrome User Experience Report. A page's actual time-to-first-byte from real visitors is a better signal than a single synthetic probe from a single location. v0.1 uses only synthetic observations to keep implementation barriers low. A v0.2 may introduce an optional `field_data` evidence field on lab checks that benefit from it, with synthetic remaining the primary signal and field enrichment as a quality upgrade.

### C.3 Multilingual and internationalisation signals

v0.1 does not include checks for `hreflang`, language declaration consistency, or locale-appropriate schema. A site serving multiple locales currently scores identically whether its hreflang implementation is correct or absent. This is a known gap and a strong candidate for v0.2.

### C.4 Accessibility overlap

Several AEO checks (heading hierarchy, direct-answer openings) overlap with accessibility requirements defined by WCAG. The standard does not claim accessibility conformance. A future version may include informative references to specific WCAG success criteria to help implementers and consumers understand the overlap.

### C.5 Temporal validity of evidence

The standard does not currently specify how long a piece of evidence remains valid for purposes of re-auditing. A check verdict derived from an evidence lookup two months ago is labelled the same as one derived from a lookup two minutes ago. Some form of `evidence_freshness` metadata is under consideration for v0.2.

### C.6 Reference implementation transparency

The reference implementation is designated in §10.3 but its internal behaviour for edge cases (e.g., how it decides whether a page's content is "editorial" for `aeo.article_schema`) is specified only in prose. A companion document listing the reference implementation's heuristic thresholds, updated alongside each spec release, is under consideration.

---

*— End of document —*

*AI Visibility Audit Standard v0.1 · Cloud WiFi Limited · CC-BY 4.0 · Published 2026-04-23*
