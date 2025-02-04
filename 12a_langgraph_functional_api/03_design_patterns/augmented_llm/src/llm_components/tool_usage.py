from dotenv import load_dotenv, find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

def search_medical_database(query: str) -> str:
    """Search medical literature database"""
    # Mock implementation
    return f"Results for: {query}"

# Bind tool to LLM
llm_with_tools = model.bind_tools([search_medical_database])

# Use the augmented LLM
def get_tools_output():
    result = llm_with_tools.invoke("Find recent studies on statins")
    return result.tool_calls
