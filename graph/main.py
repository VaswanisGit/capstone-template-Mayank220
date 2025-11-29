import sys
import argparse
from graph.state import ValidationState, load_checkpoint, save_checkpoint
from graph.research import ResearchSupervisor
from graph.synth import SynthesisSupervisor
from graph.validator import Validator

def router(input_text: str) -> str:
    """Classifies user input into a task category."""
    input_text = input_text.lower()
    if "validate" in input_text:
        return "validate"
    elif "synth" in input_text or "report" in input_text:
        return "synth"
    else:
        return "discover"

def run_research(state: ValidationState) -> ValidationState:
    return ResearchSupervisor.run(state)

def run_synth(state: ValidationState) -> ValidationState:
    return SynthesisSupervisor.run(state)

def run_validator(state: ValidationState) -> ValidationState:
    return Validator.run(state)

def main():
    parser = argparse.ArgumentParser(description="Startup Idea Validator CLI")
    parser.add_argument("--idea", type=str, help="The startup idea to validate")
    parser.add_argument("--task", type=str, help="Task category (discover, validate, synth)")
    parser.add_argument("--reset", action="store_true", help="Reset state")
    args = parser.parse_args()

    # Load or initialize state
    if args.reset:
        state = ValidationState()
        print("State reset.")
    else:
        state = load_checkpoint()

    # Update state with input
    if args.idea:
        state.input_idea = args.idea
    
    # Determine task
    if args.task:
        state.task_category = args.task
    elif state.input_idea:
        state.task_category = router(state.input_idea)
    else:
        # Interactive mode if no args
        if not state.input_idea:
            state.input_idea = input("Enter your startup idea: ")
        state.task_category = router(state.input_idea)

    print(f"Task: {state.task_category}")
    print(f"Idea: {state.input_idea}")

    # Orchestrator
    if state.task_category == "discover":
        state = run_research(state)
        state = run_validator(state)
    elif state.task_category == "validate":
        state = run_research(state)
        state = run_validator(state)
    elif state.task_category == "synth":
        state = run_synth(state)
        state = run_validator(state)
    
    # Checkpoint
    save_checkpoint(state)
    print("State saved.")

    # Summary
    print("-" * 20)
    print(f"Composite Score: {state.validation_report.get('score', 'N/A')}")
    print(f"Top Flags: {state.validation_report.get('flags', [])}")
    if state.draft_snapshot:
        print(f"Draft Snapshot Preview:\n{state.draft_snapshot[:600]}...")
    print("-" * 20)
    print("Disclaimer: This tool provides research-assistance and heuristics only; not legal, tax, or investment advice.")
    print("Human must approve before any final export (PDF/docx) is written.")
    
    # Export Prompt
    if state.draft_snapshot and state.validation_report.get("score", 0) > 0:
        export_choice = input("\nDo you want to export this report? (y/n): ").lower().strip()
        if export_choice == 'y':
            from tools.doc_tools import DocTools
            filename = f"validation_report_{state.input_idea.replace(' ', '_')}.txt"
            DocTools.generate_report(state.draft_snapshot, filename)

if __name__ == "__main__":
    main()
