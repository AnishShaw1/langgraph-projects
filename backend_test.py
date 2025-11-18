from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI 
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3
# define state

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

# define llm
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# define graph-node

def chat_node(state: ChatState):
    # take user query from state
    messages = state['messages']
    # send to llm
    response = llm.invoke(messages)
    # response store state
    return {'messages': [response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

# define graph

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

'''CONFIG = {'configurable': {'thread_id': "thread_1"}}


response = chatbot.invoke({'messages': [HumanMessage(content="what is my name ")]}, 
                          config=CONFIG)
print(response)'''
# function to retrieve all unique thread IDs
def retrieve_all_thread_ids():
    unique_threads=set() # to store unique thread IDs
    for checkpoint in checkpointer.list(None):  # iterate through all checkpoints
        unique_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(unique_threads)

'''for checkpoint in checkpointer.list(None):
    print(checkpoint)

conn.execute("DELETE FROM checkpoints WHERE thread_id = ?", ('thread_1',))
conn.execute("DELETE FROM writes WHERE thread_id = ?", ('thread_1',))
conn.commit()'''
