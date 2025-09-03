# Version 3 Difference Summary

This document summarizes changes in v3 relative to v2 and v1.

## v3 vs v2

- Added in v3:
  - Alias-based coreference merging for common entities (e.g., DOE ⇄ Department of Education)
  - Entity canonicalization (lowercase, trim, whitespace normalize) to reduce duplicates
  - Relation de-duplication by unique (subject, predicate, object)
  - Preserves v2 schema; adds updated `version` metadata
- Not changed in v3:
  - Custom NER patterns (already added in v2)
  - Enhanced relation patterns (already added in v2)
  - CoreNLP annotators configuration (v2 responsibility)
- Rationale:
  - v3 focuses on output quality normalization/clean-up to improve graph consistency and downstream ontology alignment.

### Code-level deltas (high-level)
- v2 main: `entity_relation_extraction_v2.py` performs extraction (CoreNLP + patterns + OpenIE) and writes `enhanced_corenlp_extractions_v2.json`.
- v3 main: `entity_relation_extraction_v3.py` reads v2 JSON, applies:
  - `merge_entities(...)` using canonicalized text and best-confidence merge
  - `dedup_relations(...)` using canonicalized subject/object
  - writes `enhanced_corenlp_extractions_v3.json`

### Output differences
- Entities:
  - Fewer duplicates; canonical names used for aliases
  - Higher average confidence retained via best-of-duplicates selection
- Relations:
  - Fewer duplicate edges; canonical subjects/objects unify parallel edges
- Metadata:
  - `version`: `v3_high_impact_medium_effort`

## v3 vs v1

- Additions beyond v1 (via v2 and v3):
  - Enhanced CoreNLP annotators: lemma, openie (v2)
  - Custom legislative NER patterns (v2)
  - Enhanced relation patterns (v2)
  - Confidence scoring and relation source tracking (v2)
  - Output normalization: alias merge, canonicalization, relation de-dup (v3)
- Net effect:
  - Many more domain-relevant entities and relations than v1
  - Cleaner graph with fewer duplicate entities/edges than both v1 and v2

## Alignment with Roadmap

- This v3 emphasizes “High Impact, Medium Effort” via normalization:
  - Improves graph quality without changing extraction recall logic from v2
  - Prepares ground for future items (dependency parse enhancement, context-aware entities)
- Items covered by versions:
  - Enhanced Annotators: v2
  - Custom NER Patterns: v2
  - Enhanced Relation Patterns: v2
  - v3: Canonicalization, alias/coreference merge, relation de-duplication
  - Future: Dependency Parse Enhancement; Context-Aware Entities; ML Confidence Scoring; SRL

## Logic Check (v3)

- `canonicalize(text)`: lowercases, trims, collapses whitespace, applies alias map (bidirectional build from `ALIASES` into `CANONICAL`).
- `merge_entities(entities)`: merges by `(canonical_text, type)` and keeps the highest-confidence representative.
- `dedup_relations(relations)`: canonicalizes subject/object and removes duplicate triples by set membership.
- I/O:
  - Reads: `enhanced_corenlp_extractions_v2.json`
  - Writes: `enhanced_corenlp_extractions_v3.json`
  - Schema preserved; only values normalized.

All functions are cohesive, side-effect free (except file I/O), and operate in-memory with straightforward complexity suitable for current dataset sizes.
