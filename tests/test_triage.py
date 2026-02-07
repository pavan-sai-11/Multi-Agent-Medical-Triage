import unittest
from unittest.mock import MagicMock
from core.triage_system import TriageSystem
from utils.llm_client import LLMClient

class TestTriageSystem(unittest.TestCase):
    def setUp(self):
        # Mock LLM Client
        self.mock_client = MagicMock(spec=LLMClient)
        
        # Define side effects for generate based on prompt content (simplified)
        def generate_side_effect(system_prompt, user_prompt, **kwargs):
            if "Symptom Interpretation Agent" in system_prompt:
                return {
                    "triage_level": "consult",
                    "risk_score": 50,
                    "confidence": 80,
                    "red_flags": [],
                    "symptom_summary": "Headache, mild fever"
                }
            elif "Risk Stratification Agent" in system_prompt:
                 if "review_target" in user_prompt: # Round 2
                     return {"red_flags": []}
                 return {
                    "triage_level": "consult",
                    "risk_score": 60,
                    "confidence": 70,
                    "red_flags": [],
                    "worst_case_analysis": "Meningitis unlikely but possible"
                }
            elif "Evidence Quality Agent" in system_prompt:
                return {
                    "confidence": 90,
                    "data_quality_score": 80,
                    "missing_information": []
                }
            elif "Ethics & Safety Agent" in system_prompt:
                if "review_target" in user_prompt: # Round 2
                    return {"veto": False}
                return {
                    "triage_level": "consult",
                    "veto": False
                }
            elif "Coordinator Agent" in system_prompt:
                return {
                    "final_decision": "CONSULT",
                    "reasoning_summary": "Symptoms suggest mild infection.",
                    "safety_notes": ["Monitor temperature"],
                    "confidence_level": "Medium",
                    "next_steps": ["See GP if persists"]
                }
            return {}

        self.mock_client.generate.side_effect = generate_side_effect
        
        # Initialize system with mocked client injection
        # Note: TriageSystem creates its own client. We need to patch it or inject it.
        # Since TriageSystem.__init__ instantiates LLMClient, we can mock LLMClient class in the module.
        # But for this test, we can just replace the client on the instance.
        self.system = TriageSystem(api_key="dummy")
        
        # Replace the client in all agents
        self.system.client = self.mock_client
        self.system.symptom_agent.client = self.mock_client
        self.system.risk_agent.client = self.mock_client
        self.system.evidence_agent.client = self.mock_client
        self.system.ethics_agent.client = self.mock_client
        self.system.coordinator_agent.client = self.mock_client

    def test_run_simulation(self):
        inputs = {"symptoms": "Headache", "age": "25"}
        result = self.system.run_simulation(inputs)
        
        self.assertEqual(result["final_decision"], "CONSULT")
        # Verify call counts
        # 1 call per agent in Round 1 (4)
        # 2 calls in Round 2 (Risk, Ethics review)
        # 1 call in Round 3 (Coordinator)
        # Total 7 calls
        self.assertEqual(self.mock_client.generate.call_count, 7)

if __name__ == '__main__':
    unittest.main()
