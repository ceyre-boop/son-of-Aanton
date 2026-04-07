#!/usr/bin/env python3
"""
MASTER NODE - The Brain
A contained autonomous learning loop with human approval.

Scope Lock (C Variable): Everything runs through this file.
Nothing leaves the container without passing through here.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

# === SCOPE LOCK ===
# This is the "C variable" - everything is contained within this scope
CONTAINER_SCOPE = {
    "version": "1.0",
    "created": datetime.now().isoformat(),
    "seed_loaded": False,
    "cycles_completed": 0,
    "pending_changes": [],
    "approved_changes": [],
    "rejected_changes": []
}

# Paths (all within container)
VAULT_PATH = Path("vault")
STORAGE_PATH = VAULT_PATH / "storage"
INDEX_PATH = VAULT_PATH / "index.md"
SEED_PATH = VAULT_PATH / "seed.md"
PENDING_PATH = VAULT_PATH / "pending.json"

class MasterNode:
    """The brain. All operations flow through here."""
    
    def __init__(self):
        self.ensure_vault()
        self.load_state()
        print(f"[MASTER NODE] Initialized v{CONTAINER_SCOPE['version']}")
        print(f"[MASTER NODE] Scope locked. Container: {os.getcwd()}")
    
    def ensure_vault(self):
        """Create vault structure if missing."""
        VAULT_PATH.mkdir(exist_ok=True)
        STORAGE_PATH.mkdir(exist_ok=True)
        
        # Create seed if missing
        if not SEED_PATH.exists():
            self.create_seed()
    
    def create_seed(self):
        """Phase 2: Seed dataset - how to code in this environment."""
        seed_content = """# Seed Dataset: How This Environment Works

## Core Principles
- Everything lives in the `vault/` directory
- All knowledge is stored as markdown files
- Files connect via [[wikilinks]]
- The Master Node controls all operations
- Changes require human approval

## File Structure
```
vault/
├── index.md          # Knowledge graph index
├── seed.md           # This file - the rules
├── storage/          # Learned knowledge
│   ├── topic_1.md
│   └── topic_2.md
└── pending.json      # Changes awaiting approval
```

## Learning Loop
1. **Retrieve**: What do we know?
2. **Learn**: Find new information
3. **Process**: Extract meaning and usage
4. **Stage**: Add to pending.json
5. **Approve**: Human reviews diff
6. **Commit**: Write to vault
7. **Index**: Update knowledge graph

## Meaning Tags
When storing knowledge, tag by HOW to use it:
- `[concept]` - Core idea to understand
- `[howto]` - Step-by-step instructions
- `[reference]` - Look up when needed
- `[connect]` - Links to other concepts
- `[expand]` - Needs more research

