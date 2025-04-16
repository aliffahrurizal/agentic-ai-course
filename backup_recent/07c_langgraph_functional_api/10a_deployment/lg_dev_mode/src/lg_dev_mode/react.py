from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from datetime import datetime

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
)

@tool
def get_current_time():
    """Get the current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

agent = create_react_agent(
    model=llm,
    tools=[get_current_time],
    # prompt="Reply in Shakespear's style",
)