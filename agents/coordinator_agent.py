import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class CoordinatorAgent(BaseAgent):
    def __init__(self, client: Any):
        super().__init__("Coordinator Agent", client)

    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes the final decision based on all agent outputs and the case data.
        """
        # Extract data from the final_context passed by TriageSystem
        case_data = inputs.get("initial_inputs", {})
        round1_outputs = inputs.get("round1", {})
        round2_outputs = inputs.get("round2", {})
        
        system_prompt = """
        You are the Coordinator Agent.
        Your Goal: Synthesize the debate and produce the FINAL OUTPUT.
        
        System Rules:
        1. If ANY red_flag -> URGENT
        2. If confidence < 40% -> REFUSE
        3. If disagreement > 50% -> REFUSE
        4. If avg risk > 70% -> CONSULT
        5. Else -> SELF-CARE
        
        Input: Case data + Agent opinions.
        Output: Final JSON decision.
        
        Output Format:
        {
            "final_decision": "SELF-CARE | CONSULT | URGENT | REFUSED",
            "reasoning_summary": "Plain language explanation",
            "safety_notes": ["warnings"],
            "confidence_level": "Low | Medium | High",
            "next_steps": ["non-diagnostic guidance"]
        }
        """

        user_prompt = f"""
        Case Data:
        {json.dumps(case_data, indent=2)}

        Round 1 Analysis (Independent):
        {json.dumps(round1_outputs, indent=2)}
        
        Round 2 Analysis (Review):
        {json.dumps(round2_outputs, indent=2)}
        """

        return self.client.generate(system_prompt, user_prompt)

    # synthesize method removed as it is superseded by analyze

