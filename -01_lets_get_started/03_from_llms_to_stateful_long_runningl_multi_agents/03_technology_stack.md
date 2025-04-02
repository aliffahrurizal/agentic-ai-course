# AgentiaCloud: Free Scalable Intelligence, Simplified

Agentic AI is reshaping how we approach problem-solving, we’re harnessing its power to deliver scalable, adaptable intelligence solutions. Our focus is on providing developers with the tools to create tailored AI Agent-driven workflows without unnecessary complexity. By leveraging a minimalist yet powerful architecture, we enable everything from simple queries to sophisticated multi-agent systems.

By keeping predefined constructs to a minimum, we eliminate excess and empower developers to forge custom agentic solutions—whether that’s a simple query or an intricate multi-agent workflow—tailored to our specific needs. Here’s the streamlined tools we use, in our layered architecture:

1. **LLM APIs** that support robust Agent development, and are the defacto standard for interacting with LLMs. 
2. **Lightweight Agents** with built-in guardrails, tool integration, and seamless handoff capabilities.  
3. **REST APIs** enabling fluid communication between users, agent crews, and inter-crew interactions.  
4. **Stateless Serverless Docker Containers** for efficient, scalable computing (Agents, APIs, MCP Servers).  
5. **Asynchronous Message Passing** to connect containerize AI agents dynamically.  
6. **Flexible Container Invocation** via HTTP requests or scheduled CronJobs.  
7. **Relational Managed Database Services** for robust data handling.

With these core components, we enable the deployment of virtually any agentic workflow—striking a balance between simplicity and limitless potential.

### The Foundations
 
The OpenAI Responses API serves as a key foundation for developing agentic AI systems, offering advanced capabilities for autonomous task execution. The OpenAI Agents SDK complements this by providing a powerful framework to orchestrate multi-agent workflows using the Responses API. Together, these two components form the core pillars of our technology stack for building agentic AI.

![Agent Orchestration Layer](./agent-orchestration-layer.png)


---

## Detailed Explanation of AgentiaCloud Framework Constructs

