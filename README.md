LangGraph Chatbot (Streamlit + SQLite + Gemini Tools)
🚀 Overview

This project is a full chat application built using:

LangGraph for stateful conversation management

Google Gemini Flash models for generation

DuckDuckGo, Calculator, and Stock Price tools via LangChain

A local SQLite database for persistent threads

Streamlit as the frontend UI

Automatic chat titles using a secondary lightweight LLM (llm1)

It behaves like a mini ChatGPT with:

Multiple chat threads

Persistent conversation history

Tool usage visualization

Rename + delete chat

Real-time streaming responses

✨ Features
✅ Multi-Chat Thread System

Create unlimited chat threads

Automatically saved into SQLite

Load past conversations instantly

✅ Gemini 2.5 Flash + Tools

Integrated tools:

DuckDuckGo Search

Calculator

Stock Price API

The system automatically decides when to call tools.

✅ Persistent Chat Titles

First message → auto-generated 5-word title

Titles stored locally (chat_titles.json)

Manually rename title via popup dialog

✅ Clean & Modern UI (Streamlit)

Chat UI similar to ChatGPT

Rename popup dialog (Streamlit dialog)

Delete confirmation dialog

Tool status indicator (loading → complete)

Message history displayed cleanly (tool messages filtered out)

✅ Persistent Storage (SQLite)

Stores every message in LangGraph format

Uses SqliteSaver checkpointing

Thread-specific message isolation

🧩 Architecture
1️⃣ Frontend – Streamlit

Responsible for:

User interface

Rendering chat messages

Thread list sidebar

Rename/Delete dialogs

Streaming assistant responses (token-by-token)

Sending queries to backend LangGraph

No business logic lives here — only UI and UX.

2️⃣ Backend – LangGraph + SQLite

The backend:

Manages stateful chatbot memory

Stores threads in SQLite

Runs all tool logic

Decides tool routing

Generates responses

Streams output progressively

Graph Structure:
START → chat_node → tools (conditional) → chat_node → END

Tools Integrated:

DuckDuckGo Search

Calculator

Stock Price API

Models Used:

llm (Gemini 2.5 Flash) → Main chat model

llm1 (Gemini 2.0 Flash) → For lightweight chat title generation

📦 Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd <project-folder>

2️⃣ Create virtual environment
python -m venv env
source env/bin/activate       # Mac/Linux
env\Scripts\activate          # Windows

3️⃣ Install requirements
pip install -r requirements.txt

4️⃣ Add .env
GEMINI_API_KEY=your_key
ALPHAVANTAGE_API_KEY=your_key

5️⃣ Run the app
streamlit run frontend.py

📁 Folder Structure
project/
│── backend_latest.py
│── frontend.py
│── chat_titles.json
│── chatbot.db
│── requirements.txt
│── .env
│── README.md

🗂️ Database (SQLite)

Tables created by LangGraph:

checkpoints

writes

Each thread is uniquely identified by:

thread_id (UUID)


All messages for that thread are stored and restored automatically.

⚠️ Limitations

Even though the project works smoothly, here are the important limitations:

1️⃣ Single-Machine Architecture (Not Cloud-Ready Yet)

SQLite is file-based. It cannot handle:

high concurrency

horizontal scaling

cloud-based multi-region access

For real production:
➡️ Replace SQLite with PostgreSQL or a scalable DB.

2️⃣ Tool Messages Not Truly Hidden in Database

Although filtered in UI, tool call messages still exist internally in SQLite.

This is not a big issue but:

They are not rendered in UI

They do consume storage

3️⃣ No User Authentication (Single User Only)

This system works for one user only.

If deployed publicly:

Anyone can see everyone’s chats

Sessions are not isolated

To support multi-user:
➡️ A proper backend (FastAPI) with JWT auth is required.

4️⃣ No File Upload / RAG (Yet)

This project does not include RAG.

If a user uploads a file today:

There is no vector store

No document embeddings

Adding RAG requires:

A vector DB (FAISS, Chroma, PGVector)

Embedding model

Memory retention per thread

5️⃣ Limited Gemini Free-Tier Rate Limits

Gemini Flash free-tier allows:

10 requests per minute

Tool-heavy prompts can quickly consume rate limits.

ChatTitle LLM (llm1) fixes most of this but:

Too many page reloads can still hit rate-limits

6️⃣ Streamlit Is Not a Real Backend

Streamlit cannot handle:

Multi-user authentication

High traffic

Role-based permissions

It is ideal for demos, not production chat services.

🚀 Future Improvements
1️⃣ Add User Accounts (FastAPI + JWT)

To support users safely:

Build backend with FastAPI

Store users + threads in PostgreSQL

Streamlit frontend becomes UI only

2️⃣ Add RAG (File Upload Support)

Let users upload PDFs, docs.

Needed:

Embedding model

Vector DB (FAISS, Chroma, PGVector)

Retrieve relevant chunks

Add to LangGraph state

3️⃣ Replace SQLite With PostgreSQL

For real scaling:

Postgres

MySQL

Supabase

Neon.tech

Railway Postgres

4️⃣ Add Cloud Deployment

Possible stacks:

Streamlit Cloud (UI)

FastAPI on Render / Railway (Backend)

Postgres on Neon (Database)

5️⃣ Better Tool Handling

Show a small spinner in messages:

“Fetching stock price…”

“Searching web…”

🎉 Conclusion

Your project is now a fully working LangGraph-powered chatbot with:

✔ Persistent threads
✔ Streamlit UI
✔ LangGraph state
✔ SQLite backend
✔ Gemini models
✔ Tools
✔ Auto titles
✔ Renaming + deleting chats

It is an ideal portfolio project and can be expanded into a full SaaS app with a proper backend.
