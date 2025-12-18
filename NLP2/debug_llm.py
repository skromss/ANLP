from src.llm_config import get_llm

llm = get_llm()
print("Invoking LLM...")
res = llm.invoke("Hello")
print(res.content)
