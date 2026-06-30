import streamlit as st
import json
from llama_cpp import Llama

# Set up web page title
st.set_page_config(page_title="Local AI Data Structurer", layout="wide")
st.title("🤖 Local AI: Unstructured to Structured Data")
st.caption("Running 100% Offline | Optimized for CPU")

# Cache the model so it only loads ONCE when the app starts
@st.cache_resource
def load_model():
    return Llama(
        model_path="./qwen2.5-1.5b-instruct-q4_k_m.gguf",
        n_ctx=2048,
        n_threads=4
    )

llm = load_model()

# Split layout into two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Unstructured Input")
    user_input = st.text_area(
        "Paste messy text, transcripts, or notes below:",
        height=300,
        placeholder="Type or paste something here..."
    )
    
    process_button = st.button("⚡ Transform Data", type="primary")

with col2:
    st.subheader("📊 Structured Actionable Output")
    
    if process_button and user_input:
        with st.spinner("Processing locally on CPU..."):
            # Prompt configuration
            prompt = f"""<|im_start|>system
You are a helpful assistant that extracts unstructured text into a strict JSON format. 
Your output must be raw JSON only, matching this schema:
{{
  "tasks": [
    {{"task_name": "string", "assignee": "string", "deadline_or_timeline": "string"}}
  ],
  "budget_mentions": [
    {{"item": "string", "cost": "string"}}
  ]
}}
<|im_end|>
<|im_start|>user
Extract the information from this text: {user_input}
<|im_end|>
<|im_start|>assistant
"""
            # Generate response
            response = llm(prompt, max_tokens=500, temperature=0.1)
            output_text = response['choices'][0]['text'].strip()
            
            try:
                # Format and display JSON nicely
                json_data = json.loads(output_text)
                st.json(json_data)
                
                # Add a download button for the JSON file
                st.download_button(
                    label="💾 Download JSON Dataset",
                    data=json.dumps(json_data, indent=2),
                    file_name="structured_dataset.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error("Failed to parse output as clean JSON. Try running again.")
                st.code(output_text)