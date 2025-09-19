#!/usr/bin/env python3
"""
Convert TTL to GraphML format for Cytoscape visualization
"""

import rdflib
import networkx as nx
from rdflib import Graph, Namespace, URIRef, BNode, Literal

def ttl_to_cytoscape(ttl_file, graphml_file):
    """Convert TTL to GraphML format for Cytoscape"""
    
    print(f"Loading TTL file: {ttl_file}")
    
    # Load the TTL file
    g = Graph()
    g.parse(ttl_file, format='turtle')
    
    print(f"Loaded {len(g)} triples")
    
    # Create NetworkX graph
    nx_graph = nx.Graph()
    
    # Track node types for better visualization
    node_types = {}
    
    # Add nodes and edges
    for s, p, o in g:
        # Only add edges between URI nodes (not literals)
        if isinstance(o, (URIRef, BNode)):
            # Extract labels for nodes
            s_label = str(s).split('#')[-1] if '#' in str(s) else str(s)
            o_label = str(o).split('#')[-1] if '#' in str(o) else str(o)
            
            # Add nodes with labels and types
            if str(s) not in nx_graph.nodes:
                node_type = "Unknown"
                if any(t in str(s) for t in ["Individual", "Organization", "Testimony"]):
                    node_type = "Individual" if "Individual" in str(s) else "Organization" if "Organization" in str(s) else "Testimony"
                elif any(t in str(s) for t in ["Bill", "Position"]):
                    node_type = "Bill" if "Bill" in str(s) else "Position"
                
                nx_graph.add_node(str(s), 
                                label=s_label, 
                                id=str(s),
                                node_type=node_type)
                node_types[str(s)] = node_type
            
            if str(o) not in nx_graph.nodes:
                node_type = "Unknown"
                if any(t in str(o) for t in ["Individual", "Organization", "Testimony"]):
                    node_type = "Individual" if "Individual" in str(o) else "Organization" if "Organization" in str(o) else "Testimony"
                elif any(t in str(o) for t in ["Bill", "Position"]):
                    node_type = "Bill" if "Bill" in str(o) else "Position"
                
                nx_graph.add_node(str(o), 
                                label=o_label, 
                                id=str(o),
                                node_type=node_type)
                node_types[str(o)] = node_type
            
            # Add edges with predicates
            predicate = str(p).split('#')[-1] if '#' in str(p) else str(p)
            nx_graph.add_edge(str(s), str(o), 
                            label=predicate, 
                            predicate=predicate,
                            weight=1)
    
    # Add node size based on degree (more connections = larger node)
    degrees = dict(nx_graph.degree())
    for node in nx_graph.nodes():
        nx_graph.nodes[node]['size'] = max(5, min(50, degrees[node] * 2))
    
    # Write GraphML file
    nx.write_graphml(nx_graph, graphml_file)
    
    print(f"✓ Converted to {graphml_file}")
    print(f"  Nodes: {nx_graph.number_of_nodes()}")
    print(f"  Edges: {nx_graph.number_of_edges()}")
    
    # Print node type distribution
    type_counts = {}
    for node, data in nx_graph.nodes(data=True):
        node_type = data.get('node_type', 'Unknown')
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    print("\nNode type distribution:")
    for node_type, count in sorted(type_counts.items()):
        print(f"  {node_type}: {count}")
    
    print(f"\n✓ Ready for Cytoscape!")
    print(f"1. Install RDFScape plugin in Cytoscape")
    print(f"2. File → Import → Network → From GraphML")
    print(f"3. Select: {graphml_file}")
    print(f"4. Apply Organic or Hierarchical layout")
    print(f"5. Use node_type for node coloring")

def main():
    ttl_file = "complete_updated_testimony_ontology.ttl"
    graphml_file = "testimony_graph.graphml"
    
    try:
        ttl_to_cytoscape(ttl_file, graphml_file)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have rdflib and networkx installed:")
        print("pip install rdflib networkx")

if __name__ == "__main__":
    main()
