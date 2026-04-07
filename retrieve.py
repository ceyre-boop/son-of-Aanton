import os

VAULT_DIR = "vault"

def get_vault_content(filename):
    """
    Reads a file from the vault.
    """
    filepath = os.path.join(VAULT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return None

def get_all_linked_files():
    """
    Lists all files in the vault.
    """
    return [f for f in os.listdir(VAULT_DIR) if f.endswith(".md")]
