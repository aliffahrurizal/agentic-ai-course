import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(model="gemini-2.0-flash", api_key="gemini-api-key")
    agent: AssistantAgent = AssistantAgent("assistant", model_client)
    result: TaskResult = await agent.run(task="What is the capital of France?")
    for message in result.messages:
        print(f"{message.source}: {message.content}")

def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
