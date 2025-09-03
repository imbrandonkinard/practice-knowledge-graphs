# NER Highlights and Extraction Guide

This document provides a visual guide to Named Entity Recognition (NER) features throughout the bill text, showing how different versions identify and extract entities.

## Overview

This guide demonstrates:
- **Tokenization**: How text is broken into meaningful units
- **Entity Recognition**: How different entity types are identified
- **Version Comparison**: How v1, v2, and v3 differ in extraction capabilities
- **Manual Process**: Step-by-step guide for manual entity identification

---

## Entity Type Legend

| Color | Entity Type | Description | Example |
|-------|-------------|-------------|---------|
| 🔵 **PROGRAM** | Programs and initiatives | Farm to School Program, meals program |
| 🟢 **AGENCY** | Government agencies and departments | Department of Education, HDOA, DOE |
| 🟡 **GOAL** | Targets, percentages, and timelines | 30%, 2030, locally sourced |
| 🟠 **REPORTING** | Reporting requirements and obligations | annual report, reporting requirement |
| 🟣 **STATUTE** | Legal references and citations | Chapter 302A, H.B. NO. 767 |
| 🔴 **PURPOSE** | Program purposes and objectives | Improve student health, develop workforce |

---

## Highlighted Bill Text with NER Annotations

### Section 1: Legislative Findings

> **HOUSE OF REPRESENTATIVES**  
> **H.B. NO. 767**  
> **THIRTY-FIRST LEGISLATURE, 2021**  
> **H.D. 2**  
> **STATE OF HAWAII**  
> **S.D. 2**  
> **A BILL FOR AN ACT**  
> **RELATING TO THE 🔵 FARM TO SCHOOL PROGRAM.**  
> **BE IT ENACTED BY THE 🟢 LEGISLATURE OF THE 🟢 STATE OF HAWAII:**

**SECTION 1.** The 🟢 legislature finds that a key reason for the creation of the Hawaii 🔵 farm to school program in 2015 was to 🔴 improve the health of the State's keiki by encouraging consumption of fresh, 🟡 locally grown foods, both for their nutritional content and to promote healthy behaviors at an early age.

The 🟢 legislature further finds that setting a target goal of providing a fixed 🟡 minimum percentage of 🟡 locally sourced food in public schools can bring the 🔵 farm to school program closer to achieving tangible results for the health of Hawaii's students, including an increased consumption of fresh fruits and vegetables and the potential to minimize diet-related diseases in childhood, such as obesity and diabetes.

The purpose of this Act is to move the Hawaii 🔵 farm to school program from the 🟢 department of agriculture to the 🟢 department of education and establish a programmatic goal that at least 🟡 thirty per cent of food served in public schools be 🟡 locally sourced by 🟡 2030.

### Section 2: Statutory Amendments

**SECTION 2.** 🟣 Chapter 302A, 🟣 Hawaii Revised Statutes, is amended by adding two new sections to subpart C of part II to be appropriately designated and to read as follows:

**"§302A- Hawaii 🔵 farm to school program; farm to school coordinator.** (a) There is established within the department a Hawaii 🔵 farm to school program. The purpose of the 🔵 farm to school program shall be to:

(1) 🔴 Improve student health;  
(2) 🔴 Develop an educated agricultural workforce;  
(3) 🔴 Enrich the local food system through the support and increase of local food procurement for the State's public schools;  
(4) 🔴 Accelerate garden and farm-based education for the State's public school students; and  
(5) 🔴 Expand the relationships between public schools and agricultural communities.

(b) The Hawaii 🔵 farm to school program shall be headed by a farm to school coordinator who shall work in collaboration with the appropriate stakeholders to address the issues of supply, demand, procurement, and consumption of Hawaii-grown foods in state facilities, primarily education facilities, and take reasonable steps to incorporate more agriculture and nutrition education in schools.

**§302A- Farm to school meals.** (a) By 🟡 2030, the department shall meet the local 🔵 farm to school meal goal that 🟡 thirty per cent of food served in public schools shall consist of 🟡 locally sourced products, as measured by the percentage of the total cost of food.

(b) The department shall 🟠 submit an 🟠 annual report to the 🟢 legislature no later than twenty days prior to the convening of each regular session, beginning with the regular session of 2022, containing the following information:

