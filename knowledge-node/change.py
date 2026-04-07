"""
CHANGE MODULE
Edits files and connects knowledge.
"""

from pathlib import Path
from datetime import datetime

def write_knowledge(filepath, knowledge):
    """
    Write knowledge to a markdown file.
    Formats with metadata and proper structure.
    """
    
    # Build content with metadata
    content = f"""---
discovered: {datetime.now().isoformat()}
tags: {', '.join(knowledge['tags'])}
id: {knowledge['id']}
status: approved
---

{knowledge['content']}

---
*Added by Master Node on {datetime.now().strftime('%Y-%m-%d')}*
*Tags: {', '.join(knowledge['tags'])}*
"""
    
    # Write file
    Path(filepath).write_text(content)

def update_index(index_path, knowledge, storage_path):
    """
    Update the knowledge graph index.
    Maintains connections between topics.
    """
    
    # Read existing index or create new
    if index_path.exists():
        index_content = index_path.read_text()
    else:
        index_content = "# Knowledge Graph Index\n\n"
    
    # Add new entry
    title = knowledge['title']
    tags = knowledge['tags']
    
    entry = f"\n## [[{title}]]\n"
    entry += f"- Tags: {', '.join(f'`{t}`' for t in tags)}\n"
    
    # Find related topics (simple text matching)
    related = find_related_topics(title, storage_path)
    if related:
        entry += f"- Related: {', '.join(f'[[{r}]]' for r in related[:3])}\n"
    
    # Append to index
    index_content += entry
    
    # Update stats section
    if "## Stats" not in index_content:
        index_content += "\n## Stats\n"
    
    # Write updated index
    index_path.write_text(index_content)

def find_related_topics(title, storage_path):
    """Find potentially related topics based on shared content."""
    related = []
    
    if not storage_path.exists():
        return related
    
    title_words = set(title.lower().split())
    
    for file in storage_path.glob("*.md"):
        if title.replace(' ', '_').lower() in file.stem.lower():
            continue  # Skip self
        
        content = file.read_text().lower()
        content_words = set(content.split())
        
        # Simple word overlap
        overlap = title_words & content_words
        if len(overlap) >= 2:  # At least 2 shared words
            # Extract title from file
            for line in content.split('\n'):
                if line.startswith('# '):
                    related.append(line[2:].strip())
                    break
    
    return related

def add_connection(target_file, links_to_add):
    """
    Add wikilink connections to an isolated file.
    Used by the CREATE objective.
    """
    if not target_file.exists():
        return False
    
    content = target_file.read_text()
    
    # Add connections section if not exists
    if "## Connections" not in content:
        content += "\n\n## Connections\n"
    
    # Add each link
    for link in links_to_add:
        link_text = f"- [[{link}]]\n"
        if link_text not in content:
            content += link_text
    
    target_file.write_text(content)
    return True

def create_diff(old_content, new_content):
    """
    Create a human-readable diff of changes.
    For approval review.
    """
    # Simple line-based diff
    old_lines = set(old_content.split('\n'))
    new_lines = set(new_content.split('\n'))
    
    added = new_lines - old_lines
    removed = old_lines - new_lines
    
    diff = ""
    if added:
        diff += "ADDED:\n" + '\n'.join(f"+ {line}" for line in added) + '\n'
    if removed:
        diff += "REMOVED:\n" + '\n'.join(f"- {line}" for line in removed) + '\n'
    
    return diff if diff else "No changes detected"
