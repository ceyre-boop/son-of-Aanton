"""
OLLAMA CLIENT - Local Cognition

The thinking happens inside the box.
Not a rental. Real. Independent. Free. Private.
"""

import requests
import json
from pathlib import Path

class OllamaClient:
    """
    Son of Anton's actual cognition.
    Not Anthropic's servers. His own.
    """
    
    def __init__(self, host="http://localhost:11434", model="llama3.2"):
        self.host = host
        self.model = model
        self.available = self.check_connection()
        
        if self.available:
            print(f"[OLLAMA] Connected to {model} at {host}")
            print("[OLLAMA] Cognition is local. Thinking is free.")
        else:
            print("[OLLAMA] Not available. Run: ollama run llama3.2")
            print("[OLLAMA] Will use simulation mode.")
    
    def check_connection(self):
        """Check if Ollama is running."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', '').split(':')[0] for m in models]
                return self.model in model_names or any(self.model in m for m in model_names)
            return False
        except:
            return False
    
    def think(self, prompt, system=None, temperature=0.7):
        """
        Generate a thought.
        This is Son of Anton's actual cognition.
        """
        if not self.available:
            return None
        
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system or "",
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": 800
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                print(f"[OLLAMA] Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[OLLAMA] Failed: {e}")
            return None
    
    # ==================== LEARN OBJECTIVE ====================
    
    def learn_about(self, topic):
        """
        Resolve uncertainty by learning about a topic.
        Called when there's a missing wikilink.
        """
        print(f"[OLLAMA] Learning about: {topic}")
        
        system = """You are a knowledge synthesizer. 
Create a concise markdown document about the given topic.
Use [[wikilinks]] to connect to related concepts.
Tag with [concept], [howto], [reference], or [expand] to indicate how to use this knowledge.

Format:
# Title

[tag] Brief description

## Key Points
- Point 1
- Point 2

## Connections
- [[Related Topic 1]]
- [[Related Topic 2]]

## Usage
[howto] How to apply this knowledge"""

        prompt = f"Create a knowledge document about: {topic}\n\nMake it useful, accurate, and connected to other concepts."
        
        response = self.think(prompt, system=system)
        
        if response:
            return self.parse_knowledge(response, topic)
        
        return None
    
    # ==================== GROW OBJECTIVE ====================
    
    def discover_new(self, existing_topics):
        """
        Discover something completely new.
        Called during stagnation to expand knowledge boundary.
        """
        print(f"[OLLAMA] Discovering new knowledge...")
        
        existing_list = ', '.join(list(existing_topics)[:10])
        
        system = """You are a research assistant discovering new knowledge.
Find a topic that expands the current knowledge base in an unexpected but valuable direction.
Return a markdown document with the new knowledge.

Use tags: [concept] for ideas, [howto] for methods, [reference] for facts, [expand] for questions."""

        prompt = f"""Current knowledge covers: {existing_list}

Discover a NEW topic that:
1. Is not in the current list
2. Connects to existing knowledge in surprising ways
3. Expands the boundary of what is known
4. Is practical and useful

What should we learn next?"""

        response = self.think(prompt, system=system, temperature=0.8)
        
        if response:
            return self.parse_knowledge(response, None)
        
        return None
    
    # ==================== CREATE OBJECTIVE ====================
    
    def find_connection(self, isolated_file, storage_path):
        """
        Find connections for an isolated file.
        Called when there are unexpressed connections.
        """
        print(f"[OLLAMA] Finding connections for: {isolated_file['title']}")
        
        # Get other files for context
        other_files = []
        for f in storage_path.glob("*.md"):
            if f != isolated_file['file']:
                content = f.read_text()
                title_match = __import__('re').search(r'^# (.+)$', content, __import__('re').MULTILINE)
                if title_match:
                    other_files.append(title_match.group(1))
        
        context = ', '.join(other_files[:5])
        
        system = """You are a connection finder.
Given an isolated knowledge file and a list of other topics,
identify meaningful connections between them.

Return a brief description of the connection and which topics to link."""

        prompt = f"""Isolated topic: {isolated_file['title']}
Content preview: {isolated_file['content'][:300]}...

Other topics in vault: {context}

What connections exist? How does this topic relate to others?
Suggest 2-3 specific wikilinks to add."""

        response = self.think(prompt, system=system)
        
        if response:
            return {
                "type": "connection",
                "target_file": isolated_file['file'],
                "target_title": isolated_file['title'],
                "description": response,
                "links": self.extract_links(response)
            }
        
        return None
    
    # ==================== HELPERS ====================
    
    def parse_knowledge(self, text, default_topic):
        """Parse Ollama response into structured knowledge."""
        import re
        
        # Extract title
        title_match = re.search(r'^# (.+)$', text, re.MULTILINE)
        title = title_match.group(1) if title_match else (default_topic or "New Knowledge")
        
        # Extract tags
        tags = re.findall(r'\[(concept|howto|reference|expand)\]', text)
        if not tags:
            tags = ['concept']
        
        return {
            "title": title,
            "content": text,
            "tags": list(set(tags)),
            "source": "ollama",
            "model": self.model
        }
    
    def extract_links(self, text):
        """Extract suggested wikilinks from text."""
        import re
        # Look for [[Topic]] or "Topic" mentions
        links = re.findall(r'\[\[([^\]]+)\]\]', text)
        
        # Also look for quoted topics
        quoted = re.findall(r'"([^"]+)"', text)
        
        return links + [q for q in quoted if len(q) < 50]
