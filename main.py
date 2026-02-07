import sys
import os
import json
from core.triage_system import TriageSystem
import colorama
from colorama import Fore, Style

colorama.init()

def main():
    print(Fore.GREEN + "🏥 MULTI-AGENT MEDICAL TRIAGE SYSTEM 🏥" + Style.RESET_ALL)
    print("--------------------------------------------------")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(Fore.YELLOW + "WARNING: OPENAI_API_KEY not found in environment.")
        print("Please set it in .env or environment variables." + Style.RESET_ALL)
        # Allow user to input key manually
        key_input = input("Enter OpenAI API Key (or press Enter to exit): ").strip()
        if key_input:
            api_key = key_input
        else:
            print("Exiting...")
            return

    system = TriageSystem(api_key=api_key)

    while True:
        print("\n📝 NEW CASE ENTRY")
        print("Enter patient details (leave empty to finish entry):")
        
        symptoms = input("Symptoms > ")
        if not symptoms:
            break
            
        age = input("Age > ")
        history = input("Medical History > ")
        
        inputs = {
            "symptoms": symptoms,
            "age": age,
            "history": history
        }
        
        print("\n✅ Submitting case to agents...")
        try:
            result = system.run_simulation(inputs)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(Fore.RED + f"Error during deliberation: {e}" + Style.RESET_ALL)

        cont = input("\nProcess another case? (y/n) > ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
