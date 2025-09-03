#!/usr/bin/env python3
"""
Version 3 extraction: wraps v2 output and applies:
- alias-based coreference merging (DOE, Department of Education, department)
- entity canonicalization (lowercase, strip, dedup)
- relation de-duplication (subject-predicate-object unique)
- allows multi-parent relationships (no functional constraints)
Produces enhanced_corenlp_extractions_v3.json in same format as v2 with added provenance fields when possible.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ALIASES = {
    'department of education': {'doe','dept of education','education department','department'},
    'department of agriculture': {'hdoa','dept of agriculture','agriculture department'},
    'farm to school program': {'hawaii farm to school program','farm-to-school program'},
}

# Build bidirectional alias map
CANONICAL = {}
for canon, alts in ALIASES.items():
    CANONICAL[canon] = canon
    for a in alts:
        CANONICAL[a] = canon

def canonicalize(text: str) -> str:
    if not text:
        return text
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return CANONICAL.get(t, t)

def merge_entities(entities):
    merged = {}
    best = {}
    for e in entities:
        t = canonicalize(e.get('text',''))
        if not t:
            continue
        key = (t, e.get('type',''))
        cur = merged.get(key)
        if not cur:
            merged[key] = {**e, 'text': t}
            best[key] = e.get('confidence', 0) or 0
        else:
            c = e.get('confidence', 0) or 0
            if c > best[key]:
                merged[key] = {**e, 'text': t}
                best[key] = c
    return list(merged.values())

def dedup_relations(relations):
    seen = set()
    out = []
    for r in relations:
        s = canonicalize(r.get('subject',''))
        p = r.get('predicate','')
        o = canonicalize(r.get('object',''))
        if not (s and p and o):
            continue
        key = (s,p,o)
        if key in seen:
            continue
        seen.add(key)
        r2 = dict(r)
        r2['subject'] = s
        r2['object'] = o
        out.append(r2)
    return out

def run(v2_path: str, v3_path: str):
    with open(v2_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    entities = data.get('entities', [])
    relations = data.get('relations', [])

    entities_v3 = merge_entities(entities)
    relations_v3 = dedup_relations(relations)

    out = dict(data); out['version'] = 'v3_high_impact_medium_effort'
    out['entities'] = entities_v3
    out['relations'] = relations_v3

    with open(v3_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    v2 = Path(__file__).with_name('enhanced_corenlp_extractions_v2.json')
    v3 = Path(__file__).with_name('enhanced_corenlp_extractions_v3.json')
    run(str(v2), str(v3))
    print(f"Wrote {v3}")
