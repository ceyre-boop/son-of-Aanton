import os
import shutil
from github import Github
from datetime import datetime

VAULT_DIR = "vault"
HELD_DIR = "vault/held"

# GitHub Configuration
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or "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"
GITHUB_REPO = os.environ.get("GITHUB_REPO") or "ceyre-boop/son-of-Aanton"

def await_approval(draft_paths):
    """
    Prints diff to terminal and requires y/n.
    """
    for draft_path in draft_paths:
        print(f"\n--- Checking Draft: {draft_path} ---")
        try:
            with open(draft_path, 'r') as f:
                content = f.read()
            
            print(f"Content:\n---\n{content}\n---\n")
            
            response = input(f"Approve and Commit to GitHub? (y/n): ").strip().lower()
            
            if response == 'y':
                commit(draft_path)
            else:
                if not os.path.exists(HELD_DIR):
                    os.makedirs(HELD_DIR)
                
                filename = os.path.basename(draft_path)
                held_path = os.path.join(HELD_DIR, filename)
                shutil.move(draft_path, held_path)
                print(f"Moved to held: {held_path}")
        except Exception as e:
            print(f"Error during approval process: {e}")

def commit(draft_path):
    """
    Commit via GitHub API.
    """
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print(f"--- SIMULATED GITHUB COMMIT (No GITHUB_TOKEN found) ---")
        print(f"File {draft_path} committed locally with timestamp {datetime.now()}.")
        return

    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(GITHUB_REPO)
        
        with open(draft_path, 'r') as f:
            content = f.read()
        
        filename = os.path.basename(draft_path)
        path_in_repo = f"vault/{filename}"
        
        commit_message = f"AI Update: {filename} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        try:
            # Check if file exists to update or create
            contents = repo.get_contents(path_in_repo)
            repo.update_file(contents.path, commit_message, content, contents.sha)
            print(f"GitHub: Updated {path_in_repo}")
        except:
            # File doesn't exist, create it
            repo.create_file(path_in_repo, commit_message, content)
            print(f"GitHub: Created {path_in_repo}")
            
    except Exception as e:
        print(f"Error during GitHub commit: {e}")

def rollback(reason: str):
    """
    Phase 4: Undo last action.
    Currently a placeholder that moves the last modified files in /vault to /vault/discarded.
    """
    print(f"Rollback initiated due to: {reason}")
    discard_dir = "vault/discarded"
    if not os.path.exists(discard_dir):
        os.makedirs(discard_dir)
    
    # Simple logic: Move last modified file in vault/ to discarded/
    files = [os.path.join(VAULT_DIR, f) for f in os.listdir(VAULT_DIR) if os.path.isfile(os.path.join(VAULT_DIR, f))]
    if files:
        latest_file = max(files, key=os.path.getmtime)
        shutil.move(latest_file, os.path.join(discard_dir, os.path.basename(latest_file)))
        print(f"Rolled back file: {latest_file}")
