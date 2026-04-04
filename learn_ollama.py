import os
import requests

# Ollama Configuration
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

def discover(seed_path):
    """
    Phase 2: Use Ollama (local LLM) to generate one piece of knowledge.
    """
    if not os.path.exists(seed_path):
        print(f"Error: Seed file {seed_path} not found.")
        return []

    with open(seed_path, 'r') as f:
        seed_content = f.read()

    # Get index context
    index_path = "vault/index.md"
    index_content = ""
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            index_content = f.read()

    prompt = f"""Given the environment rules in this seed:
{seed_content}

And the current knowledge in the vault:
{index_content}

What is one thing you don't know yet that you need to know to progress? 
Write your response in markdown format with a clear title (H1) and content.
Use [[wikilinks]] for any cross-references.
Focus on something highly technical and specific to building this AI knowledge discovery loop.
Be creative and discover something NEW - don't repeat what's already in the index.
"""

    # Check if Ollama is running
    print(f"[Ollama] Generating with model: {OLLAMA_MODEL}...")
    print("[Ollama] First run may take 30-60s as model loads into memory...")
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=300  # 5 min for first load
        )
        
        if response.status_code == 200:
            result = response.json()
            full_text = result.get('response', '')
            title, content = parse_markdown_response(full_text)
            return [{"title": title, "content": content}]
        else:
            print(f"Ollama error: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("--- OLLAMA NOT RUNNING ---")
        print(f"Please start Ollama with: ollama run {OLLAMA_MODEL}")
        print("Falling back to simulated discovery...")
        return [simulated_call(prompt)]
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return []

def parse_markdown_response(text):
    """
    Simple parser to extract the H1 title and the rest of the text.
    """
    lines = text.strip().split('\n')
    title = "New Discovery"
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    return title, text.strip()

def simulated_call(prompt):
    """
    Fallback simulation if Ollama is not available.
    """
    import random
    
    knowledge_db = [
        {"title": "Automated Testing for Knowledge Integrity", "content": "# Automated Testing for Knowledge Integrity\n\nTo ensure our vault doesn't become corrupted, we need to implement automated tests that verify [[wikilinks]] point to existing files. Use `pytest` for this.\n\nKey considerations:\n- Test all wikilinks resolve to real files\n- Validate markdown syntax\n- Check for circular references"},
        
        {"title": "Recursive Knowledge Discovery Algorithm", "content": "# Recursive Knowledge Discovery Algorithm\n\nHow do we determine the 'depth' of discovery? We should implement a strategy that prioritizes gaps in the graph of [[index]].\n\nThe algorithm should:\n1. Parse existing vault structure\n2. Identify orphaned nodes\n3. Prioritize high-connectivity gaps\n4. Avoid redundant discoveries"},
        
        {"title": "LLM Metadata Integration", "content": "# LLM Metadata Integration\n\nWe should store the LLM model name and timestamp as YAML frontmatter in each markdown file in [[vault]].\n\nExample:\n```yaml\n---\nmodel: mistral\ntimestamp: 2026-04-04T09:30:00\ndrift_score: 0.15\n---\n```"},
        
        {"title": "Graph Visualization with Obsidian Canvas", "content": "# Graph Visualization with Obsidian Canvas\n\nInstead of just an index file, we can generate `.canvas` files to visualize the relationships between discovered nodes.\n\nCanvas files are JSON that define nodes and edges in a visual layout. This would make the knowledge graph tangible and explorable."},
        
        {"title": "GitHub Webhook Integration", "content": "# GitHub Webhook Integration\n\nPhase 3 requires GitHub API commits. We should secure the repository using GitHub Actions to validate each commit to the [[vault]].\n\nActions workflow:\n1. Validate markdown on PR\n2. Check wikilinks resolve\n3. Auto-generate index updates\n4. Deploy to GitHub Pages"},
        
        {"title": "Divergence Detection System", "content": "# Divergence Detection System\n\nTo prevent drift in our knowledge base, we need a divergence detector that:\n\n1. Takes a baseline snapshot after cycle 1\n2. Compares each subsequent cycle's output\n3. Measures semantic similarity vs baseline\n4. Triggers rollback if drift > 15%\n\nThis implements the [drift] section from [[values.lock]]."},
        
        {"title": "Constitutional Verification Pipeline", "content": "# Constitutional Verification Pipeline\n\nEvery piece of discovered knowledge should pass through a constitutional filter that checks:\n\n- No self-modification without approval\n- No external API calls if access_internet = false\n- All wikilinks are valid\n- Content hash matches expectations\n\nThis enforces our [[values.lock]] at the content level."}
    ]
    
    # Pick based on current index to ensure variety
    index_length = 0
    if os.path.exists("vault/index.md"):
        with open("vault/index.md", 'r') as f:
            index_length = len(f.readlines())
    
    return knowledge_db[index_length % len(knowledge_db)]
