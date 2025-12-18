from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import planner_node, arxiv_search_node, author_stats_node, writer_node

def create_graph():
    """
    Constructs the LangGraph for the Literature Review Agent.
    """
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    
    # Retry logic is now inside the node itself
    workflow.add_node("arxiv_search", arxiv_search_node)
    
    workflow.add_node("author_stats", author_stats_node)
    workflow.add_node("writer", writer_node)

    # Add Edges
    # Start -> Planner
    workflow.add_edge(START, "planner")

    # Planner -> Parallel Tools
    # We fan out to both tools. They will run in parallel.
    workflow.add_edge("planner", "arxiv_search")
    workflow.add_edge("planner", "author_stats")

    # Parallel Tools -> Writer
    # Both need to finish before Writer runs.
    # In LangGraph, if multiple nodes go to one node, it waits for all predecessors?
    # Actually, in a DAG, yes. But to be safe and explicit, let's ensure synchronization.
    # Standard LangGraph behavior: if Writer depends on both, it runs once both act? 
    # Or do we need a join?
    # With StateGraph, if we have edges A->C and B->C, C will be triggered by BOTH. 
    # We want C to run ONCE after BOTH are done.
    # LangGraph doesn't automatically join dynamic parallel branches into one next step easily unless we specifically coordinate.
    # Use standard approach: edges.
    
    workflow.add_edge("arxiv_search", "writer")
    workflow.add_edge("author_stats", "writer")

    # Writer -> End
    workflow.add_edge("writer", END)

    # Compile
    return workflow.compile()
