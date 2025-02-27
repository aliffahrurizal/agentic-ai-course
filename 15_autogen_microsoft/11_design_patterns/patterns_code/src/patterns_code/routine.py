import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
from autogen_agentchat.messages import TextMessage

# Load API key from .env file (make sure your .env file contains OPENAI_API_KEY)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please define it in your .env file.")

# Initialize a shared model client (using GPT-4o in this example)
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

# Define a routine agent that fetches a status update continuously
routine_agent = AssistantAgent(
    name="status_agent",
    system_message="You are a status-monitoring agent. Every time you are invoked, produce a current status update.",
    model_client=model_client,
)

async def routine_task(cancellation_token: CancellationToken, interval: int = 5):
    """Run the status monitoring routine at specified intervals."""
    while not cancellation_token.is_cancelled():
        # Invoke the agent to get a status update
        response = await routine_agent.on_messages(
            [TextMessage(
                content="Fetch current status",
                source="user"  # Adding required source parameter
            )],
            cancellation_token
        )
        print(f"Status Update: {response.chat_message.content}")
        # Wait for the next interval
        await asyncio.sleep(interval)

async def run_routine():
    """Run the routine for 30 seconds."""
    cancellation_token = CancellationToken()
    try:
        # Run the routine task for a certain period (e.g., 30 seconds)
        await asyncio.wait_for(routine_task(cancellation_token, interval=5), timeout=30)
    except asyncio.TimeoutError:
        cancellation_token.cancel()
        print("Routine task ended.")

def main():
    asyncio.run(run_routine())

if __name__ == "__main__":
    main()
