# Knowledge Graph Visualization Guide

This guide provides alternatives to Protégé's OntoGraf for visualizing large TTL knowledge graphs without node overlap.

## Quick Start: WebVOWL (Recommended)

### Option 1: WebVOWL (Easiest - Web-based)
**Best for**: Interactive web-based visualization without installation

1. **Go to**: https://vowl.visualdataweb.org/webvowl.html
2. **Upload**: `testimony_ontology_for_webvowl.owl` (or try your TTL file directly)
3. **Explore**: Interactive visualization with zoom, pan, and filtering

**Advantages**:
- No installation required
- Specifically designed for ontologies
- Better layout algorithms than Protégé
- Interactive exploration
- Clean, non-overlapping nodes

## Desktop Tools for Large Graphs

### Option 2: Gephi (Most Powerful)
**Best for**: Large network visualization with advanced layouts

#### Installation:
```bash
# macOS
brew install --cask gephi

# Or download from: https://gephi.org/
```

#### Import Your Data:
1. **Convert TTL to GEXF format** (Gephi's native format):
```python
# Install required packages
pip install rdflib networkx

# Run conversion script (see below)
python3 ttl_to_gephi.py
```

2. **Open Gephi** → File → Open → Select your `.gexf` file
3. **Apply Layout**: 
   - Force Atlas 2 (for organic layouts)
   - Yifan Hu (for hierarchical layouts)
   - OpenOrd (for large graphs)

#### Advantages:
- Handles 1000+ nodes easily
- Multiple layout algorithms
- Interactive filtering
- High-quality export
- Community detection

### Option 3: Cytoscape (Network Analysis)
**Best for**: Complex relationship analysis

#### Installation:
```bash
# macOS
brew install --cask cytoscape

# Or download from: https://cytoscape.org/
```

#### Import Your Data:
1. **Install RDFScape plugin** (for RDF support)
2. **Import**: File → Import → Network → From RDF/OWL
3. **Apply Layout**: Layout → yFiles → Organic or Hierarchical

#### Advantages:
- Powerful network analysis
- Extensive plugin ecosystem
- Good for overlapping node management
- Customizable visualizations

## Conversion Scripts

### TTL to GEXF (for Gephi)
```python
#!/usr/bin/env python3
"""
Convert TTL to GEXF format for Gephi visualization
"""

import rdflib
import networkx as nx
from rdflib import Graph, Namespace

def ttl_to_gephi(ttl_file, gexf_file):
    """Convert TTL to GEXF format"""
    
    # Load the TTL file
    g = Graph()
    g.parse(ttl_file, format='turtle')
    
    # Create NetworkX graph
    nx_graph = nx.Graph()
    
    # Add nodes and edges
    for s, p, o in g:
        if isinstance(o, rdflib.URIRef) or isinstance(o, rdflib.BNode):
            # Add nodes
            nx_graph.add_node(str(s), label=str(s).split('#')[-1])
            nx_graph.add_node(str(o), label=str(o).split('#')[-1])
            
            # Add edges
            predicate = str(p).split('#')[-1] if '#' in str(p) else str(p)
            nx_graph.add_edge(str(s), str(o), label=predicate)
    
    # Write GEXF file
    nx.write_gexf(nx_graph, gexf_file)
    print(f"✓ Converted to {gexf_file}")
    print(f"  Nodes: {nx_graph.number_of_nodes()}")
    print(f"  Edges: {nx_graph.number_of_edges()}")

if __name__ == "__main__":
    ttl_to_gephi("complete_updated_testimony_ontology.ttl", "testimony_graph.gexf")
```

### TTL to GraphML (for Cytoscape)
```python
#!/usr/bin/env python3
"""
Convert TTL to GraphML format for Cytoscape
"""

import rdflib
import networkx as nx

def ttl_to_graphml(ttl_file, graphml_file):
    """Convert TTL to GraphML format"""
    
    # Load the TTL file
    g = Graph()
    g.parse(ttl_file, format='turtle')
    
    # Create NetworkX graph
    nx_graph = nx.Graph()
    
    # Add nodes with attributes
    for s, p, o in g:
        if isinstance(o, rdflib.URIRef) or isinstance(o, rdflib.BNode):
            # Add nodes with labels
            s_label = str(s).split('#')[-1] if '#' in str(s) else str(s)
            o_label = str(o).split('#')[-1] if '#' in str(o) else str(o)
            
            nx_graph.add_node(str(s), label=s_label, id=str(s))
            nx_graph.add_node(str(o), label=o_label, id=str(o))
            
            # Add edges with predicates
            predicate = str(p).split('#')[-1] if '#' in str(p) else str(p)
            nx_graph.add_edge(str(s), str(o), label=predicate, predicate=predicate)
    
    # Write GraphML file
    nx.write_graphml(nx_graph, graphml_file)
    print(f"✓ Converted to {graphml_file}")
    print(f"  Nodes: {nx_graph.number_of_nodes()}")
    print(f"  Edges: {nx_graph.number_of_edges()}")

if __name__ == "__main__":
    ttl_to_graphml("complete_updated_testimony_ontology.ttl", "testimony_graph.graphml")
```

## Web-based Alternatives

### Option 4: GraphDB Workbench
**Best for**: Semantic graph exploration with SPARQL

1. **Install GraphDB**: https://www.ontotext.com/products/graphdb/
2. **Import your TTL file**
3. **Use the Graph Explorer** for visualization
4. **Run SPARQL queries** with visual results

### Option 5: Neo4j Browser (with RDF import)
**Best for**: Large graph databases

1. **Install Neo4j**: https://neo4j.com/download/
2. **Import RDF data** using APOC procedures
3. **Use Neo4j Browser** for visualization
4. **Apply layout algorithms** like Force Atlas

## Recommended Workflow

### For Quick Visualization:
1. **Try WebVOWL first** (no installation needed)
2. **Upload your TTL file** directly
3. **Explore interactively**

### For Advanced Analysis:
1. **Install Gephi** for the best large graph handling
2. **Convert TTL to GEXF** using the script above
3. **Apply Force Atlas 2 layout**
4. **Use filtering and clustering** for focused views

### For Network Analysis:
1. **Use Cytoscape** with RDFScape plugin
2. **Import as GraphML** format
3. **Apply hierarchical layouts**
4. **Use network analysis plugins**

## Layout Algorithm Recommendations

### For Large Graphs (100+ nodes):
- **Force Atlas 2** (Gephi) - Organic, spreads nodes well
- **Yifan Hu** (Gephi) - Hierarchical, good for ontologies
- **OpenOrd** (Gephi) - Fast, good for very large graphs

### For Ontologies:
- **Organic** (Cytoscape) - Natural clustering
- **Hierarchical** (Cytoscape) - Tree-like structure
- **Circular** (Cytoscape) - Good for small-medium graphs

### For Networks:
- **Force-directed** - Natural node distribution
- **Stress majorization** - Minimizes edge crossings
- **Multilevel** - Good for community detection

## Troubleshooting

### WebVOWL Issues:
- Try converting TTL to OWL first
- Reduce ontology size if too large
- Check for syntax errors in TTL

### Gephi Issues:
- Use GEXF format for best compatibility
- Apply layout before visualization
- Use filtering to reduce complexity

### Cytoscape Issues:
- Install RDFScape plugin for RDF support
- Use GraphML format
- Apply layout algorithms after import

## Performance Tips

### For Very Large Graphs (1000+ nodes):
1. **Filter by node type** (show only individuals, or only organizations)
2. **Use clustering** to group related nodes
3. **Apply progressive disclosure** (show details on demand)
4. **Use multiple views** for different perspectives

### Memory Optimization:
- **Close other applications** when visualizing large graphs
- **Use 64-bit versions** of tools
- **Increase heap size** for Java-based tools

## Next Steps

1. **Try WebVOWL first** - it's the quickest option
2. **If you need more power**, install Gephi
3. **For network analysis**, use Cytoscape
4. **For semantic queries**, consider GraphDB

Each tool has its strengths - choose based on your specific needs for visualization, analysis, or exploration of your testimony ontology.
