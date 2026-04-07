"""
LEARN MODULE
Pulls new information and processes meaning.
"""

import random
import re
from pathlib import Path

# Simulated knowledge database (in real use, this would be API calls, web scraping, etc.)
KNOWLEDGE_DB = [
    {
        "title": "Graph Database Basics",
        "content": """# Graph Database Basics

A graph database stores data in nodes and edges rather than tables.

[concept] Core concepts:
- Nodes represent entities
- Edges represent relationships  
- Properties describe both

[howto] When to use:
- Complex relationships
- Network analysis
- Recommendation engines

[connect] See also: [[SQL vs NoSQL]], [[Database Design]]
""",
        "tags": ["concept", "howto", "connect"]
    },
    {
        "title": "Markdown for Knowledge Management",
        "content": """# Markdown for Knowledge Management

Why markdown is ideal for knowledge graphs:

[concept] Plain text benefits:
- Human readable
- Version control friendly
- Universal format

[howto] Best practices:
- Use [[wikilinks]] for connections
- Tag with [concept], [howto], [reference]
- Keep files focused on one topic

[expand] Research needed:
- Obsidian plugins
- Zettelkasten method
- Backlink analysis
""",
        "tags": ["concept", "howto", "expand"]
    },
    {
        "title": "Human-in-the-Loop AI",
        "content": """# Human-in-the-Loop AI

AI systems that require human approval for critical decisions.

[concept] Why it matters:
- Safety and control
- Quality assurance
- Learning from feedback

[howto] Implementation:
1. Stage changes automatically
2. Present diff for review
3. Human approves/rejects
4. System learns from decision

[reference] Use cases:
- Content moderation
- Medical diagnosis
- Financial trading
""",
        "tags": ["concept", "howto", "reference"]
    },
    {
        "title": "Self-Modifying Code",
        "content": """# Self-Modifying Code

Programs that can change their own behavior at runtime.

[concept] Approaches:
- Configuration files
- Plugin systems
- Runtime compilation

[howto] Safe practices:
- Sandbox changes
- Version everything
- Rollback capability
- Human approval gates

[expand] Research:
- Genetic algorithms
- Neural architecture search
- Program synthesis
""",
        "tags": ["concept", "howto", "expand"]
    },
    {
        "title": "Knowledge Graph Embeddings",
        "content": """# Knowledge Graph Embeddings

Representing graph nodes as vectors in continuous space.

[concept] Key idea:
- Similar nodes = close vectors
- Relationships = vector operations
- Enables ML on graphs

[howto] Common techniques:
- Node2Vec
- TransE
- GraphSAGE

[connect] Related: [[Graph Neural Networks]], [[Vector Databases]]
""",
        "tags": ["concept", "howto", "connect"]
    }
]

def discover_new_knowledge(source="simulated", seed_path=None, index_path=None):
    """
    Discover new knowledge to learn.
    
    In a real system, this would:
    - Query APIs
    - Scrape websites
    - Read documents
    - Analyze data
    """
    
    if source == "simulated":
        # Pick random knowledge not yet in index
        existing_titles = set()
        if index_path and index_path.exists():
            content = index_path.read_text()
            existing_titles = set(re.findall(r'\[\[([^\]]+)\]\]', content))
        
        # Filter out already known
        unknown = [k for k in KNOWLEDGE_DB if k['title'] not in existing_titles]
        
        if unknown:
            # Pick 1-2 random items
            count = min(random.randint(1, 2), len(unknown))
            selected = random.sample(unknown, count)
            
            # Process meaning
            processed = []
            for item in selected:
                processed.append(process_meaning(item))
            
            return processed
        else:
            print("[LEARN] No new knowledge in simulated database")
            return None
    
    elif source == "api":
        # Placeholder for real API integration
        print("[LEARN] API mode not yet implemented")
        return None
    
    else:
        print(f"[LEARN] Unknown source: {source}")
        return None

def process_meaning(knowledge_item):
    """
    Process raw knowledge to extract meaning and usage.
    
    Tags knowledge by HOW to use it:
    - [concept] - Understand this
    - [howto] - Follow these steps
    - [reference] - Look up when needed
    - [connect] - Links to other knowledge
    - [expand] - Needs more research
    """
    
    content = knowledge_item['content']
    
    # Extract explicit tags
    explicit_tags = re.findall(r'\[(concept|howto|reference|connect|expand)\]', content)
    
    # Auto-tag based on content if no explicit tags
    auto_tags = []
    if 'how to' in content.lower() or 'steps' in content.lower():
        auto_tags.append('howto')
    if 'see also' in content.lower() or 'related' in content.lower():
        auto_tags.append('connect')
    if 'research' in content.lower() or 'todo' in content.lower():
        auto_tags.append('expand')
    
    # Combine tags
    all_tags = list(set(explicit_tags + auto_tags))
    if not all_tags:
        all_tags = ['concept']  # Default
    
    return {
        "title": knowledge_item['title'],
        "content": content,
        "tags": all_tags,
        "discovered": True
    }

def extract_wikilinks(content):
    """Extract [[wikilinks]] from content."""
    return re.findall(r'\[\[([^\]]+)\]\]', content)
