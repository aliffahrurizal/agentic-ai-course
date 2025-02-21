# OpenAI Swarm Design Patterns

https://cookbook.openai.com/examples/orchestrating_agents

https://microsoft.github.io/autogen/dev//user-guide/agentchat-user-guide/swarm.html

Below is a detailed “paper” that shows how you can implement two OpenAI Swarm Agentic design patterns—**Routines** and **Handoffs**—using AutoGen. Both patterns are well supported by AutoGen’s multi‐agent, asynchronous, and team‐oriented architecture. In the sections below, we explain each design pattern and provide corresponding code examples using AutoGen’s agent and team constructs. 

---

## 1. Introduction

Swarm agentic design patterns enable multiple AI agents to work together toward a common goal by distributing tasks, communicating results, and continuously optimizing performance. Two key patterns from OpenAI’s design principles are:

1. **Routines:**  
   Agents run tasks repeatedly or continuously (often in parallel or on a schedule) to monitor, update, or maintain context. For example, an agent might routinely check data sources and update a shared knowledge base.

2. **Handoffs:**  
   One agent finishes its portion of a task and passes (“hands off”) its output to another agent to continue processing. This pattern is akin to a relay race where the baton is passed along to ensure a task is completed in sequential stages.

AutoGen—with its flexible agent definitions, asynchronous messaging, and team coordination tools (such as SelectorGroupChat)—provides a natural framework for implementing both patterns.

---

## 2. Implementing Routines with AutoGen

### 2.1 Concept

**Routines** involve agents that execute repeated or continuous tasks. In AutoGen, you can implement routines by having an agent run in a loop (or schedule periodic invocations) to perform an ongoing task, such as monitoring a data feed or periodically checking system status.

### 2.2 Code Example for Routines

Below is an example where an agent is set up to periodically fetch a “status update” from a simulated data source. The agent continuously runs a routine and prints the updated status.

```python
import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

# Load API key from .env file (make sure your .env file contains OPENAI_API_KEY)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please define it in your .env file.")

# Initialize a shared model client (using GPT-4o in this example)
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key=api_key)

# Define a routine agent that fetches a status update continuously.
routine_agent = AssistantAgent(
    name="status_agent",
    system_message="You are a status-monitoring agent. Every time you are invoked, produce a current status update.",
    model_client=model_client,
)

async def routine_task(cancellation_token: CancellationToken, interval: int = 5):
    while not cancellation_token.cancelled:
        # Invoke the agent to get a status update.
        response = await routine_agent.on_messages([{"content": "Fetch current status", "source": "routine"}], cancellation_token)
        print(f"Status Update: {response.chat_message.content.strip()}")
        # Wait for the next interval.
        await asyncio.sleep(interval)

async def run_routine():
    cancellation_token = CancellationToken()
    try:
        # Run the routine task for a certain period (e.g., 30 seconds)
        await asyncio.wait_for(routine_task(cancellation_token, interval=5), timeout=30)
    except asyncio.TimeoutError:
        cancellation_token.cancel()
        print("Routine task ended.")

asyncio.run(run_routine())
```

### Explanation

- **Status Agent:**  
  The `status_agent` is defined with a system prompt that instructs it to return a status update each time it is invoked.

- **Routine Task:**  
  A loop repeatedly calls the agent every 5 seconds (or a specified interval) until a timeout is reached.

- **Cancellation:**  
  A `CancellationToken` is used to cleanly exit the routine after 30 seconds.

---

## 3. Implementing Handoffs with AutoGen Teams

### 3.1 Concept

**Handoffs** involve a “relay” mechanism where one agent completes its portion of a task and then passes its output to another agent for further processing. AutoGen’s team constructs (such as SelectorGroupChat) allow you to implement handoffs by controlling turn‑taking between agents using custom selector functions.

### 3.2 Code Example for Handoffs

In this example, a candidate agent generates a draft solution. Then, control is handed off to an evaluator agent to provide feedback, and finally, an optimizer agent refines the solution. A custom selector function directs the flow of conversation among the agents.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Initialize a shared model client.
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Candidate agent generates a draft.
candidate_agent = AssistantAgent(
    name="candidate_agent",
    system_message="Generate a draft answer for the task.",
    model_client=model_client,
)

# Evaluator agent reviews the draft.
evaluator_agent = AssistantAgent(
    name="evaluator_agent",
    system_message="Evaluate the provided draft answer and list improvements.",
    model_client=model_client,
)

# Optimizer agent refines the draft based on evaluator feedback.
optimizer_agent = AssistantAgent(
    name="optimizer_agent",
    system_message="Refine the draft answer using the evaluator's feedback and produce an improved final version.",
    model_client=model_client,
)

# Custom selector function for handoffs.
def handoff_selector(messages):
    # If no message yet, start with the candidate.
    if not messages:
        return "candidate_agent"
    # Once the candidate has responded, let the evaluator speak.
    last_source = messages[-1].source
    if last_source == "candidate_agent":
        return "evaluator_agent"
    # After evaluator's feedback, let the optimizer respond.
    if last_source == "evaluator_agent":
        return "optimizer_agent"
    # Otherwise, end the handoff sequence.
    return None

# Create a team for the handoff flow.
team = SelectorGroupChat(
    agents=[candidate_agent, evaluator_agent, optimizer_agent],
    termination_condition=TextMentionTermination("exit"),
    selector_func=handoff_selector
)

async def handoff_flow():
    cancellation_token = CancellationToken()
    task = "Draft a proposal to improve renewable energy usage in data centers."
    print(f"Task: {task}\n{'-'*50}")
    async for message in team.run_stream(task=task, cancellation_token=cancellation_token):
        print(f"{message.source}: {message.content.strip()}")

asyncio.run(handoff_flow())
```

### Explanation

- **Candidate Agent:**  
  Generates an initial draft for the given task.

- **Evaluator Agent:**  
  Once the candidate has produced an output, the custom selector directs the next turn to the evaluator, which reviews the draft and suggests improvements.

- **Optimizer Agent:**  
  Finally, the selector passes control to the optimizer agent, which refines the solution based on the evaluator’s feedback.

- **Selector Function:**  
  The `handoff_selector` examines the conversation history and directs turn‑taking among the three agents to achieve a sequential handoff.

- **Team Coordination:**  
  The `SelectorGroupChat` handles the turn-based conversation, ensuring a smooth handoff from one agent to the next.

---

## 4. Conclusion

AutoGen provides powerful team constructs that can implement both **Routines** and **Handoffs**—two key patterns from OpenAI’s Swarm Agentic design. Routines are well suited for repeated, continuous tasks that require periodic updates, while handoffs enable sequential task processing where one agent’s output feeds directly into another’s input. Using AutoGen’s asynchronous messaging, custom selector functions, and team classes like SelectorGroupChat, developers can build complex multi-agent workflows that embody these patterns.

These detailed code examples illustrate how to configure agents, implement continuous routines, and orchestrate handoffs within teams—demonstrating AutoGen’s flexibility in orchestrating sophisticated, collaborative AI systems.

---

References:  
- OpenAI Swarm Agentic Design Patterns, orchestrating_agents, OpenAI Cookbook 
- Microsoft AutoGen Swarm User Guide 
