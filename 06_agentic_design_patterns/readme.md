# Agentic Design Patterns

[Building effective agents By Anthropic](https://www.anthropic.com/research/building-effective-agents)

[Watch: Tips for building AI agents](https://www.youtube.com/watch?v=LP5OCa20Zpg)

[How to Build AI Agents: Insights from Anthropic](https://medium.com/@muslumyildiz17/how-to-build-ai-agents-insights-from-anthropic-25e9433853be)

[An Analysis of Anthropic's Guide to Building Effective Agents](https://www.agentsdecoded.com/p/an-analysis-of-anthropics-guide-to)


Additional Reading:

https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/

Note:

LangGraph has implemented these patterns here:

https://langchain-ai.github.io/langgraph/tutorials/workflows/

We will also implement these patterns using CrewAI 0.100+ and AutoGen 0.4+

Below is a detailed article that explains and analyzes Anthropic’s “Building Effective Agents” guide. I break down the key points from the post, provide commentary on each, and share my perspective on whether I agree or disagree with the recommendations.

Introduction

Anthropic’s guide—published on December 19, 2024—details practical patterns and design choices for developing systems built around large language models (LLMs). It emphasizes that, rather than relying on overly complex frameworks, many successful teams have built agentic systems using simple, composable patterns. The article is structured to help developers choose between simple one-shot LLM calls, structured workflows, or fully autonomous agents, depending on the task at hand. In the following sections, I review and analyze each main point from the guide, explaining the underlying concepts and stating my views on their merits.
￼

What Are Agents?

Anthropic starts by defining “agents” as systems that can either be fully autonomous—dynamically directing their own processes and using tools—or more prescriptive workflows orchestrated through code. They make an important architectural distinction:
	•	Workflows: Systems with predefined code paths that orchestrate LLM calls and tool use.
	•	Agents: Systems in which the LLM actively determines its process and tool usage on the fly.

Analysis

I agree with this distinction. In practice, many applications benefit from the predictability of workflows, while more open-ended or adaptive tasks need the flexible, decision-making capacity of autonomous agents. This framework helps teams assess the complexity they require for a given application.
￼

When (and When Not) to Use Agents

The guide advocates for starting with the simplest solution—often a single LLM call augmented by retrieval or in-context examples—and only escalating to agentic systems if the task demands it. The tradeoffs include increased latency and higher costs when opting for dynamic, multi-turn decision-making.

Analysis

I strongly agree with this “start simple” philosophy. Over-engineering is a common pitfall in AI development, and adding complexity should be justified by demonstrable improvements in performance or flexibility. The emphasis on evaluating whether the tradeoff between cost/latency and performance is worthwhile resonates with best practices in software design.
￼

Using Frameworks

The guide reviews several frameworks (e.g., LangGraph from LangChain, Amazon Bedrock’s AI Agent framework, Rivet, and Vellum) that simplify the construction of agentic systems by handling low-level tasks like LLM calls and tool integration. However, it also cautions that these frameworks can add layers of abstraction, potentially making debugging more challenging and tempting developers to add unnecessary complexity.

Analysis

This is an insightful observation. Frameworks can indeed speed up initial development, but they might obscure the underlying mechanics. I agree with the recommendation to use LLM APIs (or LiteLLM or LangChain) directly at the start—this approach fosters a deeper understanding of the model’s behavior and reduces the risk of hidden bugs. As systems mature, selectively using frameworks with a clear grasp of what they abstract is a prudent strategy.
￼

Building Blocks, Workflows, and Agents

Anthropic breaks down the development process into incremental patterns, from basic building blocks to full agent architectures.

1. The Augmented LLM

Description:
The “augmented LLM” is presented as the fundamental building block, enhanced with capabilities like retrieval, tool use, and memory. This design enables the LLM to generate search queries, decide which tools to call, and determine what information to keep.

Analysis:
Enhancing LLMs with external tools and memory is a robust approach to addressing the limitations of a standalone model. I agree that tailoring these augmentations to the specific use case—and keeping their interfaces simple and well-documented—is critical for reliability and ease of debugging.
￼

2. Workflow: Prompt Chaining

Description:
Prompt chaining decomposes a complex task into sequential subtasks, where each LLM call feeds into the next. This approach allows developers to insert programmatic “gates” or checks to ensure correctness at each step.

Analysis:
Prompt chaining is effective for tasks that naturally break down into discrete stages. By simplifying each step, developers can improve overall accuracy. I agree with this method for cases such as multi-step content generation or translation tasks, where control over intermediate outputs is beneficial.
￼

3. Workflow: Routing

Description:
Routing involves classifying an input to direct it to the appropriate specialized follow-up process. This separation of concerns helps in handling diverse input types with customized prompts.

Analysis:
This workflow is especially useful in contexts such as customer support, where different queries require distinct handling. I agree that routing can optimize performance by avoiding a “one-size-fits-all” prompt; however, it demands an accurate classification mechanism, which can sometimes be challenging. Overall, the approach is well justified.
￼

4. Workflow: Parallelization

Description:
Parallelization leverages multiple simultaneous LLM calls either to handle independent subtasks (sectioning) or to obtain diverse outputs (voting).

Analysis:
The division into sectioning and voting is particularly insightful. Sectioning can drastically reduce processing time for large tasks, while voting helps balance the risk of errors by considering multiple outputs. I agree that these patterns can improve both speed and reliability, although they might increase resource usage.
￼

5. Workflow: Orchestrator-Workers

Description:
In this design, a central “orchestrator” LLM dynamically breaks down a complex task, delegates subtasks to “worker” LLMs, and synthesizes the results.

Analysis:
The orchestrator-workers pattern is a natural extension for tasks with unpredictable subtasks, such as complex coding or research tasks. I agree with this approach since it combines flexibility with division of labor. The key challenge is ensuring that the orchestrator effectively manages the context and aggregates results accurately.
￼

6. Workflow: Evaluator-Optimizer

Description:
Here, one LLM call generates an output while another evaluates and refines it in a loop. This iterative feedback process is analogous to human editing and is useful when there are clear evaluation criteria.

Analysis:
The evaluator-optimizer pattern is a smart strategy for tasks where iterative improvement can lead to significantly better results (e.g., translation, content refinement). I agree with the concept, though I note that the efficiency of the loop depends on the clarity of the evaluation metrics and the responsiveness of the model.
￼

Autonomous Agents

Description:
Moving beyond workflows, the guide defines autonomous agents as systems where the LLM interacts with users to understand a task, plans its approach, and then independently executes the necessary steps—using tools and environmental feedback along the way. These agents can pause to request human feedback when needed and incorporate stopping conditions to prevent runaway processes.

Analysis:
The concept of autonomous agents is compelling, especially as LLMs grow more capable. Their use in open-ended or multi-step tasks is promising, but they come with inherent risks such as compounding errors and higher operational costs. I agree that robust testing (e.g., in sandboxed environments) and well-designed guardrails are essential before deploying such agents in production.
￼

Combining and Customizing Patterns

Anthropic stresses that these patterns are not rigid blueprints but modular tools that can be combined and tailored to fit various use cases. The emphasis is on iterative development—start simple, measure performance, and only add complexity when it demonstrably improves outcomes.

Analysis

This iterative, measurement-driven approach is a cornerstone of good engineering practice. I agree wholeheartedly with this principle, as it encourages developers to remain flexible and only add complexity when the value is clear. It also minimizes the risk of over-engineering, which can lead to maintenance challenges.
￼

Appendices: Agents in Practice

A. Customer Support

Description:
Customer support agents combine conversational interfaces with tool integrations (e.g., accessing customer data or processing refunds). The guide explains that this domain benefits from the dynamic, conversational nature of agents combined with clearly defined success criteria.

Analysis:
The application of agentic systems in customer support is well reasoned. Conversational agents can significantly improve user experience when they have access to contextual data and clear resolution metrics. I agree that a hybrid approach—where the system interacts naturally yet adheres to strict resolution criteria—is ideal.
￼

B. Coding Agents

Description:
In the coding domain, agents can autonomously suggest or implement code changes, guided by automated tests and human review. This application leverages the structured nature of code and the availability of objective evaluation metrics.

Analysis:
The use of agents in coding is promising and reflects current trends in AI-assisted development. I agree that automated testing paired with human oversight creates a balanced approach, allowing agents to propose solutions while mitigating risk through review.
￼

Appendix 2: Prompt Engineering Your Tools

Description:
The guide emphasizes that the design of tools—the interfaces through which agents interact with external systems—is as critical as the overall prompt design. It recommends best practices such as clear documentation, example usage, and testing via workbenches to refine how agents invoke these tools.

Analysis:
I find this section particularly insightful. The success of an agent often hinges on the clarity and reliability of its tool interfaces. Investing effort into making these interfaces intuitive and robust is a best practice that I fully endorse. It echoes the broader engineering principle of designing good human-computer interfaces.
￼

Conclusion

Anthropic’s “Building Effective Agents” guide offers a comprehensive look at designing AI systems that range from simple prompt-based workflows to sophisticated autonomous agents. The key takeaways include:
	1.	Start Simple: Begin with basic LLM calls and only add complexity when needed.
	2.	Use the Right Patterns: Choose from prompt chaining, routing, parallelization, orchestrator-workers, or evaluator-optimizer based on the task.
	3.	Emphasize Transparency: Whether it’s through clear planning steps or well-documented tool interfaces, clarity is essential.
	4.	Iterate and Test: Robust performance comes from measuring outcomes, refining prompts, and ensuring that every abstraction added is justified.

Overall, I agree with the guide’s principles. Its recommendations strike a balance between leveraging powerful LLM capabilities and maintaining control over complexity, a balance that is critical for both reliability and scalability in AI applications.

This detailed analysis of Anthropic’s guide should serve as a comprehensive overview and critical appraisal of the strategies for building effective agents. Each point is well grounded in practical considerations, and while some trade-offs (like the cost of complexity) exist, the emphasis on simplicity and iterative improvement is sound engineering advice.
