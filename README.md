## SaaS-AI-Governance

An AI Governance and Security Monitoring System that discovers, inventories, and audits embedded AI capabilities across enterprise SaaS applications (Microsoft 365, Slack, GitHub, Salesforce). The system logs employee prompt interactions, handles vendor visibility limitations (`FULL_CONTENT` vs `METADATA_ONLY`), performs vector similarity indexing via FAISS, and automates Data Loss Prevention (DLP) risk evaluation using the Groq LLM API.

The project provides a centralized FastAPI backend and Streamlit dashboard to give security teams full observability over shadow AI usage and data leak risks.

---

## Features

- Automated SaaS AI capability discovery across Microsoft 365, Slack, GitHub, and Salesforce
- Asset inventory management with review workflow states (`Pending Review`, `Approved`, `Flagged`)
- Interaction audit logging capturing email, platform, model, tokens, and prompt payloads
- DLP and compliance risk scoring powered by Groq LLM (Llama 3.3 70B) with rule-based fallback
- FAISS vector store integration for prompt similarity indexing and vector searches
- Observability level handling for provider redactions (`FULL_CONTENT` vs `METADATA_ONLY`)
- Interactive Streamlit governance dashboard for real-time monitoring and asset management
- RESTful backend built with FastAPI, SQLAlchemy, and SQLite

---

## Technologies Used

- Python
- FastAPI
- Streamlit
- SQLAlchemy
- SQLite
- FAISS (faiss-cpu)
- Groq API (Llama 3.3 70B)
- Pydantic
- Uvicorn
- NumPy

---

## How to Run the Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/priyanshukushwaha0/SaaS-AI-Governance.git
   cd SaaS-AI-Governance
   
2. Create a virtual environment --> python -m venv myenv

3. Create a .env file -->
   
 - GROQ_API_KEY = YOUR_GROQ_API_KEY
 - GROQ_MODEL = llama-3.3-70b-versatile
 - DATABASE_URL=sqlite:///./saas_governance.db

5. Install dependencies --> pip install -r requirements.txt

   Run the FastAPI backend server --> uvicorn app.main:app --reload --port 8000

   Run the Streamlit app --> python -m streamlit run frontend.py

## File Structure

    SaaS-AI-Governance
         ├── app/
         │   ├── config.py            # Environment configuration & variables
         │   ├── database.py          # SQLAlchemy engine & session management
         │   ├── models.py            # Database ORM models (AIAsset, AIInteraction)
         │   ├── schemas.py           # Pydantic input/output validation schemas
         │   ├── discovery.py         # SaaS AI discovery scanner service
         │   ├── monitoring.py        # FAISS vector search engine & Groq DLP analyzer
         │   └── main.py              # FastAPI application & REST API routes
         ├── frontend.py              # Streamlit Governance Dashboard UI
         ├── requirements.txt         # Python project dependencies
         └── README.md                # System documentation    

## Project Architecture

    SaaS Applications (M365, Slack, GitHub, Salesforce)
                               │
                               ▼
                    Discovery Scanner Service
                               │
                               ▼
                  SQLite Database (SQLAlchemy)
                    (AI Assets & Audit Logs)
                               │
                               ▼
                     User AI Interaction
                               │
                               ▼
                     FastAPI REST Backend
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
        FAISS Vector Store          Groq LLM Risk Scoring
     (Similarity Indexing)          (DLP & Security Analysis)
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                    Streamlit Governance UI
