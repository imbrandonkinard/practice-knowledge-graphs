#!/usr/bin/env python3
"""
Enhanced Knowledge Graph Generator
Creates a comprehensive knowledge graph with entities, relationships, and policy insights
"""

import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Set, Tuple

BASE_IRI = "http://example.org/farm-to-school-ontology"
BASE_NS = f"{BASE_IRI}#"

NS = {
    'rdf':  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'owl':  "http://www.w3.org/2002/07/owl#",
    'rdfs': "http://www.w3.org/2000/01/rdf-schema#",
    'xsd':  "http://www.w3.org/2001/XMLSchema#",
}

for p, uri in NS.items():
    ET.register_namespace(p, uri)
ET.register_namespace('', BASE_NS)

def clean_identifier(text: str) -> str:
    """Clean text to create valid OWL identifiers"""
    cleaned = re.sub(r'[^\w\s]', '', (text or '').strip())
    cleaned = re.sub(r'\s+', '_', cleaned)
    if not cleaned:
        cleaned = 'entity'
    if not cleaned[0].isalpha():
        cleaned = 'entity_' + cleaned
    return cleaned

def add_ontology_header(root: ET.Element, name: str):
    """Add ontology header with metadata"""
    ont = ET.SubElement(root, f"{{{NS['owl']}}}Ontology")
    ont.set(f"{{{NS['rdf']}}}about", BASE_IRI)
    version_iri = ET.SubElement(ont, f"{{{NS['owl']}}}versionIRI")
    version_iri.set(f"{{{NS['rdf']}}}resource", f"{BASE_IRI}/1.0")
    comment = ET.SubElement(ont, f"{{{NS['rdfs']}}}comment")
    comment.text = f"Enhanced Farm-to-School Knowledge Graph - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Add domain-specific metadata
    domain = ET.SubElement(ont, f"{{{NS['rdfs']}}}comment")
    domain.text = "Knowledge graph for Hawaii Farm-to-School Program legislative analysis"

def define_core_classes(root: ET.Element):
    """Define comprehensive class hierarchy for legislative/food system domain"""
    
    classes = [
        ("Program", "Government programs and initiatives"),
        ("GovernmentAgency", "Government departments and agencies"),
        ("Department", "Specific government departments"),
        ("Person", "Individual people mentioned in legislation"),
        ("Location", "Geographic entities and places"),
        ("Date", "Temporal entities and time periods"),
        ("Goal", "Policy objectives and targets"),
        ("Requirement", "Legal requirements and obligations"),
        ("Report", "Reporting requirements and documents"),
        ("Food", "Food products and categories"),
        ("School", "Educational institutions"),
        ("LegislativeDocument", "Bills, acts, and legal documents"),
        ("Section", "Sections within legislative documents"),
        ("Percentage", "Percentage values and targets"),
        ("MonetaryAmount", "Financial amounts and budgets"),
        ("Stakeholder", "Organizations and groups affected by policy"),
        ("Policy", "Policies and regulations"),
        ("Process", "Processes and procedures"),
        ("Outcome", "Expected outcomes and results")
    ]
    
    for class_name, comment_text in classes:
        cls = ET.SubElement(root, f"{{{NS['owl']}}}Class")
        cls.set(f"{{{NS['rdf']}}}about", f"#{class_name}")
        label = ET.SubElement(cls, f"{{{NS['rdfs']}}}label")
        label.text = class_name
        comment = ET.SubElement(cls, f"{{{NS['rdfs']}}}comment")
        comment.text = comment_text

