import json
from llama_cpp import Llama

# Initialize the offline CPU model
print("Loading local CPU model...")
llm = Llama(
    model_path="./qwen2.5-1.5b-instruct-q4_k_m.gguf",
    n_ctx=2048,  # Context window
    n_threads=4  # Adjust based on your CPU cores
)

# Example unstructured data (can be text extracted from audio, PDF, or images)
unstructured_input = """
Meeting notes from June 30th. John said the front-end redesign will cost $5000 and take 3 weeks. 
Sarah mentioned that the server migration is delayed until next Tuesday because of a power outage. 
We need to follow up with Mark regarding the API keys by tomorrow afternoon.
"""

# Prompt to enforce structured output format
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
Extract the information from this text: {unstructured_input}
<|im_end|>
<|im_start|>assistant
"""

print("Processing data locally...")
response = llm(prompt, max_tokens=500, temperature=0.1)
output_text = response['choices'][0]['text'].strip()

print("\n--- Structured Actionable Output (JSON) ---")
print(output_text)

# Save to a local file
with open("structured_output.json", "w") as f:
    f.write(output_text)
print("\nSaved output to structured_output.json")