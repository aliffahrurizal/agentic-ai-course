from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

# Define output schema
class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query optimized for web search")
    justification: str = Field(None, description="Why this query is relevant")

# Create base LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Augment with structured output
structured_llm = llm.with_structured_output(SearchQuery)

# Use the augmented LLM
def get_structured_output():
    result = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")
    return result