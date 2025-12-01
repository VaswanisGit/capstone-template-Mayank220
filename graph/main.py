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

def run_interactive_session(state: ValidationState):
    """Runs an interactive session guiding the user through the steps."""
    print("\n" + "="*40)
    print("STARTUP IDEA VALIDATOR - INTERACTIVE MODE")
    print("="*40 + "\n")

    # 0. Check for existing session
    if state.input_idea:
        print(f"Found active session for: '{state.input_idea}'")
        choice = input("Do you want to continue with this idea? (y/n): ").lower().strip()
        if choice != 'y':
            print("Starting new session...")
            state = ValidationState()
            # We need to save the cleared state immediately to overwrite the old file
            save_checkpoint(state)

    # 1. Get Idea
    if not state.input_idea:
        state.input_idea = input("What is your startup idea? ").strip()
        if not state.input_idea:
            print("No idea provided. Exiting.")
            return
        # Save immediately after getting idea
        save_checkpoint(state)

    print(f"\nIdea captured: '{state.input_idea}'")
    
    # 2. Research
    print("\n" + "-"*40)
    print("PHASE 1: MARKET RESEARCH")
    print("   Searching for market data, competitors, and trends...")
    state = run_research(state)
    save_checkpoint(state)
    
    print("\nResearch Summary:")
    print(f"   - Evidence items found: {len(state.retrieved_evidence)}")
    for key, val in list(state.retrieved_evidence.items())[:3]:
        title = val.get('title', 'Unknown')
        print(f"   - Found: {title}")
    
    confirm = input("\nDo you want to proceed to VALIDATION based on this research? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Exiting session.")
        return

    # 3. Validation
    print("\n" + "-"*40)
    print("PHASE 2: IDEA VALIDATION")
    print("   Analyzing evidence and scoring the idea...")
    state = run_validator(state)
    save_checkpoint(state)
    
    score = state.validation_report.get('score', 0)
    flags = state.validation_report.get('flags', [])
    
    print(f"\nValidation Score: {score}/100")
    if flags:
        print("Flags raised:")
        for flag in flags:
            print(f"   - {flag}")
    else:
        print("No critical flags found.")

    confirm = input("\nDo you want to generate a SYNTHESIS report? (y/n): ").lower().strip()
    if confirm != 'y':
        print("Exiting session.")
        return

    # 4. Synthesis
    print("\n" + "-"*40)
    print("PHASE 3: REPORT SYNTHESIS")
    print("   Drafting investor snapshot and validation brief...")
    state = run_synth(state)
    # Re-run validator to update score based on draft
    state = run_validator(state)
    save_checkpoint(state)

    print("\nDraft Preview (Excerpt):")
    if state.draft_snapshot:
        print(f"{state.draft_snapshot[:500]}...\n[...truncated...]")
    
    # 5. Export
    print("\n" + "-"*40)
    print("PHASE 4: EXPORT")
    confirm = input("Do you want to save this report to a file? (y/n): ").lower().strip()
    if confirm == 'y':
        from tools.doc_tools import DocTools
        filename = f"validation_report_{state.input_idea.replace(' ', '_')}.txt"
        path = DocTools.generate_report(state.draft_snapshot, filename)
        print(f"\nReport saved to: {path}")
    
    print("\nSession Complete. Good luck with your startup!")

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
    
    # Decision: Interactive vs Batch
    if args.task:
        # Batch Mode (Legacy/Scripting)
        state.task_category = args.task
        print(f"Task: {state.task_category}")
        print(f"Idea: {state.input_idea}")

        if state.task_category == "discover":
            state = run_research(state)
            state = run_validator(state)
        elif state.task_category == "validate":
            state = run_research(state)
            state = run_validator(state)
        elif state.task_category == "synth":
            state = run_synth(state)
            state = run_validator(state)
        
        save_checkpoint(state)
        print("State saved.")
        
        # Summary
        print("-" * 20)
        print(f"Composite Score: {state.validation_report.get('score', 'N/A')}")
        print(f"Top Flags: {state.validation_report.get('flags', [])}")
        if state.draft_snapshot:
            try:
                print(f"Draft Snapshot Preview:\n{state.draft_snapshot[:600]}...")
            except UnicodeEncodeError:
                # Fallback for Windows consoles that can't handle emojis
                safe_preview = state.draft_snapshot[:600].encode('ascii', 'replace').decode('ascii')
                print(f"Draft Snapshot Preview:\n{safe_preview}...")
        print("-" * 20)
        print("Disclaimer: This tool provides research-assistance and heuristics only; not legal, tax, or investment advice.")
        print("Human must approve before any final export (PDF/docx) is written.")
        
        # Export Prompt (Only if synth was run)
        if state.task_category == "synth" and state.draft_snapshot:
             # In batch mode, we might skip interactive export or keep it simple
             pass

    else:
        # Interactive Mode (Default)
        run_interactive_session(state)

if __name__ == "__main__":
    main()
