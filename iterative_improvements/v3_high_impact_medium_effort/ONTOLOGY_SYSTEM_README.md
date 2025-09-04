# Enhanced Legislative Ontology System

## Overview
This system generates a comprehensive OWL ontology from multiple legislative bills, creating a connected knowledge graph with entities, relationships, and cross-bill connections.

## Files

### Core Generators
- **`combined_ontology_generator_threeBills.py`** - Main static generator (updated to include SB666)
- **`combined_ontology_generator_enhanced.py`** - Enhanced generator with detailed statistics and analysis
- **`combined_ontology_generator_threeBills_dynamic.py`** - Dynamic generator that processes JSON data

### Utility Scripts
- **`add_bill_to_ontology.py`** - Script to easily add new bills to the system

### Output
- **`combined_legislative_bills_ontology_threeBills.owl`** - Generated OWL ontology file

## Current Bills Included
1. **HB767** - Farm to School Program (2021)
2. **SB2182** - School Gardens (2022) 
3. **SB666** - UH Agriculture Education (2025)

## Usage

### Generate Ontology
```bash
# Basic generation
python combined_ontology_generator_threeBills.py

# Enhanced generation with detailed statistics
python combined_ontology_generator_enhanced.py
```

### Add New Bill
```bash
python add_bill_to_ontology.py <bill_id> <json_file> <title> <package>
# Example:
python add_bill_to_ontology.py HB1234 "hb1234_data.json" "New Bill Title" "NewPackage"
```

## Ontology Structure

### Entity Classes (26 total)
- **Core Legislative**: Bill, BillPackage, LegislativeReport, LegislativeBody
- **Government**: Agency, Person, Position, Organization
- **Educational**: EducationTopic, TrainingAction, EducationalSpace
- **Agricultural**: Profession, Organization (University of Hawaii, CTAHR)
- **Legal**: LegalSection, Statute, LegislativeMeasure
- **Data**: AgeStatistic, Funding, Goal, Purpose

### Object Properties (19 total)
- **Bill Relationships**: enactedBy, references, partOfPackage, referencesBill
- **Entity Relationships**: partOf, relatesTo, worksFor, serves, operatesAt
- **Program Relationships**: hasPurpose, hasGoal, hasCoordinator, hasFunding

### Data Properties (14 total)
- **Entity Data**: hasText, hasConfidence, hasSource, hasContext
- **Bill Data**: hasFullText, hasBillYear, hasMeasureVersion, hasBillNumber
- **Package Data**: hasPackageName, hasReportTitle

## Key Features

### 1. Connected Knowledge Graph
- **Bill-to-Entity References**: Each bill references its extracted entities
- **Entity Hierarchies**: CTAHR → partOf → University of Hawaii
- **Cross-Bill Connections**: S.R. No. 80 → referencesBill → SB666
- **Package Memberships**: Bills grouped into legislative packages

### 2. Comprehensive Entity Coverage
- **23 Entity Types** across all three bills
- **145+ Total Entities** dynamically extracted
- **Shared Entities** identified between bills (Department of Education, Students)

### 3. Legislative Packages
- **Healthy Schools 2021 Package**: HB767, SB2182
- **Agriculture Education 2025 Package**: SB666

## Statistics (Current)
- **3 Legislative Bills**
- **26 Entity Classes**
- **19 Object Properties**
- **14 Data Properties**
- **33 Named Individuals**
- **8 Relationship Axioms**

## Adding New Bills

### Step 1: Prepare JSON Data
Ensure your bill extraction JSON has:
```json
{
  "bill_info": {
    "bill_number": "HB1234",
    "session": "LEGISLATURE, YEAR",
    "effective_date": "DATE"
  },
  "entities": [...]
}
```

### Step 2: Add to Configuration
```bash
python add_bill_to_ontology.py HB1234 "path/to/data.json" "Bill Title" "PackageName"
```

### Step 3: Regenerate Ontology
```bash
python combined_ontology_generator_enhanced.py
```

## Benefits
1. **Scalable**: Easy to add new bills
2. **Connected**: Proper relationships between all entities
3. **Comprehensive**: Covers all major legislative entity types
4. **Queryable**: Rich OWL structure for semantic queries
5. **Maintainable**: Clear separation of concerns and modular design

## Next Steps
- Add more bills using the `add_bill_to_ontology.py` script
- Implement relationship extraction between entities
- Add confidence-weighted entity merging
- Create visualization tools for the knowledge graph
