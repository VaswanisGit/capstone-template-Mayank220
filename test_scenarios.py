import os
from graph.state import ValidationState
from graph.research import ResearchSupervisor
from graph.synth import SynthesisSupervisor
from graph.validator import Validator
from tools.doc_tools import DocTools

def run_scenario(idea: str):
    print(f"\n=== Running Scenario: {idea} ===")
    
    # 1. Initialize State
    state = ValidationState(input_idea=idea)
    
    # 2. Research
    state = ResearchSupervisor.run(state)
    
    # 3. Synthesis
    state = SynthesisSupervisor.run(state)
    
    # 4. Validation
    state = Validator.run(state)
    
    # 5. Export Report
    if state.draft_snapshot:
        filename = f"docs/test_evidence/report_{idea.replace(' ', '_').lower()}.txt"
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        path = DocTools.generate_report(state.draft_snapshot, filename)
        print(f"Report generated at: {path}")
    else:
        print("Error: No draft snapshot generated.")

def main():
    ideas = [
        "AI fashion stylist",
        "EdTech micro-tutoring app",
        "Creator economy analytics tool",
        "Local commerce marketplace"
    ]
    
    for idea in ideas:
        run_scenario(idea)

if __name__ == "__main__":
    main()
