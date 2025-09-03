# Module 4: Current Version - Enhanced Knowledge Graph

## Learning Objectives
By the end of this module, students will be able to:
- Understand the enhanced knowledge graph structure and relationships
- Explore the comprehensive entity and relationship network
- Use advanced SPARQL queries to analyze policy relationships
- Create meaningful visualizations of the knowledge graph

## Current Version Overview

### Location
All current version files are located in: `current_version/`

### Key Files
- **`farm_to_school_enhanced_ontology.owl`**: Main enhanced knowledge graph
- **`farm_to_school_ontology_webprotege.owl`**: WebProtégé-compatible version
- **`enhanced_knowledge_graph_generator.py`**: Enhanced extraction tool
- **`README.md`**: Comprehensive documentation
- **`visualization_guide.md`**: Visualization instructions

## Enhanced Knowledge Graph Features

### Comprehensive Entity Coverage (46 entities)
- **Programs**: Farm-to-school program, coordinator
- **Government Agencies**: Department of Education, Department of Agriculture, Legislature
- **Locations**: Hawaii, public schools, state facilities
- **Goals**: 30% local sourcing target, 2030 deadline
- **Food Products**: Locally sourced products, fresh agricultural products
- **Processes**: Procurement, consumption, training, education

### Rich Relationship Network (10+ relationship types)
- **Organizational**: manages, reports_to, moved_to, moved_from, headed_by
- **Policy**: requires, creates, has_goal, has_deadline, implements
- **Geographic**: located_in
- **Functional**: procures, serves, consumes, affects, collaborates_with

### Domain-Specific Classes (20 classes)
- **Legislative**: LegislativeDocument, Section, Policy, Requirement
- **Organizational**: Program, GovernmentAgency, Department, Person
- **Geographic**: Location, School
- **Temporal**: Date, Goal, Deadline
- **Food System**: Food, Process, Outcome, Stakeholder

## Key Relationships in the Knowledge Graph

### Program Transfer Relationships
```
farm_to_school_program moved_from department_of_agriculture
farm_to_school_program moved_to department_of_education
```

### Management Structure
```
department_of_education manages farm_to_school_program
farm_to_school_coordinator headed_by department_of_education
```

### Policy Goals and Deadlines
```
farm_to_school_program has_goal thirty_per_cent
farm_to_school_program has_deadline 2030
```

### Reporting and Accountability
```
department_of_education reports_to legislature
```

### Food System Relationships
```
department_of_education procures locally_sourced_products
public_schools serves locally_sourced_products
students consumes fresh_local_agricultural_products
```

## Student Activities

### Activity 1: Knowledge Graph Exploration
**Objective**: Explore the enhanced knowledge graph structure

**Materials**:
- Protégé software
- `farm_to_school_enhanced_ontology.owl`
- SPARQL query interface

**Steps**:
1. **Load the Ontology**: Open the enhanced ontology in Protégé
2. **Explore Classes**: Review the 20 domain-specific classes
3. **Examine Properties**: Study the relationship types
4. **Browse Individuals**: Look at the 46 entities
5. **Run Queries**: Use provided SPARQL examples

**Discussion Questions**:
- What types of relationships are most important for policy analysis?
- How do the organizational relationships affect implementation?
- What insights can you gain from the food system relationships?

### Activity 2: SPARQL Query Development
**Objective**: Write custom SPARQL queries for policy analysis

**Materials**:
- Enhanced ontology loaded in Protégé
- SPARQL query interface
- Policy analysis questions

**Steps**:
1. **Start Simple**: Write basic entity queries
2. **Add Relationships**: Include property relationships
3. **Filter Results**: Use WHERE clauses for specific analysis
4. **Combine Concepts**: Create complex multi-hop queries
5. **Test and Refine**: Iterate on query design

**Example Queries to Develop**:
```sparql
# Find all entities that affect student health
SELECT ?entity WHERE {
    ?entity :affects ?health_related_entity .
    ?health_related_entity rdfs:label ?label .
    FILTER(CONTAINS(LCASE(?label), "health"))
}

# Find the complete policy implementation chain
SELECT ?policy ?implementer ?target ?outcome WHERE {
    ?policy :implements ?implementer .
    ?implementer :affects ?target .
    ?target :produces ?outcome .
}

# Find all reporting relationships
SELECT ?reporter ?reported_to ?report_type WHERE {
    ?reporter :reports_to ?reported_to .
    ?reporter :produces ?report_type .
}
```

