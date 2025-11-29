I plan to execute the following steps to complete my project.

[DONE] Step 1: Set up project structure and environment

Create a virtual environment and install dependencies from requirements.txt (langgraph, langchain, chromadb, etc.).

Fork the MAT496 capstone repository and create the folder capstone-template-mayank220/.

Add the exact folder structure defined in ARCHITECTURE.md (graph/, tools/, snippets/, data/, docs/, etc.).

Create empty starter files for all required modules (state.py, main.py, research.py, synth.py, validator.py).

[DONE] Step 2: Implement global state with Pydantic

Define the ValidationState model exactly as specified (messages, input_idea, retrieved_evidence, metrics, draft_snapshot, versions, etc.) in graph/state.py.

Ensure it supports incremental updates across runs (mutable state, lists, dicts).

Add a checksum/serialization helper to save and load from ./data/state.json.

[DONE] Step 3: Build the Router + Orchestrator

Implement a deterministic keyword-based Router that classifies tasks into "discover", "validate", or "synth".

Implement Orchestrator functions:

run_research(state)

run_synth(state)

run_validator(state)

Add checkpoint saving after every run.

Build a minimal CLI using argparse or input() that:

loads state

routes request

runs appropriate subgraph

prints the task + short preview.

[DONE] Step 4: Implement the Research subgraph (RAG placeholder)

Implement ResearchSupervisor.run(state) inside graph/research.py.

Add deterministic stubs for retrieval:

tools.market_tools.search_market()

tools.template_store.load_snippets()

Save retrieved evidence to state.retrieved_evidence with provenance fields.

Add TODO markers where real embedding-based Chroma RAG would go.

[DONE] Step 5: Implement the Synthesis subgraph

Add SynthesisSupervisor.run(state) inside graph/synth.py.

Improve consistency of provenance entries.

Document known limitations.