def define_properties(root: ET.Element):
    """Define comprehensive property hierarchy"""
    
    # Organizational relationships
    org_props = [
        ("manages", "manages", "One entity manages another"),
        ("reports_to", "reports to", "Reporting relationship"),
        ("located_in", "located in", "Geographic location relationship"),
        ("moved_to", "moved to", "Transfer or relocation relationship"),
        ("moved_from", "moved from", "Source of transfer or relocation"),
        ("headed_by", "headed by", "Leadership relationship"),
        ("collaborates_with", "collaborates with", "Collaboration relationship"),
        ("affects", "affects", "Impact relationship"),
        ("implements", "implements", "Implementation relationship"),
        ("establishes", "establishes", "Creation or establishment relationship")
    ]
    
    # Policy relationships
    policy_props = [
        ("requires", "requires", "Requirement relationship"),
        ("creates", "creates", "Creation relationship"),
        ("amends", "amends", "Amendment relationship"),
        ("repeals", "repeals", "Repeal relationship"),
        ("has_goal", "has goal", "Goal relationship"),
        ("has_deadline", "has deadline", "Deadline relationship"),
        ("has_target", "has target", "Target relationship"),
        ("serves", "serves", "Service relationship"),
        ("procures", "procures", "Procurement relationship"),
        ("consumes", "consumes", "Consumption relationship")
    ]
    
    # Data properties
    data_props = [
        ("hasConfidence", "has confidence", "float", "Confidence score for extracted information"),
        ("hasPercentage", "has percentage", "float", "Percentage value"),
        ("hasAmount", "has amount", "float", "Monetary amount"),
        ("hasYear", "has year", "int", "Year value"),
        ("hasText", "has text", "string", "Original text content"),
        ("hasContext", "has context", "string", "Contextual information")
    ]
    
    # Add object properties
    for prop_name, label_text, comment_text in org_props + policy_props:
        prop = ET.SubElement(root, f"{{{NS['owl']}}}ObjectProperty")
        prop.set(f"{{{NS['rdf']}}}about", f"#{prop_name}")
        label = ET.SubElement(prop, f"{{{NS['rdfs']}}}label")
        label.text = label_text
        comment = ET.SubElement(prop, f"{{{NS['rdfs']}}}comment")
        comment.text = comment_text
    
    # Add data properties
    for prop_name, label_text, xsd_type, comment_text in data_props:
        prop = ET.SubElement(root, f"{{{NS['owl']}}}DatatypeProperty")
        prop.set(f"{{{NS['rdf']}}}about", f"#{prop_name}")
        label = ET.SubElement(prop, f"{{{NS['rdfs']}}}label")
        label.text = label_text
        comment = ET.SubElement(prop, f"{{{NS['rdfs']}}}comment")
        comment.text = comment_text
        if xsd_type:
            rng = ET.SubElement(prop, f"{{{NS['rdfs']}}}range")
            rng.set(f"{{{NS['rdf']}}}resource", f"{NS['xsd']}{xsd_type}")

def extract_enhanced_entities_and_relationships(bill_text: str) -> Tuple[Dict, List]:
    """Extract enhanced entities and relationships from bill text"""
    
    entities = {}
    relationships = []
    
    # Enhanced entity extraction with domain knowledge
    entity_patterns = {
        'Program': [
            r'farm to school program',
            r'hawaii farm to school program',
            r'farm to school coordinator'
        ],
        'GovernmentAgency': [
            r'department of education',
            r'department of agriculture',
            r'doe',
            r'hdoa',
            r'legislature',
            r'state of hawaii'
        ],
        'Location': [
            r'hawaii',
            r'public schools',
            r'state facilities',
            r'education facilities',
            r'maui county'
        ],
        'Goal': [
            r'thirty per cent',
            r'30%',
            r'locally sourced',
            r'local sourcing',
            r'2030'
        ],
        'Requirement': [
            r'annual report',
            r'reporting requirement',
            r'progress report',
            r'status report'
        ],
        'Food': [
            r'locally sourced products',
            r'fresh local agricultural products',
            r'local value-added processed',
            r'fruits',
            r'vegetables',
            r'poultry',
            r'livestock',
            r'milk',
            r'eggs'
        ],
        'Process': [
            r'procurement',
            r'consumption',
            r'training',
            r'cooking from scratch',
            r'garden and farm-based education'
        ]
    }
    
    # Extract entities
    for entity_type, patterns in entity_patterns.items():
        for pattern in patterns:
            matches = re.finditer(pattern, bill_text, re.IGNORECASE)
            for match in matches:
                text = match.group().strip()
                if text not in entities:
                    entities[text] = {
                        'type': entity_type,
                        'text': text,
                        'start_char': match.start(),
                        'end_char': match.end()
                    }
    
    # Enhanced relationship extraction
    relationship_patterns = [
        # Organizational relationships
        (r'farm to school program.*moved.*department of agriculture.*department of education', 
         'farm to school program', 'moved_from', 'department of agriculture'),
        (r'farm to school program.*moved.*department of agriculture.*department of education', 
         'farm to school program', 'moved_to', 'department of education'),
        (r'department of education.*manages.*farm to school program', 
         'department of education', 'manages', 'farm to school program'),
        (r'farm to school coordinator.*headed by.*department', 
         'farm to school coordinator', 'headed_by', 'department of education'),
        
        # Policy relationships
        (r'department.*submit.*annual report.*legislature', 
         'department of education', 'reports_to', 'legislature'),
        (r'program.*establish.*goal.*thirty per cent', 
         'farm to school program', 'has_goal', 'thirty per cent'),
        (r'program.*establish.*goal.*2030', 
         'farm to school program', 'has_deadline', '2030'),
        (r'department.*procure.*locally sourced products', 
         'department of education', 'procures', 'locally sourced products'),
        (r'schools.*serve.*locally sourced food', 
         'public schools', 'serves', 'locally sourced products'),
        (r'students.*consume.*fresh fruits.*vegetables', 
         'students', 'consumes', 'fresh local agricultural products'),
        
        # Implementation relationships
        (r'program.*implement.*policy', 
         'farm to school program', 'implements', 'farm to school policy'),
        (r'coordinator.*collaborate.*stakeholders', 
         'farm to school coordinator', 'collaborates_with', 'stakeholders'),
        (r'program.*affect.*student health', 
         'farm to school program', 'affects', 'student health'),
        (r'program.*affect.*local food system', 
         'farm to school program', 'affects', 'local food system'),
        
        # Geographic relationships
        (r'program.*located.*hawaii', 
         'farm to school program', 'located_in', 'hawaii'),
        (r'schools.*located.*hawaii', 
         'public schools', 'located_in', 'hawaii'),
    ]
    
    # Extract relationships
    for pattern, subject, predicate, obj in relationship_patterns:
        if re.search(pattern, bill_text, re.IGNORECASE):
            relationships.append({
                'subject': subject,
                'predicate': predicate,
                'object': obj,
                'confidence': 0.8,
                'context': f"Extracted from: {pattern[:50]}..."
            })
    
    return entities, relationships