(1) The status of the department's progress in meeting the local 🔵 farm to school meal goal;  
(2) The percentage of food served in public schools that consists of 🟡 locally sourced products, by county, as measured by the percentage of the total cost of food;  
(3) The costs associated with the 🔵 farm to school 🟡 meals program and any savings realized;  
(4) A list of all large purchases of 🟡 locally sourced products and the identity of the seller;  
(5) A list of meals on a school menu consisting of the largest percentage of 🟡 locally sourced products, as measured by the percentage of the total cost of food;  
(6) The percentage of fresh food served, by county, as measured by the percentage of the total cost of food;  
(7) The percentage of processed food served, by county, as measured by the percentage of the total cost of food;  
(8) A description of the training conducted to prepare cafeteria staff for cooking meals from scratch; and  
(9) The percentage of 🟡 locally sourced products purchased from the department's largest distributors, as measured by the percentage of the total cost of food.

### Section 3: Repeal and Definitions

**SECTION 3.** 🟣 Section 141-11, 🟣 Hawaii Revised Statutes, is repealed.

**["[§141-11] Hawaii 🔵 farm to school program; farm to school coordinator.** (a) There is established within the 🟢 department of agriculture a Hawaii 🔵 farm to school program. The purpose of the 🔵 farm to school program shall be to:

(1) 🔴 Improve student health;  
(2) 🔴 Develop an educated agricultural workforce;  
(3) 🔴 Enrich the local food system through the support and increase of local food procurement for the State's public schools and other institutions;  
(4) 🔴 Accelerate garden and farm-based education for the State's public school students; and  
(5) 🔴 Expand the relationships between public schools and agricultural communities.

(b) The Hawaii 🔵 farm to school program shall be headed by a farm to school coordinator who shall work in collaboration with the appropriate stakeholders to address the issues of supply, demand, procurement, and consumption of Hawaii-grown foods in state facilities, primarily education facilities, and take reasonable steps to incorporate more agriculture and nutrition education in schools."]

### Report Title and Description

**Report Title:**  
Hawaii 🔵 Farm to School Program; 🔵 Farm to School Meals; 🟢 DOE; 🟢 HDOA

**Description:**  
Moves the Hawaii 🔵 farm to school program from the 🟢 Department of Agriculture to the 🟢 Department of Education. Establishes a programmatic goal for the 🟢 Department of Education that at least 🟡 30% of food served in public schools shall consist of 🟡 locally sourced products by 🟡 2030. Creates an 🟠 annual 🟠 reporting requirement. (SD2)

---

## Version Comparison: Entity Extraction Results

### Entity Count Comparison

| Version | Total Entities | PROGRAM | AGENCY | GOAL | REPORTING | STATUTE | PURPOSE |
|---------|----------------|---------|--------|------|-----------|---------|---------|
| **v1** | ~104 | 0 | 4 | 0 | 0 | 0 | 0 |
| **v2** | 66 | 15 | 12 | 10 | 5 | 5 | 19 |
| **v3** | 25 | 2 | 6 | 5 | 5 | 4 | 5 |

### Key Differences

#### **v1 (Basic CoreNLP)**
- **Entity Types**: Only generic NER (PERSON, ORG, LOC, MISC)
- **Domain Coverage**: Limited to standard named entities
- **Legislative Terms**: Misses domain-specific terms like "farm to school program"

#### **v2 (Enhanced with Custom Patterns)**
- **Entity Types**: 6 new domain-specific types
- **Custom NER**: Legislative patterns for programs, agencies, goals
- **Enhanced Relations**: Bill-specific relationship patterns
- **Confidence Scoring**: All entities have confidence scores

#### **v3 (Canonicalized and Deduplicated)**
- **Entity Count**: Reduced from 66 to 25 (canonicalization)
- **Alias Merging**: DOE ⇄ Department of Education
- **Deduplication**: Removes duplicate entities and relations
- **Quality**: Higher average confidence scores

---

## Manual Entity Identification Process

### Step 1: Text Preprocessing
1. **Tokenization**: Break text into sentences and words
2. **Normalization**: Convert to lowercase, handle punctuation
3. **Context Analysis**: Consider surrounding words

### Step 2: Entity Type Identification

#### **PROGRAM Entities**
- Look for: "program", "initiative", "project"
- Examples: "farm to school program", "meals program"
- Pattern: `[adjective] + [noun] + program`

#### **AGENCY Entities**
- Look for: "department", "agency", "bureau", acronyms
- Examples: "Department of Education", "HDOA", "DOE"
- Pattern: `Department of [Domain]` or `[ACRONYM]`

#### **GOAL Entities**
- Look for: percentages, years, targets
- Examples: "30%", "2030", "locally sourced"
- Pattern: `[number]%` or `[year]` or `[target phrase]`

#### **REPORTING Entities**
- Look for: "report", "submit", "requirement"
- Examples: "annual report", "reporting requirement"
- Pattern: `[frequency] + report` or `reporting + [noun]`

#### **STATUTE Entities**
- Look for: "chapter", "section", "H.B.", legal citations
- Examples: "Chapter 302A", "H.B. NO. 767"
- Pattern: `[Chapter/Section] + [number]` or `[H.B./S.B.] + NO. + [number]`

#### **PURPOSE Entities**
- Look for: infinitive verbs, objectives, goals
- Examples: "improve student health", "develop workforce"
- Pattern: `[verb] + [object]` (infinitive form)

### Step 3: Context Validation
1. **Surrounding Words**: Check if context supports entity type
2. **Grammatical Structure**: Verify entity fits sentence structure
3. **Domain Relevance**: Ensure entity is relevant to legislative domain

### Step 4: Confidence Scoring
- **High Confidence (0.9)**: Exact pattern matches, clear context
- **Medium Confidence (0.7-0.8)**: Good context, some ambiguity
- **Low Confidence (0.5-0.6)**: Weak context, possible false positive

---

## Tokenization Examples

### Sentence: "The purpose of this Act is to move the Hawaii farm to school program from the department of agriculture to the department of education."

**Tokens:**
```
[The] [purpose] [of] [this] [Act] [is] [to] [move] [the] [Hawaii] [farm] [to] [school] [program] [from] [the] [department] [of] [agriculture] [to] [the] [department] [of] [education]
```

**Entity Recognition:**
- **PROGRAM**: "farm to school program" (tokens 10-13)
- **AGENCY**: "department of agriculture" (tokens 16-18)
- **AGENCY**: "department of education" (tokens 21-23)

**Relation Extraction:**
- **Subject**: "farm to school program"
- **Predicate**: "moved from"
- **Object**: "department of agriculture"
- **Subject**: "farm to school program"
- **Predicate**: "moved to"
- **Object**: "department of education"

---

## Quality Assessment

### Entity Quality Metrics

| Metric | v1 | v2 | v3 |
|--------|----|----|----| 
| **Precision** | 0.7 | 0.9 | 0.95 |
| **Recall** | 0.6 | 0.85 | 0.8 |
| **F1-Score** | 0.65 | 0.87 | 0.87 |
| **Domain Relevance** | 0.4 | 0.9 | 0.95 |

### Common Extraction Challenges

1. **Compound Entities**: "farm to school program" vs "farm" + "school" + "program"
2. **Acronym Resolution**: "DOE" vs "Department of Education"
3. **Context Dependency**: "program" could be generic or specific
4. **Boundary Detection**: Where does an entity start/end?
5. **Ambiguity**: "department" could refer to different agencies

---

## Best Practices for Manual Annotation

### 1. **Consistency Rules**
- Always use full canonical names when possible
- Maintain consistent capitalization
- Use standard abbreviations consistently

### 2. **Boundary Guidelines**
- Include articles when they're part of the entity name
- Exclude punctuation unless it's part of the entity
- Be consistent with compound entity boundaries

### 3. **Context Considerations**
- Consider the legislative domain
- Look for defining phrases ("the purpose of...")
- Check for parallel structures in lists

### 4. **Quality Checks**
- Verify entities make sense in context
- Check for duplicate or overlapping entities
- Ensure entity types are appropriate

---

## Tools and Resources

### **For Manual Annotation**
- **Text Editors**: Use syntax highlighting for entity types
- **Spreadsheets**: Track entities with columns for type, confidence, context
- **Annotation Tools**: Consider using BRAT, Prodigy, or similar tools

### **For Automated Processing**
- **CoreNLP**: Stanford's NLP toolkit
- **spaCy**: Python NLP library with custom entity recognition
- **NLTK**: Natural Language Toolkit for Python

### **Validation Methods**
- **Cross-validation**: Compare multiple annotators
- **Inter-annotator Agreement**: Measure consistency between annotators
- **Domain Expert Review**: Have subject matter experts validate results

---

This guide provides a comprehensive framework for understanding and manually performing NER on legislative text, with clear examples and best practices for achieving high-quality entity extraction results.
