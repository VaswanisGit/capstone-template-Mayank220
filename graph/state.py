# Global state definition
import json
import os
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

def save_checkpoint(state: ValidationState, filepath: str = "data/state.json"):
    """Saves the state to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        # Pydantic v2
        if hasattr(state, "model_dump_json"):
            f.write(state.model_dump_json(indent=2))
        # Pydantic v1
        else:
            f.write(state.json(indent=2))

def load_checkpoint(filepath: str = "data/state.json") -> ValidationState:
    """Loads the state from a JSON file. Returns a new state if file doesn't exist."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ValidationState(**data)
    return ValidationState()
