# AI-First CRM — HCP Module

The AI-First CRM HCP Module is an intelligent interaction logging system designed for pharmaceutical field representatives. It provides a dual-mode interface for recording Healthcare Professional (HCP) interactions: a structured form for precise data entry (Mode A) and an AI-powered chat assistant (Mode B) that uses natural language processing to extract and log interaction data. Both modes produce identical structured records in a PostgreSQL database, enabling reps to choose their preferred workflow while maintaining data consistency.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│  ┌─────────────────────┐  ┌──────────────────────────┐  │
│  │   InteractionForm   │  │     ChatPanel (AI)       │  │
│  │   (Mode A: Form)    │  │     (Mode B: Chat)       │  │
│  └────────┬────────────┘  └────────────┬─────────────┘  │
│           │                            │                 │
│  ┌────────▼────────────────────────────▼─────────────┐  │
│  │              Redux Store (RTK)                     │  │
│  │  interactionSlice │ chatSlice │ hcpSlice │ followUp│  │
│  └────────┬────────────────────────────┬─────────────┘  │
│           │                            │                 │
│  ┌────────▼────────────────────────────▼─────────────┐  │
│  │              Axios HTTP Client                     │  │
│  └────────┬────────────────────────────┬─────────────┘  │
└───────────┼────────────────────────────┼─────────────────┘
            │                            │
  POST /api/interactions      POST /api/agent/chat
            │                            │
┌───────────▼────────────────────────────▼─────────────────┐
│                    FastAPI Backend                         │
│  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │   REST Routers   │  │   LangGraph Agent            │  │
│  │   (CRUD ops)     │  │   ┌─agent_node─┐             │  │
│  │                  │  │   │  Groq LLM   │◄──┐        │  │
│  │                  │  │   │  (gemma2)   │   │        │  │
│  │                  │  │   └──┬──────────┘   │        │  │
│  │                  │  │      │ tool call     │ result │  │
│  │                  │  │   ┌──▼──────────┐   │        │  │
│  │                  │  │   │  tool_node   ├───┘        │  │
│  │                  │  │   │  (5 tools)   │            │  │
│  │                  │  │   └─────────────┘             │  │
│  └───────┬──────────┘  └──────────┬───────────────────┘  │
│          │                        │                       │
│  ┌───────▼────────────────────────▼───────────────────┐  │
│  │          Async SQLAlchemy + asyncpg                 │  │
│  └───────────────────────┬────────────────────────────┘  │
└──────────────────────────┼────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │      PostgreSQL         │
              │  hcp │ interaction      │
              │  sample │ follow_up     │
              └─────────────────────────┘
```

**Mode A (Form):** User fills structured form → POST `/api/interactions` → direct DB write (source: "form")

**Mode B (Chat):** User types natural language → POST `/api/agent/chat` → LangGraph agent → LLM extracts fields → `log_interaction` tool writes to DB (source: "chat") → extracted fields auto-populate form via Redux

## Tech Stack

| Technology | Role |
|---|---|
| React (Vite) | Frontend UI framework |
| Redux Toolkit | State management |
| Axios | HTTP client |
| Google Inter | Typography (via CDN) |
| Python + FastAPI | Backend API framework |
| Async SQLAlchemy + asyncpg | Database ORM and driver |
| Alembic | Database migrations |
| LangGraph | AI agent graph orchestration |
| LangChain + langchain-groq | LLM integration framework |
| Groq API (gemma2-9b-it) | Primary LLM for extraction and chat |
| Groq API (llama-3.3-70b-versatile) | Secondary LLM for summarization |
| PostgreSQL | Relational database |
| pydantic-settings | Configuration management |

## Prerequisites

- **PostgreSQL** 14 or above
- **Python** 3.10 or above
- **Node.js** 18 or above
- **Groq API Key** (free at [console.groq.com](https://console.groq.com))

## Setup Instructions

### Backend

```bash
# 1. Clone the repository
git clone <repo-url>
cd hcp-crm

# 2. Create and activate virtual environment
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux
# Edit .env and fill in your DATABASE_URL and GROQ_API_KEY

# 5. Run database migrations
alembic upgrade head

# 6. Seed the database
python seed.py

# 7. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Configure environment
copy .env.example .env       # Windows
# cp .env.example .env       # macOS/Linux

# 4. Start development server
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API calls to `http://localhost:8000`.

### Docker Alternative for PostgreSQL

```bash
docker run --name hcp-crm-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=hcp_crm -p 5432:5432 -d postgres:16
```

## LangGraph Tools

| Tool Name | Trigger Phrase Example | What It Does | DB Effect |
|---|---|---|---|
| `log_interaction` | "I met Dr. Priya Sharma at Apollo Hospital today. We discussed CardioMax efficacy. She was positive and agreed to trial it on 5 patients. I gave her 3 sample packs. Follow up in 2 weeks." | Extracts structured fields from natural language via LLM, validates, looks up HCP, and creates a full interaction record | Creates `Interaction` + `Sample` rows |
| `edit_interaction` | "Update interaction ID 1, change the outcome to: Doctor requested more clinical data." | Updates specific fields on an existing interaction record | Updates `Interaction` row |
| `get_hcp_profile` | "Show me the profile for Dr. Priya Sharma." | Retrieves full HCP profile with their last 5 interactions | Read-only |
| `schedule_follow_up` | "Schedule a follow-up with Dr. Priya Sharma on 2025-05-10 to discuss trial patient feedback." | Creates a follow-up task and updates the interaction's follow-up date | Creates `FollowUp` row, updates `Interaction.follow_up_date` |
| `summarize_interactions` | "Summarize my last 3 visits with Dr. Priya Sharma." | Fetches recent interactions and generates a concise summary using the larger LLM model | Read-only |

## API Reference

| Method | Route | Description |
|---|---|---|
| GET | `/api/hcps?search=query` | Search HCPs by name |
| GET | `/api/hcps/{hcp_id}` | Get HCP with last 5 interactions |
| POST | `/api/interactions` | Create a new interaction |
| GET | `/api/interactions?hcp_id=&limit=&offset=` | List interactions (paginated) |
| GET | `/api/interactions/{id}` | Get a single interaction |
| PUT | `/api/interactions/{id}` | Partial update an interaction |
| POST | `/api/follow-ups` | Create a follow-up |
| GET | `/api/follow-ups?hcp_id=&status=` | List follow-ups (filtered) |
| PUT | `/api/follow-ups/{id}` | Update a follow-up |
| POST | `/api/agent/chat` | Chat with the AI agent |
| GET | `/docs` | Swagger API documentation |

## Known Limitations

- **The assessment originally specified gemma2-9b-it as the primary LLM. This model was officially decommissioned by Groq on October 8, 2025, after this assessment was issued. The official Groq recommended replacement, llama-3.1-8b-instant, is used instead. Reference: https://console.groq.com/docs/deprecations**

- **Voice Note** feature is rendered as disabled with a "Coming Soon" tooltip. No audio functionality is implemented.
- **Conversation history** is capped at the last 10 messages sent to the agent per session.
- **Authentication** is out of scope — no login, no role-based access control.
- **Deployment** tooling is not included — the app runs locally only.
- **Real-time streaming** is not implemented — agent responses are returned as complete messages.
