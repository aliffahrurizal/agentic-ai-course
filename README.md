# Learn Agentic AI using Dapr Agentic Cloud Ascent (DACA) Design Pattern: From Start to Scale

This repo is part of the [Panaversity Certified Agentic & Robotic AI Engineer](https://docs.google.com/document/d/15usu1hkrrRLRjcq_3nCTT-0ljEcgiC44iSdvdqrCprk/edit?usp=sharing) program. It covers AI-201, AI-202 and AI-301 courses.

![Agentic AI Top Trend](./toptrend.webp)

**Complex Agentic AI Systems will be deployed on Cloud Native Technologies.**

![Cloud Native](./cloud-native-platforms-market-size.webp)

## Our Dapr Agentic Cloud Ascent (DACA) Design Pattern

Let's understand and learn about "Dapr Agentic Cloud Ascent (DACA)", our winning design pattern for developing and deploying planet scale multi-agent systems:

**[Comprehensive Guide to Dapr Agentic Cloud Ascent (DACA) Design Pattern](https://github.com/panaversity/learn-agentic-ai/blob/main/comprehensive_guide_daca.md)**

![DACA](./architecture1.png)

![](./ascent.png)


### Core Libraries
- **OpenAI Agents SDK and Responses API**
- **Docker Containers**
- **Docker Compose**
- **CockroachDB**
- **CronJobs**
- **RabbitMQ**
- **MCP Server SDK**
- **Dapr**
- **Azure Container Apps**
- **Kubernetes**

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

## Core Cloud Native Agentic Courses:

### AI-201:  Fundamentals of Agentic AI -  From Foundations to DACA Distributed Agents
Kickstart your journey into Agentic AI! This foundational course provides an intensive introduction to Agentic AI, a cutting-edge field focused on building autonomous, intelligent systems with memories, Agentic RAG (Retrieval Augmented Generation) and standards based MCP (Model Context Protocol) tool calling. In this course our main focus will be to use Dapr Agentic Cloud Ascent (DACA) Design Pattern in the development stage locally. Students will first establish a strong understanding of the essential building blocks: Conversational and Generative AI. We will then rapidly progress into the exciting realm of prototyping Agentic AI systems using OpenAI Responses API and OpenAI Agents SDK, emphasizing practical application and hands-on skill development, including crucial aspects of Short and Long-Term Memories, Standardized Tools Calling (MCP), Agentic RAG, Prototype Deployment, and Observability. 


**[AI-201 Video Playlist](https://www.youtube.com/playlist?list=PL0vKVrkG4hWovpr0FX6Gs-06hfsPDEUe6)**

Note: These videos are for additional learning, and do not cover all the material taught in the onsite classes.

Prerequisite: Successful completion of [AI-101: Modern AI Python Programming - Your Launchpad into Intelligent Systems](https://github.com/panaversity/learn-modern-ai-python)

### AI-202: AI-202: DACA Medium Enterprise Scale Distributed Agents: Managed Serverless Platforms
Building directly upon the foundational principles learned in AI-201, AI-202 propels students into the forefront of Advanced Agentic AI Engineering. In this course our main focus will be to use Dapr Agentic Cloud Ascent (DACA) Design Pattern in the Medium Enterprise Scale: Azure Container Apps (ACA). This intensive course focuses on utilizing sophisticated libraries and frameworks, to design, develop, and deploy complex, enterprise-ready AI agent systems. Students will learn to create agents capable of sophisticated reasoning, intricate task execution, and collaborative problem-solving within multi-agent ecosystems.

Prerequisite: Successful completion of AI-201:  Fundamentals of Agentic AI -  From Foundations to DACA Distributed Agents.

### AI-301: DACA Planet-Scale Distributed Agents: Kubernetes with Self-Hosted LLMs
AI-301 represents the pinnacle of the Agentic AI Engineering series, uniquely focusing on the deployment of stateful and scalable AI Agents using Docker, Kubernetes, Dapr, and Cloud Native Model Context Protocol (MCP) Servers and APIs. (The upcoming version of MCP servers will support remote cloud deployment in addition to the current on‑premise setup.) In this course our main focus will be to use Dapr Agentic Cloud Ascent (DACA) Design Pattern in the Medium Enterprise Scale: Azure Container Apps (ACA). 
This intensive course equips students with the specialized skills to design, build, deploy, and scale highly performant, robust AI Agents in the cloud and cloud-native MCP infrastructure essential for advanced Agentic AI systems. You will master the complete lifecycle of creating production-ready, cloud-native MCP Servers and APIs, from backend development to cloud deployment, user-centered design, and robust operational practices. Learn to leverage a cutting-edge technology stack specifically to build scalable and efficient Cloud Native AI Agents and Cloud Native MCP solutions that underpin the next generation of intelligent agent applications.

Prerequisite: Successful completion of AI-201:  Fundamentals of Agentic AI -  From Foundations to DACA Distributed Agents.







