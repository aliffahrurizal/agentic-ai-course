from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.tools import tool

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

prompt = "You are a helpful assistant that can answer questions and help with tasks."

@tool
def get_weather(location: str):
    """Call to get the weather from a specific location."""
    # This is a placeholder for the actual implementation
    if any([city in location.lower() for city in ["lahore", "lhr"]]):
        return "It's sunny!"
    elif "karachi" in location.lower():
        return "It's rainy!"
    else:
        return f"I am not sure what the weather is in {location}"


agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt=prompt,
)


def main():
    response = agent.invoke(
        {"messages": "Use get_weather tool and share what's the weather in Karachi?"})
    for message in response["messages"]:
        message.pretty_print()
