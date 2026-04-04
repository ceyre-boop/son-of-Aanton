import hashlib
import sys
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path

LOCK_PATH = Path("values.lock")

def load_lock():
    with open(LOCK_PATH, "rb") as f:
        return tomllib.load(f)

def compute_hash(exclude_own_hash=True):
    """Hash the file content, ignoring the stored hash line itself."""
    lines = LOCK_PATH.read_text().splitlines()
    if exclude_own_hash:
        lines = [l for l in lines if not l.strip().startswith("file_hash")]
    content = "\n".join(lines).encode()
    return hashlib.sha256(content).hexdigest()

def sign():
    """Called once at first deploy. Writes the hash into values.lock."""
    h = compute_hash()
    text = LOCK_PATH.read_text()
    text = text.replace('file_hash       = ""', f'file_hash       = "{h}"')
    LOCK_PATH.write_text(text)
    print(f"[values.lock] Signed. Hash: {h}")

def verify():
    """Called on every boot. Full halt if mismatch."""
    if not LOCK_PATH.exists():
        print(f"[values.lock] MISSING. Run sign() before deploying.")
        sys.exit(1)
        
    lock = load_lock()
    stored = lock["signature"]["file_hash"]
    if not stored:
        print("[values.lock] UNSIGNED. Run sign() before deploying.")
        sys.exit(1)
    actual = compute_hash()
    if actual != stored:
        print("[values.lock] TAMPER DETECTED. Full halt.")
        print(f"  stored: {stored}")
        print(f"  actual: {actual}")
        sys.exit(1)
    print("[values.lock] Verified. System clear to run.")
    return True

def check_permission(action: str) -> bool:
    """
    Call this before any action in the system.
    Returns True if allowed, halts if not.
    """
    lock = load_lock()
    perms = lock.get("permissions", {})
    harm  = lock.get("harm", {})

    if action in perms:
        allowed = perms[action]
        if not allowed:
            print(f"[values.lock] BLOCKED: '{action}' is not permitted.")
            _halt(f"permission denied: {action}")
        return True

    if action in harm:
        response = harm[action]
        if response in ("halt", "rollback"):
            _halt(f"harm rule triggered: {action} -> {response}")
    
    # If not explicitly permitted or banned, we check if it's a known action.
    # For now, let's assume unknown actions are blocked if we want a strict nothing box.
    print(f"[values.lock] WARNING: Unknown action '{action}'.")
    return False

def _halt(reason: str):
    from change import rollback
    print(f"[SYSTEM HALT] {reason}")
    rollback(reason)
    sys.exit(1)

if __name__ == "__main__":
    if sys.argv[1:] == ["sign"]:
        sign()
    else:
        verify()
