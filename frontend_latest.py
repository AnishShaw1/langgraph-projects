import streamlit as st
from backend_latest import chatbot, llm1, retrieve_all_thread_ids, delete_thread
from langchain_core.messages import HumanMessage, AIMessage ,ToolMessage
import uuid, json, os

# **************************************** utility functions *************************
TITLE_FILE = "chat_titles.json"

def load_chat_titles():
    if os.path.exists(TITLE_FILE):
        with open(TITLE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_chat_titles(titles_dict):
    serializable_dict = {str(k): v for k, v in titles_dict.items()}
    with open(TITLE_FILE, "w") as f:
        json.dump(serializable_dict, f)

def generate_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

# **************************************** Session Setup ******************************
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_thread_ids()

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'chat_titles' not in st.session_state:
    st.session_state['chat_titles'] = load_chat_titles()

# **************************************** Sidebar UI *********************************
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')


# Show chat list with rename buttons
for tid in st.session_state['chat_threads'][::-1]:
    title = st.session_state['chat_titles'].get(tid, "New Chat...")
    col1, col2, col3 = st.sidebar.columns([5, 1, 1])


    # --- Select chat ---
    with col1:
    # Minimal highlight: add a subtle arrow prefix for the active thread (no CSS)
        is_active = (st.session_state['thread_id'] == tid)
        display_title = ("👉 " if is_active else "") + title

        if st.button(display_title, key=f"chat_{tid}"):
            st.session_state['thread_id'] = tid
            messages = load_conversation(tid)
            temp_messages = []
            from langchain_core.messages import HumanMessage, AIMessage
            for msg in messages:
                if isinstance(msg, (HumanMessage, AIMessage)):  # skip tool messages
                    role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                    temp_messages.append({'role': role, 'content': msg.content})
            st.session_state['message_history'] = temp_messages
            st.rerun()


    
   # --- Rename chat (clean popup version) ---
    with col2:
        if st.button("✏️", key=f"rename_{tid}", help="Rename chat"):
            st.session_state['rename_target'] = tid
            st.session_state['show_rename_dialog'] = True
            st.rerun()

        # --- Delete chat ---
    with col3:
        if st.button("🗑️", key=f"delete_{tid}", help="Delete chat"):
            st.session_state['confirm_delete'] = tid  # mark this chat for confirmation
            st.rerun()

# --- Delete Confirmation Dialog ---
if st.session_state.get("confirm_delete"):
    tid = st.session_state["confirm_delete"]
    title = st.session_state["chat_titles"].get(tid, "New Chat...")

    @st.dialog("🗑️ Confirm Delete")
    def delete_chat_dialog():
        st.markdown("### ⚠️ Delete Chat")
        st.write(f"Are you sure you want to delete **'{title}'**? This action cannot be undone.")
        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes, Delete", use_container_width=True):
                delete_thread(tid)  # remove from database

                # Update session state and local storage
                if tid in st.session_state["chat_threads"]:
                    st.session_state["chat_threads"].remove(tid)
                if tid in st.session_state["chat_titles"]:
                    st.session_state["chat_titles"].pop(tid)
                    save_chat_titles(st.session_state["chat_titles"])

                st.toast("🗑️ Chat deleted successfully!", icon="⚡")
                st.session_state.pop("confirm_delete", None)

                # ✅ Only reset if no chats left
                if not st.session_state["chat_threads"]:
                    reset_chat()
                else:
                    # ✅ If deleted chat was the current one, switch to another existing one
                    if st.session_state["thread_id"] == tid:
                        st.session_state["thread_id"] = st.session_state["chat_threads"][-1]
                        messages = load_conversation(st.session_state["thread_id"])
                        st.session_state["message_history"] = [
                            {'role': 'user' if isinstance(m, HumanMessage) else 'assistant', 'content': m.content}
                            for m in messages
                        ]

                st.rerun()


        with c2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.pop("confirm_delete", None)
                st.rerun()

    delete_chat_dialog()

    
# --- Rename Dialog ---
if st.session_state.get("show_rename_dialog", False):
    tid = st.session_state.get("rename_target")
    if tid:
        old_title = st.session_state['chat_titles'].get(tid, "New Chat...")

        # ✅ Proper dialog definition
        @st.dialog("📝 Rename Chat")
        def rename_chat_dialog():
            st.markdown("### ✏️ Rename Chat")
            st.write(f"Current title: **{old_title}**")

            new_title = st.text_input(
                "Enter new title:",
                value=old_title,
                key="rename_input_dialog",
                placeholder="Type new chat name..."
            )

            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Save", use_container_width=True):
                    if new_title.strip():
                        st.session_state['chat_titles'][tid] = new_title.strip()
                        save_chat_titles(st.session_state['chat_titles'])
                        st.toast("✅ Chat renamed successfully!", icon="✨")
                    st.session_state['show_rename_dialog'] = False
                    st.rerun()
            with c2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state['show_rename_dialog'] = False
                    st.rerun()

        # ✅ Call dialog
        rename_chat_dialog()


# **************************************** Main Chat UI ************************************
for message in st.session_state['message_history']:
    # Skip any tool or empty assistant message
    if not message.get('content'):
        continue
    if message['role'] not in ['user', 'assistant']:
        continue

    # Render only valid user or assistant messages
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    if st.session_state['thread_id'] not in st.session_state['chat_titles']:
        title_prompt = f"Summarize this chat topic in 5 words or fewer:\nUser: {user_input}\nAssistant: {ai_message}"
        title_response = llm1.invoke([HumanMessage(content=title_prompt)])
        title_text = title_response.content.strip().replace('"', '')
        st.session_state['chat_titles'][st.session_state['thread_id']] = title_text
        save_chat_titles(st.session_state['chat_titles'])
        st.rerun()



