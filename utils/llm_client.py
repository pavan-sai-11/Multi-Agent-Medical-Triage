import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.is_groq = False
        
        if not self.api_key:
            print("WARNING: No API key found. System will fail if real LLM calls are attempted.")
            self.client = None
        else:
            if self.api_key.startswith("gsk_"):
                self.is_groq = True
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
            else:
                self.client = OpenAI(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str, model: str = "gpt-4o", json_mode: bool = True) -> Dict[str, Any]:
        if not self.client:
            raise ValueError("LLM Client not initialized with an API key.")

        # Adjust model for Groq if necessary
        if self.is_groq and "gpt" in model:
            model = "llama-3.3-70b-versatile"

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"} if json_mode else None
            )
            content = response.choices[0].message.content
            if json_mode:
                return json.loads(content)
            return content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return {"error": str(e)}
