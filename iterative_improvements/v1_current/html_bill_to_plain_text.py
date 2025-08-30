from bs4 import BeautifulSoup
import re

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
    
    # Format header properly
    if len(header_elements) >= 6:
        lines.append(header_elements[0])  # HOUSE OF REPRESENTATIVES
        lines.append(f"{header_elements[1]} {header_elements[2]}")  # H.B. NO. 767
        lines.append(header_elements[3])  # THIRTY-FIRST LEGISLATURE, 2021
        lines.append(header_elements[4])  # H.D. 2
        lines.append(header_elements[5])  # STATE OF HAWAII
        lines.append(header_elements[6])  # S.D. 2
        lines.append("")  # Empty line
        lines.append("A BILL FOR AN ACT")
    
    # Main content sections
    content_tags = soup.find_all(['p'], class_=['ABILLFORANACT', 'MeasureTitle', 'BEITENACTED', 'RegularParagraphs', '1Paragraph', 'Effective', 'ReportTitle', 'Description'])
    for tag in content_tags:
        # Get text with better handling of nested elements
        text = ''
        for content in tag.contents:
            if hasattr(content, 'get_text'):
                text += content.get_text()
            elif isinstance(content, str):
                text += content
        
        if text:
            # Clean up the text
            text = re.sub(r'<o:p>.*?</o:p>', '', text)
            text = re.sub(r'&nbsp;', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            if text:
                # Add labels for Report Title and Description
                if 'ReportTitle' in tag.get('class', []):
                    lines.append("Report Title:")
                    lines.append(text)
                elif 'Description' in tag.get('class', []):
                    lines.append("Description:")
                    lines.append(text)
                elif 'ABILLFORANACT' in tag.get('class', []):
                    # Skip this since we add it manually in header
                    pass
                else:
                    lines.append(text)
    
    # Join lines and clean up
    text = '\n'.join(lines)
    
    # Final cleanup
    text = re.sub(r'<.*?>', '', text)  # Remove any remaining HTML tags
    text = re.sub(r'&nbsp;', ' ', text)  # Replace HTML entities
    text = re.sub(r'\xa0', ' ', text)  # Replace non-breaking spaces
    text = re.sub(r'[ ]+', ' ', text)  # Collapse multiple spaces
    text = re.sub(r'\n{3,}', '\n\n', text)  # Limit consecutive newlines
    
    # Fix line breaks that split words inappropriately
    # This handles the case where HTML line breaks split words
    lines = text.split('\n')
    cleaned_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # If this line ends with a word and next line starts with a word, they might be connected
        if i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            # Be more conservative - only fix obvious word splits in content sections
            if (next_line and 
                not next_line.startswith(('SECTION', '(', '"', '§', 'Report Title:', 'Description:')) and
                not any(header in line for header in ['HOUSE OF REPRESENTATIVES', 'H.B. NO.', 'THIRTY-FIRST LEGISLATURE', 'H.D. 2', 'STATE OF HAWAII', 'S.D. 2', 'A BILL FOR AN ACT'])):
                # Check if this line ends with a word and next line starts with a word
                if re.search(r'\w$', line) and re.search(r'^\w', next_line):
                    # They might be connected, but let's be conservative
                    # Only join if the next line is short (likely a continuation)
                    if len(next_line) < 50:  # Arbitrary threshold
                        line = line + ' ' + next_line
                        lines[i + 1] = ''  # Mark next line as processed
        
        if line:
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    text = text.strip()
    
    return text

def save_plain_text_to_file(html_file, output_file):
    """Extract plain text from HTML file and save to output file"""
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    plain_text = html_bill_to_plain_text(html_content)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plain_text)
    
    return plain_text

# Example usage
if __name__ == "__main__":
    # Extract and display
    with open("bill.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    plain_text = html_bill_to_plain_text(html_content)
    print(plain_text)
    
    # Also save to file
    print("\n" + "="*50)
    print("Saving extracted text to 'extracted_bill.txt'...")
    with open("extracted_bill.txt", "w", encoding="utf-8") as f:
        f.write(plain_text)
    print("Extraction complete!")
