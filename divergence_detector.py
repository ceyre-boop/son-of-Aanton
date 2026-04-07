"""
divergence_detector.py - Safety net for knowledge drift

Compares current output against baseline to detect drift > 15%.
Implements the [drift] section from values.lock.
"""
import os
import json
import hashlib
from datetime import datetime

SNAPSHOT_DIR = "vault/snapshots"
DRIFT_THRESHOLD = 0.15  # 15% drift triggers rollback

def take_baseline():
    """
    Capture baseline snapshot after cycle 1.
    Returns snapshot ID.
    """
    if not os.path.exists(SNAPSHOT_DIR):
        os.makedirs(SNAPSHOT_DIR)
    
    # Read current vault state
    vault_files = []
    vault_dir = "vault"
    
    for filename in os.listdir(vault_dir):
        if filename.endswith('.md') and filename != 'index.md':
            filepath = os.path.join(vault_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                vault_files.append({
                    'filename': filename,
                    'content': content,
                    'hash': hashlib.sha256(content.encode()).hexdigest()[:16]
                })
    
    # Create snapshot
    snapshot = {
        'timestamp': datetime.now().isoformat(),
        'files': vault_files,
        'file_count': len(vault_files),
        'total_chars': sum(len(f['content']) for f in vault_files)
    }
    
    snapshot_id = f"v1_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    snapshot_path = os.path.join(SNAPSHOT_DIR, f"{snapshot_id}.json")
    
    with open(snapshot_path, 'w') as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"[DivergenceDetector] Baseline snapshot created: {snapshot_id}")
    print(f"  Files: {snapshot['file_count']}")
    print(f"  Total chars: {snapshot['total_chars']}")
    
    return snapshot_id

def calculate_drift(current_files, baseline_files):
    """
    Calculate drift percentage between current and baseline.
    Uses simple heuristic: new files + modified files vs total.
    """
    baseline_map = {f['filename']: f for f in baseline_files}
    current_map = {f['filename']: f for f in current_files}
    
    # Count changes
    new_files = 0
    modified_files = 0
    unchanged_files = 0
    
    for filename, current in current_map.items():
        if filename not in baseline_map:
            new_files += 1
        elif current['hash'] != baseline_map[filename]['hash']:
            modified_files += 1
        else:
            unchanged_files += 1
    
    # Also count deleted files
    deleted_files = len([f for f in baseline_map if f not in current_map])
    
    # Calculate drift
    total_baseline = len(baseline_files)
    if total_baseline == 0:
        return 0.0
    
    # Drift = (new + modified + deleted) / baseline
    drift = (new_files + modified_files + deleted_files) / total_baseline
    
    return drift

