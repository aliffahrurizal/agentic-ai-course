# Evaluator-optimizer
In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop:

## When to use this workflow: 
This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. 

The two signs of good fit are 
- first, that LLM responses can be demonstrably improved when a human articulates their feedback; and
- second, that the LLM can provide such feedback. 

This is analogous to the iterative writing process a human writer might go through when producing a polished document.

[LangGraph Implantation for Evaluator-optimizer](https://langchain-ai.github.io/langgraph/tutorials/workflows/#evaluator-optimizer)

## Examples

### 1. Poem Flow with Evaluator-Optimizer Pattern

```mermaid
flowchart TD
    A[User Input: System Prompt Instructions & Gold Standard] --> F[Task Simulated Personas]
    F --> C[Judge Evaluation]
    C --> D[Prompt Improvement Research]
    D --> E[Aggregate Final Report]

    style A fill:#663399,stroke:#333,stroke-width:2px
    style E fill:#663399,stroke:#333,stroke-width:2px
```

Open poem_flow project in this directory and try it.