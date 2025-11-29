from graph.state import ValidationState

class Validator:
    @staticmethod
    def run(state: ValidationState) -> ValidationState:
        print("  [Validator] Running validator subgraph...")
        state.messages.append({"role": "system", "content": "validator_run"})
        
        score = 0
        flags = []
        provenance_summary = []
        
        # 1. Check for evidence
        evidence_count = len(state.retrieved_evidence)
        if evidence_count > 0:
            score += 10
            if evidence_count >= 3:
                score += 10 # Bonus for sufficient evidence
            provenance_summary.append(f"Found {evidence_count} evidence items (Base +10, Bonus +10 if >3)")
        else:
            flags.append("No evidence found")
            
        # 2. Check for keywords in evidence (Market, Competitor)
        has_market = any("market" in str(v).lower() for v in state.retrieved_evidence.values())
        has_competitor = any("competitor" in str(v).lower() for v in state.retrieved_evidence.values())
        
        if has_market:
            score += 20
            provenance_summary.append("Market data present (+20)")
        else:
            flags.append("Missing market data")
            
        if has_competitor:
            score += 20
            provenance_summary.append("Competitor data present (+20)")
        else:
            flags.append("Missing competitor data")
            
        # 3. Check for draft snapshot
        if state.draft_snapshot and len(state.draft_snapshot) > 100:
            score += 40
            provenance_summary.append("Draft snapshot generated (+40)")
        else:
            flags.append("Draft snapshot missing or too short")
            
        # Cap score at 100
        score = min(100, score)
        
        state.validation_report = {
            "score": score,
            "flags": flags,
            "provenance_summary": provenance_summary
        }
        
        print(f"    [Validator] Score: {score}/100, Flags: {len(flags)}")
        return state
