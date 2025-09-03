# Module 3: Visualizing Knowledge Graphs with Protégé

## Learning Objectives
By the end of this module, students will be able to:
- Understand how to convert extracted entities and relations into ontology formats
- Use Protégé to visualize and explore knowledge graphs
- Design ontologies for legislative and food system domains
- Query and analyze knowledge graphs for policy insights

## What is Protégé?

### Overview
**Protégé** is a free, open-source ontology editor and knowledge graph visualization tool developed by Stanford University. It's widely used in academia and industry for:
- Creating and editing ontologies
- Visualizing knowledge graphs
- Reasoning about relationships
- Querying structured knowledge

### Why Protégé for Our Project?
- **Visualization**: Interactive graph visualization of entities and relationships
- **Reasoning**: Built-in inference engines to discover implicit relationships
- **Standards**: Supports OWL (Web Ontology Language) and RDF standards
- **Querying**: SPARQL query interface for complex knowledge retrieval
- **Collaboration**: Multiple users can work on the same ontology

## Converting Our Data to Protégé Format

### Current Data Structure
Our Stanford CoreNLP extraction produces JSON with:
```json
{
  "entities": [
    {
      "text": "farm to school program",
      "type": "PROGRAM",
      "start_char": 133,
      "end_char": 155,
      "ner": "PROGRAM"
    }
  ],
  "relations": [
    {
      "subject": "farm to school program",
      "predicate": "moved",
      "object": "department of education",
      "confidence": 0.9,
      "context": "move the hawaii farm to school program..."
    }
  ]
}
```

### Target Format: OWL Ontology
Protégé works with OWL (Web Ontology Language) files that define:
- **Classes**: Categories of entities (e.g., Program, Organization, Person)
- **Properties**: Relationships between entities (e.g., manages, located_in, affects)
- **Individuals**: Specific instances (e.g., "Hawaii Farm to School Program")
- **Axioms**: Rules and constraints

## Step-by-Step Conversion Process

### Step 1: Design the Ontology Structure

#### Core Classes for Legislative/Food System Domain
```owl
# Legislative Domain Classes
- LegislativeDocument
- Bill
- Section
- Amendment

# Organizational Classes  
- GovernmentAgency
- Department
- Program
- Organization

# Policy Classes
- Policy
- Regulation
- Requirement
- Goal

# Geographic Classes
- State
- County
- Region
- Location

# Temporal Classes
- Date
- TimePeriod
- Deadline
```

#### Core Properties (Relationships)
```owl
# Organizational Relationships
- manages (Program manages Organization)
- reports_to (Department reports_to Agency)
- located_in (Program located_in State)

# Policy Relationships
- implements (Program implements Policy)
- requires (Policy requires Requirement)
- affects (Policy affects Organization)

# Temporal Relationships
- starts_on (Program starts_on Date)
- ends_on (Program ends_on Date)
- has_deadline (Requirement has_deadline Date)

# Legislative Relationships
- amends (Bill amends Regulation)
- repeals (Bill repeals Policy)
- creates (Bill creates Program)
```

### Step 2: Convert JSON to OWL

