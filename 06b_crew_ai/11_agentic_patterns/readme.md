Below is a comprehensive, step‐by‐step tutorial that shows how to implement several agentic patterns using the latest version of CrewAI’s newly released Flows functionality. In this guide we’ll cover how to build workflows that mirror the Anthropic “Building Effective Agents” patterns—such as prompt chaining, routing, parallelization, orchestrator‐workers, evaluator‐optimizer, and autonomous agents—using CrewAI’s event‑driven Flow framework.

Table of Contents

	1.	Introduction
	2.	Prerequisites and Setup
	3.	Overview of Agentic Patterns
	4.	Implementing a Basic Flow with Prompt Chaining
	5.	Adding Routing for Conditional Task Execution
	6.	Parallelization and Aggregation with the or_ Decorator
	7.	Orchestrator-Workers: Dynamically Delegating Subtasks
	8.	Evaluator-Optimizer Pattern for Iterative Refinement
	9.	Combining Patterns in an Autonomous Agent Workflow
	10.	Conclusion and Next Steps

Introduction

CrewAI’s new Flows feature provides an event‑driven, state‑managed framework to easily build and orchestrate complex AI workflows. Instead of writing monolithic LLM calls or relying on hidden abstractions, you can now explicitly design the flow of tasks—such as chaining prompts, routing based on output, running tasks in parallel, and orchestrating dynamic delegation—much like the agentic patterns described by Anthropic.

In this tutorial we implement these patterns step by step using CrewAI Flows. We assume you are familiar with Python and basic LLM API usage.

Prerequisites and Setup
	1.	Install the Latest CrewAI:
Ensure you have CrewAI (and the tools package if needed) installed. You can install via pip:

    pip install crewai crewai[tools] --upgrade


	2.	Environment Setup:

Create and activate a virtual environment:

    uv venv 

Activate with: 

    source .venv/bin/activate

# On Windows use crewenv\Scripts\activate


	3.	API Keys and .env:

If your workflow uses external APIs (for example, an LLM or search tool), set them in a .env file:

OPENAI_API_KEY=your_openai_key_here

OPENAI_MODEL_NAME=gpt-4o-mini

SERPER_API_KEY=your_serper_key_here


	4.	Import CrewAI’s Flow Module:
In your Python code, you’ll import from crewai.flow.flow along with any additional modules (for state management, etc.).

Overview of Agentic Patterns

Before diving into code, let’s briefly review the agentic patterns we’ll implement:

	•	Prompt Chaining: Decompose a task into sequential subtasks (each output feeding the next call).
	•	Routing: Use output classification to direct different follow‑up processes.
	•	Parallelization: Run multiple LLM calls simultaneously (using the or_ helper) and aggregate results.
	•	Orchestrator-Workers: Dynamically break a task into subtasks, delegate to worker calls, and synthesize outputs.
	•	Evaluator-Optimizer: Iterate on an output by having one LLM generate a response and another refine it.
	•	Autonomous Agents: Combine the above in a loop where the agent uses tool feedback and halts based on stopping criteria.

Implementing a Basic Flow with Prompt Chaining

We start by building a simple CrewAI Flow that uses prompt chaining. In this example, the flow will first generate a topic and then use that topic to generate an outline.

from crewai.flow.flow import Flow, start, listen
from litellm import completion  # Replace with your preferred LLM API client

class TopicOutlineFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_topic(self):
        # Prompt the LLM to generate a blog topic.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Generate a creative blog topic for 2025."
            }]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        print(f"Generated Topic: {topic}")
        return topic

    @listen(generate_topic)
    def generate_outline(self, topic):
        # Now chain the output by using the topic in a follow-up prompt.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Based on the topic '{topic}', create a detailed outline for a blog post."
            }]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Generated Outline:")
        print(outline)
        return outline

if __name__ == "__main__":
    flow = TopicOutlineFlow()
    final_outline = flow.kickoff()
    print("Final Output:")
    print(final_outline)

In this flow, the @start() decorator marks the beginning, and the @listen() decorator makes the second method wait for the output of the first method.

Adding Routing for Conditional Task Execution

Next, we implement conditional routing so that the flow can choose different follow‑up steps based on the generated topic’s attributes (for example, if the topic is “tech” versus “lifestyle”).

```python 

from crewai.flow.flow import Flow, start, listen, router
from litellm import completion

class RoutedFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_topic(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a blog topic for 2025."}]
        )
        topic = response["choices"][0]["message"]["content"].strip()
        # For demonstration, add a fake flag to the state.
        self.state["is_tech"] = "tech" in topic.lower()
        print(f"Topic: {topic}")
        return topic

    @router(generate_topic)
    def route_topic(self):
        # Route based on the is_tech flag.
        if self.state.get("is_tech"):
            return "tech_route"
        else:
            return "lifestyle_route"

    @listen("tech_route")
    def generate_tech_outline(self, topic):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Create a detailed tech blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Tech Outline:")
        print(outline)
        return outline

    @listen("lifestyle_route")
    def generate_lifestyle_outline(self, topic):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Create a detailed lifestyle blog outline for: {topic}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        print("Lifestyle Outline:")
        print(outline)
        return outline

if __name__ == "__main__":
    flow = RoutedFlow()
    final_output = flow.kickoff()
    print("Final Output:")
    print(final_output)

```

Here the @router() decorator determines which branch to take. Based on the route label, a corresponding listener method is invoked.

Parallelization and Aggregation with the or_ Decorator

Sometimes you want to run several subtasks in parallel and aggregate their outputs. For instance, you might ask the model for multiple outlines and then select or merge them. CrewAI provides the or_ helper to trigger a listener when any (or all, using and_) tasks finish.

from crewai.flow.flow import Flow, start, listen, or_
from litellm import completion

class ParallelFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_variant_1(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #1."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 1: {variant}")
        return variant

    @start()
    def generate_variant_2(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #2."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 2: {variant}")
        return variant

    @listen(or_(generate_variant_1, generate_variant_2))
    def aggregate_variants(self, variant):
        # For simplicity, print the first variant received.
        print("Aggregated Variant:")
        print(variant)
        return variant

if __name__ == "__main__":
    flow = ParallelFlow()
    final = flow.kickoff()
    print("Final Aggregated Output:")
    print(final)

This flow starts two tasks in parallel and then uses or_ so that as soon as one finishes the aggregator runs.

Orchestrator-Workers: Dynamically Delegating Subtasks

For more complex problems, an orchestrator may dynamically break a task into subtasks and delegate them to “worker” flows. In CrewAI, you can simulate this by creating a flow that calls helper flows or even external Crews.

Below is a simplified example where the orchestrator splits a task (e.g., refining a draft) into multiple iterations:

from crewai.flow.flow import Flow, start, listen
from litellm import completion

class OrchestratorFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def initial_draft(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Draft a short blog post about AI automation."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = draft
        print("Initial Draft:")
        print(draft)
        return draft

    @listen(initial_draft)
    def refine_draft(self, draft):
        # Simulate dynamic task delegation: iterate refinement.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Refine this draft for clarity and style: {draft}"}]
        )
        refined = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = refined
        print("Refined Draft:")
        print(refined)
        return refined

if __name__ == "__main__":
    flow = OrchestratorFlow()
    final_draft = flow.kickoff()
    print("Final Draft:")
    print(final_draft)

This pattern shows how you can use sequential delegation within a Flow to refine outputs over multiple turns.

Evaluator-Optimizer Pattern for Iterative Refinement

For tasks that benefit from iterative evaluation (for example, when human feedback is available), you can implement a loop where one task generates output and another “evaluates” it. While CrewAI Flows do not yet have a built‑in loop decorator, you can simulate iterative refinement by chaining a generation task with an evaluation task.

from crewai.flow.flow import Flow, start, listen
from litellm import completion

class EvaluatorOptimizerFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_response(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a draft summary about the benefits of AI in education."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        print("Initial Draft Summary:")
        print(draft)
        return draft

    @listen(generate_response)
    def evaluate_and_optimize(self, draft):
        # In a real-world scenario, you might get human feedback.
        # Here, we simulate optimization by asking the model for improvements.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Critically evaluate and improve this summary: {draft}"}]
        )
        improved = response["choices"][0]["message"]["content"].strip()
        print("Improved Summary:")
        print(improved)
        return improved

if __name__ == "__main__":
    flow = EvaluatorOptimizerFlow()
    final_summary = flow.kickoff()
    print("Final Summary:")
    print(final_summary)

This simple two-step flow represents the evaluator-optimizer pattern by “asking for feedback” and then producing a refined version.

Combining Patterns in an Autonomous Agent Workflow

Finally, let’s put it all together. In many real-world applications, you might want to start with a simple prompt, then dynamically choose between workflows based on the input, run some tasks in parallel, and finally refine the results. The following example combines multiple patterns to form an autonomous agent workflow for generating and refining a content piece.

from crewai.flow.flow import Flow, start, listen, router, or_
from litellm import completion

class AutonomousAgentFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def initial_prompt(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative idea for an AI article."}]
        )
        idea = response["choices"][0]["message"]["content"].strip()
        self.state["idea"] = idea
        # Set a flag for further branching; for example, if the idea includes the word "technology"
        self.state["is_tech"] = "technology" in idea.lower()
        print("Initial Idea:")
        print(idea)
        return idea

    @router(initial_prompt)
    def choose_flow(self):
        # Route the flow based on the idea category.
        if self.state.get("is_tech"):
            return "tech_flow"
        else:
            return "general_flow"

    @listen("tech_flow")
    def tech_content(self, idea):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Develop a detailed outline for an AI article focused on technology: {idea}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        return outline

    @listen("general_flow")
    def general_content(self, idea):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Develop a detailed outline for an AI article: {idea}"}]
        )
        outline = response["choices"][0]["message"]["content"].strip()
        return outline

    @listen(or_(tech_content, general_content))
    def final_optimization(self, outline):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Improve and polish this article outline: {outline}"}]
        )
        final_outline = response["choices"][0]["message"]["content"].strip()
        print("Final Optimized Outline:")
        print(final_outline)
        return final_outline

if __name__ == "__main__":
    flow = AutonomousAgentFlow()
    final_output = flow.kickoff()
    print("Final Autonomous Agent Output:")
    print(final_output)

In this workflow:
	•	The initial prompt creates the idea.
	•	The router selects which branch to follow based on a condition.
	•	Depending on the branch, either a tech‑focused or a general outline is generated.
	•	Finally, the or_ decorator aggregates the output and a final optimization step refines the outline.

Conclusion and Next Steps

This tutorial has demonstrated how to implement multiple agentic patterns—prompt chaining, routing, parallelization, orchestrator‑workers, and evaluator‑optimizer—using the new CrewAI Flows functionality. By breaking down a complex task into a modular, event‑driven workflow, you can build robust, autonomous AI applications.

Next Steps:
	•	Experiment with state management using structured models (e.g., Pydantic) for larger workflows.
	•	Extend these examples by integrating external tools (e.g., search APIs or databases) using CrewAI’s tools framework.
	•	Explore CrewAI’s visualization features (e.g., using the plot() method) to inspect your flow’s DAG.

By iterating on these patterns and combining them as needed, you can tailor your AI agent workflows to your application’s requirements.

Happy coding, and enjoy building with CrewAI Flows!

Sources used for this tutorial include CrewAI documentation and community tutorials on CrewAI Flows.
￼
￼