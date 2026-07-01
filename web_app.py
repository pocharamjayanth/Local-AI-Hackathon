import streamlit as st
from llama_cpp import Llama
import json
import sqlite3
import datetime
import os
import subprocess

# --- CLOUD INITIALIZATION ENGINE ---
# Automatically downloads model weights if running on a fresh cloud instance
if not os.path.exists("qwen2.5-1.5b-instruct-q4_k_m.gguf"):
    with st.spinner("Initial boot: Downloading CPU-optimized model weights... Please wait."):
        subprocess.run(["python", "download_model.py"])

# --- DATABASE SETUP ---
DB_FILE = "history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_text TEXT,
            structured_output TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_extraction(input_text, output_json):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO extractions (timestamp, input_text, structured_output) VALUES (?, ?, ?)",
        (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), input_text, json.dumps(output_json))
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, input_text, structured_output FROM extractions ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# Initialize SQLite Database
init_db()

# --- STREAMLIT UI CONFIGURATION ---
st.set_page_config(page_title="CoreText AI", page_icon="⚡", layout="wide")

st.title("⚡ CoreText AI — Offline Enterprise Data Structurer")
st.caption("Running 100% locally on CPU via Qwen-2.5-1.5B-Instruct-GGUF")

# --- LOCAL MODEL INITIALIZATION ---
@st.cache_resource
def load_model():
    # Caches the model locally so it doesn't reload on every webpage interaction
    return Llama(
        model_path="qwen2.5-1.5b-instruct-q4_k_m.gguf",
        n_ctx=1024,  # Context window cap
        n_threads=4  # Optimized for standard consumer CPUs
    )

try:
    llm = load_model()
except Exception as e:
    st.error(f"Failed to load local model weights: {e}")
    st.stop()

# --- APP LAYOUT ---
tabs = st.tabs(["🚀 Data Extraction Engine", "📊 Saved Database History"])

with tabs[0]:
    st.subheader("Unstructured Telemetry / Text Stream Input")
    
    # Input field with safety info
    raw_text = st.text_area(
        "Paste raw meeting notes, logs, or schedules below:",
        height=200,
        placeholder="Example: John needs to purchase a test monitor configuration for $150 by this Friday..."
    )
    
    # Validation constraint check to prevent tensor context crashes
    MAX_CHAR_LIMIT = 1500
    current_length = len(raw_text)
    
    if current_length > MAX_CHAR_LIMIT:
        st.warning(f"⚠️ Input is too long ({current_length}/{MAX_CHAR_LIMIT} chars). Truncating text to safe limits to prevent local CPU memory overflow.")
        processed_input = raw_text[:MAX_CHAR_LIMIT]
    else:
        processed_input = raw_text

    if st.button("Execute Structural Extraction", type="primary"):
        if not processed_input.strip():
            st.warning("Please provide an unstructured data stream first.")
        else:
            # Latency handling with structural feedback indicator
            with st.spinner("Local AI processing active... Mapping content to target JSON layout (No cloud APIs used)."):
                
                system_prompt = (
                    "You are a strict data parsing engine. Analyze the input text and extract tasks and budget items. "
                    "Output a valid JSON object matching this schema precisely: "
                    "{ 'tasks': [ { 'task_name': string, 'assignee': string, 'deadline_or_timeline': string } ], "
                    "'budget': [ { 'item': string, 'cost': string } ] }. Do not include explanations, codeblocks, markdown, or text outside the raw JSON structure."
                )
                
                # Format for Qwen-2.5-Instruct sequence handling
                formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{processed_input}<|im_end|>\n<|im_start|>assistant\n"
                
                try:
                    # Run CPU execution loop
                    response = llm(
                        formatted_prompt,
                        max_tokens=512,
                        temperature=0.1,  # Lower values maximize deterministic accuracy
                        stop=["<|im_end|>", "<|im_start|>"]
                    )
                    
                    raw_output = response["choices"][0]["text"].strip()
                    
                    # Clean potential formatting bugs gently
                    if raw_output.startswith("```json"):
                        raw_output = raw_output[7:]
                    if raw_output.endswith("```"):
                        raw_output = raw_output[:-3]
                    
                    parsed_json = json.loads(raw_output.strip())
                    
                    st.success("✅ Extraction Complete & Aligned to Target Schema!")
                    
                    # Display Side-by-Side Outputs
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Visual Structural Map")
                        st.write(parsed_json)
                    with col2:
                        st.subheader("Validated JSON Stream")
                        st.code(json.dumps(parsed_json, indent=4), language="json")
                    
                    # PERSISTENCE ENGINE: Save locally to SQLite
                    save_extraction(processed_input, parsed_json)
                    st.info("💾 Record successfully synchronized to local database storage.")
                    
                except json.JSONDecodeError:
                    st.error("⚠️ Graceful Failure Handling triggered: The model produced an invalid JSON formatting sequence. Please re-run or refine the text structure.")
                    st.code(raw_output)
                except Exception as e:
                    st.error(f"Execution Error occurred: {e}")

with tabs[1]:
    st.subheader("🗄️ SQLite Local Telemetry Storage")
    history_records = get_history()
    
    if not history_records:
        st.info("No records found in local database storage.")
    else:
        # Build scannable history table layout
        for timestamp, inp, out in history_records:
            with st.expander(f"🕒 Record Timestamp: {timestamp}"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown("**Original Processed Input:**")
                    st.text(inp)
                with c2:
                    st.markdown("**Stored Structural Object:**")
                    st.code(out, language="json")