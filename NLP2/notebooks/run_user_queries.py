import sys
import os
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

from src.graph import create_graph
from langchain_core.messages import HumanMessage

def run_query(graph, query: str):
    print(f"\n{'='*50}")
    print(f"User Query: {query}")
    print(f"{'='*50}")
    
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    events = graph.stream(initial_state)
    
    for event in events:
        for key, value in event.items():
            print(f"\n--- Node: {key} ---")
            if "next" in value:
                print(f"Routing Decision: {value['next']}")
            if "messages" in value:
                last_msg = value["messages"][-1]
                if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                    print(f"Tool Call: {last_msg.tool_calls[0]['name']}")
                    print(f"Args: {last_msg.tool_calls[0]['args']}")
                elif hasattr(last_msg, "content") and last_msg.content:
                    print(f"Response: {last_msg.content}")

def main():
    graph = create_graph()
    
    queries = [
        # Conceptual/Theoretical
        "How does the ReAct pattern differ from a standard Chain of Thought?",
        
        # Design/Architecture
        "Explain the difference between a router and a supervisor agent in multi-agent systems.",
        
        # Implementation/Coding
        "Write a Python function to generate the first n numbers of the Fibonacci sequence.",
        
        # Everyday Task 1 (Theory)
        "What are the notes in a D Major scale?",
        
        # Everyday Task 2 (Practice)
        "Plan a 30-minute guitar practice routine focusing on scales."
    ]
    
    for q in queries:
        run_query(graph, q)

if __name__ == "__main__":
    main()
