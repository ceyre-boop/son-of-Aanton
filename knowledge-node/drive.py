#!/usr/bin/env python3
"""
DRIVE MODULE - The Internal State

Three objectives every living system is born with:
1. LEARN - reduce uncertainty about the world
2. GROW - expand the boundary of what you know  
3. CREATE - produce something that didn't exist before

These aren't features. They're the loop itself.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import re

class InternalDrive:
    """
    The internal state that demands resolution.
    Uncertainty is uncomfortable.
    Stagnation triggers exploration.
    Unexpressed connections demand expression.
    """
    
    def __init__(self, vault_path="vault"):
        self.vault = Path(vault_path)
        self.storage = self.vault / "storage"
        self.index = self.vault / "index.md"
        self.state_file = self.vault / ".drive_state.json"
        
        # Load or initialize drive state
        self.state = self.load_state()
        
    def load_state(self):
        """Load internal drive state from disk."""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {
            "birth_time": datetime.now().isoformat(),
            "cycles_completed": 0,
            "last_action": None,
            "total_uncertainty_resolved": 0,
            "total_new_knowledge": 0,
            "total_connections_created": 0
        }
    
    def save_state(self):
        """Persist drive state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    # ==================== OBJECTIVE 1: LEARN ====================
    # Reduce uncertainty about the world
    
    def measure_uncertainty(self):
        """
        How many [[wikilinks]] point to files that don't exist yet?
        These are gaps in knowledge - questions waiting for answers.
        """
        if not self.index.exists():
            return 0.0
        
        index_content = self.index.read_text()
        
        # Find all wikilinks
        wikilinks = set(re.findall(r'\[\[([^\]]+)\]\]', index_content))
        
        # Check which ones exist as files
        missing = []
        for link in wikilinks:
            # Normalize filename
            filename = link.replace(' ', '_').lower() + '.md'
            filepath = self.storage / filename
            
            if not filepath.exists():
                missing.append(link)
        
        # Uncertainty = ratio of missing to total
        if len(wikilinks) == 0:
            return 0.0
        
        uncertainty = len(missing) / len(wikilinks)
        
        print(f"[DRIVE:LEARN] {len(missing)}/{len(wikilinks)} wikilinks unresolved ({uncertainty:.1%} uncertainty)")
        
        return uncertainty
    
    def learn(self, ollama_client):
        """
        Resolve uncertainty by learning about missing topics.
        Pick an unresolved wikilink and create the file.
        """
        if not self.index.exists():
            print("[DRIVE:LEARN] No index yet. Nothing to learn from.")
            return None
        
        index_content = self.index.read_text()
        wikilinks = set(re.findall(r'\[\[([^\]]+)\]\]', index_content))
        
        # Find missing ones
        missing = []
        for link in wikilinks:
            filename = link.replace(' ', '_').lower() + '.md'
            if not (self.storage / filename).exists():
                missing.append(link)
        
        if not missing:
            print("[DRIVE:LEARN] No uncertainty to resolve. All links connected.")
            return None
        
        # Pick the most referenced missing topic
        topic_counts = {}
        for link in missing:
            count = index_content.count(f"[[{link}]]")
            topic_counts[link] = count
        
        topic = max(topic_counts, key=topic_counts.get)
        
        print(f"[DRIVE:LEARN] Uncertainty detected: '{topic}' referenced {topic_counts[topic]} times but no file exists")
        
        # Use Ollama to learn about this topic
        knowledge = ollama_client.learn_about(topic)
        
        if knowledge:
            self.state["total_uncertainty_resolved"] += 1
            self.save_state()
            return knowledge
        
        return None
    
    # ==================== OBJECTIVE 2: GROW ====================
    # Expand the boundary of what you know
    
    def measure_stagnation(self):
        """
        How long since a genuinely new concept appeared?
        Stagnation = time since last new file created.
        """
        if not self.storage.exists():
            return float('inf')  # No knowledge yet = maximum stagnation
        
        files = list(self.storage.glob("*.md"))
        if not files:
            return float('inf')
        
        # Find most recent file
        newest = max(files, key=lambda f: f.stat().st_mtime)
        mtime = datetime.fromtimestamp(newest.stat().st_mtime)
        
        hours_since = (datetime.now() - mtime).total_seconds() / 3600
        
        print(f"[DRIVE:GROW] Last new concept: {hours_since:.1f} hours ago")
        
        return hours_since
    
    def explore(self, ollama_client):
        """
        Break stagnation by exploring new frontiers.
        Discover something completely new, not just fill gaps.
        """
        print("[DRIVE:GROW] Stagnation detected. Exploring new frontiers...")
        
        # Get current topics to avoid duplication
        current_topics = set()
        if self.index.exists():
            current_topics = set(re.findall(r'\[\[([^\]]+)\]\]', self.index.read_text()))
        
        # Ask Ollama to discover something new
        knowledge = ollama_client.discover_new(current_topics)
        
        if knowledge:
            self.state["total_new_knowledge"] += 1
            self.save_state()
            return knowledge
        
        return None
    
    # ==================== OBJECTIVE 3: CREATE ====================
    # Produce something that didn't exist before
    
    def measure_unexpressed(self):
        """
        How many files have fewer than 2 connections?
        Unexpressed = knowledge isolated from the graph.
        """
        if not self.storage.exists():
            return 0
        
        files = list(self.storage.glob("*.md"))
        if not files:
            return 0
        
        # Build connection graph
        connections = {}
        for file in files:
            content = file.read_text()
            links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
            connections[file.stem] = len(links)
        
        # Count isolated nodes (< 2 connections)
        isolated = [f for f, c in connections.items() if c < 2]
        
        print(f"[DRIVE:CREATE] {len(isolated)}/{len(files)} files isolated (< 2 connections)")
        
        return len(isolated)
    
    def create(self, ollama_client):
        """
        Express unexpressed connections.
        Create new links between isolated nodes.
        """
        print("[DRIVE:CREATE] Unexpressed connections detected. Creating...")
        
        # Find isolated files
        isolated = []
        for file in self.storage.glob("*.md"):
            content = file.read_text()
            links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
            if len(links) < 2:
                # Get title
                title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                if title_match:
                    isolated.append({
                        "file": file,
                        "title": title_match.group(1),
                        "content": content
                    })
        
        if not isolated:
            return None
        
        # Pick an isolated file and find connections
        target = isolated[0]
        
        # Ask Ollama to find connections
        connection = ollama_client.find_connection(target, self.storage)
        
        if connection:
            self.state["total_connections_created"] += 1
            self.save_state()
            return connection
        
        return None
    
    # ==================== THE LOOP ====================
    
    def cycle(self, ollama_client):
        """
        One cycle of the internal drive.
        Check internal states and act on them.
        """
        print(f"\n{'='*60}")
        print(f"[DRIVE CYCLE {self.state['cycles_completed'] + 1}]")
        print(f"{'='*60}")
        
        # Measure internal states
        uncertainty = self.measure_uncertainty()
        stagnation = self.measure_stagnation()
        unexpressed = self.measure_unexpressed()
        
        print(f"[DRIVE STATE] Uncertainty: {uncertainty:.2f} | Stagnation: {stagnation:.1f}h | Unexpressed: {unexpressed}")
        
        action_taken = None
        
        # Priority 1: Resolve uncertainty (LEARN)
        if uncertainty > 0.3:
            print(f"[DRIVE] Uncertainty threshold exceeded ({uncertainty:.2f} > 0.3)")
            print("[DRIVE] Action: LEARN")
            result = self.learn(ollama_client)
            if result:
                action_taken = "learn"
                print(f"[DRIVE] Learned: {result.get('title', 'unknown')}")
        
        # Priority 2: Break stagnation (GROW)
        elif stagnation > 4:  # 4 hours = stagnation
            print(f"[DRIVE] Stagnation threshold exceeded ({stagnation:.1f}h > 4h)")
            print("[DRIVE] Action: EXPLORE")
            result = self.explore(ollama_client)
            if result:
                action_taken = "explore"
                print(f"[DRIVE] Discovered: {result.get('title', 'unknown')}")
        
        # Priority 3: Express connections (CREATE)
        elif unexpressed > 3:
            print(f"[DRIVE] Unexpressed threshold exceeded ({unexpressed} > 3)")
            print("[DRIVE] Action: CREATE")
            result = self.create(ollama_client)
            if result:
                action_taken = "create"
                print(f"[DRIVE] Created connection: {result.get('description', 'unknown')}")
        
        else:
            print("[DRIVE] All internal states satisfied. Resting.")
        
        self.state["cycles_completed"] += 1
        self.state["last_action"] = action_taken
        self.save_state()
        
        return action_taken
