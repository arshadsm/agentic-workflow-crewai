# 🤖 Agentic Workflow with CrewAI

> **Production multi-agent document verification system built with CrewAI and LangChain.**  
> Based on real implementation automating Florida DL & MV document verification workflows — reducing manual review time by 70%.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.30+-orange.svg)](https://crewai.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🏗️ Architecture

```
                    User / API Request
                           │
                           ▼
              ┌─────────────────────────┐
              │   FastAPI Entry Point    │
              │   JWT Auth + Rate Limit  │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │   Document Verification  │
              │        Crew             │
              └────────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Agent 1     │  │  Agent 2     │  │  Agent 3     │  │  Agent 4     │
│  Classifier  │→ │  Extractor   │→ │  Validator   │→ │  Reporter    │
│              │  │              │  │              │  │              │
│ • Doc type   │  │ • Field OCR  │  │ • Rules eng. │  │ • Audit rpt  │
│ • Quality    │  │ • Gov lookup │  │ • Compliance │  │ • Pass/Fail  │
│ • Routing    │  │ • Cross-ref  │  │ • Flagging   │  │ • Trace log  │
└──────────────┘  └──────┬───────┘  └──────────────┘  └──────────────┘
                         │
                         ▼
              ┌─────────────────────────┐
              │     MCP Tool Layer       │
              │  Government Data API     │
              │  (Real-time auth data)   │
              └─────────────────────────┘
                         │
                         ▼
              ┌─────────────────────────┐
              │   MongoDB Audit Log      │
              │   CloudWatch Metrics     │
              └─────────────────────────┘
```

---

## ⚡ Key Features

| Feature | Detail |
|---------|--------|
| **4-Agent Pipeline** | Classifier → Extractor → Validator → Reporter (sequential + memory) |
| **MCP Tool Integration** | Real-time government database queries prevent hallucination |
| **Shared Crew Memory** | Agents share context via OpenAI embeddings |
| **PII-Safe Logging** | All PII masked in logs; compliant with data privacy standards |
| **Audit Trail** | Every agent decision logged to MongoDB for regulatory review |
| **Async FastAPI** | Non-blocking endpoint with job queue for long-running workflows |
| **Configurable LLM** | GPT-4o or Claude 3 — swap via environment variable |
| **Error Recovery** | Each agent has retry logic and graceful fallback behavior |

---

## 🚀 Quick Start

```bash
git clone https://github.com/arshadshaikk/agentic-workflow-crewai
cd agentic-workflow-crewai

pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI key

# Run a verification
python -m app.run --document path/to/document.pdf --applicant-id FL12345
```

### As an API

```bash
uvicorn app.main:app --reload
```

```http
POST /api/v1/verify
Authorization: Bearer <token>
Content-Type: application/json

{
  "document_url": "s3://bucket/documents/license_scan.pdf",
  "applicant_id": "FL-2024-98765",
  "verification_type": "driver_license"
}
```

---

## 🧠 Agent Design Principles

**1. Single Responsibility** — Each agent has one clearly defined role and cannot exceed its scope.

**2. Tool Grounding** — Agents that need real-world data have MCP tools; those that don't are tool-free to reduce hallucination surface area.

**3. Temperature = 0 for deterministic tasks** — Classifier and Validator agents run at temperature 0.0 to ensure consistent, repeatable decisions.

**4. Max iterations cap** — All agents have `max_iter` limits to prevent infinite loops in production.

**5. Audit by design** — Every agent output is structured for downstream logging — no free-form responses that can't be parsed.

---

## 📁 Project Structure

```
agentic-workflow-crewai/
├── app/
│   ├── main.py                     # FastAPI app
│   ├── crew/
│   │   └── verification_crew.py    # Crew orchestration
│   ├── agents/
│   │   └── classifier.py           # All 4 agent definitions
│   ├── tasks/
│   │   └── verification_tasks.py   # Task definitions
│   ├── tools/
│   │   ├── mcp_tool.py             # Government data MCP tool
│   │   └── document_tools.py       # PDF reader, OCR tool
│   └── core/
│       ├── config.py
│       └── logging.py
├── tests/
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 🔒 Security & Compliance

- All agent API calls authenticated (JWT + mTLS for government APIs)
- PII masked in all log outputs
- MongoDB audit trail for every verification decision
- RBAC on API endpoints
- SADLC-compliant development process

---

## 👤 Author

**Arshad Shaik** — Senior Python / GenAI Developer  
📧 arshadshaikk01@gmail.com | 🔗 [LinkedIn](https://linkedin.com/in/arshadshaikk)
