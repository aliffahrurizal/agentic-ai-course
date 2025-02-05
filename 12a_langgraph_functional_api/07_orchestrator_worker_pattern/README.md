# Orchestrator-Worker
In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.

**When to use this workflow:**

This workflow is well-suited for complex tasks where you can’t predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task). Whereas it’s topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.

[LangGraph Functional API Orchestrator Worker Implementation](https://langchain-ai.github.io/langgraph/tutorials/workflows/#orchestrator-worker)
[Antropic Theory for Orchestrator Worker Design Pattern ](https://www.anthropic.com/research/building-effective-agents)


**Sectioning vs. Orchestrator-Workers:** 
One is a static decomposition (sectioning) and the other is dynamic (orchestrator-workers).
Think of it like planning a road trip:
- Orchestration is like having a navigator who can change the route based on traffic and conditions
- Sectioning is like splitting the route into equal segments beforehand

**Additional Factors:**
- Task predictability: Sectioning works when you can predict and define the subtasks in advance; orchestrator-workers are used when the task's structure isn't known beforehand.
- Coordination: Dynamic approaches require a central mechanism (the orchestrator) to manage task decomposition and result integration, which adds flexibility but also complexity.
