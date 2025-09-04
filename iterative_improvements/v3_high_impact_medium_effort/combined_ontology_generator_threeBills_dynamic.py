#!/usr/bin/env python3
"""
Generate combined ontology from HB767, SB2182, and SB666 bills
Creates a comprehensive legislative knowledge graph ontology dynamically from JSON data
"""
import json
from pathlib import Path
from collections import defaultdict

def load_bill_data():
    """Load all three bills' extraction data"""
    bills_data = {}
    
    # Load HB767 data
    with open('enhanced_corenlp_extractions_v3_0_1.json', 'r', encoding='utf-8') as f:
        bills_data['HB767'] = json.load(f)
    
    # Load SB2182 data
    with open('sb2182_processing/enhanced_corenlp_extractions_sb2182_v3_0_1.json', 'r', encoding='utf-8') as f:
        bills_data['SB2182'] = json.load(f)
    
    # Load SB666 data
    with open('sb666_processing/enhanced_corenlp_extractions_sb666_v3_0_1.json', 'r', encoding='utf-8') as f:
        bills_data['SB666'] = json.load(f)
    
    return bills_data

def extract_entities_by_type(bills_data):
    """Extract and organize entities by type across all bills"""
    entities_by_type = defaultdict(list)
    
    for bill_name, data in bills_data.items():
        for entity in data.get('entities', []):
            entity_type = entity.get('type')
            if entity_type:
                entities_by_type[entity_type].append({
                    'text': entity.get('text', ''),
                    'confidence': entity.get('confidence', 0.0),
                    'context': entity.get('context', ''),
                    'source': bill_name,
                    'normalized': entity.get('normalized_ner', '')
                })
    
    return entities_by_type

def create_owl_entity_class(entity_type, comment=""):
    """Create OWL class definition for entity type"""
    class_name = entity_type.replace('_', '').title()
    return f'''    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#{class_name}">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>{comment}</rdfs:comment>
    </owl:Class>'''

def create_owl_individual(entity_text, entity_type, confidence, source, normalized=""):
    """Create OWL individual for entity"""
    # Clean text for URI
    clean_text = entity_text.replace(' ', '').replace('.', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '')
    individual_name = f"{entity_type}_{clean_text}_{source}"[:50]  # Limit length
    
    class_name = entity_type.replace('_', '').title()
    
    return f'''    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#{individual_name}">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#{class_name}"/>
        <hasText rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_text}</hasText>
        <hasConfidence rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{confidence}</hasConfidence>
        <hasSource rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{source}</hasSource>
    </owl:NamedIndividual>'''

