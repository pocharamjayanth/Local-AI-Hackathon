import streamlit as st
import json
import time
from llama_cpp import Llama

# 1. Page Configuration & Professional Theme Styling
st.set_page_config(
    page_title="CoreText AI | Enterprise Data Structurer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished typography and cards
st.markdown("""
    <style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #2563EB;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Optimized Model Loading (Cached)
@st.cache_resource
def load_model():
    return Llama(
        model_path="./qwen2.5-1.5b-instruct-q4_k_m.gguf",
        n_ctx=2048,
        n_threads=4
    )

with st.spinner("Initializing local secure environment..."):
    llm = load_model()

# 3. Sidebar Panel (System Control & Metadata)
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=80)
    st.markdown("## System Configuration")
    st.info("**Environment:** 100% Offline\n\n**Compute:** CPU-Optimized (Edge Mode)")
    
    st.markdown("---")
    st.markdown("### Target Extraction Schema")
    st.caption("Enforcing structural integrity via localized JSON schemas.")
    st.json({
        "tasks": ["task_name", "assignee", "deadline_or_timeline"],
        "budget_mentions": ["item", "cost"]
    })

# 4. Main Dashboard Header
st.markdown('<div class="main-title">⚡ CoreText AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enterprise-grade offline extraction engine for unstructured telemetry and data streams.</div>', unsafe_allow_html=True)

# 5. Split Workspace Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 Unstructured Data Input")
    st.caption("Paste meeting transcripts, system logs, email dumps, or raw notes below.")
    
    user_input = st.text_area(
        label="Raw Input Stream",
        height=320,
        placeholder="Example: John mentioned that the front-end redesign will cost $5000 and take 3 weeks...",
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    process_button = st.button("🚀 Execute Structural Extraction", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📊 Actionable Structured Output")
    st.caption("Validated JSON fields compiled locally via CPU token evaluation.")
    
    if process_button:
        if not user_input.strip():
            st.warning("⚠️ Input stream is empty. Please provide raw text data to analyze.")
        else:
            # High-performance status banner
            status_container = st.empty()
            status_container.info("🧠 Processing locally on CPU cores...")
            
            start_time = time.time()
            
            # Prompt Engineering Block
            prompt = f"""<|im_start|>system
You are a precise data extraction agent. Extract structured information matching this strict schema:
{{
  "tasks": [
    {{"task_name": "string", "assignee": "string", "deadline_or_timeline": "string"}}
  ],
  "budget_mentions": [
    {{"item": "string", "cost": "string"}}
  ]
}}
Output raw valid JSON only. Do not wrap in markdown blocks. Do not add conversational text.
<|im_end|>
<|im_start|>user
{user_input}
<|im_end|>
<|im_start|>assistant
"""
            # Inference execution
            response = llm(prompt, max_tokens=500, temperature=0.1)
            output_text = response['choices'][0]['text'].strip()
            
            processing_time = round(time.time() - start_time, 2)
            status_container.empty() # Clear the processing message
            
            try:
                # Performance Summary Card
                st.markdown(f"""
                    <div class="metric-card">
                        <strong>Pipeline Metrics:</strong> Success | 
                        <strong>Execution Time:</strong> {processing_time}s | 
                        <strong>Compute Agent:</strong> Qwen-2.5-Local
                    </div>
                """, unsafe_allow_html=True)
                
                # Visualized JSON Output
                json_data = json.loads(output_text)
                st.json(json_data)
                
                # Professional Download Triggers
                st.markdown("---")
                st.download_button(
                    label="💾 Export Structured Dataset (.json)",
                    data=json.dumps(json_data, indent=2),
                    file_name="structured_output.json",
                    mime="application/json",
                    use_container_width=True
                )
            except Exception as e:
                st.error("🚨 Extraction parsing anomaly. System output did not strictly align with standard JSON schema.")
                with st.expander("Review Raw LLM Stream Output"):
                    st.code(output_text)
    else:
        # Placeholder view before clicking process
        st.info("💡 Awaiting input stream. Paste unstructured text data in the left panel and execute.")