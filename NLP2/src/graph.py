from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition, ToolNode

from .agents import (
    AgentState, 
    router_node, 
    theory_agent_node, 
    practice_agent_node, 
    general_agent_node,
    all_tools
)

def create_graph():
    workflow = StateGraph(AgentState)

    # 1. Add Nodes
    workflow.add_node("router", router_node)
    workflow.add_node("theory_agent", theory_agent_node)
    workflow.add_node("practice_agent", practice_agent_node)
    workflow.add_node("general_agent", general_agent_node)
    workflow.add_node("tools", ToolNode(all_tools))

    # 2. Add Entry Point
    workflow.set_entry_point("router")

    # 3. Router logic
    def route_decision(state: AgentState):
        return state["next"]

    workflow.add_conditional_edges(
        "router",
        route_decision,
        {
            "theory_agent": "theory_agent",
            "practice_agent": "practice_agent",
            "general_agent": "general_agent"
        }
    )

    # 4. Agent Loops
    # Theory
    workflow.add_conditional_edges(
        "theory_agent",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # Practice
    workflow.add_conditional_edges(
        "practice_agent",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )

    # General
    workflow.add_edge("general_agent", END)

    # 5. Tool Return Logic
    def tool_return_route(state: AgentState):
        # Return to the agent that called the tool.
        # Logic relies on the 'next' field not changing during tool execution.
        return state["next"]

    workflow.add_conditional_edges(
        "tools",
        tool_return_route,
        {
            "theory_agent": "theory_agent",
            "practice_agent": "practice_agent"
        }
    )

    return workflow.compile()