def add_individuals_and_assertions(root: ET.Element, entities: Dict, relationships: List):
    """Add individuals and property assertions to the ontology"""
    
    # Add individuals
    for text, entity_data in entities.items():
        frag = clean_identifier(text)
        cls_name = entity_data['type']
        
        indiv = ET.SubElement(root, f"{{{NS['owl']}}}NamedIndividual")
        indiv.set(f"{{{NS['rdf']}}}about", f"#{frag}")
        
        typ = ET.SubElement(indiv, f"{{{NS['rdf']}}}type")
        typ.set(f"{{{NS['rdf']}}}resource", f"#{cls_name}")
        
        label = ET.SubElement(indiv, f"{{{NS['rdfs']}}}label")
        label.text = text
        
        # Add confidence if available
        if 'confidence' in entity_data:
            conf = ET.SubElement(indiv, f"{{{NS['owl']}}}DataPropertyAssertion")
            prop = ET.SubElement(conf, f"{{{NS['owl']}}}DataProperty")
            prop.set(f"{{{NS['rdf']}}}resource", "#hasConfidence")
            val = ET.SubElement(conf, f"{{{NS['owl']}}}DataPropertyValue")
            val.text = str(entity_data['confidence'])
    
    # Add property assertions
    for rel in relationships:
        subj_frag = clean_identifier(rel['subject'])
        obj_frag = clean_identifier(rel['object'])
        pred = rel['predicate']
        
        # Create RDF triple
        desc = ET.SubElement(root, f"{{{NS['rdf']}}}Description")
        desc.set(f"{{{NS['rdf']}}}about", f"#{subj_frag}")
        
        pred_elem = ET.SubElement(desc, pred)
        pred_elem.set(f"{{{NS['rdf']}}}resource", f"#{obj_frag}")
        
        # Add confidence
        if 'confidence' in rel:
            conf_elem = ET.SubElement(desc, "hasConfidence")
            conf_elem.set(f"{{{NS['rdf']}}}datatype", f"{NS['xsd']}float")
            conf_elem.text = str(rel['confidence'])

def create_enhanced_knowledge_graph(json_file: str, bill_text_file: str, output_file: str):
    """Create enhanced knowledge graph from JSON extractions and bill text"""
    
    # Load original extractions
    with open(json_file, 'r') as f:
        original_data = json.load(f)
    
    # Load bill text for enhanced extraction
    with open(bill_text_file, 'r') as f:
        bill_text = f.read()
    
    # Extract enhanced entities and relationships
    enhanced_entities, enhanced_relationships = extract_enhanced_entities_and_relationships(bill_text)
    
    # Merge with original entities
    all_entities = {}
    for entity in original_data.get('entities', []):
        text = entity.get('text', '').strip()
        if text:
            all_entities[text] = entity
    
    # Add enhanced entities
    for text, entity_data in enhanced_entities.items():
        if text not in all_entities:
            all_entities[text] = entity_data
    
    # Merge relationships
    all_relationships = list(original_data.get('relations', []))
    all_relationships.extend(enhanced_relationships)
    
    # Create ontology
    root = ET.Element(f"{{{NS['rdf']}}}RDF", attrib={"xml:base": BASE_IRI})
    
    add_ontology_header(root, json_file)
    define_core_classes(root)
    define_properties(root)
    add_individuals_and_assertions(root, all_entities, all_relationships)
    
    # Write to file
    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ', level=0)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    # Print summary
    print(f"Enhanced Knowledge Graph Created: {output_file}")
    print(f"Entities: {len(all_entities)}")
    print(f"Relationships: {len(all_relationships)}")
    print(f"Classes: 20")
    print(f"Properties: 20+")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('Usage: python enhanced_knowledge_graph_generator.py <extractions.json> <bill_text.txt> <output.owl>')
        sys.exit(1)
    
    create_enhanced_knowledge_graph(sys.argv[1], sys.argv[2], sys.argv[3])
