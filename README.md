---
title: CoreText AI
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: web_app.py
pinned: false
---

 ⚡ Awesome CPU-First AI — CoreText Engine Edition

 👥 Developed By: Team Local Host
* **P. Jayanth**
* **Gargeya**
* **Krishna**

Training needs GPUs. Inference usually doesn't. Start with CPU; justify the GPU.  
A curated architecture blueprint, technical data stack, and implementation evidence for running AI inference on CPU — the platform you already have everywhere.

Built specifically as an operational showcase for the **Local AI Hackathon**, **CoreText AI** is an offline-first, CPU-optimized enterprise application engineered to transform unstructured data streams (logs, text streams, scattered schedules) into validated, schema-aligned JSON objects completely on-device.

### 🚀 Quick Start (Local Workspace Verification)

Follow this path from zero to local CPU inference — no cloud API dependencies, no CUDA requirements, no container overhead.

1. Repository Initialisation & Environment Isolation
Clone the repository and jump into your isolated working folder structure:
```powershell
git clone [https://github.com/pocharamjayanth/Local-AI-Hackathon.git](https://github.com/pocharamjayanth/Local-AI-Hackathon.git)
cd Local-AI-Hackathon
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate