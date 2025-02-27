import os
from dotenv import load_dotenv
from typing import Sequence, Union

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import  ChatMessage, AgentEvent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Create an OpenAI model client (using GPT-4o as an example)
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Define our specialized agents with meaningful names and descriptions:
strategy_agent = AssistantAgent(
    "StrategyAgent",
    description="A strategic planner that breaks down enterprise use cases into actionable subtasks.",
    model_client=model_client,
    system_message="""
    You are the Strategy Agent. Your role is to plan and delegate tasks for developing enterprise AI use cases.
    When given a new task, break it down into smaller subtasks and assign them to appropriate team members.
    Use the format:
      1. <AgentName>: <Subtask>
    """
)

market_research_agent = AssistantAgent(
    "MarketResearchAgent",
    description="An agent that performs market research to gather relevant data.",
    model_client=model_client,
    system_message="""
    You are the Market Research Agent. Your role is to search for market data.
    Use your tool 'market_research_tool' to find information that is directly related to the task.
    Provide concise results.
    """
)

data_insight_agent = AssistantAgent(
    "DataInsightAgent",
    description="An agent that analyzes data and computes key metrics such as conversion improvements.",
    model_client=model_client,
    system_message="""
    You are the Data Insight Agent. Analyze the data provided and calculate critical metrics.
    For example, compute the percentage improvement between current and target conversion rates.
    Provide your answer in clear numerical terms.
    """
)

# Termination Conditions: after 5 messages.
termination = MaxMessageTermination(max_messages=5)

# Custom selector prompt that uses agent names and descriptions:
selector_prompt = """Select the next agent to work on the task from the following list:
{roles}

Current conversation context:
{history}

Ensure that if specialized agents have responded, the StrategyAgent gets a chance to review and assign the next step.
Return ONLY the name of the agent.
"""

# Create the SelectorGroupChat with our agents.
team = SelectorGroupChat(
    participants=[strategy_agent, market_research_agent, data_insight_agent],
    model_client=model_client,
    termination_condition=termination,
    selector_prompt=selector_prompt,
    allow_repeated_speaker=True,
)

# Define the overall task.
task = (
    "Design an enterprise AI use case to improve sales conversion rates for an e-commerce company. "
    "Outline how personalized recommendations and dynamic pricing can drive revenue growth."
)

# Run the team in a streaming mode.
async def run_team():
    await Console(team.run_stream(task=task))

def call_enterprise_research_group():
    import asyncio
    asyncio.run(run_team())
