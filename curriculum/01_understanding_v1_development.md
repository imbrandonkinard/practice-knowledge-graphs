# Module 1: Understanding V1 Development - From HTML Bills to Knowledge Graphs

## Learning Objectives
By the end of this module, students will be able to:
- Understand the iterative development process that led to V1
- Explain why each component was necessary for legislative bill analysis
- Connect NLP techniques to real-world food system policy analysis
- Identify opportunities for improvement and next steps

## Context: Why Legislative Bill Tracking Matters for Food Systems

### The Problem
Legislative bills related to food systems often contain complex, interconnected information that's difficult to analyze manually:
- **Entities**: Organizations, people, locations, dates, amounts
- **Relations**: Who does what to whom, when, where, and how
- **Policy Changes**: Amendments, repeals, new regulations
- **Stakeholder Impacts**: How policies affect farmers, schools, consumers

### The Opportunity
By extracting structured information from bills, we can:
- Track policy evolution over time
- Identify stakeholder relationships
- Analyze policy effectiveness
- Support evidence-based decision making

## V1 Development Process: A Case Study

### Phase 1: Problem Identification
**Challenge**: How do we extract meaningful information from HTML-formatted legislative bills?

**Why HTML?**: Legislative bills are often published in HTML format on government websites, making them machine-readable but not semantically structured.

### Phase 2: Data Preprocessing (html_bill_to_plain_text.py)

#### What It Does
```python
# Key functionality:
1. Parse HTML using BeautifulSoup
2. Extract text while preserving structure
3. Clean up formatting artifacts
4. Organize content into logical sections
```

#### Why This Was Necessary
- **HTML Structure**: Bills have complex nested HTML that needs parsing
- **Formatting Issues**: Extra spaces, HTML entities, and inconsistent line breaks
- **Content Organization**: Need to identify headers, sections, and content areas
- **Data Quality**: Clean text is essential for accurate NLP processing

#### Student Activity: HTML Parsing Exploration
**Objective**: Understand how HTML structure affects text extraction

**Materials**: 
- A sample HTML bill (provided)
- Python with BeautifulSoup installed

**Steps**:
1. Load the HTML bill into Python
2. Inspect the HTML structure using `soup.prettify()`
3. Identify different HTML classes and their purposes
4. Modify the parsing logic to handle a new HTML structure
5. Compare output quality before and after changes

**Discussion Questions**:
- What HTML elements were most challenging to parse?
- How did the structure affect the quality of extracted text?
- What improvements could make the parsing more robust?

### Phase 3: Entity and Relation Extraction (entity_relation_extraction.py)

#### What It Does
```python
# Core capabilities:
1. Stanford CoreNLP integration for NLP processing
2. Entity recognition (organizations, people, locations, dates)
3. Relation extraction (who does what to whom)
4. Text chunking for memory efficiency
5. Structured output in JSON format
```

#### Why This Was Necessary
- **Scale**: Bills can be thousands of words long
- **Complexity**: Need to identify entities and their relationships
- **Accuracy**: Stanford CoreNLP provides state-of-the-art NLP capabilities
- **Structured Output**: JSON format enables further analysis and visualization

#### Student Activity: NLP Pipeline Exploration
**Objective**: Understand how NLP transforms unstructured text into structured data

**Materials**:
- The entity_relation_extraction.py script
- A sample bill text
- Access to Stanford CoreNLP (or alternative NLP tools)

**Steps**:
1. Run the extraction script on a sample bill
2. Examine the JSON output structure
3. Identify different entity types and their confidence scores
4. Analyze the extracted relations for accuracy
5. Propose improvements to the extraction logic

**Discussion Questions**:
- Which entity types were most accurately identified?
- What relations were most challenging to extract?
- How could the extraction be improved for food system-specific terminology?

### Phase 4: Output Analysis (extracted_bill_final.txt)

#### What We Achieved
The final output shows a clean, structured representation of the bill with:
- Clear section headers
- Organized content
- Removed formatting artifacts
- Preserved semantic structure

