from graph.state import ValidationState

class SynthesisSupervisor:
    @staticmethod
    def run(state: ValidationState) -> ValidationState:
        print("  [Synth] Running synthesis subgraph...")
        state.messages.append({"role": "system", "content": "synth_start"})
        # TODO: Implement real synthesis logic
        return state
