# Agentic Patterns using CrewAI

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

    On Windows use crewenv\Scripts\activate


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

## Implementing a Basic Flow with Prompt Chaining

We start by building a simple CrewAI Flow that uses prompt chaining. In this example, the flow will first generate a topic and then use that topic to generate an outline.

```python

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

```

In this flow, the @start() decorator marks the beginning, and the @listen() decorator makes the second method wait for the output of the first method.

## Adding Routing for Conditional Task Execution

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

## Parallelization and Aggregation with the or_ Decorator

Sometimes you want to run several subtasks in parallel and aggregate their outputs. For instance, you might ask the model for multiple outlines and then select or merge them. CrewAI provides the or_ helper to trigger a listener when any (or all, using and_) tasks finish.

```python

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

```

This flow starts two tasks in parallel and then uses or_ so that as soon as one finishes the aggregator runs.

## Orchestrator-Workers: Dynamically Delegating Subtasks

For more complex problems, an orchestrator may dynamically break a task into subtasks and delegate them to “worker” flows. In CrewAI, you can simulate this by creating a flow that calls helper flows or even external Crews.

Below is a simplified example where the orchestrator splits a task (e.g., refining a draft) into multiple iterations:

```python

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

```

This pattern shows how you can use sequential delegation within a Flow to refine outputs over multiple turns.

## Evaluator-Optimizer Pattern for Iterative Refinement

For tasks that benefit from iterative evaluation (for example, when human feedback is available), you can implement a loop where one task generates output and another “evaluates” it. While CrewAI Flows do not yet have a built‑in loop decorator, you can simulate iterative refinement by chaining a generation task with an evaluation task.

```python

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

```

This simple two-step flow represents the evaluator-optimizer pattern by “asking for feedback” and then producing a refined version.

## Combining Patterns in an Autonomous Agent Workflow

Finally, let’s put it all together. In many real-world applications, you might want to start with a simple prompt, then dynamically choose between workflows based on the input, run some tasks in parallel, and finally refine the results. The following example combines multiple patterns to form an autonomous agent workflow for generating and refining a content piece.

```python

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

```python

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


## Additional Agentic Patterns

Below is an extended section for the tutorial that adds two additional agentic patterns: a Meta‑Cognitive Reflection Loop and a Multi‑Agent Collaboration pattern. These patterns complement the ones already described by introducing self‑evaluation and cross‑agent communication. Each example is implemented using CrewAI Flows.

1. Meta‑Cognitive Reflection Loop

In many applications, it’s useful for an agent not only to generate an answer but also to reflect on its reasoning. This “meta‑cognitive” loop involves having the agent review its own response, identify potential issues, and then produce an improved version. Such self‑evaluation can lead to more robust outcomes.

Below is an example CrewAI Flow that demonstrates a meta‑cognitive reflection loop. In this flow, the agent first generates a draft, then “reflects” on it, and finally produces a refined answer.

```python

from crewai.flow.flow import Flow, start, listen
from litellm import completion

class MetaCognitiveFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_initial_draft(self):
        # The agent generates an initial draft on a given topic.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Draft a brief summary on the benefits of renewable energy."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        print("Initial Draft:")
        print(draft)
        return draft

    @listen(generate_initial_draft)
    def reflect_on_draft(self, draft):
        # The agent reflects on the draft and provides constructive feedback.
        reflection_prompt = (
            f"Review the following summary and point out any logical gaps, unclear points, or areas for improvement:\n\n{draft}"
        )
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": reflection_prompt}]
        )
        feedback = response["choices"][0]["message"]["content"].strip()
        print("Reflection Feedback:")
        print(feedback)
        # Save the feedback for the next step.
        self.state["feedback"] = feedback
        return feedback

    @listen(reflect_on_draft)
    def refine_draft(self, draft):
        # The agent uses its own feedback to refine the initial draft.
        feedback = self.state.get("feedback", "")
        refine_prompt = (
            f"Here is the initial summary:\n{draft}\n\nAnd here is some feedback:\n{feedback}\n\n"
            "Revise the summary to address the feedback and improve clarity and accuracy."
        )
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": refine_prompt}]
        )
        final_draft = response["choices"][0]["message"]["content"].strip()
        print("Refined Draft:")
        print(final_draft)
        return final_draft

if __name__ == "__main__":
    flow = MetaCognitiveFlow()
    final_output = flow.kickoff()
    print("Final Output:")
    print(final_output)

```

