from graph.state import ValidationState
from graph.research import ResearchSupervisor

def test_research():
    print("Testing Research Subgraph...")
    state = ValidationState(input_idea="AI Dog Walker")
    
    state = ResearchSupervisor.run(state)
    
    # Check messages
    assert any(msg["content"] == "research_start" for msg in state.messages)
    
    # Check evidence
    assert len(state.retrieved_evidence) > 0
    print("Evidence keys:", state.retrieved_evidence.keys())
    
    # Check specific content
    market_found = False
    snippet_found = False
    for key, val in state.retrieved_evidence.items():
        if "market" in key:
            market_found = True
        if "snippet" in key:
            snippet_found = True
            
    assert market_found
    assert snippet_found
    
    print("Research subgraph tests passed.")

if __name__ == "__main__":
    test_research()
