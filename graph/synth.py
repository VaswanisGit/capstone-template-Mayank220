from graph.state import ValidationState
from tools.template_store import TemplateStore

class SynthesisSupervisor:
    @staticmethod
    def run(state: ValidationState) -> ValidationState:
        print("  [Synth] Running synthesis subgraph...")
        state.messages.append({"role": "system", "content": "synth_start"})
        
        # Prepare inputs
        idea = state.input_idea or "Unknown Idea"
        evidence_list = [f"- {v.get('title', 'Item')}: {v.get('snippet', '')}" for v in state.retrieved_evidence.values()]
        evidence = "\n".join(evidence_list)
        evidence_count = len(state.retrieved_evidence)
        
        # Define the target format structure
        report_structure = """
# VALIDATION REPORT FOR: "{idea}"

🚀 EXECUTIVE SUMMARY
[Summary of the idea, market context, and brutal reality check. Is it viable? High risk?]

1. PROBLEM STATEMENT
[Bullet points of specific pain points. Who hurts? How bad?]

2. MARKET ANALYSIS
**Market Overview**
[Size, growth, trends]

**Market Reality Check**
[Why is this hard? Margins? CAC?]

**Target Customer Segments**
[Who specifically will pay?]

3. COMPETITIVE LANDSCAPE
**Direct Competitors**
[Names]

**Indirect Competitors**
[Alternatives]

**Competitive Reality**
[Why will you likely fail against them? What is the moat?]

4. KEY METRICS TO TRACK
**Marketplace/Business Metrics**
[CAC, LTV, Churn, etc.]

**Operational Metrics**
[Efficiency, fulfillment, etc.]

5. RISKS & CHALLENGES (REALISTIC & BRUTAL)
[1-5 specific risks. Be harsh.]

6. NEXT STEPS (REALISTIC & PRIORITIZED)
[1-5 actionable steps. Don't just say 'build app'. Say 'validate demand'.]

---

# INVESTOR SNAPSHOT

1. Value Proposition
[One sentence.]

2. The Problem
[Core pain.]

3. The Solution
[The product.]

4. Market Opportunity
[TAM/SAM/SOM.]

5. Traction / Validation
[Evidence found.]

6. The Ask
[Funding needs.]

7. Team
[Roles needed.]

---

⭐ 5 Brutally Honest Reasons This Startup Could Work
1. [Reason]
2. [Reason]
3. [Reason]
4. [Reason]
5. [Reason]

⚠️ 5 Brutally Honest Reasons This Startup May Not Work at All
1. [Reason]
2. [Reason]
3. [Reason]
4. [Reason]
5. [Reason]

FINAL VERDICT (REALISTIC)
[Conclusion]
"""

        # Try to use Real LLM
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import PromptTemplate
            from langchain_core.output_parsers import StrOutputParser
            import os

            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")

            print("    [Synth] Connecting to OpenAI (gpt-4o)...")
            llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
            
            prompt_text = f"""You are a top-tier Venture Capital Analyst known for being BRUTALLY HONEST and REALISTIC.
            
            Analyze the startup idea: '{{idea}}'
            
            Based on this evidence:
            {{evidence}}
            
            Generate a report following EXACTLY this structure:
            {report_structure}
            
            INSTRUCTIONS:
            1. Be BRUTAL. If the idea is generic (e.g. "Uber for X"), tear it apart.
            2. Use specific metrics and business terms (CAC, LTV, Churn).
            3. Do NOT use placeholders like "See above". Repeat information if necessary to make sections standalone.
            4. For the "5 Reasons" sections, be creative and specific to the industry.
            """
            
            prompt = PromptTemplate.from_template(prompt_text)
            chain = prompt | llm | StrOutputParser()
            
            response = chain.invoke({
                "idea": idea,
                "evidence": evidence
            })
            
            state.draft_snapshot = response
            print(f"    [Synth] Generated real LLM report ({len(response)} chars).")
            
        except Exception as e:
            print(f"    [Synth] WARNING: Could not use LLM ({e}). Falling back to smart template.")
            
            # Smart Fallback Logic
            # We will construct the report using the evidence and some heuristic templates
            
            # Determine sector for "Reasons" generation
            idea_lower = idea.lower()
            sector = "general"
            if "dog" in idea_lower or "pet" in idea_lower: sector = "pet"
            elif "ai" in idea_lower or "gpt" in idea_lower: sector = "ai"
            elif "food" in idea_lower or "delivery" in idea_lower: sector = "food"
            
            # Heuristic "Reasons" based on sector
            reasons_work = {
                "pet": [
                    "Pet owners spend irrationally on convenience and care.",
                    "Frustration with existing platforms (inconsistent quality).",
                    "Trust is underserved; a hyper-local trust network can win.",
                    "Urban density creates strong local network effects.",
                    "Niche verticals (anxious/senior pets) are underserved."
                ],
                "general": [
                    "Large addressable market if execution is perfect.",
                    "Potential for viral growth if value prop is clear.",
                    "Solves a genuine pain point for a specific niche.",
                    "Low barrier to entry allows for quick MVP testing.",
                    "Scalable business model if unit economics work."
                ]
            }
            
            reasons_fail = {
                "pet": [
                    "The idea already exists dominantly (Rover/Wag).",
                    "Unit economics are terrible for small marketplaces.",
                    "Trust & liability costs (insurance) will destroy margins.",
                    "Two-sided marketplaces are extremely hard to kickstart.",
                    "High customer churn due to direct relationships forming."
                ],
                "general": [
                    "Market is saturated with well-funded competitors.",
                    "Customer Acquisition Cost (CAC) will likely exceed LTV.",
                    "Operational complexity is higher than it appears.",
                    "Lack of clear differentiation from incumbents.",
                    "Revenue model is unproven or low-margin."
                ]
            }
            
            rw = reasons_work.get(sector, reasons_work["general"])
            rf = reasons_fail.get(sector, reasons_fail["general"])
            
            # Construct the fallback report
            draft = report_structure.replace("{idea}", idea)
            
            # Fill sections (Simulated intelligence)
            draft = draft.replace("[Summary of the idea, market context, and brutal reality check. Is it viable? High risk?]", 
                                  f"'{idea}' is a concept entering a competitive landscape. While the market shows growth, this idea faces significant execution risks. It requires distinct differentiation to survive against incumbents.")
            
            draft = draft.replace("[Bullet points of specific pain points. Who hurts? How bad?]",
                                  f"- Users struggle with finding reliable solutions for {idea}.\n- Lack of transparency in current offerings.\n- High cost or poor quality of existing alternatives.\n- Inconvenience of manual coordination.")
            
            draft = draft.replace("[Size, growth, trends]", evidence)
            
            draft = draft.replace("[Why is this hard? Margins? CAC?]",
                                  "Growth is real, but margins are likely thin. CAC will be high due to competition. Retention is the key challenge.")
            
            draft = draft.replace("[Who specifically will pay?]",
                                  "- Urban professionals with high disposable income.\n- Tech-savvy early adopters.\n- Users dissatisfied with current market leaders.")
            
            draft = draft.replace("[Names]", "Major incumbents in the sector (e.g., Market Leaders).")
            draft = draft.replace("[Alternatives]", "Manual solutions, local providers, DIY approaches.")
            draft = draft.replace("[Why will you likely fail against them? What is the moat?]",
                                  "Incumbents have deep pockets and brand trust. You need a 10x better experience, not just 'Uber for X'.")
            
            draft = draft.replace("[CAC, LTV, Churn, etc.]",
                                  "- Customer Acquisition Cost (CAC)\n- Lifetime Value (LTV)\n- Churn Rate\n- Take Rate / Margin")
            
            draft = draft.replace("[Efficiency, fulfillment, etc.]",
                                  "- Fulfillment Rate\n- Support Tickets per Order\n- Unit Economics per Transaction")
            
            draft = draft.replace("[1-5 specific risks. Be harsh.]",
                                  "1. Market Saturation: Competitors are everywhere.\n2. Unit Economics: Hard to make profitable per unit.\n3. Adoption: Users may not switch.\n4. Operations: Scaling quality is difficult.\n5. Funding: Investors are wary of this category.")
            
            draft = draft.replace("[1-5 actionable steps. Don't just say 'build app'. Say 'validate demand'.]",
                                  "1. Validate Demand: Get 100 signups before coding.\n2. Manual MVP: Run operations manually to test logic.\n3. Unit Economics: Prove you can make money on one transaction.\n4. Interviews: Talk to 50 potential users.\n5. Niche Down: Focus on a specific sub-segment first.")
            
            # Snapshot filling
            draft = draft.replace("[One sentence.]", f"A solution for {idea} targeting underserved users.")
            draft = draft.replace("[Core pain.]", "Inefficiency and lack of trust in the current market.")
            draft = draft.replace("[The product.]", f"A platform/service enabling seamless {idea}.")
            draft = draft.replace("[TAM/SAM/SOM.]", "Large TAM, but serviceable market depends on execution.")
            draft = draft.replace("[Evidence found.]", f"Found {evidence_count} market signals indicating interest.")
            draft = draft.replace("[Funding needs.]", "Pre-seed capital for MVP and initial traction.")
            draft = draft.replace("[Roles needed.]", "Founders with domain expertise and operational hustle.")
            
            # Reasons filling
            for i in range(5):
                draft = draft.replace(f"1. [Reason]", f"1. {rw[0]}", 1).replace(f"1. [Reason]", f"1. {rf[0]}", 1)
                draft = draft.replace(f"2. [Reason]", f"2. {rw[1]}", 1).replace(f"2. [Reason]", f"2. {rf[1]}", 1)
                draft = draft.replace(f"3. [Reason]", f"3. {rw[2]}", 1).replace(f"3. [Reason]", f"3. {rf[2]}", 1)
                draft = draft.replace(f"4. [Reason]", f"4. {rw[3]}", 1).replace(f"4. [Reason]", f"4. {rf[3]}", 1)
                draft = draft.replace(f"5. [Reason]", f"5. {rw[4]}", 1).replace(f"5. [Reason]", f"5. {rf[4]}", 1)
            
            draft = draft.replace("[Conclusion]", f"This idea ({idea}) has potential but is high-risk. It requires flawless execution and a focus on unit economics to survive. Do not build without validation.")
            
            draft += "\n\n(Generated via Smart Fallback - Set OPENAI_API_KEY for full AI analysis)"
            state.draft_snapshot = draft

        return state
