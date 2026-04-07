"""
RETRIEVE MODULE
Looks up what the system knows.
"""

import re
from pathlib import Path

def retrieve_knowledge(query=None, storage_path=None, index_path=None):
    """
    Retrieve knowledge from the vault.
    Returns list of knowledge items.
    """
    knowledge = []
    
    # Read index for overview
    if index_path and index_path.exists():
        index_content = index_path.read_text()
        # Extract wikilinks as knowledge nodes
        links = re.findall(r'\[\[([^\]]+)\]\]', index_content)
        knowledge.extend([{"type": "link", "content": link} for link in links])
    
    # Read all storage files
    if storage_path and storage_path.exists():
        for file in storage_path.glob("*.md"):
            content = file.read_text()
            
            # Extract title (first H1)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file.stem
            
            # Extract tags
            tags = re.findall(r'\[(concept|howto|reference|connect|expand)\]', content)
            
            knowledge.append({
                "file": str(file),
                "title": title,
                "content": content[:500],  # Preview
                "tags": tags
            })
    
    # Filter by query if provided
    if query:
        query_lower = query.lower()
        knowledge = [k for k in knowledge 
                    if query_lower in str(k).lower()]
    
    return knowledge

def get_related_topics(topic, storage_path):
    """Find topics related to a given topic."""
    related = []
    
    if not storage_path.exists():
        return related
    
    for file in storage_path.glob("*.md"):
        content = file.read_text().lower()
        if topic.lower() in content:
            # Extract title
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                related.append(title_match.group(1))
    
    return related
