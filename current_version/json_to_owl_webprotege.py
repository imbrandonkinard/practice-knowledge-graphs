#!/usr/bin/env python3
"""
JSON -> OWL (RDF/XML) for WebProtégé compatibility
- Uses RDF triples for assertions (no owl:ObjectPropertyAssertion elements)
- Adds ontology IRI, version IRI, and xml:base
"""
import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_IRI = "http://example.org/legislativeontology"
BASE_NS = f"{BASE_IRI}#"

NS = {
    'rdf':  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'owl':  "http://www.w3.org/2002/07/owl#",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
    'xsd':  "http://www.w3.org/2001/XMLSchema#",
}

for p, uri in NS.items():
    ET.register_namespace(p, uri)
ET.register_namespace('', BASE_NS)  # default


def clean_identifier(text: str) -> str:
    cleaned = re.sub(r'[^\w\s]', '', (text or '').strip())
    cleaned = re.sub(r'\s+', '_', cleaned)
    if not cleaned:
        cleaned = 'entity'
    if not cleaned[0].isalpha():
        cleaned = 'entity_' + cleaned
    return cleaned


def add_ontology_header(root: ET.Element, name: str):
    ont = ET.SubElement(root, f"{{{NS['owl']}}}Ontology")
    ont.set(f"{{{NS['rdf']}}}about", BASE_IRI)
    version_iri = ET.SubElement(ont, f"{{{NS['owl']}}}versionIRI")
    version_iri.set(f"{{{NS['rdf']}}}resource", f"{BASE_IRI}/1.0")
    comment = ET.SubElement(ont, f"{{{NS['rdfs']}}}comment")
    comment.text = f"Knowledge Graph from {name} - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


def add_class(root: ET.Element, class_name: str, comment_text: str = ""):
    cls = ET.SubElement(root, f"{{{NS['owl']}}}Class")
    cls.set(f"{{{NS['rdf']}}}about", f"#{class_name}")
    label = ET.SubElement(cls, f"{{{NS['rdfs']}}}label")
    label.text = class_name
    if comment_text:
        c = ET.SubElement(cls, f"{{{NS['rdfs']}}}comment")
        c.text = comment_text


def add_datatype_property(root: ET.Element, name: str, label_text: str, xsd_range_local: str, comment_text: str = ""):
    prop = ET.SubElement(root, f"{{{NS['owl']}}}DatatypeProperty")
    prop.set(f"{{{NS['rdf']}}}about", f"#{name}")
    label = ET.SubElement(prop, f"{{{NS['rdfs']}}}label")
    label.text = label_text
    if comment_text:
        c = ET.SubElement(prop, f"{{{NS['rdfs']}}}comment")
        c.text = comment_text
    rng = ET.SubElement(prop, f"{{{NS['rdfs']}}}range")
    rng.set(f"{{{NS['rdf']}}}resource", f"{NS['xsd']}{xsd_range_local}")


def add_object_property(root: ET.Element, name: str, label_text: str, comment_text: str = ""):
    prop = ET.SubElement(root, f"{{{NS['owl']}}}ObjectProperty")
    prop.set(f"{{{NS['rdf']}}}about", f"#{name}")
    label = ET.SubElement(prop, f"{{{NS['rdfs']}}}label")
    label.text = label_text
    if comment_text:
        c = ET.SubElement(prop, f"{{{NS['rdfs']}}}comment")
        c.text = comment_text


def add_individual(root: ET.Element, iri_fragment: str, class_name: str, label_text: str):
    indiv = ET.SubElement(root, f"{{{NS['owl']}}}NamedIndividual")
    indiv.set(f"{{{NS['rdf']}}}about", f"#{iri_fragment}")
    typ = ET.SubElement(indiv, f"{{{NS['rdf']}}}type")
    typ.set(f"{{{NS['rdf']}}}resource", f"#{class_name}")
    label = ET.SubElement(indiv, f"{{{NS['rdfs']}}}label")
    label.text = label_text


def add_object_assertion(root: ET.Element, subj_frag: str, prop_name: str, obj_frag: str):
    # RDF/XML triple style: describe subject and include predicate as element
    desc = ET.SubElement(root, f"{{{NS['rdf']}}}Description")
    desc.set(f"{{{NS['rdf']}}}about", f"#{subj_frag}")
    pred = ET.SubElement(desc, prop_name)  # default ns element => <propName>
    pred.set(f"{{{NS['rdf']}}}resource", f"#{obj_frag}")


