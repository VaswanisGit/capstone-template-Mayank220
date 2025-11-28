tools.market_tools.search_market()

tools.template_store.load_snippets()

Save retrieved evidence to state.retrieved_evidence with provenance fields.

Add TODO markers where real embedding-based Chroma RAG would go.

[TODO] Step 5: Implement the Synthesis subgraph

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

[TODO] Step 6: Implement the Validator subgraph

Implement deterministic heuristic checks inside graph/validator.py.

Score factors include:

Presence of market size estimates

At least one competitor identified

Evidence retrieved > 0

Internal logical consistency

Save to state.validation_report a dict with: {score, flags, provenance_summary}.

[TODO] Step 7: Populate snippet templates

Add sample text templates in /snippets:

investor_one_pager.txt (value prop, traction, ask, summary)

validation_brief_template.txt (Problem, Market, Competitors, Metrics, Risks)

Ensure each snippet includes a simple “provenance” field.

[TODO] Step 8: Build simple stubs for tools

Inside /tools:

template_store.py

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