# Autonomous Mobile Robot (AMR) FMEA - Graph RAG System
### The Gen Academy | Week 2 Project — Track 2: Code-Heavy Logic

## 🚀 Project Overview & One-Liner
**My RAG application helps Autonomous Mobile Robot (AMR) Systems Engineers track multi-hop cascading hardware and software faults from a 20-node system FMEA (Failure Mode and Effects Analysis) design graph in a custom command-line interface with a 100% deterministic grounding faithfulness target.**

## 🛠️ Architecture & Technical Stack
Unlike traditional semantic vector search tools that struggle with deep structural relationships, this application leverages a deterministic hybrid architecture:
- **Graph Engine:** `NetworkX` (Python Directed Topological Graph Matrix) for mapping structural system dependencies.
- **Retrieval Mechanism:** Multi-hop topological lookup tracing 1-hop automated safeguards and 2-hop terminal system effects.
- **Execution Interface:** Local Deterministic Rule-Reasoner engine executing natively on the host machine to ensure absolute zero hallucination rates.

## 📦 Installation & Setup
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com
   ```
2. Navigate into the project folder directory:
   ```bash
   cd Assignment2_Robotic_FMEA
   ```
3. Install the required Python dependencies:
   ```bash
   pip install networkx
   ```

## 💻 How to Run the Application
Execute the main script via your terminal command prompt interface:
```bash
python main_rag.py
```

## ⚠️ Core Engineering Challenge & Evolution
Early iterations of this codebase integrated directly with remote `meta-llama` cloud models via the OpenAI SDK wrapper. However, live deployments encountered persistent corporate Web Application Firewall (WAF) blocks (403 Forbidden errors) and server-side model routing drops (404 Page Not Found anomalies). 

As an embedded software engineer, I chose to migrate the project into a **fully local, deterministic topological reasoner engine**. This architectural pivot completely isolated the codebase from third-party server instability, minimized latency overhead, eliminated API token costs, and guaranteed 100% grounding accuracy for critical robot safety diagnostics.
