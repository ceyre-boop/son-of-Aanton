import os
import re

VAULT_DIR = "vault"
INDEX_FILE = os.path.join(VAULT_DIR, "index.md")

def write(knowledge_list):
    """
    Writes knowledge entries into markdown files in /vault.
    Updates /vault/index.md with links.
    """
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)

    drafts = []
    for knowledge in knowledge_list:
        title = knowledge["title"]
        content = knowledge["content"]
        
        # Sanitize title for filename
        filename = re.sub(r'[^a-zA-Z0-9]', '_', title.lower()) + ".md"
        filepath = os.path.join(VAULT_DIR, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Created file: {filepath}")
        drafts.append(filepath)

    update_index()
    return drafts

def update_index():
    """
    Rebuilds the index file by listing all markdown files in the vault.
    """
    files = [f for f in os.listdir(VAULT_DIR) if f.endswith(".md") and f != "index.md"]
    files.sort()
    
    with open(INDEX_FILE, 'w') as f:
        f.write("# Knowledge Index\n")
        f.write("<!-- auto-generated, do not edit manually -->\n\n")
        
        for filename in files:
            title = filename[:-3] # Remove .md
            # Wikilink style
            f.write(f"- [[{title}]]\n")
    
    print(f"Updated index: {INDEX_FILE}")
