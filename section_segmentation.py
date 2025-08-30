import re

def segment_bill(text):
    # Remove excessive whitespace
    text = re.sub(r'\n+', '\n', text).strip()

    # Extract Measure Title (after 'RELATING TO ...')
    measure_title_match = re.search(r'RELATING TO (.+?)\.', text, re.IGNORECASE)
    measure_title = "RELATING TO " + measure_title_match.group(1).strip() if measure_title_match else None

    # Extract Report Title and Description from labeled fields
    report_title_match = re.search(r'Report Title:\s*(.+)', text)
    report_title = report_title_match.group(1).strip() if report_title_match else None

    description_match = re.search(r'Description:\s*(.+)', text)
    description = description_match.group(1).strip() if description_match else None

    # Segment numbered sections
    section_headers = [m.start() for m in re.finditer(r'SECTION\s+\d+\.', text)]
    sections = []
    for i, start in enumerate(section_headers):
        section_num_match = re.search(r'SECTION\s+(\d+)\.', text[start:])
        section_num = int(section_num_match.group(1)) if section_num_match else i + 1
        end = section_headers[i + 1] if i + 1 < len(section_headers) else len(text)
        section_text = text[start:end].strip()
        sections.append({"SectionNumber": section_num, "Content": section_text})

    # Build output dictionary
    bill_dict = {
        "MeasureTitle": measure_title,
        "ReportTitle": report_title,
        "Description": description,
        "Companion": None,
        "Package": None,
        "CurrentReferral": None,
        "Introducers": None,
        "Act": None,
        "Statuses": None,
        "Sections": sections,
    }

    return bill_dict

# Example usage
if __name__ == "__main__":
    with open("bill.txt", "r", encoding="utf-8") as f:
        bill_text = f.read()
    segmented = segment_bill(bill_text)
    import json
    print(json.dumps(segmented, indent=2))