#### Python Script for Conversion
```python
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def json_to_owl(json_file, output_file):
    """Convert our JSON extractions to OWL ontology format"""
    
    # Load the JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Create OWL root element
    root = ET.Element("rdf:RDF")
    root.set("xmlns:rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    root.set("xmlns:owl", "http://www.w3.org/2002/07/owl#")
    root.set("xmlns:rdfs", "http://www.w3.org/2000/01/rdf-schema#")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema#")
    root.set("xmlns", "http://example.org/legislative#")
    
    # Define ontology
    ontology = ET.SubElement(root, "owl:Ontology")
    ontology.set("rdf:about", "")
    
    # Add ontology metadata
    comment = ET.SubElement(ontology, "rdfs:comment")
    comment.text = "Legislative Bill Knowledge Graph - Farm to School Program"
    
    # Define classes
    define_classes(root)
    
    # Define properties
    define_properties(root)
    
    # Add individuals from entities
    add_entities_as_individuals(root, data['entities'])
    
    # Add relationships
    add_relationships(root, data['relations'])
    
    # Write to file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

def define_classes(root):
    """Define the core classes in our ontology"""
    classes = [
        "Program", "Organization", "Department", "GovernmentAgency",
        "Policy", "Requirement", "Goal", "Location", "Date"
    ]
    
    for class_name in classes:
        class_elem = ET.SubElement(root, "owl:Class")
        class_elem.set("rdf:about", f"#{class_name}")
        
        label = ET.SubElement(class_elem, "rdfs:label")
        label.text = class_name

def define_properties(root):
    """Define object and data properties"""
    properties = [
        ("manages", "Program", "Organization"),
        ("reports_to", "Department", "GovernmentAgency"),
        ("implements", "Program", "Policy"),
        ("requires", "Policy", "Requirement"),
        ("has_goal", "Program", "Goal"),
        ("located_in", "Program", "Location"),
        ("starts_on", "Program", "Date"),
        ("affects", "Policy", "Organization")
    ]
    
    for prop_name, domain, range in properties:
        prop_elem = ET.SubElement(root, "owl:ObjectProperty")
        prop_elem.set("rdf:about", f"#{prop_name}")
        
        # Domain
        domain_elem = ET.SubElement(prop_elem, "rdfs:domain")
        domain_elem.set("rdf:resource", f"#{domain}")
        
        # Range
        range_elem = ET.SubElement(prop_elem, "rdfs:range")
        range_elem.set("rdf:resource", f"#{range}")

def add_entities_as_individuals(root, entities):
    """Convert entities to OWL individuals"""
    for entity in entities:
        # Create individual
        individual = ET.SubElement(root, "owl:NamedIndividual")
        individual.set("rdf:about", f"#{entity['text'].replace(' ', '_')}")
        
        # Add type
        type_elem = ET.SubElement(individual, "rdf:type")
        type_elem.set("rdf:resource", f"#{entity['type']}")
        
        # Add label
        label = ET.SubElement(individual, "rdfs:label")
        label.text = entity['text']

def add_relationships(root, relations):
    """Convert relations to OWL object property assertions"""
    for relation in relations:
        # Create property assertion
        assertion = ET.SubElement(root, "owl:ObjectPropertyAssertion")
        
        # Property
        prop_elem = ET.SubElement(assertion, "owl:ObjectProperty")
        prop_elem.set("rdf:resource", f"#{relation['predicate']}")
        
        # Subject
        subject_elem = ET.SubElement(assertion, "owl:SourceIndividual")
        subject_elem.set("rdf:resource", f"#{relation['subject'].replace(' ', '_')}")
        
        # Object
        object_elem = ET.SubElement(assertion, "owl:TargetIndividual")
        object_elem.set("rdf:resource", f"#{relation['object'].replace(' ', '_')}")

# Usage
json_to_owl('corenlp_extractions.json', 'legislative_ontology.owl')
```

### Step 3: Import into Protégé

#### Loading the Ontology
1. **Open Protégé**: Launch the Protégé application
2. **Open File**: File → Open → Select your `.owl` file
3. **Wait for Loading**: Protégé will parse and load the ontology
4. **Check for Errors**: Review any parsing errors in the console

#### Initial Exploration
1. **Classes Tab**: View the class hierarchy
2. **Object Properties Tab**: See defined relationships
3. **Individuals Tab**: Browse the extracted entities
4. **OntoGraf Tab**: Visualize the knowledge graph

## Visualizing the Knowledge Graph

### Using OntoGraf Plugin
**OntoGraf** is a Protégé plugin for graph visualization:

#### Installation
1. **Download**: Get OntoGraf from the Protégé plugin repository
2. **Install**: Place in Protégé plugins directory
3. **Restart**: Restart Protégé to load the plugin

#### Visualization Features
- **Interactive Graphs**: Click and drag to explore
- **Filtering**: Show/hide specific classes or properties
- **Layouts**: Different graph layout algorithms
- **Export**: Save visualizations as images

### Alternative: VOWL Plugin
**VOWL** (Visual Notation for OWL Ontologies) provides:
- **Standardized Notation**: Follows OWL visualization conventions
- **Color Coding**: Different colors for classes, properties, individuals
- **Hierarchical Layout**: Shows class hierarchies clearly

## Querying the Knowledge Graph

### SPARQL Queries
Protégé includes a SPARQL query interface for complex queries:

#### Basic Queries
```sparql
# Find all programs
SELECT ?program WHERE {
    ?program rdf:type :Program .
}

# Find what the farm to school program manages
SELECT ?managed WHERE {
    :farm_to_school_program :manages ?managed .
}

# Find all policies that affect organizations
SELECT ?policy ?organization WHERE {
    ?policy :affects ?organization .
    ?policy rdf:type :Policy .
    ?organization rdf:type :Organization .
}
```

