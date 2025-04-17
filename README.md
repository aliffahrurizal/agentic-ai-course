# Learn Agentic AI using Dapr Agentic Cloud Ascent (DACA) Design Pattern: From Start to Scale

This repo is part of the [Panaversity Certified Agentic & Robotic AI Engineer](https://docs.google.com/document/d/15usu1hkrrRLRjcq_3nCTT-0ljEcgiC44iSdvdqrCprk/edit?usp=sharing) program. It covers AI-201, AI-202 and AI-301 courses.



<p align="center">
<img src="./img/toptrend.webp" width="200">
</p>

**Complex Agentic AI Systems will be deployed on Cloud Native Technologies.**

<p align="center">
<img src="./img/cloud-native-platforms-market-size.webp" width="300">
</p>

## Our Dapr Agentic Cloud Ascent (DACA) Design Pattern

Let's understand and learn about "Dapr Agentic Cloud Ascent (DACA)", our winning design pattern for developing and deploying planet scale multi-agent systems.

### Executive Summary: Dapr Agentic Cloud Ascent (DACA)

The Dapr Agentic Cloud Ascent (DACA) guide introduces a strategic design pattern for building and deploying sophisticated, scalable, and resilient agentic AI systems. Addressing the complexities of modern AI development, DACA integrates the OpenAI Agents SDK for core agent logic with the Model Context Protocol (MCP) for standardized tool use and the Agent2Agent (A2A) protocol for seamless inter-agent communication, all underpinned by the distributed capabilities of Dapr. Grounded in AI-first and cloud-first principles, DACA promotes the use of stateless, containerized applications deployed on platforms like Azure Container Apps or Kubernetes, enabling efficient scaling from local development to planetary-scale production, potentially leveraging free-tier cloud services and self-hosted LLMs for cost optimization. The pattern emphasizes modularity, context-awareness, and standardized communication, envisioning an "Agentia World" where diverse AI agents collaborate intelligently. Ultimately, DACA offers a robust, flexible, and cost-effective framework for developers and architects aiming to create complex, cloud-native agentic AI applications that are built for scalability and resilience from the ground up.


**[Comprehensive Guide to Dapr Agentic Cloud Ascent (DACA) Design Pattern](https://github.com/panaversity/learn-agentic-ai/blob/main/comprehensive_guide_daca.md)**

<p align="center">
<img src="./img/ascent.png" width="500">
</p>

<p align="center">
<img src="./img/architecture1.png" width="400">
</p>




### Target User
- **Agentic AI Developer and AgentOps Professionals**

### Why OpenAI Agents SDK should be the main framework for agentic development for most use cases?

**Table 1: Comparison of Abstraction Levels in AI Agent Frameworks**

| **Framework**         | **Abstraction Level** | **Key Characteristics**                                                                 | **Learning Curve** | **Control Level** | **Simplicity** |
|-----------------------|-----------------------|-----------------------------------------------------------------------------------------|--------------------|-------------------|----------------|
| **OpenAI Agents SDK** | Minimal              | Python-first, core primitives (Agents, Handoffs, Guardrails), direct control           | Low               | High             | High           |
| **CrewAI**            | Moderate             | Role-based agents, crews, tasks, focus on collaboration                                | Low-Medium        | Medium           | Medium         |
| **AutoGen**           | High                 | Conversational agents, flexible conversation patterns, human-in-the-loop support       | Medium            | Medium           | Medium         |
| **Google ADK**        | Moderate             | Multi-agent hierarchies, Google Cloud integration (Gemini, Vertex AI), rich tool ecosystem, bidirectional streaming | Medium            | Medium-High      | Medium         |
| **LangGraph**         | Low-Moderate         | Graph-based workflows, nodes, edges, explicit state management                        | Very High         | Very High        | Low            |
| **Dapr Agents**       | Moderate             | Stateful virtual actors, event-driven multi-agent workflows, Kubernetes integration, 50+ data connectors, built-in resiliency | Medium            | Medium-High      | Medium         |


The table clearly identifies why OpenAI Agents SDK should be the main framework for agentic development for most use cases:
- It excels in **simplicity** and **ease of use**, making it the best choice for rapid development and broad accessibility.
- It offers **high control** with **minimal abstraction**, providing the flexibility needed for agentic development without the complexity of frameworks like LangGraph.
- It outperforms most alternatives (CrewAI, AutoGen, Google ADK, Dapr Agents) in balancing usability and power, and while LangGraph offers more control, its complexity makes it less practical for general use.

If your priority is ease of use, flexibility, and quick iteration in agentic development, OpenAI Agents SDK is the clear winner based on the table. However, if your project requires enterprise-scale features (e.g., Dapr Agents) or maximum control for complex workflows (e.g., LangGraph), you might consider those alternatives despite their added complexity. 

## Core DACA Agentic AI Courses:

### AI-201:  Fundamentals of Agentic AI and DACA AI-First Development (14 weeks)

- ⁠Agentic & DACA Theory - 1 week
- UV & ⁠OpenAI Agents SDK - 5 weeks
- ⁠Agentic Design Patterns - 2 weeks 
- ⁠Memory [LangMem & mem0] 1 week
- Postgres/Redis (Managed Cloud) - 1 week
- FastAPI (Basic)  - 2 weeks
- ⁠Containerization (Rancher Desktop) - 1 week
- Hugging Face Docker Spaces - 1 week


**[AI-201 Video Playlist](https://www.youtube.com/playlist?list=PL0vKVrkG4hWovpr0FX6Gs-06hfsPDEUe6)**

Note: These videos are for additional learning, and do not cover all the material taught in the onsite classes.

Prerequisite: Successful completion of [AI-101: Modern AI Python Programming - Your Launchpad into Intelligent Systems](https://github.com/panaversity/learn-modern-ai-python)

### AI-202: DACA Cloud-First Agentic AI Development (14 weeks)
- Rancher Desktop with Local Kubernetes - 4 weeks
- Advanced FastAPI with Kubernetes - 2 weeks
- Dapr [workflows, state, pubsub, secrets] - 3 Week
- CockRoachdb & RabbitMQ Managed Services - 2 weeks
- ⁠Model Context Protocol -  2 weeks
- ⁠Serverless Containers Deployment (ACA) - 2 weeks

Prerequisite: Successful completion of AI-201

### AI-301 DACA Planet-Scale Distributed AI Agents (14 Weeks)
- ⁠Certified Kubernetes Application Developer (CKAD) - 4 weeks
- ⁠A2A Protocol - 2 weeks
- ⁠Voice Agents - 2 weeks
- ⁠Dapr Agents/Google ADK - 2 weeks
- ⁠Self-LLMs Hosting - 1 week
- Finetuning LLMs - 3 weeks

Prerequisite: Successful completion of AI-201 & AI-202