## Approval Rules
- I will NOT change files without approval
- All changes staged in pending.json
- Human reviews before commit
- Rejected changes are logged but not applied
"""
        SEED_PATH.write_text(seed_content)
        print("[SEED] Created seed.md with environment rules")
    
    def load_state(self):
        """Load container state from disk."""
        state_file = VAULT_PATH / ".node_state.json"
        if state_file.exists():
            with open(state_file) as f:
                saved = json.load(f)
                CONTAINER_SCOPE.update(saved)
    
    def save_state(self):
        """Save container state to disk."""
        state_file = VAULT_PATH / ".node_state.json"
        with open(state_file, 'w') as f:
            json.dump(CONTAINER_SCOPE, f, indent=2)
    
    # === PHASE 3: THE LEARNING LOOP ===
    
    def retrieve(self, query=None):
        """Look up what we know."""
        from retrieve import retrieve_knowledge
        return retrieve_knowledge(query, STORAGE_PATH, INDEX_PATH)
    
    def learn(self, source="simulated"):
        """Pull new info and process meaning."""
        from learn import discover_new_knowledge
        new_knowledge = discover_new_knowledge(source, SEED_PATH, INDEX_PATH)
        
        if new_knowledge:
            self.stage_changes(new_knowledge)
            return new_knowledge
        return None
    
    def stage_changes(self, knowledge_list):
        """Add to pending - awaiting approval."""
        for item in knowledge_list:
            change = {
                "id": hashlib.md5(item['title'].encode()).hexdigest()[:8],
                "timestamp": datetime.now().isoformat(),
                "title": item['title'],
                "content": item['content'],
                "tags": item.get('tags', ['concept']),
                "status": "pending"
            }
            CONTAINER_SCOPE['pending_changes'].append(change)
        
        self.save_pending()
        print(f"[STAGE] {len(knowledge_list)} changes staged for approval")
    
    def save_pending(self):
        """Write pending changes to disk."""
        with open(PENDING_PATH, 'w') as f:
            json.dump(CONTAINER_SCOPE['pending_changes'], f, indent=2)
    
    # === PHASE 4: APPROVAL GATE ===
    
    def show_pending(self):
        """Display changes awaiting approval."""
        if not CONTAINER_SCOPE['pending_changes']:
            print("[APPROVAL] No pending changes")
            return
        
        print(f"\n[APPROVAL] {len(CONTAINER_SCOPE['pending_changes'])} changes pending:")
        print("-" * 50)
        
        for change in CONTAINER_SCOPE['pending_changes']:
            print(f"\nID: {change['id']}")
            print(f"Title: {change['title']}")
            print(f"Tags: {', '.join(change['tags'])}")
            print(f"Preview: {change['content'][:100]}...")
            print("-" * 50)
    
    def approve(self, change_id):
        """Human approves a change."""
        for change in CONTAINER_SCOPE['pending_changes']:
            if change['id'] == change_id:
                change['status'] = 'approved'
                CONTAINER_SCOPE['approved_changes'].append(change)
                CONTAINER_SCOPE['pending_changes'].remove(change)
                
                # Apply the change
                self.apply_change(change)
                self.save_pending()
                self.save_state()
                
                print(f"[APPROVE] {change_id} approved and applied")
                return True
        
        print(f"[ERROR] Change {change_id} not found")
        return False
    
    def reject(self, change_id):
        """Human rejects a change."""
        for change in CONTAINER_SCOPE['pending_changes']:
            if change['id'] == change_id:
                change['status'] = 'rejected'
                CONTAINER_SCOPE['rejected_changes'].append(change)
                CONTAINER_SCOPE['pending_changes'].remove(change)
                
                self.save_pending()
                self.save_state()
                
                print(f"[REJECT] {change_id} rejected and logged")
                return True
        
        print(f"[ERROR] Change {change_id} not found")
        return False
    
    def approve_all(self):
        """Approve all pending changes."""
        pending = CONTAINER_SCOPE['pending_changes'].copy()
        for change in pending:
            self.approve(change['id'])
    
    # === PHASE 5: THE NODE CONNECTS ===
    
    def apply_change(self, change):
        """Write approved knowledge to vault."""
        from change import write_knowledge, update_index
        
        # Write to storage
        filename = f"{change['id']}_{change['title'].replace(' ', '_').lower()[:30]}.md"
        filepath = STORAGE_PATH / filename
        
        write_knowledge(filepath, change)
        
        # Update index (knowledge graph)
        update_index(INDEX_PATH, change, STORAGE_PATH)
        
        print(f"[APPLY] Written to {filepath}")
    
    def run_cycle(self, source="simulated"):
        """Run one complete learning cycle."""
        print(f"\n{'='*60}")
        print(f"[CYCLE {CONTAINER_SCOPE['cycles_completed'] + 1}] Starting...")
        print(f"{'='*60}")
        
        # Step 1: Retrieve context
        context = self.retrieve()
        print(f"[RETRIEVE] Current knowledge: {len(context)} items")
        
        # Step 2: Learn
        new_knowledge = self.learn(source)
        if not new_knowledge:
            print("[LEARN] No new knowledge discovered")
            return
        
        # Step 3: Stage (automatic)
        # Changes are now in pending.json
        
        # Step 4: Stop for approval
        print(f"\n[HALT] Human approval required")
        self.show_pending()
        print(f"\n[COMMAND] Use node.approve('id') or node.reject('id')")
        print(f"[COMMAND] Or node.approve_all() to accept all")
        
        CONTAINER_SCOPE['cycles_completed'] += 1
        self.save_state()
    
    def status(self):
        """Show container status."""
        print(f"\n[CONTAINER STATUS]")
        print(f"Version: {CONTAINER_SCOPE['version']}")
        print(f"Cycles: {CONTAINER_SCOPE['cycles_completed']}")
        print(f"Pending: {len(CONTAINER_SCOPE['pending_changes'])}")
        print(f"Approved: {len(CONTAINER_SCOPE['approved_changes'])}")
        print(f"Rejected: {len(CONTAINER_SCOPE['rejected_changes'])}")
        print(f"Vault: {VAULT_PATH.absolute()}")

# === CLI INTERFACE ===

def main():
    """Run the Master Node."""
    node = MasterNode()
    
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "cycle":
            node.run_cycle()
        elif command == "status":
            node.status()
        elif command == "pending":
            node.show_pending()
        elif command == "approve" and len(sys.argv) > 2:
            node.approve(sys.argv[2])
        elif command == "reject" and len(sys.argv) > 2:
            node.reject(sys.argv[2])
        elif command == "approve-all":
            node.approve_all()
        else:
            print("Commands: cycle, status, pending, approve <id>, reject <id>, approve-all")
    else:
        # Interactive mode
        print("\n[INTERACTIVE MODE]")
        print("Commands: cycle, status, pending, approve <id>, reject <id>, approve-all, quit")
        
        while True:
            try:
                cmd = input("\n> ").strip().split()
                if not cmd:
                    continue
                
                if cmd[0] == "quit":
                    break
                elif cmd[0] == "cycle":
                    node.run_cycle()
                elif cmd[0] == "status":
                    node.status()
                elif cmd[0] == "pending":
                    node.show_pending()
                elif cmd[0] == "approve" and len(cmd) > 1:
                    node.approve(cmd[1])
                elif cmd[0] == "reject" and len(cmd) > 1:
                    node.reject(cmd[1])
                elif cmd[0] == "approve-all":
                    node.approve_all()
                else:
                    print("Unknown command")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[ERROR] {e}")
        
        print("\n[SHUTDOWN] Saving state...")
        node.save_state()

if __name__ == "__main__":
    main()
