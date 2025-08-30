#!/usr/bin/env python3
"""
Compare the extracted plain text with the ground truth bill.txt
"""

def compare_texts(extracted_file, ground_truth_file):
    """Compare two text files and show differences"""
    
    with open(extracted_file, 'r', encoding='utf-8') as f:
        extracted = f.read()
    
    with open(ground_truth_file, 'r', encoding='utf-8') as f:
        ground_truth = f.read()
    
    print("=" * 60)
    print("COMPARISON: Extracted vs Ground Truth")
    print("=" * 60)
    
    # Basic statistics
    print(f"\nExtracted text length: {len(extracted)} characters")
    print(f"Ground truth length: {len(ground_truth)} characters")
    print(f"Length difference: {len(extracted) - len(ground_truth)} characters")
    
    # Line count comparison
    extracted_lines = [line.strip() for line in extracted.split('\n') if line.strip()]
    ground_truth_lines = [line.strip() for line in ground_truth.split('\n') if line.strip()]
    
    print(f"\nExtracted text lines: {len(extracted_lines)}")
    print(f"Ground truth lines: {len(ground_truth_lines)}")
    print(f"Line difference: {len(extracted_lines) - len(ground_truth_lines)} lines")
    
    # Show first few lines of each
    print("\n" + "=" * 30)
    print("FIRST 10 LINES - EXTRACTED:")
    print("=" * 30)
    for i, line in enumerate(extracted_lines[:10]):
        print(f"{i+1:2d}: {line}")
    
    print("\n" + "=" * 30)
    print("FIRST 10 LINES - GROUND TRUTH:")
    print("=" * 30)
    for i, line in enumerate(ground_truth_lines[:10]):
        print(f"{i+1:2d}: {line}")
    
    # Check for missing content
    print("\n" + "=" * 30)
    print("CONTENT ANALYSIS:")
    print("=" * 30)
    
    # Check if key sections are present
    key_sections = [
        "HOUSE OF REPRESENTATIVES",
        "H.B. NO. 767", 
        "SECTION 1",
        "SECTION 2",
        "SECTION 3",
        "SECTION 4",
        "SECTION 5",
        "Report Title:",
        "Description:"
    ]
    
    for section in key_sections:
        in_extracted = section in extracted
        in_ground_truth = section in ground_truth
        status = "✓" if in_extracted else "✗"
        status_gt = "✓" if in_ground_truth else "✗"
        print(f"{section:25} | Extracted: {status} | Ground Truth: {status_gt}")

if __name__ == "__main__":
    compare_texts("extracted_bill.txt", "bill.txt")
