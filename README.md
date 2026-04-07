# Son-of-Aanton 🦾

The **Son-of-Aanton** is an AI Knowledge Discovery Loop built with a "Constitutional Core" for maximum integrity and security.

## 🌟 Key Features

- **Self-Generating Vault**: Discovers and writes knowledge to an Obsidian-compatible vault via an iterative LLM loop.
- **Constitutional Guard**: A crypto-signed `values.lock` constitution that enforces hardware boundaries and permissions.
- **Human-in-the-Loop**: Integrated approval gate for all knowledge commits.
- **Self-Indexing**: Automatically builds and maintains a [[wikilink]] based knowledge graph.

## 🛠️ Architecture

- `master_node.py`: The entry point and scope lock.
- `learn.py`: The discovery engine (Claude API / Simulated).
- `values_guard.py`: The hashing/verification enforcer.
- `change.py`: The commitment and rollback system.
- `vault/`: The knowledge repository (Obsidian Vault).

## 🚀 Getting Started

1. Initial boot and signature:
   ```bash
   python3 values_guard.py sign
   ```

2. Run a discovery cycle:
   ```bash
   python3 master_node.py 5
   ```

3. Open the `vault/` folder in Obsidian to view the knowledge graph.
