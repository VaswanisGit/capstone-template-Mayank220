from graph.state import ValidationState

class ResearchSupervisor:
    @staticmethod
    def run(state: ValidationState) -> ValidationState:
        print("  [Research] Running research subgraph...")
        state.messages.append({"role": "system", "content": "research_start"})
        # TODO: Implement real research logic
        return state
