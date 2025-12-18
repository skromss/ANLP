import os
import json
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from state import AgentState
from models import LiteraturePlan, LiteratureSummary, Paper, AuthorStats
from tools import mock_search_arxiv, mock_get_author_stats

# Load environment variables
load_dotenv(find_dotenv(usecwd=True))

# Configuration
BASE_URL = os.getenv("LITELLM_BASE_URL", "http://a6k2.dgx:34000/v1")
API_KEY = os.getenv("LITELLM_API_KEY", "sk-PHv09yWMAnXtSqkO-LAm1A")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-32b")

# Initialize LLM
llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0
)

# --- Nodes ---

def planner_node(state: AgentState) -> dict:
    """
    LLM Node: Planner.
    Analyzes the user query and creates a structured plan using Pydantic.
    """
    print("--- Planner Node ---")
    parser = PydanticOutputParser(pydantic_object=LiteraturePlan)
    
    system_prompt = """You are a research planning assistant.
    Given a user topic, create a structured search plan.
    Extract 2-3 main keywords and identify constraints.
    
    You must output a JSON object matching the following schema:
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Topic: {topic}")
    ])
    
    chain = prompt | llm | parser
    
    try:
        plan = chain.invoke({
            "topic": state["user_query"],
            "format_instructions": parser.get_format_instructions()
        })
        print(f"Generated Plan: {plan}")
        return {"plan": plan, "messages": [HumanMessage(content=f"Plan generated: {plan}")]}
    except Exception as e:
        print(f"Planner Error: {e}")
        raise e

def arxiv_search_node(state: AgentState) -> dict:
    """
    Tool Node: Arxiv Search.
    Executes search based on plan.
    Includes Manual Retry Logic since RetryPolicy was invalid.
    """
    print("--- Arxiv Search Node ---")
    plan = state["plan"]
    if not plan:
        raise ValueError("No plan found in state.")
        
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Validation logic is inside the tool (simulated failure will occur here)
            results = mock_search_arxiv(plan.keywords, plan.min_year)
            return {"papers": results}
        except Exception as e:
            print(f"[ArxivSearch] Error (Attempt {attempt+1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                print("[ArxivSearch] Max retries reached. Returning empty.")
                return {"papers": []}
            # Wait a bit if needed, but for mock we just retry
    return {"papers": []}

def author_stats_node(state: AgentState) -> dict:
    """
    Tool Node: Author Stats.
    """
    print("--- Author Stats Node ---")
    plan = state["plan"]
    
    if plan and plan.need_author_stats:
        # For simplicity in this mock, we just pick the first author from a fixed list or the plan
        # We will check a dummy author for the demo
        stats = mock_get_author_stats(["J. Smith"])
        return {"author_stats": stats}
    
    return {"author_stats": None}

def writer_node(state: AgentState) -> dict:
    """
    LLM Node: Writer.
    Synthesizes all information into a final response.
    """
    print("--- Writer Node ---")
    parser = PydanticOutputParser(pydantic_object=LiteratureSummary)
    
    system_prompt = """You are a senior science communicator.
    Write a summary based on the provided papers and author stats.
    Focus on trends and open questions.
    
    Output strictly in JSON format as per the instructions.
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Plan: {plan}\n\nPapers: {papers}\n\nAuthor Stats: {stats}")
    ])
    
    chain = prompt | llm | parser
    
    # helper for stringifying
    papers_str = "\n".join([f"- {p.title} ({p.year}): {p.summary}" for p in state.get("papers", [])])
    stats_str = str(state.get("author_stats", "None"))
    
    try:
        response = chain.invoke({
            "plan": state["plan"], 
            "papers": papers_str,
            "stats": stats_str,
            "format_instructions": parser.get_format_instructions()
        })
        return {"final_summary": response}
    except Exception as e:
        print(f"Writer Error: {e}")
        # In case of parsing error, we could retry or just raise. 
        # For this lab, raising is fine, or we could return a fallback.
        raise e
