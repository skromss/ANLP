from graph import create_graph
from langchain_core.messages import HumanMessage

def run_demo():
    print("Building Graph...")
    app = create_graph()
    
    print("Graph built. Creating visualization...")
    try:
        print(app.get_graph().draw_mermaid())
    except Exception as e:
        print(f"Could not draw graph: {e}")

    print("\n--- Starting Demo Run (Topic: 'Multi-Agent Support Systems') ---")
    
    initial_state = {
        "user_query": "Give me a short overview of recent work on Multi-Agent Support Systems in 2024-2025. Check author credibility.",
        "messages": [HumanMessage(content="Start research.")]
    }
    
    # We use stream logic to see steps
    try:
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"\n--- Output from Node: '{key}' ---")
                # print(value) 
                if "plan" in value:
                    print(f"Plan: {value['plan']}")
                if "papers" in value:
                    print(f"Papers found: {len(value['papers'])}")
                if "author_stats" in value:
                    print(f"Author Stats: {value['author_stats']}")
                if "final_summary" in value:
                    summary = value['final_summary']
                    print("\n=== FINAL GENERATED SUMMARY ===")
                    print(summary.model_dump_json(indent=2))
                    # Also print a human-readable text version
                    print("\n--- Readable Report ---")
                    print(f"**Main Trends**:\n" + "\n".join([f"- {t}" for t in summary.main_trends]))
                    print(f"\n**Notable Papers**:")
                    for p in summary.notable_papers:
                        print(f"- {p.title} ({p.year}) by {', '.join(p.authors)}")
                        print(f"  Summary: {p.summary}")
                    print(f"\n**Open Questions**:\n" + "\n".join([f"- {q}" for q in summary.open_questions]))
                    print(f"\n**Conclusion**:\n{summary.conclusion}")
                    
    except Exception as e:
        print(f"\nExecution Failed: {e}")

if __name__ == "__main__":
    run_demo()
