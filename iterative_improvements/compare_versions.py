#!/usr/bin/env python3
"""
Enhanced Version Comparison Script for Entity & Relation Extraction

This script compares the output files from different versions of the extraction system
to provide detailed analysis of differences, new features, and quality improvements.
"""

import json
import os
import sys
from typing import Dict, List, Tuple, Set
from pathlib import Path

def load_extraction_results(filepath: str) -> Dict:
    """Load extraction results from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {filepath}")
        return None

def analyze_entities(entities: List[Dict]) -> Dict:
    """Analyze entity extraction results"""
    if not entities:
        return {"count": 0, "types": set(), "avg_confidence": 0.0, "texts": set()}
    
    entity_types = set()
    entity_texts = set()
    total_confidence = 0.0
    confidence_count = 0
    
    for entity in entities:
        if 'type' in entity:
            entity_types.add(entity['type'])
        
        if 'text' in entity:
            entity_texts.add(entity['text'].lower())
        
        if 'confidence' in entity and entity['confidence'] is not None:
            total_confidence += entity['confidence']
            confidence_count += 1
    
    avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0
    
    return {
        "count": len(entities),
        "types": list(entity_types),
        "type_count": len(entity_types),
        "texts": list(entity_texts),
        "text_count": len(entity_texts),
        "avg_confidence": round(avg_confidence, 3)
    }

def analyze_relations(relations: List[Dict]) -> Dict:
    """Analyze relation extraction results"""
    if not relations:
        return {"count": 0, "types": set(), "sources": set(), "avg_confidence": 0.0, "patterns": set()}
    
    relation_types = set()
    sources = set()
    patterns = set()
    total_confidence = 0.0
    confidence_count = 0
    
    for relation in relations:
        if 'relation_type' in relation and relation['relation_type']:
            relation_types.add(relation['relation_type'])
        
        if 'source' in relation and relation['source']:
            sources.add(relation['source'])
        
        # Create pattern identifier for comparison
        if all(key in relation for key in ['subject', 'predicate', 'object']):
            pattern = f"{relation['subject']} {relation['predicate']} {relation['object']}".lower()
            patterns.add(pattern)
        
        if 'confidence' in relation and relation['confidence'] is not None:
            total_confidence += relation['confidence']
            confidence_count += 1
    
    avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0
    
    return {
        "count": len(relations),
        "types": list(relation_types),
        "type_count": len(relation_types),
        "sources": list(sources),
        "source_count": len(sources),
        "patterns": list(patterns),
        "pattern_count": len(patterns),
        "avg_confidence": round(avg_confidence, 3)
    }

def calculate_quality_score(entity_analysis: Dict, relation_analysis: Dict) -> float:
    """Calculate overall quality score (0-10 scale)"""
    # Base score from entity and relation counts
    entity_score = min(5.0, entity_analysis["count"] / 20.0)  # 100 entities = 5 points
    relation_score = min(3.0, relation_analysis["count"] / 10.0)  # 30 relations = 3 points
    
    # Bonus for variety and confidence
    type_bonus = min(1.0, (entity_analysis["type_count"] + relation_analysis["type_count"]) / 20.0)
    confidence_bonus = min(1.0, (entity_analysis["avg_confidence"] + relation_analysis["avg_confidence"]) / 2.0)
    
    total_score = entity_score + relation_score + type_bonus + confidence_bonus
    return round(min(10.0, total_score), 1)

def analyze_differences(v1_analysis: Dict, v2_analysis: Dict, analysis_type: str) -> Dict:
    """Analyze differences between two versions for entities or relations"""
    differences = {}
    
    # Count differences
    count_diff = v2_analysis["count"] - v1_analysis["count"]
    type_diff = v2_analysis["type_count"] - v1_analysis["type_count"]
    
    # New types - convert lists to sets for set operations
    v1_types = set(v1_analysis["types"])
    v2_types = set(v2_analysis["types"])
    new_types = v2_types - v1_types
    
    # New texts/patterns - convert lists to sets for set operations
    if analysis_type == "entities":
        v1_items = set(v1_analysis["texts"])
        v2_items = set(v2_analysis["texts"])
        new_items = v2_items - v1_items
        item_key = "texts"
    else:  # relations
        v1_items = set(v1_analysis["patterns"])
        v2_items = set(v2_analysis["patterns"])
        new_items = v2_items - v1_items
        item_key = "patterns"
    
    # Confidence improvement
    confidence_diff = v2_analysis["avg_confidence"] - v1_analysis["avg_confidence"]
    
    differences = {
        "count_difference": count_diff,
        "count_percentage": round((count_diff / v1_analysis["count"]) * 100, 1) if v1_analysis["count"] > 0 else 0,
        "type_difference": type_diff,
        "new_types": list(new_types),
        "new_items": list(new_items)[:10],  # Limit to first 10 for display
        "confidence_difference": round(confidence_diff, 3),
        "improvement_summary": f"+{count_diff} {analysis_type} (+{type_diff} new types)"
    }
    
    return differences

def compare_versions(v1_file: str, v2_file: str) -> Dict:
    """Compare two versions and calculate detailed differences"""
    print(f"🔍 Comparing versions...")
    print(f"v1: {v1_file}")
    print(f"v2: {v2_file}")
    print()
    
    # Load results
    v1_results = load_extraction_results(v1_file)
    v2_results = load_extraction_results(v2_file)
    
    if not v1_results or not v2_results:
        return None
    
    # Analyze entities
    v1_entities = v1_results.get('entities', [])
    v2_entities = v2_results.get('entities', [])
    
    v1_entity_analysis = analyze_entities(v1_entities)
    v2_entity_analysis = analyze_entities(v2_entities)
    
    # Analyze relations
    v1_relations = v1_results.get('relations', [])
    v2_relations = v2_results.get('relations', [])
    
    v1_relation_analysis = analyze_relations(v1_relations)
    v2_relation_analysis = analyze_relations(v2_relations)
    
    # Calculate quality scores
    v1_quality = calculate_quality_score(v1_entity_analysis, v1_relation_analysis)
    v2_quality = calculate_quality_score(v2_entity_analysis, v2_relation_analysis)
    
    # Analyze differences
    entity_differences = analyze_differences(v1_entity_analysis, v2_entity_analysis, "entities")
    relation_differences = analyze_differences(v1_relation_analysis, v2_relation_analysis, "relations")
    
    # Calculate overall improvements
    quality_improvement = v2_quality - v1_quality
    
    # Print detailed comparison
    print("📊 DETAILED VERSION COMPARISON RESULTS")
    print("=" * 60)
    
    print(f"\n🏷️  ENTITY EXTRACTION COMPARISON:")
    print(f"  v1: {v1_entity_analysis['count']} entities, {v1_entity_analysis['type_count']} types")
    print(f"  v2: {v2_entity_analysis['count']} entities, {v2_entity_analysis['type_count']} types")
    print(f"  📈 Change: {entity_differences['improvement_summary']}")
    
    if entity_differences['new_types']:
        print(f"  ✨ New entity types: {', '.join(entity_differences['new_types'])}")
    
    if entity_differences['new_items']:
        print(f"  🆕 New entities (first 10): {', '.join(entity_differences['new_items'])}")
    
    print(f"  📊 Confidence: v1: {v1_entity_analysis['avg_confidence']}, v2: {v2_entity_analysis['avg_confidence']} ({entity_differences['confidence_difference']:+})")
    
    print(f"\n🔗 RELATION EXTRACTION COMPARISON:")
    print(f"  v1: {v1_relation_analysis['count']} relations, {v1_relation_analysis['type_count']} types")
    print(f"  v2: {v2_relation_analysis['count']} relations, {v2_relation_analysis['type_count']} types")
    print(f"  📈 Change: {relation_differences['improvement_summary']}")
    
    if relation_differences['new_types']:
        print(f"  ✨ New relation types: {', '.join(relation_differences['new_types'])}")
    
    if relation_differences['new_items']:
        print(f"  🆕 New relations (first 10): {', '.join(relation_differences['new_items'])}")
    
    print(f"  📊 Confidence: v1: {v1_relation_analysis['avg_confidence']}, v2: {v2_relation_analysis['avg_confidence']} ({relation_differences['confidence_difference']:+})")
    
    # Show new sources if any
    v1_sources = set(v1_relation_analysis['sources'])
    v2_sources = set(v2_relation_analysis['sources'])
    new_sources = v2_sources - v1_sources
    if new_sources:
        print(f"  🔄 New extraction sources: {', '.join(new_sources)}")
    
    print(f"\n🎯 OVERALL QUALITY COMPARISON:")
    print(f"  v1: {v1_quality}/10")
    print(f"  v2: {v2_quality}/10")
    print(f"  📈 Improvement: +{quality_improvement} points ({quality_improvement/v1_quality*100:.1f}%)")
    
    print(f"\n🔍 FEATURE EXTRACTION ANALYSIS:")
    
    # Analyze what new features were extracted
    print(f"  📊 Entity Coverage:")
    print(f"    - v1: {v1_entity_analysis['count']} entities across {v1_entity_analysis['type_count']} types")
    print(f"    - v2: {v2_entity_analysis['count']} entities across {v2_entity_analysis['type_count']} types")
    print(f"    - New coverage: +{entity_differences['count_difference']} entities (+{entity_differences['count_percentage']}%)")
    
    print(f"  📊 Relation Coverage:")
    print(f"    - v1: {v1_relation_analysis['count']} relations across {v1_relation_analysis['type_count']} types")
    print(f"    - v2: {v2_relation_analysis['count']} relations across {v2_relation_analysis['type_count']} types")
    print(f"    - New coverage: +{relation_differences['count_difference']} relations (+{relation_differences['count_percentage']}%)")
    
    # Highlight specific improvements
    print(f"\n🚀 KEY IMPROVEMENTS IN v2:")
    
    if entity_differences['new_types']:
        print(f"  ✅ New entity types: {', '.join(entity_differences['new_types'])}")
    
    if relation_differences['new_types']:
        print(f"  ✅ New relation types: {', '.join(relation_differences['new_types'])}")
    
    if new_sources:
        print(f"  ✅ New extraction methods: {', '.join(new_sources)}")
    
    if quality_improvement > 0:
        print(f"  ✅ Overall quality improvement: +{quality_improvement} points")
    
    # Return comprehensive comparison data
    return {
        "v1": {
            "entities": v1_entity_analysis,
            "relations": v1_relation_analysis,
            "quality": v1_quality
        },
        "v2": {
            "entities": v2_entity_analysis,
            "relations": v2_relation_analysis,
            "quality": v2_quality
        },
        "differences": {
            "entities": entity_differences,
            "relations": relation_differences,
            "quality": quality_improvement
        },
        "improvements": {
            "entity_count": entity_differences['count_difference'],
            "relation_count": relation_differences['count_difference'],
            "entity_types": len(entity_differences['new_types']),
            "relation_types": len(relation_differences['new_types']),
            "quality_points": quality_improvement
        }
    }

def main():
    """Main comparison function"""
    print("🔄 Enhanced Entity & Relation Extraction Version Comparison")
    print("=" * 70)
    
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Usage: python compare_versions.py <v1_file> <v2_file>")
        print("Example: python compare_versions.py corenlp_extractions.json enhanced_corenlp_extractions_v2.json")
        print("\nThis script will analyze:")
        print("  - Entity count and type differences")
        print("  - Relation count and type differences")
        print("  - New features extracted")
        print("  - Quality score improvements")
        return
    
    v1_file = sys.argv[1]
    v2_file = sys.argv[2]
    
    # Check if files exist
    if not os.path.exists(v1_file):
        print(f"❌ v1 file not found: {v1_file}")
        return
    
    if not os.path.exists(v2_file):
        print(f"❌ v2 file not found: {v2_file}")
        return
    
    # Run enhanced comparison
    comparison = compare_versions(v1_file, v2_file)
    
    if comparison:
        print(f"\n✅ Enhanced comparison completed successfully!")
        
        # Summary of key improvements
        improvements = comparison['improvements']
        print(f"\n📈 SUMMARY OF IMPROVEMENTS:")
        print(f"  🏷️  Entities: +{improvements['entity_count']} (+{improvements['entity_types']} new types)")
        print(f"  🔗 Relations: +{improvements['relation_count']} (+{improvements['relation_types']} new types)")
        print(f"  🎯 Quality: +{improvements['quality_points']} points")
        
        # Save detailed comparison results
        output_file = "enhanced_version_comparison_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Detailed comparison results saved to: {output_file}")
        
        # Save summary for easy reference
        summary_file = "comparison_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("VERSION COMPARISON SUMMARY\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"v1 Quality Score: {comparison['v1']['quality']}/10\n")
            f.write(f"v2 Quality Score: {comparison['v2']['quality']}/10\n")
            f.write(f"Improvement: +{improvements['quality_points']} points\n\n")
            f.write(f"Entity Improvements: +{improvements['entity_count']} entities, +{improvements['entity_types']} types\n")
            f.write(f"Relation Improvements: +{improvements['relation_count']} relations, +{improvements['relation_types']} types\n")
        print(f"📝 Summary saved to: {summary_file}")
        
    else:
        print("❌ Comparison failed")

if __name__ == "__main__":
    main()
