# Knowledge Node

A contained autonomous learning loop with human approval gates.

## The Core Idea

This isn't a pre-trained AI. It's a **self-building knowledge system** that:

1. **Starts with rules** (seed.md) - learns how to exist in its environment
2. **Discovers knowledge** - finds new information autonomously
3. **Processes meaning** - tags by HOW to use it, not just WHAT it is
4. **Stages changes** - all edits go to pending, awaiting approval
5. **Connects knowledge** - builds a living graph via wikilinks

## Architecture

```
[MASTER NODE] ← Scope lock - everything flows through here
    │
    ├── retrieve.py → Look up what we know
    ├── learn.py → Find & process new knowledge
    ├── change.py → Write files (with approval)
    │
    └── vault/
        ├── seed.md → The rules of the environment
        ├── index.md → Knowledge graph
        ├── pending.json → Changes awaiting approval
        └── storage/ → Approved knowledge files
```

## Quick Start

```bash
# 1. Initialize
python master_node.py

# 2. Run learning cycle
python master_node.py cycle

# 3. Review pending changes
python master_node.py pending

# 4. Approve changes
python master_node.py approve <id>
# or
python master_node.py approve-all

# 5. Check status
python master_node.py status
```

## Interactive Mode

```bash
python master_node.py
> cycle      # Run learning cycle
> pending    # Show pending changes
> approve 1  # Approve change with ID 1
> status     # Show container status
> quit       # Save and exit
```

## How It Works

### Phase 1: Seed Dataset

`seed.md` contains the environment rules:
- How the file structure works
- What the learning loop does
- How to tag knowledge by meaning
- The approval process

This is the "self-awareness" - knowledge of how to be.

### Phase 2: Learning Loop

1. **Retrieve** - Check current knowledge graph
2. **Learn** - Discover new information (simulated or API)
3. **Process** - Extract meaning and usage tags
4. **Stage** - Add to `pending.json`
5. **Halt** - Wait for human approval

### Phase 3: Approval Gate

The system **stops** and waits. You review:
```
ID: 1a2b3c4d
Title: Graph Database Basics
Tags: concept, howto, connect
Preview: A graph database stores data in nodes...
```

Then approve: `node.approve('1a2b3c4d')`

### Phase 4: Connection

Approved knowledge:
1. Written to `storage/` as markdown
2. Added to `index.md` with wikilinks
3. Connected to related topics

## Safety (Scope Lock)

- **Nothing writes files without approval**
- **All changes tracked in pending.json**
- **Container scope = current directory only**
- **State saved to .node_state.json**

## Extending

### Add Real Learning Sources

Edit `learn.py`:
```python
def discover_from_api():
    # Call your API
    # Process results
    return knowledge
```

### Customize Knowledge Processing

Edit `process_meaning()` in `learn.py`:
- Add custom tags
- Change extraction logic
- Add validation rules

### Add Automated Checks

Edit `change.py`:
```python
def validate_change(knowledge):
    # Your validation logic
    return True/False
```

## Philosophy

> "Normal AI = you dump data in, it retrieves.  
> This system = it finds its own data, learns meaning, and rebuilds itself — but you hold the key."

The Master Node is not the intelligence. It's the **container** that keeps learning safe, structured, and human-approved.
