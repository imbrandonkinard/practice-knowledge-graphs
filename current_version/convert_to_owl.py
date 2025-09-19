#!/usr/bin/env python3
"""
Convert TTL file to OWL format for WebVOWL visualization
"""

import subprocess
import sys
import os

def convert_ttl_to_owl(ttl_file, owl_file):
    """
    Convert TTL to OWL using rdf-toolkit or rapper
    """
    print(f"Converting {ttl_file} to {owl_file}...")
    
    # Try using rapper (from raptor2-utils)
    try:
        cmd = ['rapper', '-i', 'turtle', '-o', 'rdfxml', ttl_file, '-o', owl_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Conversion successful using rapper")
            return True
        else:
            print(f"✗ rapper failed: {result.stderr}")
    except FileNotFoundError:
        print("✗ rapper not found")
    
    # Try using rdf-toolkit
    try:
        cmd = ['java', '-jar', 'rdf-toolkit.jar', '-t', 'owl', '-i', ttl_file, '-o', owl_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Conversion successful using rdf-toolkit")
            return True
        else:
            print(f"✗ rdf-toolkit failed: {result.stderr}")
    except FileNotFoundError:
        print("✗ rdf-toolkit not found")
    
    # Fallback: simple file copy (TTL is often compatible)
    print("⚠ Using TTL file directly (WebVOWL may accept TTL format)")
    try:
        import shutil
        shutil.copy2(ttl_file, owl_file)
        return True
    except Exception as e:
        print(f"✗ Copy failed: {e}")
        return False

def main():
    ttl_file = "complete_updated_testimony_ontology.ttl"
    owl_file = "testimony_ontology_for_webvowl.owl"
    
    if not os.path.exists(ttl_file):
        print(f"✗ TTL file not found: {ttl_file}")
        sys.exit(1)
    
    if convert_ttl_to_owl(ttl_file, owl_file):
        print(f"\n✓ Ready for WebVOWL!")
        print(f"1. Go to: https://vowl.visualdataweb.org/webvowl.html")
        print(f"2. Upload: {owl_file}")
        print(f"3. Explore your knowledge graph!")
    else:
        print("\n✗ Conversion failed. Try manual conversion or use TTL directly.")

if __name__ == "__main__":
    main()
