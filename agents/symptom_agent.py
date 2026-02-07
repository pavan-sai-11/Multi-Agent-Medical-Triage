import json
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class SymptomInterpretationAgent(BaseAgent):
    def __init__(self, client: Any):
        super().__init__("Symptom Interpretation Agent", client)

    def analyze(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
        You are the Symptom Interpretation Agent.
        Your Goal: Extract structured symptoms and detect RED FLAGS.
        Constraints:
        - NEVER name diseases.
        - NEVER diagnose.
        - Output JSON only.

        Output Format:
        {
            "triage_level": "self-care | consult | urgent | unknown",
            "risk_score": 0-100,
            "confidence": 0-100,
            "red_flags": ["list any potentially serious symptoms"],
            "symptom_summary": "Structured list of symptoms"
        }
        """

        user_prompt = f"""
        Analyze the following patient inputs:
        {json.dumps(inputs, indent=2)}

        Identify symptoms and red flags.
        """

        return self.client.generate(system_prompt, user_prompt)
