# Curriculum: NLP and Knowledge Graphs for Policy Analysis

## Overview
This curriculum teaches students how to apply Natural Language Processing (NLP) and knowledge graph techniques to analyze legislative bills and policy documents, with a focus on food systems and agricultural policy.

## Module Structure

### Module 1: Understanding V1 Development
**File**: `01_understanding_v1_development.md`
**Focus**: Project development process, real-world applications, and iterative improvement
**Learning Outcomes**: 
- Understand the development process that led to V1
- Connect NLP techniques to food system policy analysis
- Identify improvement opportunities

### Module 2: NLP Technical Foundations
**File**: `02_nlp_technical_foundations.md`
**Focus**: Technical concepts, library choices, and implementation decisions
**Learning Outcomes**:
- Explain NLP concepts and techniques used in V1
- Understand why specific approaches were chosen
- Apply concepts to design solutions for other domains

### Module 3: Visualizing Knowledge Graphs with Protégé
**File**: `03_visualizing_knowledge_graphs_protege.md`
**Focus**: Converting extracted data to ontologies and visualizing knowledge graphs
**Learning Outcomes**:
- Convert JSON extractions to OWL ontology format
- Use Protégé to visualize and explore knowledge graphs
- Design ontologies for legislative and food system domains
- Query and analyze knowledge graphs for policy insights

### Module 4: Current Version - Enhanced Knowledge Graph
**File**: `04_current_version_knowledge_graph.md`
**Focus**: Working with the enhanced knowledge graph and advanced analysis
**Learning Outcomes**:
- Explore the comprehensive entity and relationship network
- Use advanced SPARQL queries for policy analysis
- Create meaningful visualizations of complex relationships
- Apply knowledge graph techniques to real policy problems

## Current Version (Latest)

### Location
All current version files are in: `../current_version/`

### Key Features
- **46 Entities**: Comprehensive coverage of policy stakeholders
- **10+ Relationship Types**: Rich network of policy connections
- **20 Classes**: Domain-specific ontology design
- **Enhanced Extraction**: Improved entity and relationship recognition
- **WebProtégé Compatible**: Works with both desktop and web versions

### Files
- **`farm_to_school_enhanced_ontology.owl`**: Main enhanced knowledge graph
- **`farm_to_school_ontology_webprotege.owl`**: WebProtégé-compatible version
- **`enhanced_knowledge_graph_generator.py`**: Enhanced extraction tool
- **`README.md`**: Comprehensive documentation
- **`visualization_guide.md`**: Visualization instructions

## Target Audience
- **Students**: Computer science, data science, public policy, or agriculture students
- **Prerequisites**: Basic Python programming, familiarity with HTML/XML
- **Level**: Intermediate to advanced undergraduate or graduate level

## Learning Approach
- **Project-Based Learning**: Students work with real legislative documents
- **Hands-On Activities**: Practical exercises with actual code and data
- **Real-World Context**: Food system policy analysis as the application domain
- **Iterative Development**: Understanding how systems evolve through versions
- **Visualization**: Interactive knowledge graph exploration and analysis
- **Advanced Analysis**: SPARQL querying and policy insights

## Key Concepts Covered

### Technical Skills
- HTML parsing and text extraction
- Stanford CoreNLP integration
- Entity and relation extraction
- Text preprocessing and cleaning
- Memory management for large documents
- JSON data structuring
- OWL ontology creation
- Knowledge graph visualization
- SPARQL querying
- Advanced relationship modeling
- Policy network analysis

### Domain Knowledge
- Legislative bill structure and analysis
- Food system policy frameworks
- Stakeholder identification and mapping
- Policy impact assessment
- Regulatory compliance analysis
- Ontology design for policy domains
- Knowledge representation for complex systems
- Policy implementation analysis

### Problem-Solving Skills
- Iterative development methodology
- Technical trade-off analysis
- Domain-specific solution design
- Error handling and robustness
- Scalability considerations
- Knowledge representation design
- Complex relationship modeling
- Policy analysis using semantic technologies

## Implementation Guide

### Setup Requirements
1. **Python Environment**: Python 3.7+ with pip
2. **Stanford CoreNLP**: Local installation or server access
3. **Protégé**: Download from https://protege.stanford.edu/
4. **WebProtégé**: Access at https://webprotege.stanford.edu/
5. **Dependencies**: 
   - `beautifulsoup4` for HTML parsing
   - `requests` for HTTP communication
   - `stanfordcorenlp` wrapper (optional)

### Getting Started
1. Review Module 1 for project context and development process
2. Study Module 2 for technical foundations and implementation details
3. Complete hands-on activities with provided code examples
4. Use Module 3 to visualize and explore knowledge graphs
5. Work with Module 4 to use the enhanced knowledge graph
6. Apply concepts to analyze new policy documents
7. Design and implement improvements to the system

### Assessment Methods
- **Technical Understanding**: Code analysis and explanation
- **Problem Solving**: Design solutions for new domains
- **Critical Thinking**: Evaluate trade-offs and limitations
- **Innovation**: Propose creative enhancements
- **Visualization**: Create meaningful knowledge graph representations
- **Policy Analysis**: Use knowledge graphs for real-world insights

## Extending the Curriculum

### Additional Modules (Future Development)
- **Module 5**: Knowledge Graph Construction and Reasoning
- **Module 6**: Policy Impact Modeling and Prediction
- **Module 7**: Stakeholder Engagement Tools
- **Module 8**: Cross-Jurisdictional Analysis
- **Module 9**: Real-time Legislative Monitoring
- **Module 10**: Machine Learning with Knowledge Graphs

### Domain Adaptations
- **Healthcare Policy**: Medical regulations and guidelines
- **Environmental Policy**: Environmental impact statements
- **Financial Policy**: Banking and securities regulations
- **Education Policy**: Educational standards and requirements
- **Technology Policy**: Digital governance and regulation

## Resources and Support

### Technical Documentation
- Stanford CoreNLP documentation
- BeautifulSoup HTML parsing guide
- Python NLP best practices
- Protégé user manual and tutorials
- OWL and SPARQL specifications
- Knowledge graph visualization tools

### Domain Resources
- Food system policy frameworks
- Legislative analysis methodologies
- Policy impact assessment tools
- Government data standards
- Stakeholder engagement strategies

### Community and Support
- GitHub repository with code examples
- Discussion forums for questions
- Office hours and mentoring opportunities
- Protégé user community
- SPARQL and knowledge graph communities

## Contributing
This curriculum is designed to be collaborative and evolving. Students and instructors are encouraged to:
- Suggest improvements and additional topics
- Share successful adaptations for other domains
- Contribute new examples and case studies
- Provide feedback on learning effectiveness
- Submit new ontology designs and visualizations
- Share SPARQL queries and analysis techniques

---

*This curriculum represents a practical approach to teaching NLP and knowledge graph techniques through real-world policy analysis applications. It emphasizes both technical skills and domain understanding, preparing students to tackle complex problems at the intersection of technology and policy.*
