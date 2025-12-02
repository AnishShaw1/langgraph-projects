🌟 README.md — LangGraph Chatbot (Streamlit + SQLite + Gemini Tools)

A modern, multi-thread AI chatbot built using LangGraph, Google Gemini, Streamlit, and SQLite.
This project behaves like a mini ChatGPT: persistent chats, tools, streaming responses, thread management, rename/delete dialogs, auto-chat-title, and more.

🚀 Features
✔️ Multi-Chat Thread System

Create unlimited chat threads

Persistent storage in SQLite

Load previous chats instantly

Auto-generated titles per conversation

✔️ LangGraph-Powered Stateful Conversations

Graph structure controls the flow:
START → chat_node → tools? → chat_node → END

Automatic state restoration from SQLite

Perfect for long discussions

✔️ Integrated Tools

Uses LangChain tools inside LangGraph:

Tool	Purpose
🔍 DuckDuckGo Search	Real-time search
➗ Calculator	Math operations
📈 Stock Price API	Fetch live stock prices
✔️ Modern Streamlit UI

Real-time streaming AI messages

Tool activity indicator (loading → complete)

Dialog popups for renaming & deleting chats

Clean chat display (tool messages hidden)

Arrow indicator for active chat thread

✔️ Two LLMs

Gemini 2.5 Flash → Main chat model

Gemini 2.0 Flash → Lightweight chat-title generator (avoids rate limits)

🧠 Architecture Overview
1️⃣ Frontend — frontend_latest.py (Streamlit)

Handles:

UI (chat area + sidebar)

Thread creation/selection/deletion

Rename dialog

Streaming responses

Filtering out ToolMessages

Local caching of chat titles (chat_titles.json)

Frontend does NOT store any state permanently — only UI management.

2️⃣ Backend — backend_latest.py (LangGraph + SQLite)

Handles:

LangGraph state transitions

Gemini LLM calls

Tool routing (DuckDuckGo, calculator, stock)

SQLite checkpointing

Auto title generation

Backend Flow:
START
  ↓
chat_node → (if tools required) → tool_node → chat_node
  ↓
END


Messages are saved in SQLite automatically via:

SqliteSaver(checkpointer)


Each thread is uniquely identified by:

thread_id (UUID)

📁 Project Structure (Only These Files Needed)

Your GitHub repository should contain only these files:

project/
│── frontend_latest.py        # Streamlit UI
│── backend_latest.py         # LangGraph backend
│── requirements.txt          # Dependencies
│── chatbot.db                # SQLite database (auto-created)
│── chat_titles.json          # Stores chat titles locally
│── .env                      # API keys (Gemini, AlphaVantage)
│── README.md                 # This file


No extra files are required.
This is a clean, minimal, production-ready folder layout for your GitHub.

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/AnishShaw1/langgraph-projects
cd langgraph-projects

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate      # Windows
# OR
source env/bin/activate   # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Create a .env file

Inside the project folder:

GEMINI_API_KEY=your_api_key
ALPHAVANTAGE_API_KEY=your_api_key

5️⃣ Run the app
streamlit run frontend_latest.py

🗃️ Database (SQLite)

LangGraph creates two tables automatically:

checkpoints

writes

These store:

messages

tool outputs

graph transitions

state metadata

A new thread is created for each conversation:

thread_id = UUID


Every chat is restored by:

chatbot.get_state(config={"configurable": {"thread_id": tid}})

⚠️ Limitations

Even though the system works great, here are the real limitations:

1️⃣ SQLite Limits Scaling

SQLite cannot handle:

many concurrent users

high traffic

distributed systems

For real deployment:
➡️ Replace SQLite with PostgreSQL / PGVector / ChromaDB.

2️⃣ No User Authentication

This system is single-user only by design.

If deployed publicly:

Every user sees same threads

No login system

No isolation

To add multi-user:
➡️ Use FastAPI backend with JWT authentication.

3️⃣ No RAG or File Upload

Your current system does not support:

PDF uploads

Document embeddings

Vector search

To add RAG:

Add file uploader

Embed documents

Store embeddings in FAISS/Chroma/PGVector

Add retrieval in LangGraph

4️⃣ Gemini Free-Tier Rate Limits

Gemini Flash free-tier allows:

10 requests per minute

Tools (DuckDuckGo) also add traffic

The secondary model (llm1) helps reduce rate-limit errors for chat-title generation.

5️⃣ Streamlit Is Not a Full Backend

Streamlit cannot handle:

Authentication

Multi-user concurrency

High traffic

For production:
➡️ Use Streamlit only as frontend, and build backend with FastAPI.

🚀 Future Improvements
🌟 1. Multi-User Support

Add FastAPI backend for:

JWT authentication

Separate user accounts

Per-user threads

Secure access to SQLite/Postgres

🌟 2. Add RAG (PDF Upload → Ask Questions)

Add:

PDF upload

Text chunking

Embeddings

Vector DB

Retrieval node in LangGraph

🌟 3. Move to PostgreSQL

Replace SQLite with Postgres for scaling:

More users

More threads

More concurrency

🌟 4. Better Tool Visualization

Add:

"Searching…"

"Calculating…"

Richer tool output UI

🌟 5. Deploy to Cloud

Suggested stack:

Component	Platform
Backend	FastAPI on Railway/Render
DB	PostgreSQL or Neon
Frontend	Streamlit Cloud / Vercel
File Storage (RAG)	Supabase Storage
