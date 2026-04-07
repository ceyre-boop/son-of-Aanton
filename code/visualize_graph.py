#!/usr/bin/env python3
"""
Knowledge Graph Visualizer for Son of Anton
Generates visualizations of the mathematical knowledge base
"""

import os
import re
import json
from datetime import datetime

# Try to import graphviz, fall back to text representation
try:
    from graphviz import Digraph
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
    print("Warning: graphviz not installed. Install with: pip install graphviz")

def extract_wikilinks(content):
    """Extract [[wikilinks]] from markdown content"""
    pattern = r'\[\[([^\]]+)\]\]'
    return re.findall(pattern, content)

def parse_vault(vault_dir='vault'):
    """Parse all markdown files in vault directory"""
    nodes = {}
    edges = []
    
    for filename in os.listdir(vault_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(vault_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        node_id = filename.replace('.md', '')
        
        # Extract title (first H1)
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else node_id
        
        # Detect rung based on content
        rung = detect_rung(content, node_id)
        
        nodes[node_id] = {
            'title': title,
            'rung': rung,
            'filename': filename
        }
        
        # Extract links
        links = extract_wikilinks(content)
        for link in links:
            edges.append((node_id, link))
    
    return nodes, edges

def detect_rung(content, node_id):
    """Detect which rung a file belongs to based on content analysis"""
    rung_keywords = {
        1: ['logic', 'proof', 'axiom', 'contradiction', 'incompleteness', 'true', 'false', 'valid', 'sound'],
        2: ['number', 'arithmetic', 'zero', 'infinity', 'peano', '1+1', 'numeral', 'division'],
        3: ['variable', 'equation', 'function', 'algebra', 'solve', 'identity', 'symmetry', 'group'],
        4: ['set', 'subset', 'union', 'intersection', 'russell', 'zfc', 'empty set', 'element'],
        5: ['graph', 'node', 'edge', 'path', 'centrality', 'adjacency', 'tree', 'cycle'],
        6: ['probability', 'bayes', 'conditional', 'uncertainty', 'prior', 'posterior', 'random'],
        7: ['information', 'entropy', 'shannon', 'compression', 'kolmogorov', 'bits', 'encoding']
    }
    
    content_lower = content.lower()
    node_lower = node_id.lower()
    
    for rung, keywords in rung_keywords.items():
        for kw in keywords:
            if kw in content_lower or kw in node_lower:
                return rung
    
    return 0  # Unknown rung

def generate_dot_visualization(nodes, edges, output_file='canvas/knowledge_graph'):
    """Generate Graphviz DOT visualization"""
    if not GRAPHVIZ_AVAILABLE:
        print("Graphviz not available. Generating text summary instead.")
        return generate_text_summary(nodes, edges)
    
    dot = Digraph(comment='Son of Anton Knowledge Graph')
    dot.attr(rankdir='TB', size='20,20')
    
    # Color scheme for rungs
    rung_colors = {
        0: '#cccccc',  # Unknown - gray
        1: '#ff6b6b',  # Logic - red
        2: '#4ecdc4',  # Arithmetic - teal
        3: '#45b7d1',  # Algebra - blue
        4: '#96ceb4',  # Set Theory - green
        5: '#ffeaa7',  # Graph Theory - yellow
        6: '#dfe6e9',  # Probability - light gray
        7: '#fd79a8'   # Information Theory - pink
    }
    
    # Add nodes
    for node_id, data in nodes.items():
        color = rung_colors.get(data['rung'], '#cccccc')
        dot.node(node_id, data['title'], 
                style='filled', 
                fillcolor=color,
                shape='box')
    
    # Add edges
    for source, target in edges:
        if target in nodes:  # Only add edges to existing nodes
            dot.edge(source, target)
    
    # Save
    dot.render(output_file, format='png', cleanup=True)
    print(f"Graph saved to {output_file}.png")
    return output_file + '.png'

def generate_text_summary(nodes, edges):
    """Generate text-based summary when graphviz unavailable"""
    output = []
    output.append("# Son of Anton Knowledge Graph Summary\n")
    output.append(f"Generated: {datetime.now().isoformat()}\n")
    output.append(f"Total Nodes: {len(nodes)}\n")
    output.append(f"Total Edges: {len(edges)}\n\n")
    
    # Group by rung
    rung_counts = {}
    for node_id, data in nodes.items():
        rung = data['rung']
        if rung not in rung_counts:
            rung_counts[rung] = []
        rung_counts[rung].append((node_id, data['title']))
    
    output.append("## Nodes by Rung\n")
    for rung in sorted(rung_counts.keys()):
        output.append(f"\n### Rung {rung}\n")
        for node_id, title in sorted(rung_counts[rung]):
            output.append(f"- [[{node_id}]]: {title}\n")
    
    # Edge summary
    output.append("\n## Connections\n")
    for source, target in sorted(edges):
        if target in nodes:
            output.append(f"- [[{source}]] → [[{target}]]\n")
    
    output_file = 'canvas/knowledge_graph_summary.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output)
    
    print(f"Summary saved to {output_file}")
    return output_file

def generate_canvas_json(nodes, edges, output_file='canvas/knowledge_graph.canvas'):
    """Generate Obsidian Canvas file"""
    canvas_data = {
        "nodes": [],
        "edges": []
    }
    
    # Position nodes in a grid based on rung
    positions = {}
    rung_y = {0: 0, 1: 100, 2: 300, 3: 500, 4: 700, 5: 900, 6: 1100, 7: 1300}
    rung_x = {rung: 0 for rung in range(8)}
    
    for node_id, data in nodes.items():
        rung = data['rung']
        x = rung_x[rung]
        y = rung_y[rung]
        rung_x[rung] += 250  # Spacing between nodes
        
        positions[node_id] = (x, y)
        
        canvas_data["nodes"].append({
            "id": node_id,
            "type": "file",
            "file": f"vault/{node_id}.md",
            "x": x,
            "y": y,
            "width": 200,
            "height": 100
        })
    
    # Add edges
    edge_id = 0
    for source, target in edges:
        if target in positions and source in positions:
            canvas_data["edges"].append({
                "id": f"edge_{edge_id}",
                "fromNode": source,
                "toNode": target
            })
            edge_id += 1
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, indent=2)
    
    print(f"Canvas file saved to {output_file}")
    return output_file

def main():
    """Main entry point"""
    print("Son of Anton Knowledge Graph Visualizer")
    print("=" * 40)
    
    # Ensure canvas directory exists
    os.makedirs('canvas', exist_ok=True)
    
    # Parse vault
    print("\nParsing vault...")
    nodes, edges = parse_vault()
    print(f"Found {len(nodes)} nodes and {len(edges)} edges")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    
    # Graphviz PNG
    graph_file = generate_dot_visualization(nodes, edges)
    
    # Obsidian Canvas
    canvas_file = generate_canvas_json(nodes, edges)
    
    print("\n" + "=" * 40)
    print("Visualization complete!")
    print(f"Files generated:")
    print(f"  - {graph_file}")
    print(f"  - {canvas_file}")
    print(f"\nOpen {canvas_file} in Obsidian to explore your knowledge graph.")

if __name__ == '__main__':
    main()
