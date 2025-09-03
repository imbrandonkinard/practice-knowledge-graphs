# Version 3: High Impact - Medium Effort

## Goals
- Support multi-parent relationships and richer relation extraction
- Improve entity quality via coreference resolution and canonicalization
- Output ontology-ready data with provenance and time (optional fields)

## What's Implemented in v3 (initial)
- Baseline copied from v2 as starting point
- v3 script scaffold (coref/linking stubs to be implemented next)
- Updated ontology/export guidance to allow multi-parent relations (non-functional props)

## Next Steps (Planned Work)
1. Coreference resolution
   - Add lightweight coref (e.g., spaCy coref or `neuralcoref` alternative)
   - Merge mentions ("DOE", "Department of Education", "department") into one canonical entity
2. Entity canonicalization / linking
   - Abbreviation expansion, fuzzy matching, embedding similarity
   - Stable IDs per canonical entity
3. Relation extraction upgrades
   - Dependency-based patterns for governance verbs (manages, reports_to, moved_to)
   - Add OpenIE or transformer RE model to capture broader relations
   - De-duplicate relations; attach confidence and sentence context
4. Ontology modeling changes
   - Ensure properties like `reports_to`, `manages` are NOT functional
   - Add optional Role/Assignment reification for n-ary cases (with `hasStart`, `hasEnd`)
5. Provenance & time (optional in JSON)
   - Include `sourceSentence`, `sourceSpan`, `docId`, and optional `validTime` for relations
6. Evaluation & tests
   - Add SPARQL/JSON tests to show one entity with 2+ parents
   - Regression tests comparing v2 vs v3 improvements

## Run (temporary)
- Use `entity_relation_extraction_v3.py` (to be added) similar to v2 runner
- Input: `extracted_bill_final.txt`
- Output: `enhanced_corenlp_extractions_v3.json`

## Deliverables
- `entity_relation_extraction_v3.py`
- `enhanced_corenlp_extractions_v3.json`
- Updated docs and examples

