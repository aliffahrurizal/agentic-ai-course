# Learn Agentic AI

This repo is part of the [Panaversity Certified Agentic and Robotic AI Engineer](https://docs.google.com/document/d/15usu1hkrrRLRjcq_3nCTT-0ljEcgiC44iSdvdqrCprk/edit?usp=sharing) program. It covers AI-201 and AI-202 courses.

![Agentic AI Top Trend](toptrend.webp)

## Watch The NVIDIA CEO Jensen Huang Keynote at CES 2025

[![HR for Agents](hr.jpeg)](https://www.youtube.com/watch?v=k82RwXqZHY8 "NVIDIA CEO Jensen Huang Keynote at CES 2025")


Reference:

https://www.linkedin.com/posts/alexwang2911_aiagents-robotics-technology-activity-7282829390445453314-QLeS

### AI-201: Fundamentals of Agentic AI

Covers Chapters from -01 to 11

**[AI-201 Video Playlist](https://www.youtube.com/playlist?list=PL0vKVrkG4hWpDokw004ujFI6U_58WChPl)**

Note: These videos are for additional learning, and do not cover all the material taught in the onsite classes.

### Projects for AI-201 Students

To begin with all AI-201 students will complete these projects:

Generative AI Projects:
https://github.com/panaversity/learn-agentic-ai/tree/main/02_generative_ai_for_beginners/PROJECTS

Agentic AI Projects:
https://github.com/panaversity/learn-agentic-ai/tree/main/05_crew_ai/PROJECTS

Project Checking: Your Instructors will check your project on the due date in class. You will be removed from
the class until you successfully complete your project and submit it.

All AI-201 students will complete these projects (links included in form) and submit them in this form:
https://forms.gle/VSZaLDBwCHNPzY5Z6

Project Checking: Your Instructors will check your project on the due date in class. You will be removed from
the class until you successfully complete your project and submit it.

### AI-202: Advanced Agentic AI Engineering

Covers Chapters 12 and onwards

**[AI-202 Video Playlist](https://www.youtube.com/playlist?list=PL0vKVrkG4hWoHDg46N85-9NDhmOaPWEwA)**

Note: These videos are for additional learning, and do not cover all the material taught in the onsite classes.

### Projects for AI-202 Students

All AI-202 students will complete these projects (links included in form) and submit them in this form:
https://forms.gle/Zfp2CWSmp9e91Wkk9


Project Checking: Your Instructors will check your project on the due date in class. You will be removed from
the class until you successfully complete your project and submit it.

## Which is the Best Agentic Framework?

Let's break down CrewAI, Autogen, and LangGraph for agentic development to help you decide which might be "better" for your needs.  There isn't a single "best" – it highly depends on what you prioritize in your agentic development project.

Here's a comparative look across several key dimensions:

**1. Core Philosophy & Structure:**

* **CrewAI:**  **Focuses on structured teams of agents with specialized roles.**  It's designed to mimic human teams, where each agent ("crew member") has a specific task and collaborates towards a common goal.  Think of it as organizing agents into a well-defined project team.
    * **Key Concept:**  Crews, Agents with Roles, Tasks, Collaboration within teams.
    * **Analogy:**  Building a small company with specialized departments working together.

* **Autogen:** **Emphasizes conversational agents and flexible, dynamic multi-agent conversations.** It's about creating agents that can fluidly interact, debate, and refine ideas through natural language conversations.  Think of it as setting up a dynamic forum or discussion group of agents.
    * **Key Concept:** Conversational Agents, Multi-Agent Chat, Dynamic Interaction, Flexibility.
    * **Analogy:**  Setting up a lively debate or brainstorming session among experts.

* **LangGraph:** **Prioritizes building robust, stateful, and reliable agentic workflows as graphs.**  It offers a more programmatic and state-centric approach, allowing you to define complex workflows and manage state transitions explicitly. Think of it as architecting a complex, reliable system with agents as nodes in a workflow graph.
    * **Key Concept:**  Workflows as Graphs, Stateful Agents, Robustness, Reliability, Explicit State Management.
    * **Analogy:**  Designing a complex assembly line or a robust data processing pipeline with agent components.

**2. Ease of Use & Learning Curve:**

* **CrewAI:**  **Relatively easy to get started with, especially if you understand the concept of teams and roles.** The API is designed to be intuitive for defining agents, tasks, and crews.  Good for beginners wanting to structure agent collaborations quickly.
    * **Learning Curve:**  Gentle to Moderate. Focuses on team structure, which is conceptually straightforward.

* **Autogen:** **Also relatively easy to begin with, particularly for conversational scenarios.**  Setting up basic agent chats is straightforward.  Complexity increases as you dive deeper into more nuanced agent behavior and conversation management.
    * **Learning Curve:** Gentle to Moderate.  Easy start, but mastering complex conversations requires more effort.

* **LangGraph:** **Steeper learning curve initially.** The graph-based workflow approach is more programmatic and requires understanding state management and graph concepts.  Offers more control but demands a more engineering-oriented mindset.
    * **Learning Curve:** Moderate to Steep.  Requires understanding graph workflows and state management.

**3. Flexibility & Customization:**

* **CrewAI:** **Structured but offers good flexibility within its team-based paradigm.** You can customize agent roles, tasks, tools, and collaboration strategies within a crew. Less flexible if you want to deviate significantly from the team structure.
    * **Flexibility:** Medium. Excellent within its team-based structure, less so outside of it.

* **Autogen:** **Highly flexible and customizable for conversational flows.** You have a lot of control over agent behavior, prompts, conversation styles, and integration of tools.  Adaptable to a wide range of conversational and interactive agent scenarios.
    * **Flexibility:** High.  Very adaptable for diverse conversational and interactive agent needs.

* **LangGraph:** **Extremely flexible and highly customizable for workflow design.** You have granular control over every node (agentic step) in the graph, state transitions, error handling, and more.  Best for building very specific and complex agentic workflows with precise control.
    * **Flexibility:** Very High.  Offers the most granular control over complex workflow design.

**4. Complexity Handling:**

* **CrewAI:** **Good for managing moderate complexity, especially in task delegation and team coordination.**  The crew structure helps break down complex projects into manageable agent tasks within a team. Can become less manageable for very intricate workflows beyond team interactions.
    * **Complexity Handling:**  Moderate.  Effective for team-based project breakdown, less so for highly intricate workflows.

* **Autogen:** **Handles conversational complexity well, especially in dynamic multi-agent discussions.** Can manage complex interactions and idea refinement through conversation. May become challenging to track state and manage long, branching conversations without explicit state management.
    * **Complexity Handling:** Moderate to High for conversational complexity. Can become complex to manage state in long conversations.

* **LangGraph:** **Designed explicitly for handling high complexity in workflows and state management.** The graph structure allows you to model and manage intricate, multi-step agentic processes with clear state transitions, error handling, and branching logic. Best for truly complex, production-ready agent systems.
    * **Complexity Handling:** High to Very High.  Excellent for managing intricate workflows, state, and complex system architectures.

**5. Collaboration & Teamwork (Agentic):**

* **CrewAI:** **Strongest focus on agent collaboration and teamwork.**  It's built around the concept of crews working together, making it ideal for scenarios where agents need to collaborate closely to achieve a shared objective.
    * **Collaboration Focus:**  Very High. Core strength is team-based agent collaboration.

* **Autogen:** **Supports multi-agent conversations and collaboration, but more in a dynamic, less structured way.** Agents can debate, discuss, and refine ideas, but the collaboration is driven by conversation rather than a predefined team structure.
    * **Collaboration Focus:** Medium to High.  Supports conversation-driven collaboration in a flexible manner.

* **LangGraph:** **Supports collaboration implicitly through workflow design.** You can design workflows where agents interact and exchange information as part of a larger process. Collaboration is defined programmatically within the graph, rather than being the central organizing principle like in CrewAI.
    * **Collaboration Focus:** Medium. Collaboration is supported as part of workflow design, not the primary focus.

**6. Scalability & Robustness:**

* **CrewAI:** **Scalability and robustness depend on how well you design your crews and agents.** Can scale if you effectively parallelize tasks and manage resource usage within your crews. Robustness needs to be considered in agent design and task handling.
    * **Scalability/Robustness:** Medium. Requires design considerations for scalability and robustness.

* **Autogen:** **Scalability depends on conversation management and resource usage.** Handling very large numbers of concurrent conversations or very long conversations might require careful management. Robustness depends on agent behavior and error handling in conversations.
    * **Scalability/Robustness:** Medium. Scalability and robustness require management of conversational complexity.

* **LangGraph:** **Designed with scalability and robustness in mind.** The graph-based approach allows for building more robust and maintainable agentic workflows. Explicit state management, error handling, and observability features contribute to building reliable systems.
    * **Scalability/Robustness:** High. Designed for building robust and scalable agentic systems.

**7. Specific Use Cases:**

* **CrewAI:**
    * **Project-based agentic tasks:** Research projects, content creation, structured problem-solving where tasks can be delegated to specialized agents within a team.
    * **Simulating human teams:** Scenarios where you want to mimic the workflow of a human project team with specialized roles.
    * **Learning about structured agent collaboration:** Good starting point for understanding agentic teamwork.

* **Autogen:**
    * **Conversational agents and assistants:** Building chatbots, interactive agents, agents for debate, brainstorming, and idea generation.
    * **Multi-agent simulations and games:** Scenarios where you want to simulate dynamic interactions between agents.
    * **Exploring emergent behavior in agent conversations:** Researching how agents interact and evolve ideas through dialogue.

* **LangGraph:**
    * **Complex, production-ready agentic systems:** Building robust applications requiring intricate workflows, state management, and reliability (e.g., complex automation, data processing pipelines).
    * **Systems with well-defined workflows:** Applications where the agentic process can be clearly modeled as a workflow graph with distinct steps and state transitions.
    * **Applications needing strong state management and error handling:** Scenarios requiring precise control over state and robust error recovery in agentic workflows.

**Summary Table:**

| Feature             | CrewAI                                  | Autogen                                  | LangGraph                                    |
|----------------------|------------------------------------------|------------------------------------------|---------------------------------------------|
| **Core Philosophy** | Structured Teams                        | Conversational Agents                     | Workflow Graphs                             |
| **Ease of Use**     | Moderate                                 | Moderate                                 | Moderate to Steep                          |
| **Flexibility**      | Medium (Team-centric)                     | High (Conversation-centric)               | Very High (Workflow-centric)                 |
| **Complexity Handling**| Moderate (Team-based)                     | Moderate to High (Conversation-based)     | High to Very High (Workflow & State-based) |
| **Collaboration**    | Very High (Teamwork)                    | Medium to High (Conversational)          | Medium (Workflow-integrated)                |
| **Scalability/Robustness**| Medium (Design-dependent)              | Medium (Conversation Management)         | High (Designed for Robustness)             |
| **Best For**         | Team-based Projects, Structured Tasks    | Conversational Agents, Dynamic Interaction | Complex Workflows, Production Systems        |

**Which is "Better"?**

**There's no universally "better" choice.** It boils down to your specific project goals and priorities:

* **Choose CrewAI if:** You want to build agents that work together as structured teams to solve problems, and you value clear roles and team-based collaboration. It's a good entry point to structured agentic development.

* **Choose Autogen if:** You are focused on creating conversational agents that can interact dynamically, debate, and refine ideas through natural language. It excels in building interactive and conversational AI.

* **Choose LangGraph if:** You are building complex, production-grade agentic systems that require robust workflows, explicit state management, and high reliability. It's the best choice for intricate, scalable, and dependable agentic applications.

**Recommendation:**

* **Start with CrewAI or Autogen if you are new to agentic development and want a quicker ramp-up.** Experiment with their more intuitive APIs.
* **Consider LangGraph if you anticipate building complex, production-ready systems from the outset, or if you find the need for robust state management and workflow control becomes critical as your projects evolve.**

Ultimately, the best way to decide is to **experiment with each framework** on a small project relevant to your needs. Try building a simple application with each to get a feel for their strengths and weaknesses in practice. You might even find that a combination of these frameworks could be beneficial for certain complex projects.

