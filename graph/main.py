# Main Graph Entry Point
from langgraph.graph import StateGraph, END
from .state import AgentState

def build_graph():
    workflow = StateGraph(AgentState)
    # Add nodes and edges here
    return workflow.compile()
