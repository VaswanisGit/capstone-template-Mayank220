# System Architecture

## Overview
This document describes the architecture of the capstone project.

# Startup Idea Validator — SIMPLE ARCHITECTURE
**Version:** 1.0  
**Audience:** Antigravity Builder / LLM Code Generator

> This file is the single source of truth. Antigravity MUST follow the structure, filenames and constraints exactly. Keep it simple and deterministic.

---

# 1. Goal (one line)
CLI tool that helps founders validate a startup idea by: collecting quick market evidence (RAG), estimating simple metrics (TAM/SAM/SOM), producing a short validation report and a 1-page investor snapshot.

---

# 2. High-level constraints (must follow)
- CLI-only. No servers, no UI.  
- Local persistence: `./data/state.json`.  
- Use **LangGraph** for orchestration and **LangChain** for prompt chains & retrieval.  
- Keep outputs sourced: every factual claim in the report must include a provenance pointer saved in state.  
- Human approval required before any “final export” file is written.

---

# 3. Minimal tech (must use)
- Python 3.11+  
- `langgraph`  
- `langchain` + `langchain-openai` (for LLM wrapper)  
- `chromadb` (local vector store)  
- `python-dotenv`  
- `presidio-analyzer` (optional stub for PII scan)  
- `python-docx` or `reportlab` (for a simple PDF/DOCX export)

(Keep dependency list minimal in `requirements.txt` — user will run installs locally.)

---

# 4. Folder structure (exact)
/Grog-freelance-local
├── graph
│ ├── state.py # Pydantic state model
│ ├── main.py # CLI runner, Router + Orchestrator
│ ├── research.py # Research (RAG) subgraph
│ ├── synth.py # Synthesis (report builder) subgraph
│ └── validator.py # Simple validator
├── tools
│ ├── template_store.py
│ ├── market_tools.py
│ └── doc_tools.py
├── snippets
│ ├── investor_one_pager.txt
│ └── validation_brief_template.txt
├── data
│ └── vector_db/
├── requirements.txt
├── .env
├── README.md
└── docs
└── ARCHITECTURE.md # (this file)

python
Copy code

Do not create extra top-level folders.

---

# 5. Global state (`graph/state.py`)
Create a Pydantic model `ValidationState` with exactly these fields:

```python
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ValidationState(BaseModel):
    messages: List[Dict[str, Any]] = []
    task_category: Optional[str] = None   # "discover","validate","synth"
    input_idea: Optional[str] = None
    extracted_facts: Dict[str, Any] = {}
    retrieved_evidence: Dict[str, Any] = {}
    metrics: Dict[str, Any] = {}
    draft_snapshot: Optional[str] = None
    validation_report: Dict[str, Any] = {}
    versions: List[Dict[str, Any]] = []
No other attributes.

6. Router & Orchestrator (graph/main.py) — behavior
Router: classify user input into "discover", "validate", or "synth". Fallback "discover". Use simple keyword rules (deterministic).

Orchestrator: exposes run_research(state), run_synth(state), and run_validator(state). These call the corresponding modules.

Checkpointing: write state.dict() to ./data/state.json after each run. Provide a load_checkpoint() helper.

CLI: read input (argparse or input()), load or create state, call Router, run the appropriate subgraph, run validator, checkpoint, print a short summary (task, top score, short excerpt of draft_snapshot).

Add TODO comments where real LLM/Chroma calls will go.

7. Subgraphs (very small)
7.1 Research (graph/research.py)
Purpose: build a short evidence bundle for the idea using local snippets + Chroma RAG + market_tools stubs.

Implementation: ResearchSupervisor.run(state) should:

append "research_start" to state.messages

run tools.market_tools.search_market(query) and template_store.search_snippets(query) (stubs)

save retrieved items (text + provenance) to state.retrieved_evidence

return state

Keep it a single function — no complex node graph inside.

7.2 Synthesis (graph/synth.py)
Purpose: build a ~1–2 page validation brief and 1-page investor snapshot.

Implementation: SynthesisSupervisor.run(state) should:

append "synth_start" to state.messages

call a LangChain chain (placeholder) to assemble sections (Problem, Solution, Market, Metrics, Risks, Next steps)

write assembled text to state.draft_snapshot

return state

7.3 Validator (graph/validator.py)
Purpose: simple checks and scoring.

Implementation: Validator.run(state) should:

append "validator_run" to state.messages

perform deterministic heuristic checks (e.g., checks for presence of TAM, at least one competitor, basic unit economics if revenue model present)

populate state.validation_report with: score (0–100), flags (list), and provenance_summary

return state

Keep all logic local and heuristic-based (no heavy ML required).

8. Tools (simple stubs in /tools)
template_store.py
load_snippets(path) → load files from /snippets as text blocks (return list of dicts with id,text,provenance).

market_tools.py
search_market(query, k=3) → deterministic placeholder returning a list of small dicts with title,snippet,provenance. (No web calls; placeholder only; mark TODO for real integration.)

doc_tools.py
generate_pdf(text, out_path) → write text into a simple PDF or TXT file; return {"ok": True, "path": out_path}.

All tools should print one-line logs when called.

9. Snippets (starter content)
Create two small templates in /snippets:

investor_one_pager.txt — one-line placeholders for title, value prop, market, traction, ask.

validation_brief_template.txt — basic headings for Problem / Market / Competitors / Metrics / Risks / Next Steps.

These are used by template_store.load_snippets.

10. Minimal requirements.txt (suggested)
Keep this file minimal. Example pins (user will install locally):

ini
Copy code
langgraph==0.1.0
langchain==0.2.11
langchain-openai==0.1.8
openai==1.0.0
python-dotenv==1.0.0
chromadb==0.4.24
pydantic==1.10.11
Add comment: # NOTE: install globally if not using a virtualenv.

11. CLI output & disclaimer
After each run print a small summary:

Task: state.task_category

Composite score: state.validation_report.get("score")

Top flags: state.validation_report.get("flags")

Draft snapshot preview (first 600 characters)

Then print:
Disclaimer: This tool provides research-assistance and heuristics only; not legal, tax, or investment advice.

Human must approve before any final export (PDF/docx) is written.

12. Simplicity rules (must follow)
One file per concern (state, main, research, synth, validator, tools).

Each subgraph has one run(state) entrypoint. Keep code short and readable.

Add TODO comments for any external API or production integration.

All retrieved evidence must be recorded with a provenance field in state.retrieved_evidence.

If Antigravity cannot implement an external integration deterministically, it must leave a clear TODO and not invent data.

13. Mermaid diagram (simple, keep exact text)
Include this mermaid block near the top or bottom of the file — keep it exactly as below:

mermaid
Copy code
graph TD
  User_Input --> T[Task Classifier / Router]
  T --> Orch[Orchestrator / Queue / Retry / Timeouts]

  Orch -->|discover/validate/synth| R_Sup[Research Supervisor]
  R_Sup --> R_Search[Market Search / RAG]
  R_Search --> R_Audit[Save evidence]

  Orch -->|validate/synth| S_Sup[Synthesis Supervisor]
  S_Sup --> S_Retr[Template Retriever]
  S_Retr --> S_Draft[Draft Assembler]
  S_Draft --> S_Audit[Save draft]

  S_Audit --> Validator
  R_Audit --> Validator

  subgraph ValidatorChecks
    Validator --> V1(Score)
    Validator --> V2(Flags)
    Validator --> V3(Provenance)
  end

  Validator --> Human_Review[Human Gate: Approve Export]
  Human_Review --> Finalize[Export & Archive]
  Finalize --> Archive[Versioned Storage + Audit Log]
14. Final note to Antigravity (strict)
Produce exactly the files in section 4.

docs/ARCHITECTURE.md must contain this text exactly (including the mermaid).

Do not generate extra services or UI.

Use TODO markers where LLM/Chroma integrations are required.

If uncertain about any external integration, create a deterministic stub and clearly label it TODO.