#### Complex Queries
```sparql
# Find programs that implement policies affecting specific organizations
SELECT ?program ?policy ?organization WHERE {
    ?program :implements ?policy .
    ?policy :affects ?organization .
    ?program rdf:type :Program .
    ?policy rdf:type :Policy .
    ?organization rdf:type :Organization .
}

# Find all relationships involving the Department of Education
SELECT ?subject ?predicate ?object WHERE {
    {
        :department_of_education ?predicate ?object .
        BIND(:department_of_education AS ?subject)
    } UNION {
        ?subject ?predicate :department_of_education .
        BIND(:department_of_education AS ?object)
    }
}
```

## Student Activities

### Activity 1: Ontology Design
**Objective**: Design an ontology for a different policy domain

**Materials**: 
- Protégé software
- Sample policy documents
- Ontology design templates

**Steps**:
1. **Domain Analysis**: Choose a policy domain (healthcare, environment, education)
2. **Entity Identification**: List key entities and their types
3. **Relationship Mapping**: Define relationships between entities
4. **Class Hierarchy**: Design a logical class structure
5. **Property Definition**: Create object and data properties
6. **Implementation**: Build the ontology in Protégé

### Activity 2: Data Conversion
**Objective**: Convert real extraction data to OWL format

**Materials**:
- JSON extraction files
- Python conversion script
- Protégé software

**Steps**:
1. **Analyze Data**: Review the structure of extracted entities and relations
2. **Design Mapping**: Plan how to map JSON to OWL classes and properties
3. **Implement Conversion**: Modify the conversion script for your data
4. **Validate Output**: Check the generated OWL file for errors
5. **Import to Protégé**: Load and explore the resulting ontology

### Activity 3: Visualization and Analysis
**Objective**: Use Protégé to analyze policy relationships

**Materials**:
- Loaded ontology in Protégé
- OntoGraf or VOWL plugin
- SPARQL query interface

**Steps**:
1. **Graph Exploration**: Use visualization plugins to explore the knowledge graph
2. **Query Development**: Write SPARQL queries to answer specific questions
3. **Relationship Analysis**: Identify patterns in policy relationships
4. **Insight Generation**: Draw conclusions about policy structure and impact
5. **Report Creation**: Document findings and visualizations

## Advanced Features

### Reasoning and Inference
Protégé includes reasoners that can:
- **Classify**: Automatically categorize individuals
- **Consistency Checking**: Find logical contradictions
- **Property Inference**: Discover implicit relationships
- **Query Answering**: Answer complex questions using reasoning

### Collaborative Development
- **Version Control**: Track changes to ontologies
- **Multi-user Editing**: Multiple people can work on the same ontology
- **Commenting**: Add annotations and discussions
- **Export Formats**: Share in various standard formats

## Integration with Other Tools

### Web-based Visualization
- **WebVOWL**: Web-based ontology visualization
- **Ontology2Graph**: Convert to various graph formats
- **Neo4j Integration**: Export to graph databases

### Analysis Tools
- **RDF/OWL Libraries**: Python, Java, JavaScript libraries
- **Graph Analytics**: Network analysis tools
- **Machine Learning**: Use knowledge graphs for ML tasks

## Assessment and Evaluation

### Technical Skills Assessment
- **Ontology Design**: Can students create logical class hierarchies?
- **Data Conversion**: Can students map between different data formats?
- **Query Writing**: Can students write effective SPARQL queries?
- **Visualization**: Can students create meaningful graph visualizations?

### Domain Understanding Assessment
- **Policy Analysis**: Can students identify key policy relationships?
- **Stakeholder Mapping**: Can students map organizational relationships?
- **Impact Assessment**: Can students analyze policy effects?
- **Insight Generation**: Can students draw meaningful conclusions?

## Resources and Further Learning

### Protégé Resources
- **Official Documentation**: https://protege.stanford.edu/
- **Tutorials**: Step-by-step guides for beginners
- **Plugin Repository**: Additional tools and visualizations
- **Community Forums**: Support and collaboration

### Ontology Standards
- **OWL Documentation**: Web Ontology Language specifications
- **RDF Standards**: Resource Description Framework
- **SPARQL Tutorials**: Query language for RDF
- **Best Practices**: Ontology design guidelines

### Domain-Specific Resources
- **Legal Ontologies**: Existing ontologies for legal domains
- **Government Data**: Standards for government information
- **Policy Analysis**: Methodologies for policy research
- **Food Systems**: Frameworks for agricultural policy analysis

---

*This module provides hands-on experience with knowledge graph visualization and analysis using industry-standard tools. Students will learn to convert raw extraction data into structured ontologies and use powerful visualization and query tools to gain insights from policy documents.*
