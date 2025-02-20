import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

async def main() -> None:

    

    # Create the model client
    model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(model="gemini-2.0-flash", api_key=gemini_api_key)
    agent: AssistantAgent = AssistantAgent("assistant", model_client)
    result: TaskResult = await agent.run(task="What is the capital of France?")
    for message in result.messages:
        print(f"{message.source}: {message.content}")

def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
