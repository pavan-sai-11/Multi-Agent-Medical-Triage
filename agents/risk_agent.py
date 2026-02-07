import json
from typing import Dict, Any
from agents.base_agent import BaseAgent

class RiskStratificationAgent(BaseAgent):
    def __init__(self, client: Any):
        super().__init__("Risk Stratification Agent", client)

    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
        You are the Risk Stratification Agent (The Skeptic).
        Your Goal: Assume the WORST PLAUSIBLE CASE. Penalize optimism.
        Constraints:
        - Flag anything potentially life-threatening.
        - Output JSON only.

        Output Format:
        {
            "triage_level": "self-care | consult | urgent | unknown",
            "risk_score": 0-100,
            "confidence": 0-100,
            "red_flags": ["worst-case scenarios"],
            "worst_case_analysis": "Explanation of what could go wrong"
        }
        """

        user_prompt = f"""
        Evaluate the risks for:
        {json.dumps(inputs, indent=2)}
        """

        return self.client.generate(system_prompt, user_prompt)