### Activity 3: Visualization Creation
**Objective**: Create meaningful visualizations of the knowledge graph

**Materials**:
- Protégé with OntoGraf or VOWL plugin
- Enhanced ontology
- Visualization guidelines

**Steps**:
1. **Choose Focus**: Select specific relationship types to visualize
2. **Apply Filters**: Show only relevant entities and relationships
3. **Adjust Layout**: Use appropriate layout algorithms
4. **Add Context**: Include legends and annotations
5. **Export Results**: Save visualizations for documentation

**Visualization Types**:
- **Organizational Chart**: Government hierarchy and management
- **Policy Flow**: Implementation and accountability chains
- **Food System Network**: Production to consumption relationships
- **Stakeholder Map**: All affected parties and their connections
- **Timeline**: Policy evolution and key milestones

### Activity 4: Policy Analysis Using Knowledge Graph
**Objective**: Use the knowledge graph to analyze policy effectiveness

**Materials**:
- Enhanced ontology
- Policy analysis framework
- Stakeholder identification tools

**Steps**:
1. **Identify Stakeholders**: Use the knowledge graph to find all affected parties
2. **Map Relationships**: Understand how different entities interact
3. **Analyze Goals**: Examine policy objectives and targets
4. **Assess Implementation**: Review the implementation structure
5. **Evaluate Impact**: Consider the effects on different stakeholders

**Analysis Questions**:
- Who are the key stakeholders in the farm-to-school program?
- How does the organizational structure support or hinder implementation?
- What are the potential bottlenecks in the policy implementation chain?
- How might changes to the program affect different stakeholders?

## Advanced Topics

### Knowledge Graph Enhancement
1. **Additional Relationships**: Temporal, causal, and impact relationships
2. **Entity Expansion**: Financial data, specific suppliers, individual schools
3. **Policy Evolution**: Version control and change tracking
4. **Cross-References**: Links to related legislation and regulations

### Integration with Other Systems
1. **Legislative Databases**: Connect to official government data
2. **School Information Systems**: Link to actual school data
3. **Food System Databases**: Connect to agricultural and food data
4. **Performance Metrics**: Include outcome and impact data

### Machine Learning Applications
1. **Relationship Prediction**: Predict new relationships based on patterns
2. **Policy Impact Modeling**: Model the effects of policy changes
3. **Stakeholder Analysis**: Identify key influencers and decision makers
4. **Anomaly Detection**: Find unusual patterns in policy implementation

## Assessment and Evaluation

### Technical Skills Assessment
- **Query Writing**: Can students write effective SPARQL queries?
- **Visualization**: Can students create meaningful graph visualizations?
- **Analysis**: Can students use the knowledge graph for policy insights?
- **Enhancement**: Can students propose improvements to the knowledge graph?

### Domain Understanding Assessment
- **Policy Analysis**: Can students identify key policy relationships?
- **Stakeholder Mapping**: Can students map organizational and stakeholder networks?
- **Implementation Understanding**: Can students explain how policies are implemented?
- **Impact Assessment**: Can students analyze policy effects on different groups?

## Resources and Further Learning

### Technical Resources
- **SPARQL Tutorials**: Advanced query writing techniques
- **Ontology Design**: Best practices for knowledge representation
- **Graph Visualization**: Tools and techniques for network analysis
- **RDF/OWL Standards**: Official specifications and guidelines

### Domain Resources
- **Policy Analysis Methods**: Frameworks for analyzing public policy
- **Food System Research**: Academic and practical resources
- **Legislative Analysis**: Tools and techniques for bill analysis
- **Stakeholder Engagement**: Methods for involving affected parties

### Community Resources
- **Protégé User Community**: Forums and support
- **SPARQL Community**: Query examples and best practices
- **Knowledge Graph Community**: Research and applications
- **Policy Analysis Networks**: Professional communities

---

*This module provides hands-on experience with the enhanced knowledge graph, enabling students to explore complex policy relationships and develop advanced analysis skills using semantic web technologies.*
