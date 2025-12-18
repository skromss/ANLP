import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.graph import create_graph

def main():
    graph = create_graph()
    try:
        mermaid_code = graph.get_graph().draw_mermaid()
        print(mermaid_code)
    except Exception as e:
        print(f"Error generating mermaid graph: {e}")

if __name__ == "__main__":
    main()
