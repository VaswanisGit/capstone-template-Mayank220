from graph.state import ValidationState
from tools.market_tools import MarketTools
from tools.template_store import TemplateStore

class ResearchSupervisor:
    @staticmethod
    def run(state: ValidationState) -> ValidationState:
        print("  [Research] Running research subgraph...")
        state.messages.append({"role": "system", "content": "research_start"})
        
        query = state.input_idea or "startup idea"
        
        # 1. Market Search
        market_evidence = MarketTools.search_market(query)
        
        # 2. Template Search (Internal Knowledge)
        internal_snippets = TemplateStore.search_snippets(query)
        
        # 3. Save to State
        # We'll store them in retrieved_evidence with unique keys
        for i, item in enumerate(market_evidence):
            key = f"market_{i}"
            state.retrieved_evidence[key] = item
            
        for i, item in enumerate(internal_snippets):
            key = f"snippet_{item['id']}"
            state.retrieved_evidence[key] = item
            
        print(f"    [Research] Saved {len(state.retrieved_evidence)} evidence items.")
        
        # TODO: Implement real research logic (Chroma RAG, etc.)
        return state