def add_data_assertion(root: ET.Element, subj_frag: str, prop_name: str, literal: str, dtype_local: str):
    desc = ET.SubElement(root, f"{{{NS['rdf']}}}Description")
    desc.set(f"{{{NS['rdf']}}}about", f"#{subj_frag}")
    prop = ET.SubElement(desc, prop_name)
    prop.set(f"{{{NS['rdf']}}}datatype", f"{NS['xsd']}{dtype_local}")
    prop.text = literal


PROPERTY_MAP = {
    'moved': 'moved_to',
    'established': 'establishes',
    'requires': 'requires',
    'affects': 'affects',
    'manages': 'manages',
    'reports': 'reports_to',
    'located': 'located_in',
    'starts': 'starts_on',
    'ends': 'ends_on',
    'creates': 'creates',
    'amends': 'amends',
    'repeals': 'repeals',
}

CLASS_MAP = {
    'PROGRAM': 'Program',
    'ORGANIZATION': 'Organization',
    'DEPARTMENT': 'Department',
    'AGENCY': 'Agency',
    'PERSON': 'Person',
    'LOCATION': 'Location',
    'DATE': 'Date',
    'MONEY': 'MonetaryAmount',
    'PERCENT': 'Percentage',
    'POLICY': 'Policy',
    'REQUIREMENT': 'Requirement',
    'GOAL': 'Goal',
}


def convert(input_json: str, output_owl: str) -> bool:
    with open(input_json, 'r') as f:
        data = json.load(f)

    root = ET.Element(f"{{{NS['rdf']}}}RDF", attrib={"xml:base": BASE_IRI})

    add_ontology_header(root, input_json)

    # Classes (only those referenced)
    seen_classes = set()
    for ent in data.get('entities', []):
        cls = CLASS_MAP.get(ent.get('type', '').upper(), ent.get('type', 'Entity').title())
        if cls not in seen_classes:
            add_class(root, cls, f"Class for {ent.get('type', 'ENTITY')} entities")
            seen_classes.add(cls)

    # Properties
    add_datatype_property(root, 'hasConfidence', 'has confidence', 'float', 'Confidence score for extracted info')

    seen_obj_props = set()
    for rel in data.get('relations', []):
        pred = PROPERTY_MAP.get(rel.get('predicate', '').strip().lower()) or clean_identifier(rel.get('predicate', 'related_to'))
        if pred not in seen_obj_props:
            add_object_property(root, pred, pred.replace('_', ' ').title(), f"Derived from predicate '{rel.get('predicate')}'")
            seen_obj_props.add(pred)

    # Individuals
    seen_indivs = set()
    for ent in data.get('entities', []):
        txt = (ent.get('text') or '').strip()
        typ = CLASS_MAP.get(ent.get('type', '').upper(), ent.get('type', 'Entity').title())
        if not txt:
            continue
        frag = clean_identifier(txt)
        if frag in seen_indivs:
            continue
        add_individual(root, frag, typ, txt)
        seen_indivs.add(frag)

    # Assertions from relations
    for rel in data.get('relations', []):
        s = clean_identifier((rel.get('subject') or '').strip())
        o = clean_identifier((rel.get('object') or '').strip())
        if not s or not o:
            continue
        p = PROPERTY_MAP.get((rel.get('predicate') or '').strip().lower()) or clean_identifier(rel.get('predicate', 'related_to'))
        add_object_assertion(root, s, p, o)
        if 'confidence' in rel:
            try:
                add_data_assertion(root, s, 'hasConfidence', str(float(rel['confidence'])), 'float')
            except Exception:
                pass

    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ', level=0)
    tree.write(output_owl, encoding='utf-8', xml_declaration=True)
    return True


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python json_to_owl_webprotege.py <input.json> [output.owl]')
        sys.exit(1)
    input_json = sys.argv[1]
    output_owl = sys.argv[2] if len(sys.argv) > 2 else 'ontology_webprotege.owl'
    if convert(input_json, output_owl):
        print(f'Wrote {output_owl}')
        print('Upload this file to WebProtégé. If it still fails, validate with xmllint and check WebProtégé logs.')
