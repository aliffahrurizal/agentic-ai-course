import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

agent: Agent = Agent(name="Assistant", 
                     instructions="You are a helpful assistant",  
                     model=OpenAIChatCompletionsModel(
                        model="gemini-2.0-flash",
                        openai_client=external_client)
    )

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
