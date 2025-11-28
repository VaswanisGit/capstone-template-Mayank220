from graph.state import ValidationState
from graph.synth import SynthesisSupervisor
from tools.template_store import TemplateStore

def test_synth():
    print("Testing Synthesis Subgraph...")
    state = ValidationState(input_idea="AI Cat Sitter")
    
    # Mock some evidence
    state.retrieved_evidence = {"mock_1": {"title": "Cats", "snippet": "Cats are cool"}}
    
    state = SynthesisSupervisor.run(state)
    
    # Check messages
    assert any(msg["content"] == "synth_start" for msg in state.messages)
    
    # Check draft snapshot
    assert state.draft_snapshot is not None
    assert "VALIDATION REPORT" in state.draft_snapshot
    assert "AI Cat Sitter" in state.draft_snapshot
    assert "Evidence items analyzed: 1" in state.draft_snapshot
    
    print("Synthesis subgraph tests passed.")

if __name__ == "__main__":
    test_synth()
