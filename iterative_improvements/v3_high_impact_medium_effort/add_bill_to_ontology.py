#!/usr/bin/env python3
"""
Add New Bill to Combined Ontology
Simple script to add a new bill to the existing ontology structure
"""
import json
import sys
from pathlib import Path

def add_bill_to_config(bill_id, json_file, title, package="DefaultPackage"):
    """Add a new bill to the BILLS_CONFIG in the enhanced generator"""
    
    # Read the current enhanced generator
    with open('combined_ontology_generator_enhanced.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the BILLS_CONFIG section
    start_marker = "BILLS_CONFIG = {"
    end_marker = "}"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("❌ Could not find BILLS_CONFIG in enhanced generator")
        return False
    
    # Find the end of the config
    brace_count = 0
    end_idx = start_idx
    for i, char in enumerate(content[start_idx:], start_idx):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    
    # Extract current config
    config_section = content[start_idx:end_idx]
    
    # Add new bill
    new_bill_entry = f'''    '{bill_id}': {{
        'file': '{json_file}',
        'title': '{title}',
        'package': '{package}'
    }},'''
    
    # Insert before the closing brace
    new_config = config_section[:-1] + new_bill_entry + '\n}'
    
    # Replace in content
    new_content = content[:start_idx] + new_config + content[end_idx:]
    
    # Write back
    with open('combined_ontology_generator_enhanced.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Added {bill_id} to BILLS_CONFIG")
    return True

def validate_bill_data(json_file):
    """Validate that the JSON file has the expected structure"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_keys = ['bill_info', 'entities']
        for key in required_keys:
            if key not in data:
                print(f"❌ Missing required key '{key}' in {json_file}")
                return False
        
        print(f"✅ Validated {json_file}")
        return True
        
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {json_file}: {e}")
        return False

def main():
    """Add a new bill to the ontology configuration"""
    if len(sys.argv) != 5:
        print("Usage: python add_bill_to_ontology.py <bill_id> <json_file> <title> <package>")
        print("Example: python add_bill_to_ontology.py HB1234 'hb1234_data.json' 'New Bill Title' 'NewPackage'")
        sys.exit(1)
    
    bill_id = sys.argv[1]
    json_file = sys.argv[2]
    title = sys.argv[3]
    package = sys.argv[4]
    
    print(f"🔧 Adding {bill_id} to ontology configuration...")
    print(f"   File: {json_file}")
    print(f"   Title: {title}")
    print(f"   Package: {package}")
    
    # Validate the JSON file
    if not validate_bill_data(json_file):
        sys.exit(1)
    
    # Add to config
    if add_bill_to_config(bill_id, json_file, title, package):
        print(f"\n✅ Successfully added {bill_id}!")
        print(f"   Run 'python combined_ontology_generator_enhanced.py' to regenerate the ontology")
    else:
        print(f"❌ Failed to add {bill_id}")
        sys.exit(1)

if __name__ == '__main__':
    main()
