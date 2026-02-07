import streamlit as st
import os
import io
import contextlib
import re
from dotenv import load_dotenv
from core.triage_system import TriageSystem

# Load env
load_dotenv()

st.set_page_config(page_title="Medical Triage System", page_icon="🏥", layout="wide")

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

st.title("🏥 Multi-Agent Medical Triage System")
st.markdown("---")

# Sidebar for Config
with st.sidebar:
    st.header("Configuration")
    api_key_env = os.getenv("OPENAI_API_KEY", "")
    api_key = st.text_input("API Key (OpenAI/Groq)", type="password", value=api_key_env)
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    else:
        st.warning("Please provide an API Key to proceed.")

# Inputs
col1, col2 = st.columns(2)
with col1:
    symptoms = st.text_area("Symptoms", height=150, placeholder="e.g., Severe headache, stiff neck, sensitivity to light...")
with col2:
    age = st.text_input("Age", placeholder="e.g., 25")
    history = st.text_area("Medical History", height=100, placeholder="e.g., None, Diabetes, Hypertension...")

if st.button("Run Triage Analysis", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ API Key is missing!")
    elif not symptoms or not age:
        st.error("❌ Please provide both Symptoms and Age.")
    else:
        # Initialize System
        try:
            with st.spinner("Initializing Agents..."):
                system = TriageSystem(api_key=api_key)
            
            inputs = {
                "symptoms": symptoms,
                "age": age,
                "history": history
            }

            st.info("🤖 Agents are deliberating... Please wait.")

            # Capture stdout to show the "thinking" process
            f = io.StringIO()
            result = None
            
            with contextlib.redirect_stdout(f):
                try:
                     result = system.run_simulation(inputs)
                except Exception as e:
                    st.error(f"Error during simulation: {e}")
            
            logs = strip_ansi(f.getvalue())
            
            # Layout for results
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                st.subheader("📋 Agent Deliberation Logs")
                st.code(logs, language="text", line_numbers=True)

            with res_col2:
                if result:
                    st.subheader("🏆 Final Decision")
                    st.markdown("---")
                    
                    decision = result.get("final_decision", "UNKNOWN").upper()
                    
                    color = "grey"
                    if "URGENT" in decision: color = "#FF4B4B"
                    elif "CONSULT" in decision: color = "#FFA500"
                    elif "SELF-CARE" in decision: color = "#09AB3B"
                    elif "REFUSED" in decision: color = "#555555"

                    st.markdown(
                        f"""
                        <div style="
                            background-color: {color};
                            color: white;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            font-size: 24px;
                            font-weight: bold;
                            margin-bottom: 20px;
                        ">
                            {decision}
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"**Reasoning Summary:**\n\n{result.get('reasoning_summary', 'N/A')}")
                    
                    safety = result.get('safety_notes', [])
                    if safety:
                        st.warning("**⚠️ Safety Notes:**\n\n" + "\n".join([f"- {s}" for s in safety]))

                    next_steps = result.get('next_steps', [])
                    if next_steps:
                        st.info("**👉 Next Steps:**\n\n" + "\n".join([f"- {s}" for s in next_steps]))
                    
                    with st.expander("Raw JSON Output"):
                        st.json(result)

        except Exception as e:
            st.error(f"System Error: {e}")
