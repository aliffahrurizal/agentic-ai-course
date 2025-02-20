# Agentic AI Design Patterns with Teams Implementation

AutoGen’s team constructs—like the SelectorGroupChat and RoundRobinGroupChat—are designed to coordinate multi‑agent interactions, making them especially well‑suited to implementing several of Anthropic’s design patterns. In particular, teams are a natural fit for:

1. **Routing:**  
   With teams, you can deploy a router agent alongside specialized agents (e.g., a math agent and a general agent). By using a custom speaker selector within the team, the router’s decision can direct the conversation flow to the appropriate agent.

2. **Orchestrator‑Workers:**  
   Teams allow you to group an orchestrator (or planner) with multiple worker agents. The orchestrator can delegate subtasks to different workers (sequentially or in parallel) and then aggregate their outputs into a final response—all within a coordinated team conversation.

3. **Evaluator‑Optimizer:**  
   In a team, one agent can first generate a candidate solution, another can evaluate that output, and a third can optimize it. The team’s routing logic (via a custom selector) can facilitate the turn‑taking needed for such iterative improvement.

Below, we detail each with code examples.

---

## 1. Routing with Teams

In this example, a router agent classifies a user query as “MATH” or “GENERAL” and, using a custom selector function, the team directs the conversation to either a math‑specialized agent or a general‑purpose agent.

```python
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Initialize model client (replace with your API key or load from env)
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Specialized agents
math_agent = AssistantAgent(
    name="math_agent",
    system_message="You are a math expert. Answer math questions step-by-step.",
    model_client=model_client,
)

general_agent = AssistantAgent(
    name="general_agent",
    system_message="You are a general-purpose assistant. Answer everyday questions concisely.",
    model_client=model_client,
)

# Router agent classifies the query.
router_agent = AssistantAgent(
    name="router_agent",
    system_message=(
        "Classify the following query. If it is math-related, reply 'MATH'. "
        "Otherwise, reply 'GENERAL'. Only output one word."
    ),
    model_client=model_client,
)

# Custom selector that checks the last message from the router to choose the speaker.
def custom_selector(messages):
    if messages:
        last_msg = messages[-1]
        if last_msg.source == "router_agent":
            decision = last_msg.content.strip().upper()
            if "MATH" in decision:
                return "math_agent"
            elif "GENERAL" in decision:
                return "general_agent"
    # If no decision yet, let the router speak.
    return "router_agent"

# Create a team including all three agents.
team = SelectorGroupChat(
    agents=[router_agent, math_agent, general_agent],
    termination_condition=TextMentionTermination("exit"),
    selector_func=custom_selector
)

async def routing_team_flow():
    cancellation_token = CancellationToken()
    user_query = "Calculate the derivative of x^2."
    print(f"User Query: {user_query}\n{'-'*50}")
    async for message in team.run_stream(task=user_query, cancellation_token=cancellation_token):
        print(f"{message.source}: {message.content}")

asyncio.run(routing_team_flow())
```

### Explanation

- The **router_agent** first processes the query and outputs a one‑word classification.
- The **custom_selector** checks the last message from the router. Based on the decision, it directs the team turn to either the math_agent or general_agent.
- The **SelectorGroupChat** then manages the conversation flow accordingly.

---

## 2. Orchestrator‑Workers with Teams

Here, an orchestrator agent breaks a complex task into subtasks and delegates them to multiple worker agents within the team. The orchestrator then aggregates the results.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Shared model client.
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Orchestrator agent to split the task and aggregate responses.
orchestrator = AssistantAgent(
    name="orchestrator",
    system_message="Decompose the following task into two subtasks (one per line) and later aggregate the results.",
    model_client=model_client,
)

# Worker agents to handle subtasks.
worker_a = AssistantAgent(
    name="worker_a",
    system_message="Solve the first subtask.",
    model_client=model_client,
)

worker_b = AssistantAgent(
    name="worker_b",
    system_message="Solve the second subtask.",
    model_client=model_client,
)

