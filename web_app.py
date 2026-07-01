import streamlit as st
import os
import sqlite3
import json
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# Set up clean web shell metadata configuration matrix
st.set_page_config(
    page_title="CoreText AI — Engine Workspace",
    page_icon="⚡",
    layout="wide"
)

# 🧠 Title Block Layout Pipeline
st.title("⚡ CoreText AI — Offline Enterprise Data Structurer")
st.caption("Operational Runtime: 100% Local CPU Architecture Validation Showcase")

# 📥 Persistent Weight Verification & Auto-Download Layer
MODEL_DIR = "."
MODEL_FILE = "qwen2.5-1.5b-instruct-q4_k_m.gguf"
local_model_path = os.path.join(MODEL_DIR, MODEL_FILE)

@st.cache_resource
def initialize_local_ai_engine():
    # If model weights don't exist in the container directory, stream them down immediately
    if not os.path.exists(local_model_path):
        with st.spinner("📦 Initialization: Streaming Qwen-1.5B GGUF weights from network cache... Please wait..."):
            try:
                hf_hub_download(
                    repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF",
                    filename=MODEL_FILE,
                    local_dir=MODEL_DIR,
                    local_dir_use_symlinks=False
                )
            except Exception as e:
                st.error(f"Network handshake failed during weight download sequence: {e}")
                return None
                
    try:
        # Load the llama-cpp-python binding runtime engine inside memory limits
        llm = Llama(
            model_path=local_model_path,
            n_ctx=2048,
            n_threads=2,       # Optimized for standard multi-tenant cloud CPUs
            verbose=False
        )
        return llm
    except Exception as e:
        st.error(f"Runtime Engine Matrix Compilation Error: {e}")
        return None

# Instantiating AI Engine
llm_engine = initialize_local_ai_engine()

# 🗄️ SQLite History State Layers Initialization
def initialize_persistence_matrix():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            raw_input TEXT,
            structured_json TEXT
        )
    """)
    conn.commit()
    conn.close()

initialize_persistence_matrix()

# 📑 Main Presentation Interface Columns layout split
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Raw Unstructured Input Stream")
    user_input_stream = st.text_area(
        "Paste messy telemetry logs, stream dumps, or scattered notes here:",
        height=280,
        placeholder="Example: LOG [2026-07-01 10:14] Server-A temperature spike 84C. Admin action triggered by Jayanth."
    )
    
    submit_button = st.button("⚡ Transform & Structure Data", use_container_width=True)

with col2:
    st.subheader("📤 Validated Schema-Aligned JSON Object")
    
    if submit_button:
        if not user_input_stream.strip():
            st.warning("Input buffer empty. Supply a text stream execution target.")
        elif llm_engine is None:
            st.error("AI Engine initialization offline. Check architecture runtime boundaries.")
        else:
            with st.spinner("Processing local CPU inference loops..."):
                # System instructions forcing valid deterministic structured mapping
                prompt = (
                    "<|im_start|>system\n"
                    "You are a core data structure engine. Analyze the input stream and extract the information into a single, clean, valid JSON object. Do not explain, do not add text outside the JSON, do not use markdown code blocks.\n"
                    "<|im_end|>\n"
                    f"<|im_start|>user\n{user_input_stream}\n<|im_end|>\n"
                    "<|im_start|>assistant\n"
                )
                
                try:
                    # CPU Execution inference step block
                    response = llm_engine(
                        prompt,
                        max_tokens=512,
                        temperature=0.1,  # Low temperature forces deterministic precision
                        stop=["<|im_end|>", "\n\n"]
                    )
                    
                    raw_output_text = response["choices"][0]["text"].strip()
                    
                    # Clean up random character fragments if any exist outside the boundaries
                    if "```json" in raw_output_text:
                        raw_output_text = raw_output_text.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw_output_text:
                        raw_output_text = raw_output_text.split("```")[1].split("```")[0].strip()
                        
                    # Validate parsing conformity via standard json decoder engine
                    parsed_json_object = json.loads(raw_output_text)
                    formatted_json_string = json.dumps(parsed_json_object, indent=4)
                    
                    # Print parsed code structure direct to browser workspace
                    st.code(formatted_json_string, language="json")
                    
                    # Persist record entry immediately to history database cache
                    conn = sqlite3.connect("history.db")
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO records (raw_input, structured_json) VALUES (?, ?)",
                        (user_input_stream, formatted_json_string)
                    )
                    conn.commit()
                    conn.close()
                    st.success("Data parsing loop successfully completed. Records committed to database storage.")
                    
                except json.JSONDecodeError:
                    st.error("Engine Output Formatting Error: Code structure broke parsing constraints.")
                    st.text_area("Raw Response Output Fragment:", value=raw_output_text, height=150)
                except Exception as e:
                    st.error(f"Inference Loop Disruption Error: {e}")
    else:
        st.info("Awaiting execution trigger request. Fill out the unstructured input matrix to start.")

# 📜 History Database View Component Section Layout
st.markdown("---")
st.subheader("📜 System Logs & Persistence Layer Ledger (`history.db`)")

conn = sqlite3.connect("history.db")
cursor = conn.cursor()
cursor.execute("SELECT id, timestamp, raw_input, structured_json FROM records ORDER BY id DESC LIMIT 5")
db_rows = cursor.fetchall()
conn.close()

if db_rows:
    for row in db_rows:
        with st.expander(f"Record Entry #{row[0]} — Timestamp: {row[1]}"):
            st.text(f"Raw Input Source Data:\n{row[2]}")
            st.code(row[3], language="json")
else:
    st.caption("Local database history cache empty. Successful