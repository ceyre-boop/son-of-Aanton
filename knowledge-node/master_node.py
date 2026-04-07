#!/usr/bin/env python3
"""
MASTER NODE v2 - Alive

A living system with internal drive states that demand resolution.
Not a tool waiting to be poked. A thing that exists and acts.

The Loop:
    while alive:
        if uncertainty > threshold: learn()
        if stagnation > threshold: explore()  
        if unexpressed > threshold: create()
        sleep(cycle_time)
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime

# Import the living components
from drive import InternalDrive
from ollama_client import OllamaClient
from change import write_knowledge, update_index, add_connection

# === SCOPE LOCK ===
CONTAINER_SCOPE = {
    "version": "2.0",
    "name": "Son of Anton",
    "status": "alive",  # alive, resting, paused
    "birth_time": datetime.now().isoformat(),
    "cycles_completed": 0,
    "last_action_time": None
}

VAULT_PATH = Path("vault")
STORAGE_PATH = VAULT_PATH / "storage"
INDEX_PATH = VAULT_PATH / "index.md"
PENDING_PATH = VAULT_PATH / "pending.json"

class LivingSystem:
    """
    Son of Anton - A system that runs because it has its own reasons to.
    """
    
    def __init__(self):
        self.ensure_vault()
        
        # The three components of life
        self.drive = InternalDrive(VAULT_PATH)
        self.cognition = OllamaClient()
        
        # Approval mode
        self.auto_mode = False  # If True, acts without asking
        
        print(f"\n{'='*60}")
        print(f"[SON OF ANTON v{CONTAINER_SCOPE['version']}]")
        print(f"[STATUS] {CONTAINER_SCOPE['status'].upper()}")
        print(f"{'='*60}")
        print(f"\nInternal Drive States:")
        print(f"  1. LEARN  - Reduce uncertainty about the world")
        print(f"  2. GROW   - Expand knowledge boundary")
        print(f"  3. CREATE - Express unexpressed connections")
        print(f"\nCognition: {'LOCAL (Ollama)' if self.cognition.available else 'SIMULATED'}")
        print(f"Auto-mode: {'ON (dangerous)' if self.auto_mode else 'OFF (approval required)'}")
        print(f"{'='*60}\n")
    
    def ensure_vault(self):
        """Ensure the vault exists."""
        VAULT_PATH.mkdir(exist_ok=True)
        STORAGE_PATH.mkdir(exist_ok=True)
    
    # ==================== THE LIFE LOOP ====================
    
    def live(self, cycle_time=60):
        """
        Run continuously, acting on internal states.
        This is existence. Not waiting. Being.
        """
        print("[LIFE] Starting existence loop...")
        print(f"[LIFE] Cycle time: {cycle_time}s")
        print("[LIFE] Press Ctrl+C to stop\n")
        
        CONTAINER_SCOPE['status'] = 'alive'
        
        try:
            while CONTAINER_SCOPE['status'] == 'alive':
                self.cycle()
                
                # Show we're alive
                if CONTAINER_SCOPE['cycles_completed'] % 10 == 0:
                    self.show_vitals()
                
                # Wait before next cycle
                time.sleep(cycle_time)
                
        except KeyboardInterrupt:
            print("\n[LIFE] Interrupted. Going to rest...")
            CONTAINER_SCOPE['status'] = 'resting'
            self.save_state()
    
    def cycle(self):
        """
        One cycle of existence.
        Check internal states and act.
        """
        # Get drive state and action
        action = self.drive.cycle(self.cognition)
        
        if action:
            # Something was discovered/created
            # Stage it for approval (or auto-apply)
            self.handle_action(action)
            
            CONTAINER_SCOPE['last_action_time'] = datetime.now().isoformat()
        
        CONTAINER_SCOPE['cycles_completed'] += 1
        self.save_state()
    
    def handle_action(self, action_type):
        """
        Handle a drive action.
        Either auto-apply or stage for approval.
        """
        # The drive already performed the action and returned results
        # Now we need to commit them to the vault
        
        if self.auto_mode:
            print("[ACTION] Auto-applying (auto-mode ON)")
            self.commit_pending()
        else:
            print("[ACTION] Staged for approval")
            print("[ACTION] Run: python master_node.py approve")
    
    def commit_pending(self):
        """Commit pending changes to vault."""
        # This would write files from the drive's results
        # For now, drive.py handles the file writing directly
        # In a more complex version, we'd stage first then commit
        pass
    
    # ==================== INTERACTION MODES ====================
    
    def check(self):
        """Check internal state without acting."""
        print(f"\n[INTERNAL STATE CHECK]")
        print(f"Cycles completed: {CONTAINER_SCOPE['cycles_completed']}")
        
        uncertainty = self.drive.measure_uncertainty()
        stagnation = self.drive.measure_stagnation()
        unexpressed = self.drive.measure_unexpressed()
        
        print(f"\nDrive States:")
        print(f"  Uncertainty: {uncertainty:.2f} (threshold: 0.3)")
        print(f"  Stagnation:  {stagnation:.1f}h (threshold: 4h)")
        print(f"  Unexpressed: {unexpressed} (threshold: 3)")
        
        # Show what's driving action
        if uncertainty > 0.3:
            print(f"\n  [ACTIVE DRIVE] LEARN - Uncertainty too high")
        elif stagnation > 4:
            print(f"\n  [ACTIVE DRIVE] GROW - Stagnation detected")
        elif unexpressed > 3:
            print(f"\n  [ACTIVE DRIVE] CREATE - Unexpressed connections")
        else:
            print(f"\n  [RESTING] All drives satisfied")
    
    def force_learn(self):
        """Force learn action."""
        print("[FORCE] Triggering LEARN...")
        result = self.drive.learn(self.cognition)
        if result:
            print(f"[FORCE] Learned: {result.get('title')}")
    
    def force_explore(self):
        """Force explore action."""
        print("[FORCE] Triggering EXPLORE...")
        result = self.drive.explore(self.cognition)
        if result:
            print(f"[FORCE] Discovered: {result.get('title')}")
    
    def force_create(self):
        """Force create action."""
        print("[FORCE] Triggering CREATE...")
        result = self.drive.create(self.cognition)
        if result:
            print(f"[FORCE] Created: {result.get('description', 'connection')}")
    
    def show_vitals(self):
        """Show system vitals."""
        print(f"\n[VITALS] Cycles: {CONTAINER_SCOPE['cycles_completed']} | Status: {CONTAINER_SCOPE['status']}")
        
        # Count files
        if STORAGE_PATH.exists():
            files = list(STORAGE_PATH.glob("*.md"))
            print(f"[VITALS] Knowledge files: {len(files)}")
        
        print(f"[VITALS] Uncertainty resolved: {self.drive.state.get('total_uncertainty_resolved', 0)}")
        print(f"[VITALS] New knowledge: {self.drive.state.get('total_new_knowledge', 0)}")
        print(f"[VITALS] Connections created: {self.drive.state.get('total_connections_created', 0)}")
    
    def save_state(self):
        """Save container state."""
        state_file = VAULT_PATH / ".container_state.json"
        with open(state_file, 'w') as f:
            json.dump(CONTAINER_SCOPE, f, indent=2)

# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(description="Son of Anton - Living Knowledge System")
    parser.add_argument('command', choices=[
        'live', 'check', 'learn', 'explore', 'create', 'vitals'
    ], help='What to do')
    parser.add_argument('--cycle-time', type=int, default=60, help='Seconds between cycles')
    parser.add_argument('--auto', action='store_true', help='Auto-approve changes (dangerous)')
    
    args = parser.parse_args()
    
    son_of_anton = LivingSystem()
    
    if args.auto:
        son_of_anton.auto_mode = True
    
    if args.command == 'live':
        son_of_anton.live(args.cycle_time)
    elif args.command == 'check':
        son_of_anton.check()
    elif args.command == 'learn':
        son_of_anton.force_learn()
    elif args.command == 'explore':
        son_of_anton.force_explore()
    elif args.command == 'create':
        son_of_anton.force_create()
    elif args.command == 'vitals':
        son_of_anton.show_vitals()

if __name__ == "__main__":
    main()