Explanation:
	•	The flow starts by drafting a summary.
	•	Next, the reflection step uses a prompt to ask the model to critique its own work.
	•	Finally, the initial draft and the feedback are combined to create a refined summary. This loop helps the agent self‑evaluate and improve iteratively.

2. Multi‑Agent Collaboration

In more complex tasks, different “agents” with specialized roles can collaborate to achieve a final result. For instance, one agent might focus on content generation while another reviews for style or technical correctness. The following example demonstrates a multi‑agent collaboration pattern using CrewAI Flows. Here, two “sub‑agents” generate distinct parts of a document, and then a final aggregation step synthesizes their outputs.

```python

from crewai.flow.flow import Flow, start, listen, or_
from litellm import completion

class MultiAgentCollaborationFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_introduction(self):
        # Agent A generates the introduction section.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a concise introduction for an article on AI ethics."}]
        )
        introduction = response["choices"][0]["message"]["content"].strip()
        print("Introduction Generated:")
        print(introduction)
        return introduction

    @start()
    def generate_conclusion(self):
        # Agent B generates the conclusion section.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a compelling conclusion for an article on AI ethics."}]
        )
        conclusion = response["choices"][0]["message"]["content"].strip()
        print("Conclusion Generated:")
        print(conclusion)
        return conclusion

    @listen(or_(generate_introduction, generate_conclusion))
    def synthesize_article(self, content):
        # The aggregator waits for both sections to be ready.
        # Here, for simplicity, we assume the first finished call triggers synthesis.
        # In practice, you might wait for both using more advanced state management.
        synthesis_prompt = (
            f"Given the following content from different sections of an article:\n{content}\n"
            "Combine and refine them into a coherent article section."
        )
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": synthesis_prompt}]
        )
        final_article = response["choices"][0]["message"]["content"].strip()
        print("Synthesized Article Section:")
        print(final_article)
        return final_article

if __name__ == "__main__":
    flow = MultiAgentCollaborationFlow()
    final_article = flow.kickoff()
    print("Final Article Section:")
    print(final_article)

```

Explanation:
	•	Two agents (or tasks) are started in parallel: one generates an introduction, and the other a conclusion for an AI ethics article.
	•	The or_ helper is used to trigger a synthesis step as soon as one section is complete. (In a production scenario, you may prefer to wait until both parts are ready, or you can merge their outputs in a state‑driven manner.)
	•	The synthesis step combines the generated parts and produces a coherent output, demonstrating how different agent roles can collaborate.

Conclusion

By incorporating these additional patterns—a Meta‑Cognitive Reflection Loop for self‑evaluation and Multi‑Agent Collaboration for distributed task handling—you can further enhance the robustness and flexibility of your CrewAI Flows. These examples illustrate how to modularize tasks and bring together the strengths of different approaches in your AI agent workflows.



## Advanced Agentic Patterns


Below are a couple of advanced agentic patterns that can further extend your toolkit when building intelligent workflows. In addition to the patterns we’ve already covered (prompt chaining, routing, parallelization, orchestrator‑workers, evaluator‑optimizer, meta‑cognitive reflection, and multi‑agent collaboration), consider the following two:

	1.	Retrieval Augmentation Loop
This pattern enables the agent to actively seek out external, up‑to‑date information during its task. Rather than relying solely on its built‑in knowledge, the agent generates a query, uses a retrieval mechanism (for example, a search API or database call), and then incorporates the retrieved information into its final output. This is especially useful in domains where the world is changing rapidly (news, market data, technical developments, etc.) and can help mitigate knowledge cutoff issues.
Below is an example CrewAI Flow code that implements a retrieval augmentation loop. In this example, the agent generates a query, retrieves simulated data (via a helper function), and then summarizes that data.

