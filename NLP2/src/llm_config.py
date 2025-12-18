import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables if they exist
load_dotenv()

# Configuration from the user request
BASE_URL = os.getenv("LITELLM_BASE_URL", "http://a6k2.dgx:34000/v1")
API_KEY = os.getenv("LITELLM_API_KEY", "sk-PHv09yWMAnXtSqkO-LAm1A")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-32b")

def get_llm(temperature=0.7):
    """
    Returns a configured ChatOpenAI instance using the vLLM endpoint.
    """
    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_base=BASE_URL,
        openai_api_key=API_KEY,
        temperature=temperature,
    )
