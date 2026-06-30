\# ⚡ CoreText AI — Offline Enterprise Data Structurer



An offline-first, CPU-optimized AI engine designed to seamlessly transform unstructured telemetry, scattered notes, log files, and text streams into highly structured, actionable JSON datasets. 



Built specifically for the \*\*Local AI Hackathon\*\*, this application runs 100% locally on standard consumer CPUs without requiring an active internet connection, external APIs, or heavy GPU hardware.



\---



\## 🚀 Core Technical Alignment



This project strictly adheres to all hackathon edge-computing constraints:

\* \*\*Offline-First Architecture:\*\* Zero remote API dependencies. Token evaluation and parsing take place entirely on-device, safeguarding data privacy.

\* \*\*CPU-Optimized Inference:\*\* Powered by a 4-bit quantized \*\*Qwen-2.5-1.5B-Instruct-GGUF\*\* model running over a high-performance `llama-cpp-python` backend tailored for speed on standard CPU architectures.

\* \*\*Deterministic Structured Outputs:\*\* Utilizes strict system prompting structures to enforce structural validation rules directly onto unstructured data streams.



\---



\## 🛠️ Tech Stack \& Architecture



\* \*\*Frontend Dashboard:\*\* Streamlit (Python-based enterprise-grade UI)

\* \*\*Local Inference Engine:\*\* Llama-cpp-python

\* \*\*Local Large Language Model:\*\* Qwen-2.5 1.5B Instruct (Quantized Q4\_K\_M GGUF format)

\* \*\*Environment Isolation:\*\* Python Virtual Environment (`venv`)



\---



\## ⚙️ Local Setup Installation Instructions



Follow these step-by-step instructions to clone, configure, and execute the system in \*\*Windows PowerShell 5.1\*\*:



\### 1. Environment Initialization

Clone the repository and navigate into the working folder structure:

```powershell

git clone \[https://github.com/pocharamjayanth/Local-AI-Hackathon.git](https://github.com/pocharamjayanth/Local-AI-Hackathon.git)

cd Local-AI-Hackathon

