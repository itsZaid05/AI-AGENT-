from langchain_perplexity import ChatPerplexity 
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image, display
from langgraph.graph.message import add_messages
import os

load_dotenv()

class State(TypedDict):
    message: str

# LLM model
llm = ChatPerplexity(model="llama-3.1-sonar-small-128k-online")

def chatbot(state: State):
    return {"message": [llm.invoke(state["message"])]}

graph_builder = StateGraph(State)

# Add node
graph_builder.add_node("llmchatbot", chatbot)

# Add edges
graph_builder.add_edge(START, "llmchatbot")
graph_builder.add_edge("llmchatbot", END)

# Compile the graph
graph = graph_builder.compile()

# Visualize the graph
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass

# TavilySearch tool — YOUR original import
from langchain_tavily import TavilySearch

tool = TavilySearch(max_results=2)
tool.invoke("What is langgraph")

# Your multiply tool — fixed syntax
def multiply(a: int, b: int) -> int:
    """Multiply a and b"""
    return a * b

# Tools list
tools = [tool, multiply]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Tool definition node — fixed syntax
def tool_definition(state: State):
    return {"message": [llm_with_tools.invoke(state["message"])]}

# Second graph with tools — your structure
builder = StateGraph(State)
builder.add_node("tool_calling_llm", tool_definition)

# Add edges
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,

)
builder.add_edge("tool_calling_llm", END)
toolkit=builder.compile()
# If you want conditions — keep this:
# builder.add_conditional_edges("tool_calling_llm", tools_condition)

result=toolkit.invoke({"message":"whats the score of ind vs eng test match"})
print (result)