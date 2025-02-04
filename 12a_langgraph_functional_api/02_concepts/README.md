# Functional API¶

https://langchain-ai.github.io/langgraph/concepts/functional_api/

The Functional API allows you to add LangGraph's key features -- persistence, memory, human-in-the-loop, and streaming — to your applications with minimal changes to your existing code. 

It is designed to integrate these features into existing code that may use standard language primitives for branching and control flow, such as if statements, for loops, and function calls. Unlike many data orchestration frameworks that require restructuring code into an explicit pipeline or DAG, the Functional API allows you to incorporate these capabilities without enforcing a rigid execution model.

## Action Plan

Here we will cover LangGraph Key Features including:

- Overview
- Example
- Entrypoint
    - Injectable Parameters
    - Executing
    - Resuming
    - State Management
    - entrypoint.final
- Task
    - Execution
    - When to use a task
- Serialization
- Determinism
- Idempotency
- Functional API vs. Graph API
- Common Pitfalls
- Handling side effects
- Non-deterministic control flow
- Patterns
    - Parallel execution
    - Calling subgraphs
    - Calling other entrypoints

After completing above we will be learning AI Workflows and AI Agents Design patterns by implementing solutions that create some value in industry. Finally we will look into deploying AI Agents and elements to make them ready for production.