#### Student Activity: Output Quality Assessment
**Objective**: Evaluate the quality of the extraction process

**Materials**:
- Original HTML bill
- Extracted plain text
- Entity/relation JSON output

**Steps**:
1. Compare original HTML to extracted text
2. Identify any information loss or distortion
3. Assess the quality of entity extraction
4. Evaluate relation extraction accuracy
5. Propose metrics for measuring extraction quality

**Discussion Questions**:
- What information was preserved vs. lost?
- How accurate were the entity extractions?
- What would make this output more useful for policy analysis?

## Connecting to Food Systems and Policy Analysis

### Real-World Applications
1. **Policy Tracking**: Monitor how food system policies evolve over time
2. **Stakeholder Mapping**: Identify who is affected by policy changes
3. **Impact Assessment**: Analyze the effectiveness of food system interventions
4. **Comparative Analysis**: Compare policies across different jurisdictions

### Food System-Specific Considerations
- **Agricultural Terminology**: Specialized vocabulary for farming, processing, distribution
- **Regulatory Language**: Legal terms and compliance requirements
- **Stakeholder Networks**: Complex relationships between farmers, processors, retailers, consumers
- **Geographic Context**: Local vs. regional vs. national policy implications

## V1 Limitations and Improvement Opportunities

### Technical Limitations
1. **Memory Constraints**: Large bills may exceed processing limits
2. **Accuracy**: NLP models may not understand domain-specific terminology
3. **Scalability**: Processing multiple bills simultaneously
4. **Error Handling**: Robust handling of malformed input

### Domain-Specific Limitations
1. **Food System Vocabulary**: Need for specialized entity recognition
2. **Policy Context**: Understanding legislative intent and impact
3. **Temporal Analysis**: Tracking policy changes over time
4. **Cross-Reference**: Linking related bills and regulations

## Next Steps: Building on V1

### Immediate Improvements
1. **Domain Adaptation**: Train models on food system terminology
2. **Validation**: Implement quality checks for extracted information
3. **Integration**: Connect to legislative databases and tracking systems

### Long-term Vision
1. **Knowledge Graph Construction**: Build interconnected policy networks
2. **Impact Modeling**: Predict policy effects on food systems
3. **Stakeholder Engagement**: Tools for public participation in policy analysis
4. **Comparative Analysis**: Cross-jurisdictional policy learning

## Student Reflection and Discussion

### Key Takeaways
- **Iterative Development**: Each version builds on previous learnings
- **Domain Understanding**: Technical solutions must address real-world needs
- **Data Quality**: Clean input is essential for meaningful output
- **Continuous Improvement**: Always look for ways to enhance the system

### Discussion Questions
1. How could this system be adapted for other policy domains?
2. What additional data sources would enhance the analysis?
3. How could stakeholders use this information to improve food systems?
4. What ethical considerations arise from automated policy analysis?

## Assessment and Evaluation

### Learning Outcomes Assessment
- **Technical Understanding**: Can students explain the purpose of each component?
- **Critical Thinking**: Can students identify limitations and improvement opportunities?
- **Domain Knowledge**: Can students connect technical solutions to food system challenges?
- **Innovation**: Can students propose creative enhancements to the system?

### Project-Based Learning
Students will work in teams to:
1. Analyze a different legislative bill using the V1 system
2. Identify specific improvements for food system analysis
3. Propose and implement one enhancement
4. Present findings to the class

## Resources and Further Reading

### Technical Resources
- Stanford CoreNLP documentation
- BeautifulSoup HTML parsing guide
- Python NLP best practices
- JSON data structure tutorials

### Domain Resources
- Food system policy frameworks
- Legislative analysis methodologies
- Stakeholder engagement strategies
- Policy impact assessment tools

---

*This module provides the foundation for understanding how technical solutions can address real-world policy analysis challenges. Students will gain both technical skills and domain knowledge, preparing them to contribute to the development of more sophisticated policy analysis tools.*
