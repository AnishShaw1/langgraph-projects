from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI 
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchResults
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3


# define llm
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm1 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
# Tools

search_tool = DuckDuckGoSearchResults()


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=RP2J23DYDVG9996S"
    r = requests.get(url)
    return r.json()

tools = [search_tool, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)

# define state

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

# define graph-node
from google.api_core.exceptions import ServiceUnavailable
def chat_node(state: ChatState):
    # take user query from state
    messages = state['messages']
    # send to llm
    try:
        response = llm_with_tools.invoke(messages)
        return {'messages': [response]}
    except ServiceUnavailable:
        error_msg = "⚠️ Gemini service is temporarily overloaded. Please try again in a few seconds."
        return {'messages': [HumanMessage(content=error_msg)]}
    except Exception as e:
        error_msg = f"❌ Unexpected error: {str(e)}"
        return {'messages': [HumanMessage(content=error_msg)]}

tool_node = ToolNode(tools)


conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

# define graph

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')


chatbot = graph.compile(checkpointer=checkpointer)

# function to retrieve all unique thread IDs
def retrieve_all_thread_ids():
    unique_threads=set() # to store unique thread IDs
    for checkpoint in checkpointer.list(None):  # iterate through all checkpoints
        unique_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(unique_threads)



# 🔥 delete thread completely (DB cleanup)
def delete_thread(thread_id: str):
    conn.execute("DELETE FROM checkpoints WHERE thread_id = ?", (thread_id,))
    conn.execute("DELETE FROM writes WHERE thread_id = ?", (thread_id,))
    conn.commit()