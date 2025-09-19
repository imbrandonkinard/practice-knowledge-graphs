#!/usr/bin/env python3
"""
Testimony Data Extractor for Knowledge Graph

Extracts structured data from legislative testimony PDFs in the format:
Bill | Version | Testifier | Organization/Individual | Position | Summary
"""

import PyPDF2
import re
import json
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class TestimonyRecord:
    bill: str
    version: str
    testifier: str
    organization: str
    position: str  # Support/Oppose/Comments
    summary: str

class TestimonyExtractor:
    """Extract testimony data from PDF files"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.records = []
        
    def extract_text_from_pdf(self) -> str:
        """Extract all text from PDF file"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
    
    def extract_bill_info(self, text: str) -> tuple:
        """Extract bill number and version from text"""
        # Look for bill patterns like SB1548, HB1234, etc.
        bill_pattern = r'(S|H)B\s*(\d{4})'
        bill_match = re.search(bill_pattern, text, re.IGNORECASE)
        
        if bill_match:
            bill_type = bill_match.group(1)
            bill_number = bill_match.group(2)
            bill = f"{bill_type}B {bill_number}"
        else:
            bill = "Unknown"
        
        # Look for version patterns
        version_pattern = r'(SD\d+|HD\d+|CD\d+|SD\d+HD\d+CD\d+)'
        version_match = re.search(version_pattern, text, re.IGNORECASE)
        version = version_match.group(1) if version_match else "Original"
        
        return bill, version
    
    def extract_testimony_records(self, text: str) -> List[TestimonyRecord]:
        """Extract individual testimony records from text"""
        records = []
        
        # Extract bill info
        bill, version = self.extract_bill_info(text)
        
        # Split text into sections - look for common testimony patterns
        # This is a simplified approach - may need refinement based on actual PDF structure
        
        # Look for testimony sections
        testimony_sections = self._split_into_testimonies(text)
        
        for section in testimony_sections:
            record = self._parse_testimony_section(section, bill, version)
            if record:
                records.append(record)
        
        return records
    
    def _split_into_testimonies(self, text: str) -> List[str]:
        """Split text into individual testimony sections"""
        # Look for common patterns that indicate new testimonies
        # This is a heuristic approach - may need adjustment
        
        # Split on common testimony indicators
        split_patterns = [
            r'\n\s*Testimony\s+of\s+',
            r'\n\s*Submitted\s+by\s+',
            r'\n\s*From:\s+',
            r'\n\s*Organization:\s+',
            r'\n\s*Position:\s+',
            r'\n\s*Comments:\s+',
            r'\n\s*Support:\s+',
            r'\n\s*Oppose:\s+'
        ]
        
        sections = [text]  # Start with full text
        
        for pattern in split_patterns:
            new_sections = []
            for section in sections:
                parts = re.split(pattern, section, flags=re.IGNORECASE)
                new_sections.extend(parts)
            sections = new_sections
        
        # Filter out very short sections
        return [s.strip() for s in sections if len(s.strip()) > 100]
    
    def _parse_testimony_section(self, section: str, bill: str, version: str) -> Optional[TestimonyRecord]:
        """Parse a single testimony section"""
        if len(section.strip()) < 50:
            return None
        
        # Extract testifier name (look for common patterns)
        testifier = self._extract_testifier_name(section)
        
        # Extract organization
        organization = self._extract_organization(section)
        
        # Determine position
        position = self._extract_position(section)
        
        # Extract summary (first few sentences or key content)
        summary = self._extract_summary(section)
        
        if not testifier and not organization:
            return None
        
        return TestimonyRecord(
            bill=bill,
            version=version,
            testifier=testifier or "Unknown",
            organization=organization or "Individual",
            position=position,
            summary=summary
        )
    
    def _extract_testifier_name(self, text: str) -> str:
        """Extract testifier name from text"""
        # Look for common name patterns
        name_patterns = [
            r'Testimony\s+of\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Submitted\s+by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'From:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Name:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'Testifier:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_organization(self, text: str) -> str:
        """Extract organization from text"""
        # Look for organization patterns
        org_patterns = [
            r'Organization:\s*([^\n]+)',
            r'From:\s*([^\n]+)',
            r'Representing:\s*([^\n]+)',
            r'Department\s+of\s+([^\n]+)',
            r'University\s+of\s+([^\n]+)',
            r'Association\s+of\s+([^\n]+)',
            r'Commission\s+of\s+([^\n]+)',
            r'Board\s+of\s+([^\n]+)'
        ]
        
        for pattern in org_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_position(self, text: str) -> str:
        """Extract position (Support/Oppose/Comments) from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['support', 'favor', 'endorse', 'recommend']):
            return "Support"
        elif any(word in text_lower for word in ['oppose', 'against', 'object', 'concern']):
            return "Oppose"
        else:
            return "Comments"
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary from text"""
        # Take first few sentences or key content
        sentences = re.split(r'[.!?]+', text)
        summary_sentences = []
        
        for sentence in sentences[:3]:  # First 3 sentences
            sentence = sentence.strip()
            if len(sentence) > 20:  # Meaningful length
                summary_sentences.append(sentence)
        
        summary = '. '.join(summary_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary[:500]  # Limit length
    
    def extract_all(self) -> List[TestimonyRecord]:
        """Extract all testimony records from PDF"""
        print(f"Extracting testimony data from: {self.pdf_path}")
        
        text = self.extract_text_from_pdf()
        if not text:
            print("No text extracted from PDF")
            return []
        
        print(f"Extracted {len(text)} characters from PDF")
        
        records = self.extract_testimony_records(text)
        print(f"Found {len(records)} testimony records")
        
        return records
    
    def save_to_csv(self, output_file: str):
        """Save records to CSV file"""
        import csv
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Bill', 'Version', 'Testifier', 'Organization/Individual', 'Position', 'Summary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in self.records:
                writer.writerow({
                    'Bill': record.bill,
                    'Version': record.version,
                    'Testifier': record.testifier,
                    'Organization/Individual': record.organization,
                    'Position': record.position,
                    'Summary': record.summary
                })
        
        print(f"Saved {len(self.records)} records to {output_file}")
    
    def save_to_json(self, output_file: str):
        """Save records to JSON file"""
        data = []
        for record in self.records:
            data.append({
                'bill': record.bill,
                'version': record.version,
                'testifier': record.testifier,
                'organization': record.organization,
                'position': record.position,
                'summary': record.summary
            })
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.records)} records to {output_file}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python testimony_extractor.py <pdf_file>")
        print("Example: python testimony_extractor.py SB1548_TESTIMONY_EDU_02-07-25_.PDF.pdf")
        return
    
    pdf_file = sys.argv[1]
    
    # Extract testimony data
    extractor = TestimonyExtractor(pdf_file)
    records = extractor.extract_all()
    extractor.records = records
    
    if not records:
        print("No testimony records found")
        return
    
    # Print summary
    print(f"\n📊 EXTRACTION SUMMARY")
    print(f"=" * 50)
    print(f"Total Records: {len(records)}")
    print(f"Bill: {records[0].bill if records else 'Unknown'}")
    print(f"Version: {records[0].version if records else 'Unknown'}")
    
    # Count positions
    positions = {}
    for record in records:
        positions[record.position] = positions.get(record.position, 0) + 1
    
    print(f"\nPosition Breakdown:")
    for pos, count in positions.items():
        print(f"  {pos}: {count}")
    
    # Save results
    base_name = pdf_file.replace('.pdf', '').replace('.PDF', '')
    csv_file = f"{base_name}_testimony_data.csv"
    json_file = f"{base_name}_testimony_data.json"
    
    extractor.save_to_csv(csv_file)
    extractor.save_to_json(json_file)
    
    # Print first few records as preview
    print(f"\n📋 SAMPLE RECORDS:")
    print(f"=" * 50)
    for i, record in enumerate(records[:3]):
        print(f"\nRecord {i+1}:")
        print(f"  Testifier: {record.testifier}")
        print(f"  Organization: {record.organization}")
        print(f"  Position: {record.position}")
        print(f"  Summary: {record.summary[:100]}...")

if __name__ == "__main__":
    main()
