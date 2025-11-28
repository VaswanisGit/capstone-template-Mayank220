from graph.state import ValidationState, save_checkpoint, load_checkpoint
import os

def test_state():
    print("Testing ValidationState...")
    state = ValidationState(input_idea="Test Idea")
    assert state.input_idea == "Test Idea"
    assert state.messages == []
    print("ValidationState initialized correctly.")

    print("Testing checkpointing...")
    save_checkpoint(state, "data/test_state.json")
    assert os.path.exists("data/test_state.json")
    
    loaded_state = load_checkpoint("data/test_state.json")
    assert loaded_state.input_idea == "Test Idea"
    print("Checkpointing worked correctly.")
    
    # Cleanup
    if os.path.exists("data/test_state.json"):
        os.remove("data/test_state.json")
    print("Test passed!")

if __name__ == "__main__":
    test_state()
