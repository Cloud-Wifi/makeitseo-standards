#!/usr/bin/env python3
"""
AI Visibility Audit Standard — JSON Schema exporter

Reads STANDARD.md front matter and produces audit-report.schema.json
deterministically. Same input => byte-identical output (Platform Spec §5.2).

Usage:
    python3 export_json_schema.py STANDARD.md > audit-report.schema.json
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("pyyaml required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# Detection method -> evidence field type hints.
# Keeps the schema expressive without inventing per-check scalar types
# that would drift from the spec prose.
EVIDENCE_FIELD_HINTS = {
    # seo.https
    "final_url": {"type": "string", "format": "uri"},
    "final_protocol": {"type": "string", "enum": ["http", "https"]},
    # seo.mobile_viewport
    "viewport_value": {"type": ["string", "null"]},
    # seo.title_tag
    "title_text": {"type": ["string", "null"]},
    "title_length": {"type": "integer", "minimum": 0},
    # seo.meta_description
    "description_text": {"type": ["string", "null"]},
    "description_length": {"type": "integer", "minimum": 0},
    # seo.canonical_url
    "canonical_href": {"type": ["string", "null"]},
    "resolves_to_self": {"type": "boolean"},
    # seo.robots_indexability
    "robots_txt_disallows": {"type": "boolean"},
    "meta_robots_directives": {"type": "array", "items": {"type": "string"}},
    "x_robots_tag": {"type": ["string", "null"]},
    # seo.sitemap_present
    "sitemap_url": {"type": ["string", "null"]},
    "sitemap_reachable": {"type": "boolean"},
    "sitemap_valid_xml": {"type": "boolean"},
    # aeo.faq_schema
    "schema_found": {"type": "boolean"},
    "question_count": {"type": "integer", "minimum": 0},
    # aeo.heading_hierarchy
    "h1_count": {"type": "integer", "minimum": 0},
    "skipped_levels": {
        "type": "array",
        "items": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 2},
    },
    "heading_outline": {"type": "array", "items": {"type": "string"}},
    # aeo.direct_answer_opening
    "first_paragraph_text": {"type": ["string", "null"]},
    "word_count": {"type": "integer", "minimum": 0},
    "contains_definition": {"type": "boolean"},
    # aeo.article_schema
    "required_properties_present": {"type": "array", "items": {"type": "string"}},
    # aeo.organization_schema
    "has_name": {"type": "boolean"},
    "has_url": {"type": "boolean"},
    # geo.llms_txt_present
    "llms_txt_reachable": {"type": "boolean"},
    "llms_txt_valid": {"type": "boolean"},
    # geo.sameas_authority
    "sameas_count": {"type": "integer", "minimum": 0},
    "authoritative_domains": {"type": "array", "items": {"type": "string"}},
    # geo.directory_presence
    "directory_sources_checked": {"type": "array", "items": {"type": "string"}},
    "listings_found": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "record_url": {"type": ["string", "null"], "format": "uri"},
                "match_type": {"type": "string", "enum": ["exact", "fuzzy", "partial"]},
            },
            "required": ["source", "match_type"],
            "additionalProperties": False,
        },
    },
    "sources_timestamp": {
        "type": "object",
        "additionalProperties": {"type": "string", "format": "date-time"},
    },
    # geo.about_page_depth
    "about_page_url": {"type": ["string", "null"], "format": "uri"},
    "entity_markers": {"type": "array", "items": {"type": "string"}},
    # geo.entity_consistency
    "canonical_entity_name": {"type": ["string", "null"]},
    "name_variants": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["source", "value"],
            "additionalProperties": False,
        },
    },
    "address_variants": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "source": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["source", "value"],
            "additionalProperties": False,
        },
    },
}


def extract_front_matter(md_path: Path) -> dict:
    """Extract and parse the YAML front matter from STANDARD.md."""
    content = md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError("STANDARD.md must start with YAML front matter")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Malformed front matter: expected --- ... --- at top of file")
    return yaml.safe_load(parts[1])


def check_schema(check_id: str, check_def: dict) -> dict:
    """Build a JSON Schema for a single check entry in the audit report.

    At the `full` level, verdict + evidence are required and evidence must
    contain every evidence_required field. At lower levels, evidence is
    optional — that constraint is applied conditionally at the top level,
    not here, so this schema describes the maximal valid check entry.
    """
    verdicts = check_def["verdicts"]
    evidence_required = check_def.get("evidence_required", [])

    evidence_props = {}
    for field in evidence_required:
        # If we have a hint, use it; otherwise accept any type (future-compat).
        evidence_props[field] = EVIDENCE_FIELD_HINTS.get(
            field, {"description": f"Evidence field '{field}' — type unspecified"}
        )
    # Implementations may record supplementary evidence beyond the required set.
    # Preserve, don't reject (Platform Spec §3.5 graceful-unknown handling).

    schema = {
        "type": "object",
        "properties": {
            "verdict": {
                "type": "string",
                "enum": verdicts,
                "description": f"Verdict for check {check_id}. One of: {', '.join(verdicts)}.",
            },
            "evidence": {
                "type": "object",
                "properties": evidence_props,
                "additionalProperties": True,
            },
            "truncation_reason": {
                "type": "string",
                "description": "Required when verdict is 'not_checked' due to truncation (spec §8.3).",
            },
        },
        "required": ["verdict"],
        "additionalProperties": True,
    }
    return schema


def build_schema(fm: dict) -> dict:
    """Build the complete JSON Schema for an audit report."""
    # SemVer is semantically a string; coerce in case YAML loaded it as a number.
    version = str(fm["version"])
    checks = fm["checks"]
    pillars = list(fm["pillars"].keys())

    # Per-check schemas
    check_schemas = {cid: check_schema(cid, cdef) for cid, cdef in sorted(checks.items())}

    # Pillar score schema — value is an integer 0–95 or null (pillar skipped).
    pillar_score_schema = {
        "type": ["integer", "null"],
        "minimum": 0,
        "maximum": 95,
        "description": "Integer pillar score capped at 95, or null if pillar is excluded.",
    }

    # Standard-level required check paths (fully qualified)
    standard_required_checks = sorted(checks.keys())

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://standard.makeitseo.io/v{version}/audit-report.schema.json",
        "title": "AI Visibility Audit Report",
        "description": (
            f"Canonical JSON Schema for audit reports conformant to the AI Visibility "
            f"Audit Standard v{version}. Maintained by Cloud WiFi Limited. Generated "
            f"from STANDARD.md — do not edit by hand."
        ),
        "type": "object",

        "properties": {
            "standard_version": {
                "type": "string",
                "const": version,
                "description": "The standard version this audit conforms to.",
            },
            "level": {
                "type": "string",
                "enum": ["minimal", "standard", "full"],
                "description": "The conformance level claimed by this audit.",
            },
            "audited_url": {
                "type": "string",
                "format": "uri",
                "description": "The URL that was audited.",
            },
            "timestamp": {
                "type": "string",
                "format": "date-time",
                "description": "ISO 8601 timestamp of when the audit was produced.",
            },
            "implementation": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "url": {"type": "string", "format": "uri"},
                },
                "required": ["name", "version"],
                "additionalProperties": True,
            },
            "checks": {
                "type": "object",
                "description": (
                    "Map of check IDs to verdict+evidence entries. Known check IDs "
                    "(from the spec) are strictly typed. Non-standard check IDs MUST "
                    "be namespaced outside the core pillars (e.g., 'ext.vendor.custom') "
                    "and are preserved but excluded from scoring."
                ),
                "properties": check_schemas,
                "patternProperties": {
                    # Non-standard checks must use a namespace prefix outside pillars.
                    # The patternProperties here is permissive for extension IDs.
                    r"^(?!(seo|aeo|geo)\.)[a-z0-9_]+\.[a-z0-9_.]+$": {
                        "type": "object",
                        "properties": {
                            "verdict": {
                                "type": "string",
                                "enum": ["pass", "warning", "fail", "not_checked"],
                            },
                            "evidence": {"type": "object"},
                        },
                        "required": ["verdict"],
                        "additionalProperties": True,
                    },
                },
                "additionalProperties": False,
                "minProperties": 1,
            },
            "scoring": {
                "type": "object",
                "properties": {
                    "pillar_scores": {
                        "type": "object",
                        "properties": {p: pillar_score_schema for p in pillars},
                        "required": pillars,
                        "additionalProperties": False,
                    },
                    "overall_score": {
                        "type": ["integer", "null"],
                        "minimum": 0,
                        "maximum": 95,
                    },
                    "overall_score_semantics": {
                        "type": "string",
                        "minLength": 1,
                        "description": (
                            "Single-sentence plain-language statement of what the overall "
                            "score measures and does not measure. Required at the 'full' "
                            "conformance level (spec §7.2)."
                        ),
                    },
                },
                "required": ["pillar_scores", "overall_score"],
                "additionalProperties": False,
            },
            "methodology": {
                "type": "object",
                "properties": {
                    "engine_version": {"type": "string"},
                    "data_sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "queried_at": {"type": "string", "format": "date-time"},
                            },
                            "required": ["name", "queried_at"],
                            "additionalProperties": True,
                        },
                    },
                },
                "required": ["engine_version", "data_sources"],
                "additionalProperties": True,
            },
        },

        "required": ["standard_version", "audited_url", "timestamp", "checks"],

        "additionalProperties": True,

        # Conditional requirements by declared conformance level.
        "allOf": [
            # If level = "standard" or "full", all 17 checks must be present.
            {
                "if": {
                    "properties": {"level": {"enum": ["standard", "full"]}},
                    "required": ["level"],
                },
                "then": {
                    "properties": {
                        "checks": {
                            "required": standard_required_checks,
                        }
                    }
                },
            },
            # If level = "full", scoring and methodology must be present,
            # scoring must include overall_score_semantics, and every known
            # check's evidence must include its required fields.
            {
                "if": {
                    "properties": {"level": {"const": "full"}},
                    "required": ["level"],
                },
                "then": {
                    "required": ["scoring", "methodology"],
                    "properties": {
                        "scoring": {
                            "required": [
                                "pillar_scores",
                                "overall_score",
                                "overall_score_semantics",
                            ],
                        },
                        "checks": {
                            "properties": {
                                cid: {
                                    "required": ["verdict", "evidence"],
                                    "properties": {
                                        "evidence": {
                                            "required": cdef.get("evidence_required", []),
                                        }
                                    },
                                }
                                for cid, cdef in sorted(checks.items())
                                if cdef.get("evidence_required")
                            },
                        },
                    },
                },
            },
        ],

        # Examples — one minimal, one standard, one full.
        "examples": [
            {
                "standard_version": version,
                "audited_url": "https://example.com",
                "timestamp": "2026-04-23T10:30:00Z",
                "checks": {"seo.https": {"verdict": "pass"}},
            },
        ],
    }

    return schema


def main():
    if len(sys.argv) != 2:
        print("Usage: export_json_schema.py STANDARD.md", file=sys.stderr)
        sys.exit(2)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"Not found: {md_path}", file=sys.stderr)
        sys.exit(2)

    fm = extract_front_matter(md_path)
    schema = build_schema(fm)

    # Deterministic output: sort keys at every level, consistent indent, trailing newline.
    output = json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False)
    print(output)


if __name__ == "__main__":
    main()