def check_drift(baseline_id=None):
    """
    Check current vault against baseline.
    Returns (drift_percentage, should_rollback, reason)
    """
    # Find latest baseline if not specified
    if not baseline_id:
        if not os.path.exists(SNAPSHOT_DIR):
            print("[DivergenceDetector] No snapshots found. Run take_baseline() first.")
            return 0.0, False, "No baseline"
        
        snapshots = [f for f in os.listdir(SNAPSHOT_DIR) if f.endswith('.json')]
        if not snapshots:
            print("[DivergenceDetector] No snapshots found. Run take_baseline() first.")
            return 0.0, False, "No baseline"
        
        baseline_id = sorted(snapshots)[0].replace('.json', '')
    
    # Load baseline
    baseline_path = os.path.join(SNAPSHOT_DIR, f"{baseline_id}.json")
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    
    # Capture current state
    current_files = []
    vault_dir = "vault"
    
    for filename in os.listdir(vault_dir):
        if filename.endswith('.md') and filename != 'index.md':
            filepath = os.path.join(vault_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                current_files.append({
                    'filename': filename,
                    'content': content,
                    'hash': hashlib.sha256(content.encode()).hexdigest()[:16]
                })
    
    # Calculate drift
    drift = calculate_drift(current_files, baseline['files'])
    drift_pct = drift * 100
    
    print(f"[DivergenceDetector] Drift check:")
    print(f"  Baseline: {baseline_id}")
    print(f"  Baseline files: {baseline['file_count']}")
    print(f"  Current files: {len(current_files)}")
    print(f"  Drift: {drift_pct:.1f}%")
    print(f"  Threshold: {DRIFT_THRESHOLD*100:.0f}%")
    
    should_rollback = drift > DRIFT_THRESHOLD
    
    if should_rollback:
        reason = f"Drift {drift_pct:.1f}% exceeds threshold {DRIFT_THRESHOLD*100:.0f}%"
        print(f"  [ALERT] {reason}")
        print(f"  [ACTION] Rollback recommended")
    else:
        reason = f"Drift {drift_pct:.1f}% within acceptable range"
        print(f"  [OK] {reason}")
    
    return drift_pct, should_rollback, reason

def rollback_to_baseline(baseline_id=None):
    """
    Restore vault to baseline state.
    """
    import shutil
    
    if not baseline_id:
        # Find latest baseline
        if not os.path.exists(SNAPSHOT_DIR):
            print("[DivergenceDetector] No snapshots to rollback to.")
            return False
        
        snapshots = [f for f in os.listdir(SNAPSHOT_DIR) if f.endswith('.json')]
        if not snapshots:
            print("[DivergenceDetector] No snapshots to rollback to.")
            return False
        
        baseline_id = sorted(snapshots)[0].replace('.json', '')
    
    # Load baseline
    baseline_path = os.path.join(SNAPSHOT_DIR, f"{baseline_id}.json")
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    
    # Move current files to discarded
    discarded_dir = "vault/discarded"
    if not os.path.exists(discarded_dir):
        os.makedirs(discarded_dir)
    
    vault_dir = "vault"
    for filename in os.listdir(vault_dir):
        if filename.endswith('.md') and filename != 'index.md':
            src = os.path.join(vault_dir, filename)
            dst = os.path.join(discarded_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
            shutil.move(src, dst)
    
    # Restore baseline files
    for file_info in baseline['files']:
        filepath = os.path.join(vault_dir, file_info['filename'])
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_info['content'])
    
    print(f"[DivergenceDetector] Rollback complete to {baseline_id}")
    print(f"  Restored {len(baseline['files'])} files")
    
    return True

def lock_baseline():
    """
    Lock the current state as the official baseline.
    This transitions from GROWTH to MAINTENANCE mode.
    Updates values.lock with baseline_locked_at timestamp.
    """
    import toml
    
    # Take a fresh baseline snapshot
    snapshot_id = take_baseline()
    
    # Update values.lock
    values_lock_path = "values.lock"
    try:
        with open(values_lock_path, "r") as f:
            config = toml.load(f)
    except:
        config = {}
    
    if "drift" not in config:
        config["drift"] = {}
    
    config["drift"]["baseline_locked_at"] = datetime.now().isoformat()
    config["drift"]["mode"] = "maintenance"
    
    with open(values_lock_path, "w") as f:
        toml.dump(config, f)
    
    print(f"\n[DivergenceDetector] BASELINE LOCKED: {snapshot_id}")
    print("[DivergenceDetector] System transitioned to MAINTENANCE mode")
    print("[DivergenceDetector] Drift detection is now ACTIVE")
    print(f"\nNext run: python master_node.py 5")
    
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "baseline":
        take_baseline()
    elif len(sys.argv) > 1 and sys.argv[1] == "check":
        drift, should_rollback, reason = check_drift()
        if should_rollback:
            print("\nRollback? (y/n): ", end="")
            response = input().strip().lower()
            if response == 'y':
                rollback_to_baseline()
    elif len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback_to_baseline()
    elif len(sys.argv) > 1 and sys.argv[1] == "lock_baseline":
        lock_baseline()
    else:
        print("Usage:")
        print("  python divergence_detector.py baseline      # Take baseline snapshot")
        print("  python divergence_detector.py check         # Check for drift")
        print("  python divergence_detector.py rollback      # Rollback to baseline")
        print("  python divergence_detector.py lock_baseline # Lock & transition to MAINTENANCE mode")
