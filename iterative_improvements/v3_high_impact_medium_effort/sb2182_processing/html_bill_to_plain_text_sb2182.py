from bs4 import BeautifulSoup
import re
import sys

def html_bill_to_plain_text(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get all text content, preserving structure
    lines = []
    
    # Process specific sections in order
    # Header section - combine related elements
    header_elements = []
    header_tags = soup.find_all(['p', 'td'], class_=['ChamberHeading', 'MeasureNumberHeading'])
    for tag in header_tags:
        text = tag.get_text(strip=True)
        if text and text not in ['', '&nbsp;', '<o:p></o:p>']:
            header_elements.append(text)
    
    # Format header properly - adapted for Senate bill format
    if len(header_elements) >= 6:
        lines.append(header_elements[0])  # THE SENATE
        lines.append(f"{header_elements[1]} {header_elements[2]}")  # S.B. NO. 2182
        lines.append(header_elements[3])  # THIRTY-FIRST LEGISLATURE, 2022
        lines.append(header_elements[4])  # S.D. 1
        lines.append(header_elements[5])  # STATE OF HAWAII
        lines.append(header_elements[6])  # H.D. 1
        lines.append(header_elements[7])  # C.D. 1
    
    # Add bill title and enactment clause
    title_tag = soup.find('p', class_='MeasureTitle')
    if title_tag:
        lines.append(title_tag.get_text(strip=True))
    
    enactment_tag = soup.find('p', class_='BEITENACTED')
    if enactment_tag:
        lines.append(enactment_tag.get_text(strip=True))
    
    # Process regular paragraphs
    regular_paragraphs = soup.find_all('p', class_='RegularParagraphs')
    for p in regular_paragraphs:
        text = p.get_text(strip=True)
        if text and text not in ['', '&nbsp;', '<o:p></o:p>']:
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            lines.append(text)
    
    # Process numbered paragraphs
    numbered_paragraphs = soup.find_all('p', class_='1Paragraph')
    for p in numbered_paragraphs:
        text = p.get_text(strip=True)
        if text and text not in ['', '&nbsp;', '<o:p></o:p>']:
            # Clean up extra whitespace
            text = re.sub(r'\s+', ' ', text)
            lines.append(text)
    
    # Process effective date
    effective_tag = soup.find('p', class_='Effective')
    if effective_tag:
        text = effective_tag.get_text(strip=True)
        if text and text not in ['', '&nbsp;', '<o:p></o:p>']:
            text = re.sub(r'\s+', ' ', text)
            lines.append(text)
    
    # Process report title and description
    report_title = soup.find('p', class_='ReportTitle')
    if report_title:
        lines.append(f"Report Title: {report_title.get_text(strip=True)}")
    
    description = soup.find('p', class_='Description')
    if description:
        lines.append(f"Description: {description.get_text(strip=True)}")
    
    # Join all lines with newlines
    full_text = '\n'.join(lines)
    
    # Final cleanup
    full_text = re.sub(r'\n\s*\n', '\n\n', full_text)  # Remove excessive newlines
    full_text = re.sub(r'[ \t]+', ' ', full_text)  # Normalize whitespace
    
    return full_text

def main():
    if len(sys.argv) != 3:
        print("Usage: python html_bill_to_plain_text_sb2182.py <input_html_file> <output_txt_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        plain_text = html_bill_to_plain_text(html_content)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(plain_text)
        
        print(f"Successfully converted {input_file} to {output_file}")
        print(f"Output length: {len(plain_text)} characters")
        
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