```python

from crewai.flow.flow import Flow, start, listen
from litellm import completion

# Dummy retrieval function (in a real implementation, connect to an API or database)
def retrieve_information(query):
    # Simulate retrieval by returning a placeholder summary
    return f"Retrieved information relevant to: {query}"

class RetrievalAugmentationFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_query(self):
        # Ask the LLM to formulate a query for additional information.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a query to retrieve current data on renewable energy adoption trends."}]
        )
        query = response["choices"][0]["message"]["content"].strip()
        print("Generated Query:", query)
        return query

    @listen(generate_query)
    def retrieve_data(self, query):
        # Retrieve external data using the generated query.
        data = retrieve_information(query)
        print("Retrieved Data:", data)
        return data

    @listen(retrieve_data)
    def summarize(self, data):
        # Summarize the retrieved data.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Summarize the following information concisely: {data}"}]
        )
        summary = response["choices"][0]["message"]["content"].strip()
        print("Summary:", summary)
        return summary

if __name__ == "__main__":
    flow = RetrievalAugmentationFlow()
    final_summary = flow.kickoff()
    print("Final Summary:", final_summary)

```

	2.	Confidence-Based Escalation
In some applications, it’s valuable for the agent to evaluate the quality or confidence of its own output and then decide whether to proceed, refine the result, or trigger a fallback (such as human review or an alternative strategy). In this pattern, after generating an answer, the agent asks itself to rate the response (using its own internal judgment or a secondary LLM call) and then uses that rating to determine if additional processing is required.

Below is an example CrewAI Flow that demonstrates a confidence-based escalation loop. Here, the agent generates an explanation, assesses its own confidence on a scale, and then decides if it should escalate the output for fallback processing.

```python

from crewai.flow.flow import Flow, start, listen
from litellm import completion

class ConfidenceEscalationFlow(Flow):
    model = "gpt-4o-mini"

    @start()
    def generate_response(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a short explanation of quantum computing."}]
        )
        output = response["choices"][0]["message"]["content"].strip()
        print("Initial Response:", output)
        return output

    @listen(generate_response)
    def assess_confidence(self, output):
        # Ask the model to rate its own confidence in the generated response.
        prompt = f"On a scale of 1 to 10, how confident are you in the quality of the following explanation?\n{output}"
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        rating_str = response["choices"][0]["message"]["content"].strip()
        try:
            rating = int(rating_str)
        except Exception:
            rating = 5  # Default if the response cannot be parsed
        print("Confidence Rating:", rating)
        self.state["confidence"] = rating
        return rating

    @listen(assess_confidence)
    def escalate_if_needed(self, rating):
        # If the confidence is below a certain threshold, trigger fallback logic.
        if rating < 7:
            print("Confidence too low. Escalating to fallback process.")
            # Insert fallback logic here (e.g., a refined prompt, human notification, etc.)
            return "Fallback: Human review required."
        else:
            print("Confidence adequate. Proceeding with the output.")
            return "Output accepted."

if __name__ == "__main__":
    flow = ConfidenceEscalationFlow()
    result = flow.kickoff()
    print("Final Outcome:", result)

```

Additional Considerations

Beyond these patterns, it’s also important to consider:
	•	Hierarchical Task Decomposition:
While similar to orchestrator‑workers, a hierarchical approach recursively decomposes a complex task into multiple levels of subtasks. This can be useful in multi‑step projects where tasks can be nested.

	•	Dynamic Memory and Context Updating:
Agents that incorporate an evolving memory (or episodic memory) can maintain context over long interactions or across multiple sessions. This pattern is crucial for applications like dialogue systems or long‑term planning.

	•	Fallback and Safe-Exit Patterns:
Designing agents with clear escape hatches—when they detect high uncertainty, anomalous behavior, or potential risks—ensures that they can default to a safe mode or request human intervention.

While the two examples above (retrieval augmentation and confidence-based escalation) are concrete additions, these additional considerations often blend into your overall design strategy. Their implementation in CrewAI Flows would follow similar principles: generate an output, assess it (perhaps via an extra LLM call or an external check), and then branch or iterate based on the result.

Conclusion

When building advanced agentic systems, being aware of additional patterns like retrieval augmentation, confidence-based escalation, hierarchical task decomposition, dynamic memory updating, and safe‐exit strategies can significantly improve robustness and adaptability. These patterns, when implemented using the modular CrewAI Flows framework, allow you to craft workflows that are not only powerful but also resilient in real‑world applications.

