# This is the scope lock. Everything runs through here.
import os
import storage
import retrieve
import learn_ollama as learn
import change
import values_guard
import divergence_detector
import toml

SEED_PATH = "vault/seed.md"
APPROVAL_REQUIRED = True

# SYSTEM MODE: "growth" or "maintenance"
# GROWTH: Drift detection OFF - system changes rapidly, no baseline exists
# MAINTENANCE: Drift detection ON - baseline established, watch for unexpected drift
SYSTEM_MODE = "growth"  # Switch to "maintenance" after ~30 clean cycles + baseline lock

def get_system_mode():
    """
    Read mode from values.lock [drift] section.
    Falls back to SYSTEM_MODE constant if not found.
    """
    try:
        with open("values.lock", "r") as f:
            config = toml.load(f)
            return config.get("drift", {}).get("mode", SYSTEM_MODE)
    except:
        return SYSTEM_MODE

def get_growth_cycles_required():
    """Get minimum cycles required before maintenance mode can activate."""
    try:
        with open("values.lock", "r") as f:
            config = toml.load(f)
            return config.get("drift", {}).get("growth_cycles_required", 30)
    except:
        return 30

def get_baseline_locked():
    """Check if baseline has been explicitly locked."""
    try:
        with open("values.lock", "r") as f:
            config = toml.load(f)
            return config.get("drift", {}).get("baseline_locked_at", "") != ""
    except:
        return False

def run(num_cycles=1):
    # Phase 4: Constitutional Verify on boot
    values_guard.verify()
    
    # Determine current mode
    current_mode = get_system_mode()
    growth_required = get_growth_cycles_required()
    baseline_locked = get_baseline_locked()
    
    print(f"--- Starting Discovery Loop (Cycles: {num_cycles}) ---")
    print(f"[System] Mode: {current_mode.upper()}")
    
    if current_mode == "maintenance":
        if not baseline_locked:
            print("[WARNING] Maintenance mode requested but no baseline locked!")
            print("[WARNING] Run: python divergence_detector.py lock_baseline")
            print("[WARNING] Falling back to GROWTH mode...")
            current_mode = "growth"
        else:
            print("[System] Drift detection: ACTIVE")
    else:
        print(f"[System] Drift detection: OFF (growth phase)")
        print(f"[System] Need {growth_required} cycles before maintenance mode")
    
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
        
        # Phase 4: Divergence Detection (MAINTENANCE MODE ONLY)
        if current_mode == "maintenance":
            if i == 0 and not baseline_taken:
                # Take baseline after first cycle in maintenance mode
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
        else:
            # GROWTH MODE: Just report cycle count toward maintenance threshold
            cycles_remaining = max(0, growth_required - (i + 1))
            if cycles_remaining > 0:
                print(f"[Growth] {cycles_remaining} more cycles until maintenance mode eligible")

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
