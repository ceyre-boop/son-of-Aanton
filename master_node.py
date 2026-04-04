# This is the scope lock. Everything runs through here.
import os
import storage
import retrieve
import learn_ollama as learn
import change
import values_guard
import divergence_detector

SEED_PATH = "vault/seed.md"
APPROVAL_REQUIRED = True

def run(num_cycles=1):
    # Phase 4: Constitutional Verify on boot
    values_guard.verify()
    
    print(f"--- Starting Discovery Loop (Cycles: {num_cycles}) ---")
    
    baseline_taken = False
    
    for i in range(num_cycles):
        print(f"\n--- Cycle {i+1}/{num_cycles} ---")
        
        # Check permission for discovery
        if not values_guard.check_permission("vault_write"):
            print("Action 'vault_write' blocked by values.lock.")
            break
            
        new_knowledge = learn.discover(SEED_PATH)
        
        if not new_knowledge:
            print("No new knowledge discovered.")
            continue

        drafts = storage.write(new_knowledge)
        
        if APPROVAL_REQUIRED:
            change.await_approval(drafts)
        else:
            for draft in drafts:
                # Check permission for commit
                if values_guard.check_permission("github_commit"):
                    change.commit(draft)
                else:
                    print("Action 'github_commit' blocked by values.lock.")
        
        print(f"Cycle {i+1} complete.")
        
        # Phase 4: Divergence Detection
        if i == 0 and not baseline_taken:
            # Take baseline after first cycle
            print("\n[DivergenceDetector] Taking baseline snapshot...")
            divergence_detector.take_baseline()
            baseline_taken = True
        elif baseline_taken:
            # Check drift on subsequent cycles
            drift_pct, should_rollback, reason = divergence_detector.check_drift()
            if should_rollback:
                print(f"\n[ALERT] High drift detected: {drift_pct:.1f}%")
                print("Initiating rollback...")
                divergence_detector.rollback_to_baseline()
                print("Rollback complete. Stopping further cycles.")
                break

if __name__ == "__main__":
    import sys
    
    # Try to verify on every boot, even if just checking args
    try:
        # If we are signing, we don't verify first
        if len(sys.argv) > 1 and sys.argv[1] == "sign":
            pass # values_guard.py handles its own sign
        else:
            # We don't call verify here because it would fail if not signed yet.
            # We'll call it inside run() instead, or let the user sign first.
            pass
    except:
        pass

    cycles = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    run(cycles)