def create_combined_ontology():
    """Create combined OWL ontology dynamically from bill data"""
    
    # Load data
    bills_data = load_bill_data()
    entities_by_type = extract_entities_by_type(bills_data)
    
    # Entity type descriptions
    type_descriptions = {
        'PROGRAM': 'Programs and initiatives',
        'AGENCY': 'Government agencies and departments',
        'GOAL': 'Goals and objectives',
        'REPORTING': 'Reporting requirements',
        'STATUTE': 'Statutory references',
        'PURPOSE': 'Purposes and intents',
        'LEGISLATIVE_BODY': 'Legislative bodies and chambers',
        'SESSION_IDENTIFIER': 'Legislative session identifiers',
        'LOCATION': 'Locations and places',
        'PERSON': 'People and individuals',
        'INTEREST_GROUP': 'Interest groups and stakeholders',
        'HEALTH_GOAL': 'Health-related goals',
        'LEGAL_SECTION': 'Legal sections and references',
        'POSITION': 'Positions and roles',
        'FUNDING': 'Funding and financial resources',
        'EDUCATIONAL_SPACE': 'Educational spaces and facilities',
        'PROFESSION': 'Occupational roles and professions',
        'ORGANIZATION': 'Organizations and institutions',
        'EDUCATION_TOPIC': 'Educational subjects and topics',
        'TRAINING_ACTION': 'Training activities and programs',
        'LEGISLATIVE_MEASURE': 'Legislative measures and resolutions',
        'AGE_STAT': 'Age-related statistics',
        'BILL': 'Legislative bills'
    }
    
    owl_content = '''<?xml version="1.0"?>
<rdf:RDF xmlns="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#"
     xml:base="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills"
     xmlns:owl="http://www.w3.org/2002/07/owl#"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
     xmlns:xml="http://www.w3.org/XML/1998/namespace"
     xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
     xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
    <owl:Ontology rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills">
        <rdfs:comment>Combined ontology for HB767 (Farm to School), SB2182 (School Gardens), and SB666 (UH Agriculture Education) bills</rdfs:comment>
        <rdfs:label>Combined Legislative Bills Ontology</rdfs:label>
    </owl:Ontology>
    
    <!-- Object Properties -->
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasPurpose">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Purpose"/>
        <rdfs:comment>Relates a program to its purposes</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasGoal">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Goal"/>
        <rdfs:comment>Relates a program to its goals</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasCoordinator">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Position"/>
        <rdfs:comment>Relates a program to its coordinator position</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasFunding">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Funding"/>
        <rdfs:comment>Relates a program to its funding</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#operatesAt">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Location"/>
        <rdfs:comment>Relates a program to its operating locations</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#serves">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Person"/>
        <rdfs:comment>Relates a program to the people it serves</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#managedBy">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Program"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Agency"/>
        <rdfs:comment>Relates a program to the agency that manages it</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#enactedBy">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeBody"/>
        <rdfs:comment>Relates a bill to the legislative body that enacted it</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#references">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegalSection"/>
        <rdfs:comment>Relates a bill to legal sections it references</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#partOfPackage">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage"/>
        <rdfs:comment>Relates a bill to a legislative package</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#referencesBill">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Relates a bill to another bill it references</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#amends">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Relates a bill to another bill it amends</rdfs:comment>
    </owl:ObjectProperty>
    
    <owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#supersedes">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:comment>Relates a bill to another bill it supersedes</rdfs:comment>
    </owl:ObjectProperty>
    
    <!-- Data Properties -->
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasConfidence">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
        <rdfs:comment>Confidence score for entity extraction</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasText">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Original text of the entity</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasSource">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Source bill for the entity</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasContext">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Context in which the entity appears</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasFullText">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Full text of the bill</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasBillYear">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Year of the bill</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasMeasureVersion">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Measure version of the bill (e.g., H.D. 1, S.D. 1)</rdfs:comment>
    </owl:DatatypeProperty>
    
    <owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#hasBillNumber">
        <rdfs:domain rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
        <rdfs:comment>Bill number (e.g., HB767, SB2182, SB666)</rdfs:comment>
    </owl:DatatypeProperty>
    
    <!-- Base Entity Class -->
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity">
        <rdfs:comment>Base class for all extracted entities</rdfs:comment>
    </owl:Class>
    
    <!-- Bill Classes -->
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legislative bills</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#BillPackage">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Package of related bills</rdfs:comment>
    </owl:Class>
    
    <owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#LegislativeReport">
        <rdfs:subClassOf rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Entity"/>
        <rdfs:comment>Legislative reports and documents</rdfs:comment>
    </owl:Class>
    
    <!-- Entity Classes (dynamically generated) -->'''
    
    # Add entity classes
    for entity_type in sorted(entities_by_type.keys()):
        if entity_type != 'BILL':  # Bill class already defined
            description = type_descriptions.get(entity_type, f"{entity_type} entities")
            owl_content += f"\n{create_owl_entity_class(entity_type, description)}"
    
    owl_content += "\n\n    <!-- Named Individuals -->"
    
    # Add bill individuals
    for bill_name, data in bills_data.items():
        bill_info = data.get('bill_info', {})
        bill_number = bill_info.get('bill_number', bill_name)
        session = bill_info.get('session', '')
        effective_date = bill_info.get('effective_date', '')
        bill_year = bill_info.get('bill_year', '')
        measure_versions = bill_info.get('measure_versions', [])
        
        owl_content += f'''
    <owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#{bill_name}">
        <rdf:type rdf:resource="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#Bill"/>
        <hasBillNumber rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{bill_number}</hasBillNumber>
        <hasSession rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{session}</hasSession>
        <hasEffectiveDate rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{effective_date}</hasEffectiveDate>
        <hasBillYear rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{bill_year}</hasBillYear>'''
        
        for version in measure_versions:
            owl_content += f'''
        <hasMeasureVersion rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{version}</hasMeasureVersion>'''
        
        owl_content += f'''
    </owl:NamedIndividual>'''
    
    # Add entity individuals (sample of each type)
    for entity_type, entities in entities_by_type.items():
        if entity_type == 'BILL':
            continue
            
        # Take up to 5 examples of each type
        sample_entities = entities[:5]
        for entity in sample_entities:
            owl_content += f"\n{create_owl_individual(entity['text'], entity_type, entity['confidence'], entity['source'], entity['normalized'])}"
    
    owl_content += "\n\n</rdf:RDF>"
    
    return owl_content

def main():
    """Generate combined ontology"""
    owl_content = create_combined_ontology()
    
    output_file = 'combined_legislative_bills_ontology_threeBills_dynamic.owl'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(owl_content)
    
    # Load data for statistics
    bills_data = load_bill_data()
    entities_by_type = extract_entities_by_type(bills_data)
    
    total_entities = sum(len(entities) for entities in entities_by_type.values())
    total_types = len(entities_by_type)
    
    print(f"Dynamic combined ontology created: {output_file}")
    print(f"Ontology includes:")
    print(f"- {total_types} entity types")
    print(f"- {total_entities} total entities")
    print(f"- 12 object properties")
    print(f"- 8 data properties")
    print(f"- Bill individuals: {', '.join(bills_data.keys())}")
    print(f"- Entity types: {', '.join(sorted(entities_by_type.keys()))}")
    
    # Show entity counts by type
    print("\nEntity counts by type:")
    for entity_type, entities in sorted(entities_by_type.items()):
        print(f"  {entity_type}: {len(entities)}")

if __name__ == '__main__':
    main()