1. **LLM APIs**  
   - **Purpose**: These serve as the core interface for interacting with large language models (LLMs), enabling agents to perform tasks ranging from simple queries to complex multi-step reasoning. They are standardized, robust, and widely supported.  
   - **Choice**: We’ve selected **[OpenAI Chat Completion](https://platform.openai.com/docs/guides/text?api-mode=responses)** and **Responses AI** as our LLM APIs. OpenAI’s Chat Completion APIs have become the de facto industry standard and are a proven choice for its versatility and agent-friendly features (e.g., function calling), while Responses API may offer complementary capabilities.  
   - **Why It Matters**: These APIs provide a reliable foundation for agentic workflows, ensuring developers can tap into cutting-edge AI capabilities with ease.

2. **Lightweight Agents**  
   - **Purpose**: These are modular AI units designed for specific tasks, equipped with guardrails (to ensure safe operation), tool integration (e.g., web search, file parsing, etc.), and handoff capabilities (to collaborate with other agents).  
   - **Choice**: We’re using the **[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)** to build these agents. This SDK offers a streamlined way to create lightweight agents with built-in features like memory management **([LangMem](https://langchain-ai.github.io/langmem/)** integration) and tool usage.  
   - **Why It Matters**: Lightweight agents minimize resource use while enabling flexible, scalable workflows, whether deployed individually or as part of a crew.

3. **REST APIs**  
   - **Purpose**: REST APIs facilitate seamless communication between users, agents, and agent crews over HTTP, providing a stateless, standardized interface for real-time interactions.  
   - **Choice**: **[FastAPI](https://fastapi.tiangolo.com/)** is our framework here. FastAPI is a high-performance, Python-based tool that supports asynchronous programming and auto-generates OpenAPI documentation, accelerating development.  
   - **Why It Matters**: It ensures low-latency, scalable communication, critical for user-facing applications and inter-agent coordination.

4. **Stateless Serverless Docker Containers**  
   - **Purpose**: These containers package our application logic (e.g., agents, APIs, MCP Servers) in a portable, stateless format, allowing automatic scaling and easy deployment without persistent internal state.  
   - **Choice**: We’re using **[Docker Containers](https://www.docker.com/resources/what-container/)**, which provide a lightweight, consistent runtime environment deployable across platforms. For container hosting we use **[Hugging Face Docker Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-docker)** (free hosting with built-in CI/CD) for prototyping, and [Kubernetes](https://kubernetes.io/) on [always free Oracle VMs](https://github.com/nce/oci-free-cloud-k8s) for production training. 
   - **Why It Matters**: Containers support rapid deployment and efficient resource utilization, aligning with the lean framework’s focus on simplicity and scalability. Deploying AI agents using Docker containers is widely regarded as a best practice and is considered the de facto industry standard. Docker containers offer a lightweight, portable, and consistent environment, ensuring that AI applications run reliably across various platforms. Moreover, Docker's widespread adoption has led to a rich ecosystem of tools and services that further enhance its utility in deploying AI agents. In summary, Docker containers provide a standardized and efficient approach to deploying AI agents, making them a preferred choice in the industry. 

   In addition, stateless containers, which do not retain data between sessions, enhance scalability by enabling rapid replication and distribution across multiple environments. It also allows them to be deployed as serverless containers. We can deploy these stateless containers not in Hugging Face Container Spaces, and Kuberneties but also in most cloud services:


   **Summary Table Across Providers**

   | Provider/Service            | Event-Driven Containers | Scheduled Containers |
   |-----------------------------|-------------------------|----------------------|
   | **AWS ECS**                 | Yes                     | Yes                  |
   | **AWS EKS**                 | Yes                     | Yes                  |
   | **AWS Fargate**             | Yes                     | Yes                  |
   | **AWS Lambda**              | Yes                     | Yes                  |
   | **AWS Batch**               | Indirectly              | Yes                  |
   | **Azure Container Apps**    | Yes                     | Yes                  |
   | **Azure Container Jobs**    | Yes                     | Yes                  |
   | **Azure AKS**               | Yes                     | Yes                  |
   | **Azure Functions**         | Yes                     | Yes                  |
   | **Azure ACI**               | Indirectly              | Indirectly           |
   | **GCP GKE**                 | Yes                     | Yes                  |
   | **GCP Cloud Run**           | Yes                     | Indirectly           |
   | **GCP Cloud Functions**     | Yes                     | Yes                  |
   | **GCP Cloud Scheduler**     | No                      | Yes                  |
   | **IBM IKS**                 | Yes                     | Yes                  |
   | **IBM Code Engine**         | Yes                     | Yes                  |
   | **OCI OKE**                 | Yes                     | Yes                  |
   | **OCI Functions**           | Yes                     | Yes                  |
   | **OCI Container Instances** | Indirectly              | Indirectly           |
   | **DO DOKS**                 | Yes                     | Yes                  |
   | **DO App Platform**         | Limited                 | Yes                  |

---


5. **Asynchronous Message Passing**  
   - **Purpose**: This enables non-blocking, dynamic communication between containerized agents or system components, ideal for parallel or independent task processing.  
   - **Choice**: **[RabbitMQ](https://www.cloudamqp.com/plans.html#rmq)** for prototyping. **[Kafka for Kubernetes](https://www.redhat.com/en/topics/integration/why-run-apache-kafka-on-kubernetes) for production**. It is a distributed streaming platform optimized for high-throughput, fault-tolerant messaging, connecting agents in complex workflows.  
   - **Why It Matters**: Asynchronous messaging decouples components, enhancing resilience and supporting event-driven architectures.

6. **Flexible Container Invocation**  
   - **Purpose**: This allows containers to be triggered either on-demand (via HTTP requests) or on a schedule (via cron-like jobs), offering versatility in execution patterns.  
   - **Choice**: For development we use [python-crontab](https://pypi.org/project/python-crontab/). For prototyping, we’re using **[cron-job.org](https://cron-job.org/en/)**, a free online scheduling service.  For production, we’re opting for **[Kubernetes CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)**, which integrates with Kubernetes for robust scheduling.  
   - **Why It Matters**: Flexible invocation supports both real-time and batch processing, accommodating diverse use cases efficiently.

7. **Relational Managed Database Services**  
   - **Purpose**: A relational database provides structured data storage with ACID compliance, handling user data, agent states, or logs reliably.  
   - **Choice**: **[CockroachDB](https://www.cockroachlabs.com/)** is our selection. CockroachDB is a distributed SQL database compatiable with Postgres designed for scalability and resilience, with managed services to reduce operational burden. Implement abstraction layers (e.g., ORMs for databases) to ease provider switches, we will use SQLModel for this.   
   - **Why It Matters**: It ensures robust data persistence, vital for tracking workflows or maintaining system integrity.

---

### Two Main Constructs Enabling the AgentiaCloud Framework

The entire framework hinges on two key constructs, which make both prototyping and production deployments possible:  
- **Event-Driven Container Invocation**: Containers triggered by events, such as HTTP requests, enable real-time responsiveness. This is the backbone of user-initiated workflows or agent interactions.  
- **Scheduled Container Invocation**: Containers executed on a predefined schedule (via cron jobs) support batch processing or periodic tasks, adding flexibility to the system. They will also be used to **pull asynchronous messages from RabbitMQ and Kafka**.  
Together, these constructs provide the versatility to handle virtually any agentic workflow, whether invoked dynamically or routinely, in both prototype and production environments.

---

### Development Stack (Local): Open Source

The development, prototype and production stacks are identical in terms of the tools and technologies used. The only difference lies in how they are deployed. This unified development approach ensures developers can build and test locally or in a cloud environment using the same stack, transitioning seamlessly to either prototyping or production deployment.  
- **LLM APIs**: OpenAI Chat Completion (Google Gemini - Free Tier), Responses API 
- **Lightweight Agents**: OpenAI Agents SDK (Open Source) 
- **REST APIs**: FastAPI (Open Source)
- **Stateless Serverless Docker Containers**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Docker Compose](https://docs.docker.com/compose/) (Free Tier and Open Source)
- **Asynchronous Message Passing**: [RabbitMQ Docker Image](https://hub.docker.com/_/rabbitmq/) (Open Source) 
- **Flexible Container Invocation**: [python-crontab](https://pypi.org/project/python-crontab/) (Open Source).
- **Relational Database**: [Postgres Docker Image](https://hub.docker.com/_/postgres) (Open Source). Implement abstraction layers (e.g., ORMs for databases) to ease provider switches, we will use SQLModel (Open Source). 
- **Developing inside a Container** [Visual Studio Code Dev Containers Extension](https://code.visualstudio.com/docs/devcontainers/containers)

### Prototype Stack: Free Deployment

The prototype stack is designed for rapid iteration and is completely free of charge or uses free tiers, leveraging cost-effective tools for testing and validation.  
- **LLM APIs**: OpenAI Chat Completion Compatible Google Gemini APIs which has a generious free tier, and Responses API  
- **Lightweight Agents**: OpenAI Agents SDK  
- **REST APIs**: FastAPI  
- **Stateless Serverless Docker Containers**: Docker Containers deployed on **[Hugging Face Docker Spaces](https://huggingface.co/docs/hub/en/spaces-sdks-docker)** (free hosting with built-in CI/CD)  
- **Asynchronous Message Passing**: RabbitMQ (Free tier).  
- **Flexible Container Invocation**: cron-job.org (totally free online scheduling service)  
- **Relational Managed Database Services**: CockroachDB Serverless (free tier). Implement abstraction layers (e.g., ORMs for databases) to ease provider switches, we will use SQLModel (Open Source).  
- **Cost**: Fully free for prototyping, minimizing financial barriers during development.

---

### Production Stack: Cloud Native and Open Source

The production stack is optimized for scalability, reliability, and performance, using enterprise-grade tools while maintaining the same development stack, differing only in deployment.  
- **LLM APIs**: Any LLM which is compatible with OpenAI Chat Completion API (most are), Responses API  
- **Lightweight Agents**: OpenAI Agents SDK  
- **REST APIs**: FastAPI  
- **Stateless Serverless Docker Containers**: Docker Containers orchestrated by **Kubernetes** (for auto-scaling and resilience)  
- **Asynchronous Message Passing**: Kafka on Kubernetes (multi-broker, high-availability setup) or RabbitMQ on Kubernetes
- **Flexible Container Invocation**: Kubernetes CronJob (natively integrated with Kubernetes) The developer will have to migrate from cron-job.org to Kubernetes CronJob.
- **Relational Managed Database Services**: CockroachDB Serverless (fully managed, multi-region deployment) on Postgres for Kubernetes. Implement abstraction layers (e.g., ORMs for databases) to ease provider switches, we will use SQLModel (Open Source).  
  
---

### Training Developers for Production Deployment

To equip developers with Kubernetes DevOps skills for production deployment, we leverage **Oracle Cloud Infrastructure (OCI)**, which offers a "free forever" tier which Offers 2 AMD VMs (1/8 OCPU, 1 GB RAM each) or up to 4 Arm-based VMs (24 GB RAM total). [These VMs are used to deploy our own Kubernetes cluster](https://github.com/nce/oci-free-cloud-k8s), providing a hands-on environment to learn cluster management, scaling, and deployment. Once developers master these skills, they can confidently deploy our agentic workflows to any cloud Kubernetes platform (e.g., AWS, GCP, Azure), ensuring portability and flexibility. This training bridges the gap between prototyping and production, empowering developers to handle real-world deployments.

References:

https://www.ronilsonalves.com/articles/how-to-deploy-a-free-kubernetes-cluster-with-oracle-cloud-always-free-tier

https://medium.com/@Phoenixforge/a-weekend-project-with-k3s-and-oracle-cloud-free-tier-99eda1aa49a0

---

### Summary

This AgentiaCloud framework balances simplicity and power, with a unified development stack that adapts to free prototyping (via Hugging Face Docker Spaces, cron-job.org) or robust production (via Kubernetes, OCI-trained DevOps). The two core constructs—event-driven and scheduled container invocation—underpin its versatility, enabling any short-term or long-term workflow in any environment. 
