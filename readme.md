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

Load templates from /snippets such as:

validation_brief_template.txt

investor_one_pager.txt

Build a LangChain prompt chain placeholder that assembles:

Problem

Solution

Market Summary

Evidence highlights

Basic metrics (TAM/SAM/SOM placeholder)

Risks + Next steps

Save output to state.draft_snapshot.

[DONE] Step 6: Implement the Validator subgraph

Implement deterministic heuristic checks inside graph/validator.py.

Score factors include:

Presence of market size estimates

At least one competitor identified

Load snippet files into Python dicts.

Return snippet text + provenance.

market_tools.py

Return deterministic placeholder “market evidence” objects.

Add TODO where real RAG or web API would eventually plug in.

doc_tools.py

Implement a minimal PDF or TXT export tool.

Only export after human confirmation.

[TODO] Step 9: Design final report + CLI export flow

Define clear final sections in the business validation report.

Ensure draft_snapshot follows a clean consulting structure.

Add a CLI prompt asking:
“Do you want to export this report? (y/n)”

On “yes”, call doc_tools.generate_pdf() or write a .txt.

[TODO] Step 10: Create sample startup ideas and test full system

Prepare sample ideas:

AI fashion stylist

EdTech micro-tutoring app

Creator economy analytics tool

Local commerce marketplace

Run test flows for:

Discover → Validate → Synth

Collect example outputs and place them inside /docs/ as test evidence.

[TODO] Step 11: Improve prompt engineering + refine outputs

Tuned prompts for structured reasoning.

Improve clarity of validation_report scoring system.

Improve consistency of provenance entries.

Document known limitations.