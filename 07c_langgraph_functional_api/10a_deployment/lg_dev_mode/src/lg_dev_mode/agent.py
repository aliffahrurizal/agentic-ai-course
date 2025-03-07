from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages
from typing_extensions import Optional
from langchain_core.messages import BaseMessage

from langgraph.func import entrypoint, task

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
)

@task
def call_model(messages: list[BaseMessage]):
    response = llm.invoke(messages)
    return response

@entrypoint()
def pr(messages: list[BaseMessage], previous: Optional[list[BaseMessage]] = []):
    print(f"Previous: {previous}")
    print(f"Input: {messages}")

    if previous:
        messages = add_messages(previous, messages)

    response = llm.invoke(messages)
        
    return entrypoint.final(value=response, save=add_messages(messages, response))
