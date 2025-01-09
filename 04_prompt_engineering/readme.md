# Prompt Engineering for AI Agents

**We will start with [Learn Prompting](https://learnprompting.org/docs/introduction) and then moving to the [Prompt Engineering Guide](https://www.promptingguide.ai/) as your skills and knowledge evolve.**

## Basic Learning Path

1. [Prompt Engineering](https://learnprompting.org/docs/basics/prompt_engineering)
2. [Instruction prompting](https://learnprompting.org/docs/basics/instructions)
3. [Assigning Roles](https://learnprompting.org/docs/basics/roles)
4. [Shot-Based Prompting](https://learnprompting.org/docs/basics/few_shot)
5. [Parts of a Prompt: Understanding the Key Elements](https://learnprompting.org/docs/basics/prompt_structure)
6. [How to Create Effective Prompts: Essential Tips and Best Practices](https://learnprompting.org/docs/basics/ai_prompt_tips)
7. [Combining Prompting Techniques](https://learnprompting.org/docs/basics/combining_techniques)
8. [Chatbots vs. LLMs](https://learnprompting.org/docs/basics/chatbot_basics)
9. [Priming Prompt](https://learnprompting.org/docs/basics/priming_prompt)
10. [Limitations of LLMs](https://learnprompting.org/docs/basics/pitfalls)

## Intermediate Learning Path

1. [Chain-of-Thought Prompting](https://learnprompting.org/docs/intermediate/chain_of_thought)
2. [Zero-Shot Chain-of-Thought](https://learnprompting.org/docs/intermediate/zero_shot_cot)
3. [Self-Consistency](https://learnprompting.org/docs/intermediate/self_consistency)
4. [Generated Knowledge](https://learnprompting.org/docs/intermediate/generated_knowledge)
5. [Least-to-Most Prompting](https://learnprompting.org/docs/intermediate/least_to_most)
6. [Revisiting Roles](https://learnprompting.org/docs/intermediate/revisiting_roles)
7. [LLM Settings](https://learnprompting.org/docs/intermediate/configuration_hyperparameters)

## Advanced Learning Path

1. [Zero-Shot Prompting Techniques](https://learnprompting.org/docs/advanced/zero_shot/introduction): [Emotion Prompting](https://learnprompting.org/docs/advanced/zero_shot/emotion_prompting), [Re-reading (RE2)](https://learnprompting.org/docs/advanced/zero_shot/re_reading), [Rephrase and Respond (RaR)](https://learnprompting.org/docs/advanced/zero_shot/re_reading), [Role Prompting](https://learnprompting.org/docs/advanced/zero_shot/role_prompting), [System 2 Attention (S2A)](https://learnprompting.org/docs/advanced/zero_shot/s2a), and [SimToM](https://learnprompting.org/docs/advanced/zero_shot/simtom)
2. [Few-Shot Prompting Techniques](https://learnprompting.org/docs/advanced/few_shot/introduction): [Self-Ask Prompting](https://learnprompting.org/docs/advanced/few_shot/self_ask), [Self-Generated In-Context Learning (SG-ICL)](https://learnprompting.org/docs/advanced/few_shot/self_generated_icl), [K-Nearest Neighbor (KNN) Prompting](https://learnprompting.org/docs/advanced/few_shot/k_nearest_neighbor_knn), [Vote-K Prompting](https://learnprompting.org/docs/advanced/few_shot/vote-k), [Prompt Mining](https://learnprompting.org/docs/advanced/few_shot/prompt_mining)
3. [Thought Generation Techniques](https://learnprompting.org/docs/advanced/thought_generation/introduction)
4. [Ensembling Prompting Techniques](https://learnprompting.org/docs/advanced/ensembling/introduction): [Mixture of Reasoning Experts (MoRE)](https://learnprompting.org/docs/advanced/ensembling/mixture_of_reasoning_experts_more), [Consistency-based Self-adaptive Prompting (COSP)](https://learnprompting.org/docs/advanced/ensembling/consistency_based_self_adaptive_prompting), [Max Mutual Information (MMI) Method](https://learnprompting.org/docs/advanced/ensembling/max_mutual_information_method), [DiVeRSe (Diverse Verifier on Reasoning Step)](https://learnprompting.org/docs/advanced/ensembling/diverse_verifier_on_reasoning_step), [Prompt Paraphrasing](https://learnprompting.org/docs/advanced/ensembling/prompt_paraphrasing), [Universal Self-Adaptive Prompting (USP)](https://learnprompting.org/docs/advanced/ensembling/universal_self_adaptive_prompting), [Universal Self-Consistency](https://learnprompting.org/docs/advanced/ensembling/universal_self_consistency), [Multi-Chain Reasoning (MCR)](https://learnprompting.org/docs/advanced/ensembling/multi-chain-reasoning)

#### Note for Chain-of-Thought Prompting:

OpenAI's o1 model represents a significant advancement in AI reasoning capabilities, particularly when compared to earlier models like GPT-4o. Here's a detailed comparison focusing on the application of Chain-of-Thought (CoT) prompting:

**Chain-of-Thought Prompting with GPT-4o:**

- **Explicit Prompting Required:** To engage in step-by-step reasoning, users must explicitly instruct GPT-4o to "think step by step" or "show your reasoning." Without such prompts, the model may provide direct answers without detailed explanations.

- **Performance in Complex Tasks:** While capable, GPT-4o's effectiveness in complex reasoning tasks is limited. For instance, it solved only 13% of problems on the International Mathematics Olympiad (IMO) qualifying exam.

**o1's Built-in Reasoning Capabilities:**

- **Internal Chain-of-Thought Processing:** o1 is designed to internally process a chain of thought before responding, eliminating the need for explicit CoT prompts. This design allows o1 to handle complex problems more effectively.

- **Enhanced Performance:** o1 significantly outperforms GPT-4o in complex reasoning tasks. It achieved an 83% success rate on the IMO qualifying exam and ranked in the 89th percentile in Codeforces coding competitions.

- **Reinforcement Learning Integration:** o1's training incorporated reinforcement learning, enabling it to refine its reasoning processes and adapt strategies for problem-solving.

**Key Differences:**

- **User Interaction:** With GPT-4o, users must prompt the model to engage in detailed reasoning. In contrast, o1 autonomously employs internal reasoning, streamlining user interaction.

- **Response Time and Cost:** o1's internal reasoning process requires more computational resources, leading to longer response times and higher costs compared to GPT-4o.

- **Accuracy and Reliability:** o1's built-in reasoning reduces the likelihood of errors and hallucinations, making it more reliable for complex tasks.

**Considerations for Use:**

- **Task Complexity:** For straightforward tasks, GPT-4o may suffice. However, for complex problem-solving in areas like mathematics, coding, and scientific reasoning, o1's advanced capabilities are advantageous.

- **Resource Allocation:** Due to o1's higher computational demands and associated costs, it's essential to assess whether its enhanced reasoning aligns with your project's requirements and budget.

In summary, while GPT-4o can perform chain-of-thought reasoning when explicitly prompted, o1 inherently integrates this capability, offering superior performance in complex reasoning tasks. This integration simplifies user interaction and enhances accuracy, albeit with increased computational requirements.

 

 

## Advanced Papers

Techniques for prompting LLMs in more sophisticated ways began to take off in 2022. They coalesced in moves toward agentic AI early this year. Foundational examples of this body of work include:

1. [Chain of Thought prompting](https://arxiv.org/abs/2201.11903), which asks LLMs to think step by step
2. [Self-consistency](https://arxiv.org/abs/2203.11171), which prompts a model to generate several responses and pick the one that’s most consistent with the others
3. [ReAct](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), which interleaves reasoning and action steps to accomplish a goal
4. [Self-Refine](https://arxiv.org/abs/2303.17651), which enables an agent to reflect on its own output
5. [Reflexion](https://arxiv.org/abs/2303.11366), which enables a model to act, evaluate, reflect, and repeat.
6. [Test-time compute](https://arxiv.org/abs/2408.03314), which increases the amount of processing power allotted to inference

Reference:

https://www.deeplearning.ai/the-batch/issue-281/


## For AI Agents

[What is prompt engineering and why it matters for AI Agents](https://medium.com/@alvaro_72265/what-is-prompt-engineering-and-why-it-matters-for-ai-agents-0c1537d64b14)

