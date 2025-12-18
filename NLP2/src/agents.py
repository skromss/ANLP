import operator
from typing import Annotated, Sequence, TypedDict, Union, Literal

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .llm_config import get_llm
from .tools import search_music_theory, suggest_practice_routine, get_chord_notes

# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# --- Router Agent ---
def router_node(state: AgentState):
    llm = get_llm(temperature=0)
    
    system_prompt = (
        "You are a Music Tutor Router. Use the user's latest message to decide where to route the request.\n"
        "Categories:\n"
        "1. 'theory_agent': Questions about music theory, scales, intervals, definitions, or history.\n"
        "2. 'practice_agent': Requests for practice routines, chord notes, technique exercises, or planning a session.\n"
        "3. 'general_agent': Casual conversation, greetings, or off-topic queries.\n\n"
        "Output ONLY the exact destination string (e.g., 'theory_agent'). Do not add any explanation."
    )
    
    messages = [
        SystemMessage(content=system_prompt), 
        state["messages"][-1]
    ]
    
    response = llm.invoke(messages)
    content = response.content.strip().lower()
    
    if "theory" in content:
        return {"next": "theory_agent"}
    elif "practice" in content:
        return {"next": "practice_agent"}
    else:
        return {"next": "general_agent"}

# --- Theory Agent (Music) ---
def theory_agent_node(state: AgentState):
    llm = get_llm(temperature=0.3)
    tools = [search_music_theory]
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = (
        "You are a Music Theory Expert. Answer questions using the 'search_music_theory' tool if needed. "
        "Explain concepts clearly as if teaching a student."
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- Practice Agent (Planner) ---
def practice_agent_node(state: AgentState):
    llm = get_llm(temperature=0.3)
    tools = [suggest_practice_routine, get_chord_notes]
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = (
        "You are a Music Practice Coach. Help students plan their practice sessions or look up specific chords. "
        "Use 'suggest_practice_routine' for schedules and 'get_chord_notes' for chord info."
    )
    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# --- General Agent ---
def general_agent_node(state: AgentState):
    llm = get_llm(temperature=0.7)
    system_prompt = "You are a friendly Music Assistant. Provide general answers or chat with the user."
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# --- Tool Node ---
all_tools = [search_music_theory, suggest_practice_routine, get_chord_notes]
