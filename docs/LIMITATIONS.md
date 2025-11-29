# Known Limitations

## 1. Deterministic Stubs
- **Market Research**: The `MarketTools.search_market` function currently returns hardcoded placeholder data. It does not perform actual web searches or RAG.
- **Snippet Retrieval**: `TemplateStore` loads all snippets regardless of the query. It does not use semantic search.

## 2. Placeholder Synthesis
- **LLM Integration**: The `SynthesisSupervisor` uses simple string formatting to generate reports. It does not use an LLM (like GPT-4) to synthesize information intelligently.
- **Content Quality**: The generated content is repetitive and generic due to the lack of a real generative model.

## 3. Heuristic Validation
- **Scoring**: The validation score is based on simple keyword presence and file length checks. It does not evaluate the actual quality or feasibility of the startup idea.
- **Flags**: Flags are binary and based on the presence/absence of specific data types.

## 4. Local Storage
- **State Persistence**: State is saved to a local JSON file (`data/state.json`). There is no database integration for multi-user support or cloud persistence.

## 5. Export Format
- **File Type**: Reports are currently exported as plain text files. PDF or DOCX export is not yet implemented.
