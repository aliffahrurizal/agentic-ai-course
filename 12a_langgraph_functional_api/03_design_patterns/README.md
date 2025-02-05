# Design Patterns

Design patterns are essentially tried‐and‑true templates or best practices for solving recurring problems in system design. In classic software engineering, these patterns (like those described in the Gang of Four book) help developers create reliable, maintainable, and scalable systems.

When it comes to AI applications—especially those built on large language models—the term “design patterns” has been adapted to describe common architectural approaches for integrating AI capabilities (such as retrieval, tool use, memory, and multi‑turn reasoning) into applications. 

[Building effective agents By Anthropic](https://www.anthropic.com/research/building-effective-agents)

[LangGraph Implementation design patterns for Building effective agents By Anthropic](https://langchain-ai.github.io/langgraph/tutorials/workflows/)

[Pure Python Implementation of design patterns for Building effective agents By Anthropic](https://www.agentrecipes.com/)

### AI Workflows and AI Agents

![Workflows vs AI Agents](../assets/workflows_vs_agents.png)

**AI Workflows** are systems that follow a predetermined, hard‑coded sequence of steps. The design patterns used in workflows are about orchestrating a series of AI calls and tool integrations in a predictable, repeatable manner. For example, a customer support workflow might use routing to classify queries and then sequentially process them via prompt chaining. In these systems, the sequence and logic are predefined by the developer, which makes them reliable and easier to audit.

**AI Agents**, on the other hand, are designed to have more autonomy. They’re built to dynamically decide their own course of action—essentially “thinking” through a problem by planning, reflecting, and adapting on the fly. While agents may also use the same underlying design patterns (like prompt chaining or routing), they incorporate additional layers that support:

- **Autonomy:** Allowing the agent to choose when and which tools to call without explicit pre‑programmed instructions.
- **Dynamic Planning and Reflection:** Enabling the agent to evaluate its own outputs (using evaluator‑optimizer loops, for instance) and decide whether it needs to adjust its approach.
- **Error Recovery:** Because autonomous decisions can lead to unexpected errors, agents often include additional mechanisms to detect and recover from mistakes.

In short, design patterns in the AI domain serve as templates for constructing both static workflows and dynamic agents. The fundamental building blocks are often similar, but the architecture of an AI agent includes extra layers to enable autonomous, adaptable decision-making compared to the more linear, predetermined nature of AI workflows.

### AI Workflows vs. AI Agents: Are the Design Patterns Different?

Workflows and agents are both approaches to using AI in applications, but they differ fundamentally in how much autonomy the system has.

- **Shared Foundations:** Both AI workflows and AI agents rely on many of the same core design patterns (such as prompt chaining, routing, parallelization, orchestrator‑workers, and evaluator‑optimizer) as building blocks.
- **Key Difference:** The difference is in how these patterns are orchestrated. Workflows use them in a fixed, predetermined manner, resulting in predictable and repeatable behavior. In contrast, agents leverage these patterns as part of a more dynamic and autonomous system—incorporating extra mechanisms for reasoning, self-reflection, and decision‑making.
- **Implication:** For developers, this means that while you might start by building a workflow for a well‑defined task, pushing the boundaries (or “going agentic”) requires additional design considerations to handle unpredictability and ensure that the system can adjust its behavior based on context.

## Action Plan

We will start off by understanding Design Patterns to build AI Workflows and move forward to building blocks and architectures for AI Agents. LangGraph Functional API is a tool to implement these design patterns for solving meaningful problems to create real value.

Review the augmented_llm codebase to understand the basic building blocks for these workflows.

## Combining and customizing these patterns

These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases. The key to success, as with any LLM features, is measuring performance and iterating on implementations. To repeat: you should consider adding complexity only when it demonstrably improves outcomes.

## Summary

**Workflows**  
• **Predefined Process:** Workflows are systems where the sequence of steps is fixed in advance. The code paths, rules, and integration points (such as specific API calls or tool uses) are pre‑designed.  
• **Predictability and Control:** Because each step is clearly defined, workflows are very predictable and easier to audit and debug. They’re ideal for tasks where the procedure doesn’t change much from case to case.  
• **Example:** Many customer support systems use workflows that first classify a query (routing) and then pass it through a series of steps (like auto‑responses, data lookup, and final human review). These are essentially hard‑coded sequences that always follow the same route.

**Agents**  
• **Dynamic Autonomy:** In contrast, agents are designed to decide for themselves what steps to take. They can dynamically plan their own sequence of actions, choose which tools to call, and even decide when to ask for human input.  
• **Flexibility and Adaptability:** This autonomy allows agents to tackle tasks that are less structured or that might require creative problem‑solving. However, this flexibility can also make them less predictable and sometimes more error‑prone.  
• **Example:** Anthropic’s Claude 3.5 Sonnet with its “computer use” feature is an early example of an agent. It doesn’t follow a hard‑coded script; instead, it determines how to navigate a desktop interface to fill forms, book trips, or order food—acting much more like a human would, but with AI reasoning.

**In Summary:**  
• Workflows are like assembly lines: each step is predetermined and consistent, making them reliable and easy to manage.  
• Agents, on the other hand, are more like human workers who assess the situation, plan their own actions, and adapt on the fly. They promise greater flexibility and potential but come with challenges in reliability and predictability.

This distinction is at the heart of current debates in AI design. 

While workflows are useful for well‑defined, routine tasks, true agents—capable of autonomous reasoning and dynamic decision-making—are the next frontier in AI development.  

#### Additional Reading Resources:

[How to Build AI Agents: Insights from Anthropic](https://medium.com/@muslumyildiz17/how-to-build-ai-agents-insights-from-anthropic-25e9433853be)

[An Analysis of Anthropic's Guide to Building Effective Agents](https://www.agentsdecoded.com/p/an-analysis-of-anthropics-guide-to)
