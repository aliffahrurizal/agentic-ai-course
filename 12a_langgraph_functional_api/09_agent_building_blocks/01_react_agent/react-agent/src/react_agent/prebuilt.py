from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
)

prompt = """
You are a helpful assistant that can answer questions and help with tasks.
"""

agent = create_react_agent(
    model=llm,
    tools=[],
    prompt=prompt,
)


def main():
    response = agent.invoke({"messages": "What is the capital of the moon?"})
    for message in response["messages"]:
        message.pretty_print()


