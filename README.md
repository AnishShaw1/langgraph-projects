🌟 LangGraph Chatbot (Streamlit + SQLite + Gemini Tools)

A modern AI-powered chatbot built using LangGraph, Google Gemini, Streamlit, and SQLite, supporting persistent multi-thread conversations with tool usage, dialog popups, and streaming responses — similar to ChatGPT.

🚀 Live Demo

Add your deployment link here

📌 Features
💬 Multi-Thread Chat System

Create unlimited chat threads

Persistent storage using SQLite

Restore conversations instantly

Auto-generated short titles

🧠 LangGraph Stateful Conversation Engine

Powered by a custom LangGraph workflow:

START → chat_node → (tools?) → chat_node → END


Automatic message persistence

State restored via SQLite checkpoints

Tool routing based on LLM decisions

🔧 Built-in Tools
Tool	Purpose
🔍 DuckDuckGo Search	Real-time search
➗ Calculator	Math operations
📈 Stock API	Live stock prices
🎨 Modern Streamlit UI

Smooth streaming responses

Tool-activity status indicator

Clean UI (ToolMessages hidden in history)

Popup dialogs for Rename & Delete

Arrow indicator for active thread

🤖 Dual-LLM Architecture

Gemini 2.5 Flash → main conversation model

Gemini 2.0 Flash → lightweight auto-title generator
(prevents rate-limit errors)

🛠️ Tech Stack

Frontend: Streamlit

Backend: LangGraph + LangChain

LLM: Google Gemini Flash

Tools: Search, Calculator, Stock API

Database: SQLite

State Management: LangGraph Checkpointer

🏗️ Architecture Overview
User
  │
  ▼
───────────────────────────────
 Streamlit UI (frontend)
───────────────────────────────
  │
  ▼ request with thread_id
───────────────────────────────
 LangGraph Backend (chatbot)
───────────────────────────────
 chat_node → tool_node → chat_node
───────────────────────────────
  │
  ▼
───────────────────────────────
 SQLite Database (persistent)
───────────────────────────────

📁 Project Structure

Only these files are required:

project/
│── frontend_latest.py     # Streamlit UI
│── backend_latest.py      # LangGraph backend engine
│── requirements.txt       # Dependencies
│── chatbot.db             # SQLite conversation storage
│── chat_titles.json       # Local title cache
│── .env                   # API keys (Gemini, Stock API)
│── README.md              # This file

⚙️ Installation
1️⃣ Clone repo
git clone https://github.com/AnishShaw1/langgraph-projects
cd langgraph-projects

2️⃣ Create virtual environment
python -m venv env
env\Scripts\activate      # Windows
source env/bin/activate   # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add .env file
GEMINI_API_KEY=your_key
ALPHAVANTAGE_API_KEY=your_key

5️⃣ Run app
streamlit run frontend_latest.py

🗃️ Database Details (SQLite)

LangGraph automatically generates:

1. checkpoints table

Stores:

message history

state metadata

transitions

2. writes table

Stores:

tool results

tool execution logs

Each chat is identified using:

thread_id = UUID

⚠️ Limitations
1️⃣ SQLite Scaling Limits

Good for local/single-user use, but not for:

high traffic

many users

concurrent writes

➡️ For production: PostgreSQL + PGVector or ChromaDB.

2️⃣ No User Authentication

This project is single-user only.

If deployed publicly:

every visitor sees the same chat threads

➡️ Multi-user requires FastAPI + JWT + DB.

3️⃣ No RAG (Retrieval-Augmented Generation)

Currently lacks:

PDF upload

text chunking

embeddings

vector search

➡️ Can be added using FAISS / Chroma + a retrieval node in LangGraph.

4️⃣ Gemini Free-Tier Rate Limits

10 requests/min

search tool increases usage

Using a second model (llm1) reduces title-generation pressure.

5️⃣ Streamlit is not a backend

Streamlit cannot handle:

real authentication

multi-user concurrency

secure APIs

➡️ Should be UI only for production-level apps.

🚀 Future Improvements
🌟 Multi-User Accounts

Using FastAPI backend:

JWT login

per-user threads

secure role-based access

🌟 Add RAG Workflow

Upload PDFs

Generate embeddings

Store vectors

Retrieve context in LangGraph

🌟 Migrate to PostgreSQL

handles large datasets

supports concurrency

ideal for multi-user platforms

🌟 Enhanced Tool UI

dedicated tool output cards

better search visualization

🌟 Cloud Deployment

Recommended stack:

Component	Platform
Backend	FastAPI on Railway/Render
DB	PostgreSQL / Neon
Frontend	Streamlit Cloud
File Storage	Supabase
⭐ Final Notes

This project is a complete example of how to combine:

✔ LangGraph
✔ Gemini Flash
✔ LangChain Tools
✔ SQLite persistence
✔ Streamlit UI

into a clean, functional, ChatGPT-like chatbot with tool support.
