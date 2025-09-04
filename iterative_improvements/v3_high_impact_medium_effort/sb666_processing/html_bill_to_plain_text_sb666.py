from bs4 import BeautifulSoup
import re
import sys

def safe_get_text(tag):
    if not tag:
        return ""
    return tag.get_text(strip=True) if hasattr(tag, 'get_text') else str(tag).strip()

def html_bill_to_plain_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style
    for script in soup(["script", "style"]):
        script.decompose()

    lines = []

    # Header table parsing (robust)
    chamber = safe_get_text(soup.find('p', class_='ChamberHeading')) or safe_get_text(soup.find('td', class_='ChamberHeading'))
    if chamber:
        lines.append(chamber)

    # Measure number (e.g., S.B. NO. 666)
    num_label = safe_get_text(soup.find('p', class_='MeasureNumberHeading'))
    # The number value is often in a separate cell with ChamberHeading class
    num_value_cells = soup.find_all('p', class_='ChamberHeading')
    number_val = ""
    if len(num_value_cells) >= 2:
        number_val = safe_get_text(num_value_cells[1])
    measure_line = (num_label + " " + number_val).strip()
    if measure_line:
        lines.append(measure_line)

    # Session and version row
    # Look for any ChamberHeading containing a year and any containing X.D. Y
    chamber_paras = [safe_get_text(p) for p in soup.find_all('p', class_='ChamberHeading')]
    session = next((p for p in chamber_paras if re.search(r"\b(19|20)\d{2}\b", p)), "")
    if session:
        lines.append(session)
    version = next((p for p in chamber_paras if re.search(r"\b[HSC]\.D\.\s*\d+\b", p, re.IGNORECASE)), "")
    if version:
        lines.append(version)

    state = next((p for p in chamber_paras if 'STATE OF HAWAII' in p.upper()), "")
    if state:
        lines.append(state)

    # Title and enactment
    title = safe_get_text(soup.find('p', class_='MeasureTitle'))
    if title:
        lines.append(title)
    enacted = safe_get_text(soup.find('p', class_='BEITENACTED'))
    if enacted:
        lines.append(enacted)

    # Regular paragraphs
    for p in soup.find_all('p', class_='RegularParagraphs'):
        txt = safe_get_text(p)
        if txt and txt not in ['&nbsp;', '<o:p></o:p>']:
            txt = re.sub(r'\s+', ' ', txt)
            lines.append(txt)

    # Numbered items
    for p in soup.find_all('p', class_='1Paragraph'):
        txt = safe_get_text(p)
        if txt and txt not in ['&nbsp;', '<o:p></o:p>']:
            txt = re.sub(r'\s+', ' ', txt)
            lines.append(txt)

    # Effective
    effective = safe_get_text(soup.find('p', class_='Effective'))
    if effective:
        effective = re.sub(r'\s+', ' ', effective)
        lines.append(effective)

    # Report title and description if present
    report_title = safe_get_text(soup.find('p', class_='ReportTitle'))
    if report_title:
        lines.append(f"Report Title: {report_title}")
    description = safe_get_text(soup.find('p', class_='Description'))
    if description:
        lines.append(f"Description: {description}")

    out = '\n'.join([l for l in lines if l])
    out = re.sub(r'\n\s*\n', '\n\n', out)
    return out


def main():
    if len(sys.argv) != 3:
        print("Usage: python html_bill_to_plain_text_sb666.py <input_html_file> <output_txt_file>")
        sys.exit(1)
    input_file, output_file = sys.argv[1], sys.argv[2]
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        txt = html_bill_to_plain_text(html_content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(txt)
        print(f"Converted {input_file} -> {output_file} ({len(txt)} chars)")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
