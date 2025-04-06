# **Dapr Agentic Cloud Ascent (DACA)** Deployments

Let's understand and learn about "Dapr Agentic Cloud Ascent (DACA)", our winning design pattern for developing and deploying planet scale multi-agent systems:

**[Comprehensive Guide to Dapr Agentic Cloud Ascent (DACA) Design Pattern](https://github.com/panaversity/learn-agentic-ai/blob/main/comprehensive_guide_daca.md)**

The DACA series has progressed from local development to planetary-scale deployment, covering:
- **Local Development**: Building and testing the application with Dapr, Docker, and Docker Compose.
- **Prototyping**: Deploying to Hugging Face Docker Spaces for early testing.
- **Medium Enterprise Scale**: Using Azure Container Apps (ACA) for cost-efficient scaling to thousands of users.
- **Planet-Scale**: Deploying to Kubernetes on Oracle Cloud (free tier) and Civo Kubernetes (managed service) to handle tens of thousands of requests per minute with no API limits.

Each tutorial builds on the previous one, introducing new tools, services, and scaling strategies while maintaining the core DACA application (`chat_service`, `analytics_service`, `review_ui`).

The Local Development Tutorials are available here:

https://github.com/panaversity/learn-agentic-ai/tree/main/01_openai_agents/17_daca_local_dev

