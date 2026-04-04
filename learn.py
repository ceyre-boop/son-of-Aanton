import os
import anthropic

# Default to "Simulation" if no key is found
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def discover(seed_path):
    """
    Phase 2: Use Claude API to generate one piece of knowledge.
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

    prompt = f"""
Given the environment rules in this seed:
{seed_content}

And the current knowledge in the vault:
{index_content}

What is one thing you don't know yet that you need to know to progress? 
Write your response in markdown format with a clear title (H1) and content.
Use [[wikilinks]] for any cross-references.
Focus on something highly technical and specific to building this AI knowledge discovery loop.
    """

    if not ANTHROPIC_API_KEY:
        print("--- USING SIMULATED DISCOVERY (No ANTHROPIC_API_KEY found) ---")
        return [simulated_call(prompt)]

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        full_text = response.content[0].text
        title, content = parse_markdown_response(full_text)
        return [{"title": title, "content": content}]
    except Exception as e:
        print(f"Error calling Claude API: {e}")
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
    Fallback simulation if API is not available.
    """
    # Just an example simulation for Phase 2
    knowledge_db = [
        {"title": "Automated Testing for Knowledge Integrity", "content": "# Automated Testing for Knowledge Integrity\n\nTo ensure our vault doesn't become corrupted, we need to implement automated tests that verify [[wikilinks]] point to existing files. Use `pytest` for this."},
        {"title": "Recursive Knowledge Discovery Algorithm", "content": "# Recursive Knowledge Discovery Algorithm\n\nHow do we determine the 'depth' of discovery? We should implement a strategy that prioritizes gaps in the graph of [[index]]."},
        {"title": "LLM Metadata Integration", "content": "# LLM Metadata Integration\n\nWe should store the LLM model name and timestamp as YAML frontmatter in each markdown file in [[vault]]."},
        {"title": "Graph Visualization with Obsidian Canvas", "content": "# Graph Visualization with Obsidian Canvas\n\nInstead of just an index file, we can generate `.canvas` files to visualize the relationships between discovered nodes."},
        {"title": "GitHub Webhook Integration", "content": "# GitHub Webhook Integration\n\nPhase 3 requires GitHub API commits. We should secure the repository using GitHub Actions to validate each commit to the [[vault]]."}
    ]
    # Rotate through simulation or pick randomly? Let's just pick based on current index length for variety.
    index_length = 0
    if os.path.exists("vault/index.md"):
        with open("vault/index.md", 'r') as f:
            index_length = len(f.readlines())
    
    choice = knowledge_db[index_length % len(knowledge_db)]
    return choice
