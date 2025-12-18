from typing import List
import random
from models import Paper, AuthorStats

class ToolError(Exception):
    """Simulated error for testing retries."""
    pass

# Global counter to simulate transient failure
_SEARCH_ATTEMPTS = 0

def mock_search_arxiv(keywords: List[str], min_year: int) -> List[Paper]:
    """
    Mock tool to search for papers.
    Simulates a network failure on the first call to test retry logic.
    """
    global _SEARCH_ATTEMPTS
    _SEARCH_ATTEMPTS += 1
    
    print(f"[ArxivSearch] Attempt {_SEARCH_ATTEMPTS} for keywords: {keywords}")
    
    # Simulate failure on first attempt
    if _SEARCH_ATTEMPTS == 1:
        raise ToolError("Simulated connection error to Arxiv API.")

    return [
        Paper(
            title="Advances in Multi-Agent Reinforcement Learning",
            authors=["J. Smith", "A. Doe"],
            summary="A comprehensive survey of MARL techniques in 2024.",
            year=2024
        ),
        Paper(
            title="LangGraph: A New Era of Agent Orchestration",
            authors=["B. Harrison", "C. Wu"],
            summary="Introducing graph-based control flow for LLM agents.",
            year=2025
        ),
        Paper(
            title="Optimizing Retrieval Augmented Generation",
            authors=["J. Smith"],
            summary="Techniques for better RAG performance.",
            year=2024
        )
    ]

def mock_get_author_stats(authors: List[str]) -> AuthorStats:
    """Mock tool to get author statistics."""
    print(f"[AuthorStats] Fetching stats for: {authors[:3]}...")
    return AuthorStats(
        top_authors=["J. Smith"],
        average_h_index=45.5,
        note="J. Smith is a highly cited researcher in this field."
    )
