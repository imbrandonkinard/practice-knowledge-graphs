# Current Version: Enhanced Farm-to-School Knowledge Graph

## Overview
This folder contains the current version of our knowledge graph system, including enhanced entity and relationship extraction for the Hawaii Farm-to-School Program legislative analysis.

## Files

### Core Data
- **`corenlp_extractions.json`**: Original Stanford CoreNLP extractions
- **`farm_to_school_enhanced_ontology.owl`**: Enhanced knowledge graph in OWL format
- **`farm_to_school_ontology_webprotege.owl`**: WebProtégé-compatible version

### Tools
- **`enhanced_knowledge_graph_generator.py`**: Enhanced knowledge graph generator
- **`json_to_owl_webprotege.py`**: WebProtégé-compatible converter

## Knowledge Graph Statistics

### Enhanced Version
- **Entities**: 46 unique entities
- **Relationships**: 10 meaningful relationships
- **Classes**: 20 domain-specific classes
- **Properties**: 20+ object and data properties

### Entity Types
- **Programs**: Farm-to-school program, coordinator
- **Government Agencies**: Department of Education, Department of Agriculture, Legislature
- **Locations**: Hawaii, public schools, state facilities
- **Goals**: 30% local sourcing target, 2030 deadline
- **Food Products**: Locally sourced products, fresh agricultural products
- **Processes**: Procurement, consumption, training, education

### Relationship Types
- **Organizational**: manages, reports_to, moved_to, moved_from, headed_by
- **Policy**: requires, creates, has_goal, has_deadline, implements
- **Geographic**: located_in
- **Functional**: procures, serves, consumes, affects, collaborates_with

## Key Relationships in the Knowledge Graph

### Program Transfer
- `farm_to_school_program` **moved_from** `department_of_agriculture`
- `farm_to_school_program` **moved_to** `department_of_education`

### Management Structure
- `department_of_education` **manages** `farm_to_school_program`
- `farm_to_school_coordinator` **headed_by** `department_of_education`

### Policy Goals
- `farm_to_school_program` **has_goal** `thirty_per_cent`
- `farm_to_school_program` **has_deadline** `2030`

### Reporting Requirements
- `department_of_education` **reports_to** `legislature`

### Food System Relationships
- `department_of_education` **procures** `locally_sourced_products`
- `public_schools` **serves** `locally_sourced_products`
- `students` **consumes** `fresh_local_agricultural_products`

### Geographic Context
- `farm_to_school_program` **located_in** `hawaii`
- `public_schools` **located_in** `hawaii`

## Usage Instructions

### For Protégé Desktop
1. Open Protégé
2. File → Open → Select `farm_to_school_enhanced_ontology.owl`
3. Explore Classes, Object Properties, and Individuals tabs
4. Use SPARQL queries to analyze relationships

### For WebProtégé
1. Go to https://webprotege.stanford.edu/
2. Upload `farm_to_school_ontology_webprotege.owl`
3. Explore the knowledge graph in the web interface

### Regenerating the Knowledge Graph
```bash
python enhanced_knowledge_graph_generator.py corenlp_extractions.json extracted_bill_final.txt farm_to_school_enhanced_ontology.owl
```

## SPARQL Query Examples

### Find All Programs
```sparql
SELECT ?program WHERE {
    ?program rdf:type :Program .
}
```

### Find Management Relationships
```sparql
SELECT ?manager ?managed WHERE {
    ?manager :manages ?managed .
}
```

### Find Policy Goals
```sparql
SELECT ?program ?goal WHERE {
    ?program :has_goal ?goal .
}
```

### Find Geographic Relationships
```sparql
SELECT ?entity ?location WHERE {
    ?entity :located_in ?location .
}
```

### Find All Relationships for Farm-to-School Program
```sparql
SELECT ?relation ?target WHERE {
    :farm_to_school_program ?relation ?target .
}
```

## Domain Insights

### Policy Analysis
The knowledge graph reveals the complex organizational and policy relationships in the Hawaii Farm-to-School Program:

1. **Organizational Change**: Program moved from Agriculture to Education department
2. **Clear Goals**: 30% local sourcing target by 2030
3. **Accountability**: Annual reporting to legislature
4. **Stakeholder Network**: Multiple entities involved in implementation

### Food System Impact
The relationships show how the policy affects the local food system:
- Government procurement drives demand for local products
- Schools serve as distribution points
- Students are the end consumers
- Local farmers benefit from increased demand

### Implementation Structure
The knowledge graph illustrates the implementation hierarchy:
- Legislature sets policy and receives reports
- Department of Education manages the program
- Farm-to-school coordinator leads implementation
- Schools and students are the beneficiaries

## Future Enhancements

### Additional Relationships
- Temporal relationships (when events occur)
- Causal relationships (why policies were created)
- Impact relationships (effects on different stakeholders)
- Resource relationships (funding, personnel, facilities)

### Enhanced Entity Recognition
- Financial amounts and budgets
- Specific food products and suppliers
- School districts and individual schools
- Farmer organizations and cooperatives

### Policy Evolution Tracking
- Version control for policy changes
- Amendment and repeal relationships
- Cross-references to related legislation
- Implementation timeline tracking

---

*This enhanced knowledge graph provides a comprehensive view of the Hawaii Farm-to-School Program, enabling detailed analysis of policy relationships, stakeholder connections, and implementation structure.*
