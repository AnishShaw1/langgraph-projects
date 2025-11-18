import streamlit as st
from backend import chatbot,llm
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# **************************************** utility functions *************************

def generate_thread_id():
    """Generate a unique ID for each chat thread."""
    return uuid.uuid4()

def add_thread(thread_id):
    """Add a new thread to session state if it doesn't exist already."""
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    """Start a completely new chat session."""
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['message_history'] = []

def load_conversation(thread_id):
    """Load stored conversation messages for a given thread."""
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Return empty list if no messages exist
    return state.values.get('messages', [])


# **************************************** Session Setup ******************************
# Streamlit re-runs code after every interaction, so we persist data in session_state.

# Initialize chat_threads FIRST to avoid race conditions
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

# Then initialize thread_id and immediately add it to threads
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    add_thread(st.session_state['thread_id'])

# Initialize message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Track chat titles (dict: thread_id → title)
if 'chat_titles' not in st.session_state:
    st.session_state['chat_titles'] = {}



# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

# Button to start a new chat
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')


    
# Use a radio button list instead of multiple buttons
# This preserves which chat is selected even after reruns.
selected_thread = st.sidebar.radio(
    "Select a conversation",
    st.session_state['chat_threads'][::-1],  # latest chats first
    format_func=lambda tid: st.session_state['chat_titles'].get(tid, "New Chat...")
)

# Load messages only when a new thread is selected
if selected_thread != st.session_state['thread_id']:
    st.session_state['thread_id'] = selected_thread
    messages = load_conversation(selected_thread)
    
    # Convert LangChain message objects into displayable dicts
    temp_messages = []
    for msg in messages:
        role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
        temp_messages.append({'role': role, 'content': msg.content})
    st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# Display chat history (user & assistant messages)
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])  # markdown preserves formatting better than text()

# Input box for new user messages
user_input = st.chat_input('Type here')

if user_input:
    # Add user message to history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.markdown(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # Stream assistant response in real time
    with st.chat_message("assistant"):
        def ai_only_stream():
            """Stream only the assistant's generated content."""
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content or ""

        ai_message = st.write_stream(ai_only_stream())

    # Add assistant message to history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # Generate a smart title using Gemini
    if st.session_state['thread_id'] not in st.session_state['chat_titles']:
        title_prompt = f"Summarize this chat topic in 5 words or fewer:\nUser: {user_input}\nAssistant: {ai_message}"
        title_response = llm.invoke([HumanMessage(content=title_prompt)])
        title_text = title_response.content.strip().replace('"', '')
        st.session_state['chat_titles'][st.session_state['thread_id']] = title_text
        st.rerun()  # Refresh sidebar to show new title 
