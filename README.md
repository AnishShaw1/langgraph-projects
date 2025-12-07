🌟 LangGraph Chatbot

A modern AI-powered chatbot built using LangGraph, Google Gemini, Streamlit, and SQLite, offering persistent multi-thread conversations, tool-augmented responses, auto chat titles, and a clean chat UI—similar to ChatGPT.

🚀 Live Demo

👉 (Add your Hugging Face / Streamlit Cloud link here)

📌 Features
💬 Multi-Thread Chat System

Create unlimited conversations

Each chat stored with a unique thread_id

Auto-load past conversations

Auto-generated chat titles

🧠 LangGraph-Powered Stateful Conversations

Chat flow managed through a graph:
START → chat_node → (tool?) → chat_node → END

State persistence using SQLite checkpoints

Smooth multi-step conversation handling

🔧 Integrated Tools
Tool	Purpose
🔍 DuckDuckGo Search	Real-time web search
➗ Calculator	Basic arithmetic operations
📈 Stock Price API	Live stock market data

Tools are triggered intelligently by the LLM when needed.

🎨 Modern Streamlit UI

Real-time streaming responses

Tool activity indicator

Rename chat (dialog popup)

Delete chat (confirmation dialog)

Clean message rendering (Tool messages hidden)

Arrow indicator (👉) for currently active chat

🤖 Dual LLM Architecture

Gemini 2.5 Flash → Main chat model

Gemini 2.0 Flash → Lightweight title generator

Helps avoid rate-limits & improves responsiveness

🛠️ Tech Stack

LLM: Gemini 2.5 Flash / Gemini 2.0 Flash

Framework: LangGraph + LangChain Tools

Frontend: Streamlit

Database: SQLite (checkpoints + writes tables)

APIs: DuckDuckGo, AlphaVantage Stock API

State Storage: Local JSON + SQLite

🏗️ Architecture
                 User
                  │
                  ▼
        ┌───────────────────┐
        │    Streamlit UI   │
        │ (frontend_latest) │
        └───────────────────┘
                  │
        Chat Request (thread_id)
                  │
                  ▼
        ┌───────────────────┐
        │  LangGraph Engine │
        │ (backend_latest)  │
        ├───────────────────┤
        │ chat_node         │
        │ tool_node         │
        └───────────────────┘
                  │
          Uses Tools? ── Yes → 🔧 ToolNode  
                  │
                  ▼
        ┌───────────────────┐
        │   SQLite DB       │
        │ checkpoints/writes│
        └───────────────────┘


✔ Automatic saving of chat state
✔ Restored instantly on load

📁 Project Structure

Only these essential files are required:

project/
│── frontend_latest.py        # Streamlit UI
│── backend_latest.py         # LangGraph backend
│── requirements.txt          # Dependencies
│── chatbot.db                # SQLite database (auto-created)
│── chat_titles.json          # Local title storage
│── .env                      # API keys (Gemini, AlphaVantage)
│── README.md                 # Documentation


No extra files needed — clean & minimal.

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/AnishShaw1/langgraph-projects
cd langgraph-projects

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate   # Windows
# or
source env/bin/activate  # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure .env
GEMINI_API_KEY=your_gemini_api_key
ALPHAVANTAGE_API_KEY=your_stock_api_key

5️⃣ Run the app
streamlit run frontend_latest.py

🗂 Database (SQLite)

LangGraph creates two tables:

1. checkpoints

Stores:

messages

graph transitions

version metadata

2. writes

Stores:

intermediate tool outputs

incremental state updates

Each conversation is tied to a unique thread_id.

⚠️ Limitations
1️⃣ SQLite Scalability

SQLite is excellent for local apps, but not built for multi-user concurrency.

For production use:
➡️ Replace with PostgreSQL / PGVector / ChromaDB

2️⃣ No User Authentication

This app is single-user only.

Deploying publicly without login = ❌ unsafe.
To add authentication:
➡️ Build a backend using FastAPI + JWT.

3️⃣ No RAG / File Upload

Currently, the chatbot does not support:

PDF uploads

Document embeddings

Retrieval-Augmented Generation

For RAG:
➡️ Add embeddings + FAISS/Chroma + retrieval node in LangGraph.

4️⃣ Gemini Free-Tier Rate Limits

10 req/min limit

Search tool increases LLM calls

Using a second LLM for titles helps reduce errors

5️⃣ Streamlit Is Not a Backend

Streamlit cannot handle:

Multi-user scaling

Authentication

Heavy concurrency

Use Streamlit ONLY as the UI layer.

🚀 Future Improvements
🌟 1. Add Multi-User Support

Using FastAPI backend for:

Login/signup

User isolation

Per-user thread storage

🌟 2. Add Full RAG System

PDF upload

Chunking + embeddings

Vector search

RAG chain inside LangGraph

🌟 3. Migrate to PostgreSQL

Needed for:

More users

High concurrency

Larger dataset

🌟 4. Enhanced Tool UI

“Searching…” animation

Rich visualization of tool results

🌟 5. Cloud Deployment

Recommended stack:

Component	Platform
Backend	FastAPI on Railway / Render
DB	PostgreSQL or Neon
Frontend	Streamlit Cloud / Vercel
File Storage	Supabase Storage
⭐ Final Notes

This project demonstrates:

✔ LangGraph State Machines
✔ Persistent chat threads
✔ Tool-using LLM workflow
✔ Streamlit chat UI
✔ Clean architecture with minimal files
