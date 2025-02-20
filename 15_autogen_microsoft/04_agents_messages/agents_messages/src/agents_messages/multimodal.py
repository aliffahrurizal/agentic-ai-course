import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import Response
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

from io import BytesIO

import PIL
import requests
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")



model_client: OpenAIChatCompletionClient = OpenAIChatCompletionClient(model="gemini-2.0-flash", api_key=gemini_api_key)
    
agent: AssistantAgent = AssistantAgent(
    name="assistant",
    model_client=model_client
)

async def main() -> None:
    # Create a multi-modal message with random image and text.
    pil_image = PIL.Image.open(BytesIO(requests.get("https://picsum.photos/300/200").content))
    img = Image(pil_image)
    multi_modal_message = MultiModalMessage(content=["Can you describe the content of this image?", img], source="user")

    response: Response = await agent.on_messages(
        [multi_modal_message],
        cancellation_token=CancellationToken(),
    )

    print(response.chat_message.content)


def run_main():
    asyncio.run(main())


if __name__ == "__main__":
    run_main()
