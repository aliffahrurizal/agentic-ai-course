# Workflow: Routing

Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts. Without this workflow, optimizing for one kind of input can hurt performance on other inputs.

https://www.agentrecipes.com/routing

Examples where routing is useful:

- Directing different types of customer service queries (general questions, refund requests, technical support) into different downstream processes, prompts, and tools.
- Routing easy/common questions to smaller models like Gemini 1.5 Flash and hard/unusual questions to more capable models like Gemini-2.0-flash-exp to optimize cost and speed. We will use  gemini-1.5-flash-8b-001 for routing.

