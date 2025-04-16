from langgraph.func import entrypoint, task
from langgraph.graph.message import add_messages

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import ToolMessage
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


tools = [get_weather]

tools_by_name = {tool.name: tool for tool in tools}


@task
def call_model(messages):
    """Call model with a sequence of messages."""
    response = llm.bind_tools(tools).invoke(messages)
    return response


@task
def call_tool(tool_call):
    tool = tools_by_name[tool_call["name"]]
    observation = tool.invoke(tool_call["args"])
    return ToolMessage(content=observation, tool_call_id=tool_call["id"], name=tool_call["name"])


@entrypoint()
def agent(messages):
    llm_response = call_model(messages).result()
    while True:
        if not llm_response.tool_calls:
            break

        # Execute tools
        tool_result_futures = [
            call_tool(tool_call) for tool_call in llm_response.tool_calls
        ]
        tool_results = [fut.result() for fut in tool_result_futures]

        # Append to message list
        messages = add_messages(messages, [llm_response, *tool_results])

        # Call model again
        llm_response = call_model(messages).result()

    return llm_response

def main():
    user_message = {"role": "user", "content": "Use get_weather tool and share what's the weather in Lahore?"}

    for step in agent.stream([user_message]):
        for message in step.values():
            message.pretty_print()