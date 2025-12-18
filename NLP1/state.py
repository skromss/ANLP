from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from models import LiteraturePlan, Paper, AuthorStats, LiteratureSummary

class AgentState(TypedDict):
    """State of the literature review agent."""
    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    plan: Optional[LiteraturePlan]
    papers: List[Paper]
    author_stats: Optional[AuthorStats]
    final_summary: Optional[LiteratureSummary]
