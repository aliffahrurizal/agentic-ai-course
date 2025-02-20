# Agentic AI Design Patterns with Autogen

[Anthropic’s research on effective agents](https://www.anthropic.com/research/building-effective-agents)

Below is a detailed “paper” that explains how AutoGen 0.4.7+ can be used to implement each of the five Anthropic agentic design patterns—along with code examples. In our discussion, we cover:

1. **Prompt Chaining:** Passing the output of one prompt as the input to the next agent.  
2. **Routing:** Directing a user query to the most appropriate specialized agent.  
3. **Parallelization:** Running multiple agents concurrently to process different parts of a task.  
4. **Orchestrator‑Workers:** Using an orchestrator agent to delegate subtasks to worker agents and then aggregate results.  
5. **Evaluator‑Optimizer:** Iteratively refining outputs by evaluating and then optimizing results.

The Anthropic research on building effective agents [citeturn2search13] outlines these patterns; AutoGen’s flexible, asynchronous, and multi‑agent architecture makes it possible to implement all five.

---

## 1. Introduction

Modern AI systems increasingly rely on agentic design patterns to solve complex tasks by decomposing work into multiple stages, routing queries to specialized agents, running agents in parallel, orchestrating subtasks, and iteratively optimizing results. In this paper, we demonstrate that AutoGen 0.4.7+ can implement all five of the following Anthropic design patterns:
  
1. **Prompt Chaining**  
2. **Routing**  
3. **Parallelization**  
4. **Orchestrator‑Workers**  
5. **Evaluator‑Optimizer**

We provide a brief explanation and a code example for each design pattern using AutoGen.

---

## 2. Background

AutoGen is an open‑source programming framework that supports building multi‑agent AI applications. Its recent 0.4.7+ update introduces an asynchronous, event‑driven architecture with powerful multi‑agent orchestration, flexible team configurations (such as RoundRobinGroupChat and SelectorGroupChat), and built‑in support for tool integration and state management. These features naturally lend themselves to implementing the Anthropic design patterns described in [Anthropic’s Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) [citeturn2search13].

---

## 3. Implementing Anthropic Design Patterns with AutoGen

### 3.1. Workflow: Prompt Chaining

**Concept:** The output of one agent is used as the input prompt for the next.  
**Example:** A planner agent breaks a task into steps; then each step is fed sequentially to a worker agent.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Shared model client
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Planner agent decomposes the task
planner = AssistantAgent(
    name="planner",
    system_message="Decompose the following task into clear, sequential steps. Separate each step by a newline.",
    model_client=model_client,
)

# Worker agent processes individual steps
worker = AssistantAgent(
    name="worker",
    system_message="Execute the given step and provide a concise result.",
    model_client=model_client,
)

async def prompt_chaining_flow(task: str, cancellation_token: CancellationToken) -> None:
    # Planner decomposes the task.
    planning_response = await planner.on_messages([{"content": task, "source": "user"}], cancellation_token)
    steps = [step.strip() for step in planning_response.chat_message.content.split("\n") if step.strip()]
    print("Planned Steps:")
    for step in steps:
        print(f"- {step}")

    # Chain each step to the worker.
    for step in steps:
        response = await worker.on_messages([{"content": step, "source": "planner"}], cancellation_token)
        print(f"Result for '{step}': {response.chat_message.content.strip()}")

asyncio.run(prompt_chaining_flow("Analyze current AI trends and summarize them.", CancellationToken()))
```

### 3.2. Workflow: Routing

**Concept:** A dedicated router agent examines a user query and directs it to the appropriate specialized agent (e.g., math vs. general).  
**Example:** A router agent classifies a query as "MATH" or "GENERAL" and forwards the query accordingly.

```python
import os
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Initialize model client
model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Define specialized agents
math_agent = AssistantAgent(
    name="math_agent",
    system_message="You are an expert in mathematics. Answer math queries step-by-step.",
    model_client=model_client,
)

general_agent = AssistantAgent(
    name="general_agent",
    system_message="You are a general-purpose assistant. Answer everyday questions concisely.",
    model_client=model_client,
)

# Define router agent
router_agent = AssistantAgent(
    name="router_agent",
    system_message=(
        "Classify the following query. If it relates to mathematics, reply 'MATH'. "
        "Otherwise, reply 'GENERAL'. Only output one word."
    ),
    model_client=model_client,
)

async def routing_flow(query: str, cancellation_token: CancellationToken) -> None:
    # Get classification from router.
    router_response = await router_agent.on_messages([{"content": query, "source": "user"}], cancellation_token)
    decision = router_response.chat_message.content.strip().upper()
    print(f"Router Decision: {decision}")

    # Route query to the selected agent.
    target_agent = math_agent if "MATH" in decision else general_agent
    response = await target_agent.on_messages([{"content": query, "source": "router_agent"}], cancellation_token)
    print(f"Response: {response.chat_message.content.strip()}")

asyncio.run(routing_flow("Calculate the derivative of x^2.", CancellationToken()))
```

### 3.3. Workflow: Parallelization

**Concept:** Multiple agents process parts of a task concurrently.  
**Example:** Splitting a task into sub-queries and processing them in parallel.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Two worker agents for parallel execution.
worker1 = AssistantAgent(
    name="worker1",
    system_message="Process part 1 of the task.",
    model_client=model_client,
)
worker2 = AssistantAgent(
    name="worker2",
    system_message="Process part 2 of the task.",
    model_client=model_client,
)

async def parallel_flow(query1: str, query2: str, cancellation_token: CancellationToken) -> None:
    # Run both queries in parallel.
    task1 = worker1.on_messages([{"content": query1, "source": "user"}], cancellation_token)
    task2 = worker2.on_messages([{"content": query2, "source": "user"}], cancellation_token)
    responses = await asyncio.gather(task1, task2)
    print("Worker1 Response:", responses[0].chat_message.content.strip())
    print("Worker2 Response:", responses[1].chat_message.content.strip())

asyncio.run(parallel_flow("Summarize recent trends in AI ethics.", "Summarize recent trends in AI regulation.", CancellationToken()))
```

### 3.4. Workflow: Orchestrator‑Workers

**Concept:** An orchestrator agent delegates subtasks to multiple worker agents and then aggregates the results.  
**Example:** A planner/orchestrator splits a task into subtasks, dispatches them to workers, and then aggregates their outputs via a verifier.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Define orchestrator and worker agents.
orchestrator = AssistantAgent(
    name="orchestrator",
    system_message="Split the task into subtasks and aggregate worker outputs.",
    model_client=model_client,
)

worker_a = AssistantAgent(
    name="worker_a",
    system_message="Handle subtask A.",
    model_client=model_client,
)

worker_b = AssistantAgent(
    name="worker_b",
    system_message="Handle subtask B.",
    model_client=model_client,
)

async def orchestrator_workers_flow(task: str, cancellation_token: CancellationToken) -> None:
    # Orchestrator decomposes task into two subtasks.
    orchestrator_response = await orchestrator.on_messages(
        [{"content": task, "source": "user"}], cancellation_token
    )
    subtasks = orchestrator_response.chat_message.content.split("\n")
    subtask_a = subtasks[0].strip() if subtasks else "Subtask A"
    subtask_b = subtasks[1].strip() if len(subtasks) > 1 else "Subtask B"
    # Process subtasks in parallel.
    result_a, result_b = await asyncio.gather(
        worker_a.on_messages([{"content": subtask_a, "source": "orchestrator"}], cancellation_token),
        worker_b.on_messages([{"content": subtask_b, "source": "orchestrator"}], cancellation_token)
    )
    aggregated_input = f"{result_a.chat_message.content}\n{result_b.chat_message.content}"
    # Use orchestrator to aggregate.
    aggregation_response = await orchestrator.on_messages(
        [{"content": aggregated_input, "source": "workers"}], cancellation_token
    )
    print("Final Aggregated Output:", aggregation_response.chat_message.content.strip())

asyncio.run(orchestrator_workers_flow("Analyze the impact of AI on healthcare and finance.", CancellationToken()))
```

### 3.5. Workflow: Evaluator‑Optimizer

**Concept:** One agent evaluates the outputs from another agent (or agents), and an optimizer agent refines the results.  
**Example:** A candidate solution is generated, then an evaluator assesses it, and finally an optimizer revises it for improvement.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(model="gpt-4o", api_key="your_api_key_here")

# Candidate generator agent
candidate_agent = AssistantAgent(
    name="candidate_agent",
    system_message="Generate a draft solution for the given task.",
    model_client=model_client,
)

# Evaluator agent assesses the draft.
evaluator_agent = AssistantAgent(
    name="evaluator_agent",
    system_message="Evaluate the following solution and provide constructive feedback.",
    model_client=model_client,
)

# Optimizer agent refines the solution.
optimizer_agent = AssistantAgent(
    name="optimizer_agent",
    system_message="Optimize the solution based on the evaluator's feedback. Provide the improved version.",
    model_client=model_client,
)

async def evaluator_optimizer_flow(task: str, cancellation_token: CancellationToken) -> None:
    # Step 1: Candidate generation.
    candidate_response = await candidate_agent.on_messages([{"content": task, "source": "user"}], cancellation_token)
    candidate_solution = candidate_response.chat_message.content.strip()
    print("Candidate Solution:", candidate_solution)

    # Step 2: Evaluation.
    evaluation_response = await evaluator_agent.on_messages([{"content": candidate_solution, "source": "candidate_agent"}], cancellation_token)
    feedback = evaluation_response.chat_message.content.strip()
    print("Evaluator Feedback:", feedback)

    # Step 3: Optimization.
    optimizer_input = f"Candidate Solution: {candidate_solution}\nFeedback: {feedback}"
    optimized_response = await optimizer_agent.on_messages([{"content": optimizer_input, "source": "evaluator_agent"}], cancellation_token)
    optimized_solution = optimized_response.chat_message.content.strip()
    print("Optimized Solution:", optimized_solution)

asyncio.run(evaluator_optimizer_flow("Draft a proposal to reduce energy consumption in data centers.", CancellationToken()))
```

---

## 4. Conclusion

AutoGen 0.4.7+ is a highly flexible framework that supports all five of the Anthropic agentic design patterns—prompt chaining, routing, parallelization, orchestrator‑workers, and evaluator‑optimizer. By leveraging its asynchronous, event‑driven architecture and multi‑agent orchestration capabilities, developers can design complex workflows that distribute tasks among specialized agents, aggregate results, and iteratively refine outputs. The code examples provided above serve as a foundation that you can expand upon to build sophisticated agentic AI systems for a variety of applications.

Each pattern has its unique strengths:
- **Prompt chaining** enables sequential task processing.
- **Routing** ensures queries are directed to the most appropriate agent.
- **Parallelization** accelerates processing by running agents concurrently.
- **Orchestrator‑workers** allow coordinated task delegation and aggregation.
- **Evaluator‑optimizer** facilitates iterative improvement of solutions.

Together, these patterns illustrate how AutoGen 0.4.7+ can be employed to build next‑generation AI applications that are both robust and scalable.

---

 [citeturn2search13]  


