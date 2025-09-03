# Protégé Quick Start Guide

## Getting Started with Your Knowledge Graph

### Step 1: Install Protégé
1. **Download**: Go to https://protege.stanford.edu/
2. **Install**: Download and install the latest version
3. **Launch**: Open Protégé application

### Step 2: Load Your Ontology
1. **Open File**: File → Open
2. **Select**: Choose `farm_to_school_ontology.owl`
3. **Wait**: Let Protégé parse the ontology (may take a moment)

### Step 3: Explore Your Knowledge Graph

#### Classes Tab
- **View**: All entity types (Program, Organization, Department, etc.)
- **Hierarchy**: See how classes relate to each other
- **Properties**: View properties associated with each class

#### Object Properties Tab
- **Relationships**: See all relationship types (moved_to, manages, etc.)
- **Domain/Range**: Understand what types of entities can have these relationships

#### Individuals Tab
- **Entities**: Browse all extracted entities
- **Types**: See what type each entity is
- **Properties**: View relationships for each entity

#### OntoGraf Tab (if plugin installed)
- **Visualization**: Interactive graph of your knowledge
- **Navigation**: Click and drag to explore relationships
- **Filtering**: Show/hide specific types of entities

### Step 4: Query Your Knowledge Graph

#### SPARQL Query Tab
Use these example queries to explore your data:

```sparql
# Find all programs
SELECT ?program WHERE {
    ?program rdf:type :Program .
}

# Find what the farm to school program is related to
SELECT ?relation ?target WHERE {
    :farm_to_school_program ?relation ?target .
}

# Find all relationships involving departments
SELECT ?subject ?predicate ?object WHERE {
    ?subject ?predicate ?object .
    {
        ?subject rdf:type :Department .
    } UNION {
        ?object rdf:type :Department .
    }
}
```

### Step 5: Visualize Relationships

#### Using OntoGraf Plugin
1. **Install**: Download OntoGraf from Protégé plugins
2. **Open**: Go to Window → OntoGraf
3. **Explore**: 
   - Click on entities to see their relationships
   - Use filters to focus on specific types
   - Export images of your visualizations

#### Alternative: VOWL Plugin
1. **Install**: Download VOWL plugin
2. **Open**: Window → VOWL
3. **View**: Standardized ontology visualization

## What You'll See in Your Knowledge Graph

### Entities (Individuals)
- **farm_to_school_program**: The main program being discussed
- **department_of_education**: Target department for the program
- **department_of_agriculture**: Source department
- **hawaii**: Geographic location
- **2030**: Target date for goals

### Relationships (Object Properties)
- **moved_to**: Program moved from one department to another
- **establishes**: One entity creates another
- **requires**: Policy requirements
- **affects**: Impact relationships

### Classes
- **Program**: Government programs and initiatives
- **Agency**: Government departments and agencies
- **Location**: Geographic entities
- **Goal**: Policy objectives and targets

## Tips for Exploration

### Start Simple
1. **Browse Individuals**: Get familiar with the entities
2. **Check Relationships**: See how entities connect
3. **Run Basic Queries**: Start with simple SPARQL queries
4. **Visualize**: Use graph visualization to see the big picture

### Ask Questions
- What programs are mentioned in the bill?
- Which departments are involved?
- What are the key relationships?
- How do policies affect different stakeholders?

### Experiment
- **Modify Queries**: Change SPARQL queries to explore different aspects
- **Filter Visualizations**: Focus on specific entity types
- **Export Results**: Save interesting visualizations and query results

## Troubleshooting

### Common Issues
1. **File Won't Load**: Check that the OWL file is valid XML
2. **No Visualization**: Install OntoGraf or VOWL plugins
3. **Empty Results**: Check SPARQL query syntax
4. **Slow Performance**: Large ontologies may take time to load

### Getting Help
- **Protégé Documentation**: https://protege.stanford.edu/
- **SPARQL Tutorials**: Online resources for query syntax
- **Community Forums**: Protégé user community

## Next Steps

### Enhance Your Ontology
1. **Add More Classes**: Define additional entity types
2. **Refine Properties**: Make relationships more specific
3. **Add Constraints**: Define rules and restrictions
4. **Import Standards**: Use existing legal or government ontologies

### Advanced Analysis
1. **Reasoning**: Use built-in reasoners to find implicit relationships
2. **Consistency Checking**: Verify logical consistency
3. **Classification**: Automatically categorize entities
4. **Query Optimization**: Write efficient SPARQL queries

### Integration
1. **Export Formats**: Convert to other graph formats
2. **Web Visualization**: Use web-based tools
3. **Database Integration**: Import into graph databases
4. **API Development**: Create services for querying

---

*This quick start guide will get you exploring your legislative knowledge graph in Protégé. The interactive visualization and querying capabilities will help you discover insights about policy relationships and stakeholder connections.*
