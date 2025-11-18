import streamlit as st
from backend_rename_delete import chatbot, llm, retrieve_all_thread_ids, delete_thread
from langchain_core.messages import HumanMessage, AIMessage
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
        if st.button(title, key=f"chat_{tid}"):
            st.session_state['thread_id'] = tid
            messages = load_conversation(tid)
            temp_messages = []
            from langchain_core.messages import HumanMessage, AIMessage
            for msg in messages:
                role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
                temp_messages.append({'role': role, 'content': msg.content})
            st.session_state['message_history'] = temp_messages
            st.rerun()

    # --- Rename chat ---
    with col2:
        rename_key = f"rename_input_{tid}"
        if st.button("✏️", key=f"rename_{tid}", help="Rename chat"):
            st.session_state[f"renaming_{tid}"] = True

        if st.session_state.get(f"renaming_{tid}", False):
            new_title = st.text_input(
                "Enter new title:",
                value=st.session_state['chat_titles'].get(tid, "New Chat..."),
                key=rename_key
            )
            if st.button("Save", key=f"save_{tid}"):
                st.session_state['chat_titles'][tid] = new_title.strip()
                save_chat_titles(st.session_state['chat_titles'])  # persist to JSON
                st.session_state[f"renaming_{tid}"] = False
                st.rerun()
        # --- Delete chat ---
    with col3:
        if st.button("🗑️", key=f"delete_{tid}", help="Delete chat"):
            st.session_state['confirm_delete'] = tid  # mark this chat for confirmation
            st.rerun()

# --- Confirm deletion section (below loop) ---
if st.session_state.get('confirm_delete'):
    tid = st.session_state['confirm_delete']
    title = st.session_state['chat_titles'].get(tid, "New Chat...")
    st.sidebar.warning(f"Delete '{title}'?")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("Yes, delete", key="confirm_yes"):
            delete_thread(tid)  # remove from database
            # Remove from in-memory and title store
            if tid in st.session_state['chat_threads']:
                st.session_state['chat_threads'].remove(tid)
            if tid in st.session_state['chat_titles']:
                st.session_state['chat_titles'].pop(tid)
                save_chat_titles(st.session_state['chat_titles'])
            st.session_state.pop('confirm_delete', None)
            st.rerun()
    with c2:
        if st.button("Cancel", key="confirm_no"):
            st.session_state.pop('confirm_delete', None)
            st.rerun()


    


# **************************************** Main Chat UI ************************************
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message("assistant"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content or ""

        ai_message = st.write_stream(ai_only_stream())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    if st.session_state['thread_id'] not in st.session_state['chat_titles']:
        title_prompt = f"Summarize this chat topic in 5 words or fewer:\nUser: {user_input}\nAssistant: {ai_message}"
        title_response = llm.invoke([HumanMessage(content=title_prompt)])
        title_text = title_response.content.strip().replace('"', '')
        st.session_state['chat_titles'][st.session_state['thread_id']] = title_text
        save_chat_titles(st.session_state['chat_titles'])
        st.rerun()
