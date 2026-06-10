# 🏥 MediGuide AI — Health Information Agent

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

> An AI-powered health information agent that searches real medical sources in real time, checks for emergencies first, and delivers structured, sourced responses — built with LangGraph, Groq, and Tavily.

⚠️ **Disclaimer:** MediGuide provides general health information only. It is NOT a substitute for professional medical advice. Always consult a qualified healthcare professional.


## ✨ What Makes This Different

Most health chatbots answer from **training data alone** — which can be outdated or hallucinated. MediGuide:

- 🔍 **Searches in real time** — fetches live content from WHO, NHS, Mayo Clinic via Tavily
- 🚨 **Safety first** — scans for emergency keywords BEFORE the LLM does anything
- 📋 **Structured responses** — fixed output format enforced via prompt engineering
- 📚 **Always cites sources** — never states medical facts without backing them up
- ⚕️ **Never diagnoses** — responsible AI design baked into the system prompt

---

## 🏗️ Architecture

```
User types symptoms
        ↓
[Node 1] Emergency Check
        ↓
Emergency?
├── YES → 🚨 "Call 112 now" → STOP
└── NO  ↓
[Node 2] Tavily Web Search
  (WHO, NHS, Mayo Clinic)
        ↓
[Node 3] LLM Analysis
  (Groq + Llama 3.3)
        ↓
Structured response shown to user
```

This is a **ReAct-style agent loop** — Reason → Act → Observe — implemented as a LangGraph state machine. Each node does one job, passes results via shared state, and conditional edges route emergencies away from the normal flow entirely.

---

## 🛠️ Tech Stack

| Tool | Role | Why |
|---|---|---|
| **LangGraph** | Agent flow control | Defines step-by-step logic with conditional paths |
| **LangChain** | LLM + tool connector | Connects Groq, Tavily and agent cleanly |
| **Groq + Llama 3.3** | The LLM brain | Free, extremely fast, open source |
| **Tavily** | Web search | Built for AI agents — returns clean text not messy HTML |
| **Streamlit** | Web UI | Python into web app with zero frontend code |

---

## 📁 Project Structure

```
mediguide/
├── prompts.py       # Agent personality and rules (prompt engineering)
├── tools.py         # Search + emergency safety check functions
├── agent.py         # LangGraph brain — connects everything
├── app.py           # Streamlit UI — what users see
└── requirements.txt # All dependencies
```

Each file has exactly **one responsibility** — clean separation of concerns makes the project easy to extend and debug.

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/khushimgajjar/mediguide-agent
cd mediguide-agent
```

### 2. Install dependencies
```bash
pip install -r mediguide/requirements.txt
```

### 3. Set up API keys
Create a `.env` file in the `mediguide/` folder:
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your free keys here:
- Groq → https://console.groq.com
- Tavily → https://app.tavily.com

### 4. Run the app
```bash
cd mediguide
streamlit run app.py
```

---


---

## 📝 Blog Post

Read the full technical breakdown on Medium:

👉 [Building MediGuide: An AI Health Agent with LangGraph, Groq and Tavily](https://medium.com/@khushimgajjar)


[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/khushi-gajjar1)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/khushimgajjar)
[![Kaggle](https://img.shields.io/badge/Kaggle-Expert-20BEFF?style=flat-square&logo=kaggle)](https://www.kaggle.com/khushikhushikhushi)
[![Medium](https://img.shields.io/badge/Medium-Blog-black?style=flat-square&logo=medium)](https://medium.com/@khushimgajjar)

---

*Built with ❤️ for responsible, accessible health information*
