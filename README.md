# AMD Smart Product Assistant — Backend API 🚀

Welcome to the backend repository of the **AMD Smart Product Assistant**! This is a state-of-the-art FastAPI-based chatbot backend powered by **AMD GPUs** (via **vLLM + ROCm** on AMD Developer Cloud) and a robust **RAG (Retrieval Augmented Generation)** pipeline over a PostgreSQL database with `pgvector` support.

---

## 🛠️ Tech Stack & Features

* **Framework:** FastAPI (Python 3.12 / 3.14 compatible)
* **Database:** Supabase PostgreSQL with `pgvector` for vector embedding similarity search.
* **ORM:** SQLAlchemy v2 + Alembic for migrations.
* **RAG Pipeline:** Blazing-fast vector similarity search with graceful keyword frequency-scoring fallback if embeddings aren't generated.
* **LLM Engine:** vLLM (ROCm-optimized) on AMD Developer Cloud, with an intelligent local Mock AI provider for offline/local development.
* **Security:** API Key Authentication for Admin operations (`x-admin-key`).
* **Rate Limiting:** Built-in IP-based rate limiting (`slowapi`) allowing up to 20 chat requests/minute.
* **Performance stats & metrics:** Aggregates total requests, latencies, model distributions, and requests today.
* **Graceful Fallback:** Automatic switch to Mock AI with descriptive warnings if the vLLM server goes offline/timeouts during live demos.

---

## 🏃 Getting Started (Local Development)

### 1. Prerequisites
* Python 3.12+
* PostgreSQL with `pgvector` installed (or use a Supabase instance).

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```
Key configuration values:
```ini
APP_ENV=local
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/amd_smart_product_assistant
AI_PROVIDER=mock          # Use "mock" for local dev, "vllm" for AMD Cloud
VLLM_BASE_URL=            # URL to vLLM server on AMD Cloud
VLLM_MODEL=               # Model name (e.g. meta-llama/Llama-3-8B-Instruct)
ADMIN_API_KEY=change-me   # Keep it secure
```

### 3. Setting Up Virtual Environment
Create a fresh virtual environment and install dependencies:
```bash
python3 -m venv new_venv
source new_venv/bin/activate
pip install -r requirements.txt
```

### 4. Running Database Migrations
Run Alembic migrations to construct the schema:
```bash
PYTHONPATH=. alembic upgrade head
```

### 5. Seeding the AMD Knowledge Base
Populate the database with initial AMD ROCm, Ryzen, Instinct, and Radeon articles:
```bash
PYTHONPATH=. python scripts/seed_db_direct.py
```

### 6. Start the Server
Start the development server:
```bash
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```
Your API will be live at `http://localhost:8000`. You can visit Swagger UI docs at `http://localhost:8000/docs`.

---

## 🐳 Running with Docker / Docker Compose

You can boot up both the API and a `pgvector` PostgreSQL container instantly using Docker:

```bash
docker-compose up --build
```
This sets up:
* **`api`** on `http://localhost:8000`
* **`db`** (`pgvector/pgvector:pg16` image) on `localhost:5432`

---

## 📊 Core API Endpoints

### 💬 Chat Endpoints
* **`POST /api/chat`** — Main chat completion endpoint. Submits user questions, performs RAG context retrieval, queries LLM, logs latency/model metadata, and respects rate limits.
* **`GET /api/chat/sessions`** — Retrieves list of user sessions (history).
* **`GET /api/chat/sessions/{session_id}/messages`** — Retrieves complete chat message history of a specific session.

### 📝 Feedback Endpoints
* **`POST /api/feedback`** — Accepts user ratings (`helpful`, `not_helpful`, `unclear`, `incorrect`) with comments.

### 👑 Admin Endpoints (Require Header: `x-admin-key`)
* **`POST /api/admin/knowledge/upload`** — Upload new knowledge documents. Automatically attempts to calculate embeddings via `sentence-transformers` if available.
* **`GET /api/admin/knowledge`** — Lists all uploaded articles in the database.
* **`DELETE /api/admin/knowledge/{doc_id}`** — Removes an article.
* **`GET /api/admin/stats`** — Real-time performance analytics dashboard (total requests, model usage distribution, avg latency, requests today).

---

## 🌟 Intelligent Graceful Fallback Demo

During live demos, network instability or vLLM cold starts can occur. This backend handles that gracefully:
* If `VLLM_BASE_URL` times out or raises connection/HTTP status errors, the router intercepts the failure.
* It dynamically spawns an internal `mock` provider instance.
* Returns a marked fallback response `[Fallback] <answer>` with the model set to `fallback:amd-smart-assistant-mock`.
* **Result:** Zero crashes on stage, juri remains wowed, and the system continues to operate stably.
