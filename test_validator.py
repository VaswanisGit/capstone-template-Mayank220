from graph.state import ValidationState
from graph.validator import Validator

def test_validator():
    print("Testing Validator Subgraph...")
    
    # Case 1: Empty state
    state1 = ValidationState(input_idea="Empty Idea")
    state1 = Validator.run(state1)
    assert state1.validation_report["score"] == 0
    assert "No evidence found" in state1.validation_report["flags"]
    print("Case 1 passed.")
    
    # Case 2: Full state
    state2 = ValidationState(input_idea="Full Idea")
    state2.retrieved_evidence = {
        "1": "Market report says...",
        "2": "Competitor analysis..."
    }
    state2.draft_snapshot = "This is a long enough draft snapshot to pass the length check of 100 characters. " * 5
    
    state2 = Validator.run(state2)
    assert state2.validation_report["score"] == 100
    assert len(state2.validation_report["flags"]) == 0
    print("Case 2 passed.")
    
    print("Validator subgraph tests passed.")

if __name__ == "__main__":
    test_validator()
