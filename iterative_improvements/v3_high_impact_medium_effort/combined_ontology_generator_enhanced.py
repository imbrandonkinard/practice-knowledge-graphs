#!/usr/bin/env python3
"""
Enhanced Combined Ontology Generator for Legislative Bills
Supports dynamic addition of new bills and provides detailed statistics
"""
import json
from pathlib import Path
from collections import defaultdict

# Configuration for bills to include
BILLS_CONFIG = {
    'HB767': {
        'file': 'enhanced_corenlp_extractions_v3_0_1.json',
        'title': 'Farm to School Program',
        'package': 'HealthySchools2021Package'
    },
    'SB2182': {
        'file': 'sb2182_processing/enhanced_corenlp_extractions_sb2182_v3_0_1.json',
        'title': 'School Gardens',
        'package': 'HealthySchools2021Package'
    },
    'SB666': {
        'file': 'sb666_processing/enhanced_corenlp_extractions_sb666_v3_0_1.json',
        'title': 'UH Agriculture Education',
        'package': 'AgricultureEducationPackage'
    }
}

def load_bill_data():
    """Load all configured bills' extraction data"""
    bills_data = {}
    
    for bill_id, config in BILLS_CONFIG.items():
        try:
            with open(config['file'], 'r', encoding='utf-8') as f:
                bills_data[bill_id] = json.load(f)
            print(f"✓ Loaded {bill_id}: {config['title']}")
        except FileNotFoundError:
            print(f"⚠ Warning: Could not load {bill_id} from {config['file']}")
        except Exception as e:
            print(f"✗ Error loading {bill_id}: {e}")
    
    return bills_data

def analyze_ontology_content(owl_content):
    """Analyze the generated ontology content and return statistics"""
    stats = {
        'entity_classes': owl_content.count('<owl:Class rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#'),
        'object_properties': owl_content.count('<owl:ObjectProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#'),
        'data_properties': owl_content.count('<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#'),
        'named_individuals': owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#'),
        'bills': 0,
        'packages': 0,
        'relationships': 0
    }
    
    # Count bills
    stats['bills'] += owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#HB')
    stats['bills'] += owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#SB')
    
    # Count packages
    stats['packages'] = owl_content.count('<owl:NamedIndividual rdf:about="http://www.semanticweb.org/legislative/ontologies/2025/combined-bills#.*Package')
    
    # Count relationships (axioms)
    stats['relationships'] = owl_content.count('<owl:Axiom>')
    
    return stats

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

def generate_ontology_statistics(bills_data, entities_by_type, stats):
    """Generate detailed statistics about the ontology"""
    print(f"\n📊 ONTOLOGY STATISTICS")
    print(f"{'='*50}")
    print(f"📁 Structure:")
    print(f"  • Entity Classes: {stats['entity_classes']}")
    print(f"  • Object Properties: {stats['object_properties']}")
    print(f"  • Data Properties: {stats['data_properties']}")
    print(f"  • Named Individuals: {stats['named_individuals']}")
    print(f"  • Relationships: {stats['relationships']}")
    
    print(f"\n📜 Bills Included:")
    for bill_id, config in BILLS_CONFIG.items():
        if bill_id in bills_data:
            bill_info = bills_data[bill_id].get('bill_info', {})
            print(f"  • {bill_id}: {config['title']}")
            print(f"    - Session: {bill_info.get('session', 'N/A')}")
            print(f"    - Effective: {bill_info.get('effective_date', 'N/A')}")
            print(f"    - Package: {config['package']}")
    
    print(f"\n🏷️  Entity Types ({len(entities_by_type)} types):")
    for entity_type, entities in sorted(entities_by_type.items()):
        print(f"  • {entity_type}: {len(entities)} entities")
    
    print(f"\n📦 Legislative Packages:")
    print(f"  • Healthy Schools 2021 Package (HB767, SB2182)")
    print(f"  • Agriculture Education 2025 Package (SB666)")
    
    print(f"\n🔗 Key Relationships:")
    print(f"  • Bill-to-Entity references")
    print(f"  • Entity hierarchical relationships")
    print(f"  • Cross-bill connections")
    print(f"  • Package memberships")

def main():
    """Generate enhanced combined ontology with detailed statistics"""
    print("🚀 Enhanced Combined Ontology Generator")
    print("="*50)
    
    # Load bill data
    print("\n📂 Loading bill data...")
    bills_data = load_bill_data()
    
    if not bills_data:
        print("❌ No bill data loaded. Exiting.")
        return
    
    # Extract entities
    print("\n🔍 Analyzing entities...")
    entities_by_type = extract_entities_by_type(bills_data)
    
    # Import and use the existing ontology generator
    from combined_ontology_generator_threeBills import create_combined_ontology
    owl_content = create_combined_ontology()
    
    # Analyze content
    stats = analyze_ontology_content(owl_content)
    
    # Write output
    output_file = 'combined_legislative_bills_ontology_threeBills.owl'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(owl_content)
    
    print(f"\n✅ Combined ontology created: {output_file}")
    
    # Generate detailed statistics
    generate_ontology_statistics(bills_data, entities_by_type, stats)
    
    print(f"\n🎯 SUMMARY")
    print(f"{'='*50}")
    print(f"Successfully generated ontology with {stats['bills']} bills, {stats['entity_classes']} classes, and {stats['relationships']} relationships.")
    print(f"Ready for use in knowledge graph applications!")

if __name__ == '__main__':
    main()