# Custom selector for orchestrator-workers team.
def orchestrator_selector(messages):
    # Check if the orchestrator has already produced subtasks.
    for msg in messages:
        if msg.source == "orchestrator" and "subtask" in msg.content.lower():
            # After subtasks are produced, select a worker alternatively.
            # (For simplicity, we alternate based on message count.)
            if len(messages) % 2 == 0:
                return "worker_a"
            else:
                return "worker_b"
    # Initially, let the orchestrator speak.
    return "orchestrator"

# Create the team with the orchestrator and worker agents.
team = SelectorGroupChat(
    agents=[orchestrator, worker_a, worker_b],
    termination_condition=TextMentionTermination("exit"),
    selector_func=orchestrator_selector
)

async def orchestrator_workers_flow():
    cancellation_token = CancellationToken()
    task = "Analyze the impact of AI on healthcare and finance."
    print(f"Task: {task}\n{'-'*50}")
    async for message in team.run_stream(task=task, cancellation_token=cancellation_token):
        print(f"{message.source}: {message.content}")

asyncio.run(orchestrator_workers_flow())
```

### Explanation

- The **orchestrator** first breaks the main task into two subtasks.
- The custom selector then alternates between **worker_a** and **worker_b** to handle these subtasks.
- The team conversation collects and aggregates responses, simulating an orchestrator‑workers workflow.

---

## 3. Evaluator‑Optimizer with Teams

This pattern involves an agent generating a candidate solution, an evaluator agent providing feedback, and an optimizer agent refining the solution. Teams can coordinate this iterative process.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Shared model client.
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Candidate agent generates a draft solution.
candidate_agent = AssistantAgent(
    name="candidate_agent",
    system_message="Generate a draft solution for the given task.",
    model_client=model_client,
)

# Evaluator agent reviews the draft.
evaluator_agent = AssistantAgent(
    name="evaluator_agent",
    system_message="Evaluate the following solution and provide constructive feedback.",
    model_client=model_client,
)

# Optimizer agent refines the solution based on feedback.
optimizer_agent = AssistantAgent(
    name="optimizer_agent",
    system_message="Optimize the solution based on the evaluator's feedback. Provide the improved solution.",
    model_client=model_client,
)

# Custom selector for evaluator-optimizer team.
def evaluator_optimizer_selector(messages):
    # If the candidate's output is available, let evaluator speak.
    if any(msg.source == "candidate_agent" for msg in messages):
        # If evaluator has already spoken, then let the optimizer speak.
        if any(msg.source == "evaluator_agent" for msg in messages):
            return "optimizer_agent"
        else:
            return "evaluator_agent"
    # Otherwise, start with the candidate.
    return "candidate_agent"

# Create the team with candidate, evaluator, and optimizer agents.
team = SelectorGroupChat(
    agents=[candidate_agent, evaluator_agent, optimizer_agent],
    termination_condition=TextMentionTermination("exit"),
    selector_func=evaluator_optimizer_selector
)

async def evaluator_optimizer_flow():
    cancellation_token = CancellationToken()
    task = "Draft a proposal to reduce energy consumption in data centers."
    print(f"Task: {task}\n{'-'*50}")
    async for message in team.run_stream(task=task, cancellation_token=cancellation_token):
        print(f"{message.source}: {message.content}")

asyncio.run(evaluator_optimizer_flow())
```

### Explanation

- The team starts with the **candidate_agent** generating a draft.
- The custom selector then directs the conversation to the **evaluator_agent** to provide feedback.
- Finally, the selector shifts the turn to the **optimizer_agent** to refine the solution.
- The team chat orchestrates these turns to produce an improved final output.

---

## 4. Conclusion

AutoGen teams—through constructs like SelectorGroupChat—are a powerful tool for implementing agentic design patterns. They naturally support workflows such as:

- **Routing:** Directing queries to specialized agents.
- **Orchestrator‑Workers:** Delegating and aggregating subtasks.
- **Evaluator‑Optimizer:** Iteratively refining solutions.

By leveraging a custom selector function, you can dynamically control the flow of conversation in a multi‑agent team, matching the Anthropic design patterns with robust, asynchronous, and collaborative implementations.

These examples illustrate how AutoGen 0.4.7+ teams can be adapted to implement complex multi-agent workflows, providing a flexible foundation for building next‑generation AI applications.

