"""
prewarm_ollama.py - Load model into memory once for fast discovery loops
"""
import requests
import sys
import time

OLLAMA_HOST = "http://localhost:11434"
MODEL = "llama3.2"

def check_ollama_running():
    """Check if Ollama server is up."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/version", timeout=5)
        return resp.status_code == 200
    except:
        return False

def check_model_available(model):
    """Check if model is downloaded."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = resp.json().get('models', [])
            return any(m['name'].startswith(model) for m in models)
    except:
        pass
    return False

def warm_model(model):
    """Load model into memory with a simple prompt."""
    print(f"[Prewarm] Loading {model} into memory...")
    print("[Prewarm] This takes 30-90 seconds on first load...")
    print("[Prewarm] (Subsequent runs will be instant)")
    
    start = time.time()
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": "Say 'ready' and nothing else.",
                "stream": False,
                "options": {"num_predict": 2}  # Minimal tokens
            },
            timeout=300  # 5 minutes
        )
        
        elapsed = time.time() - start
        if resp.status_code == 200:
            print(f"[Prewarm] [OK] Model loaded in {elapsed:.1f}s")
            print(f"[Prewarm] Response: {resp.json().get('response', '').strip()}")
            return True
        else:
            print(f"[Prewarm] [X] Error: {resp.status_code}")
            print(f"[Prewarm] {resp.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"[Prewarm] [X] Timeout after 5 minutes")
        print(f"[Prewarm] Model may be too large for your system")
        return False
    except Exception as e:
        print(f"[Prewarm] [X] Error: {e}")
        return False

def main():
    print("=== Ollama Model Prewarm ===\n")
    
    # Check Ollama server
    if not check_ollama_running():
        print("[X] Ollama server not running!")
        print("  Start it with: ollama serve")
        sys.exit(1)
    print("[OK] Ollama server is running")
    
    # Check model exists
    if not check_model_available(MODEL):
        print(f"[X] Model '{MODEL}' not found!")
        print(f"  Download with: ollama pull {MODEL}")
        sys.exit(1)
    print(f"[OK] Model '{MODEL}' is available")
    
    # Warm the model
    if warm_model(MODEL):
        print("\n=== Ready for discovery loops ===")
        print("Run: python master_node.py 5")
    else:
        print("\n=== Failed to warm model ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
