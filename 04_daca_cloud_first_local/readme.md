# DACA Cloud Native

This module trains **Agentic AI Developers** to build planet-scale, multi-AI agent systems using the **Dapr Agentic Cloud Ascent (DACA)** architecture. DACA leverages Kubernetes for orchestration and Dapr for distributed capabilities, with AI agents as stateful Dapr Actors, FastAPI APIs for user interaction, and Pub/Sub for scalable agent communication. The core modules progress from coding to cloud native development, focusing on scalable agents while minimizing noise. 

## Core Modules

- **01_intro_fastapi/**: Build agent endpoints with FastAPI. Covers basics, validation, parameters, and a `/chat` API for DACA agents, integrating later with Dapr Pub/Sub.
- **02_cloud_native_setup/**: Set up Kubernetes for DACA agents. Includes YAML basics, Rancher Desktop, containers, Kubernetes, and Helm for Dapr apps.
- **03_dapr_intro/**: Intro to Dapr with Helm, configuring Pub/Sub (`pubsub.yaml`) and state stores (`statestore.yaml`) for distributed agent logic.
- **04_agent_actors/**: Build DACA agents as Dapr Actors. Includes fundamentals, Dapr actor implementation, agent design, multi-agent systems, and FastAPI/Kubernetes integration.
- **05_daca_advanced_experimental**: Optional topics for evaluation, including workflows (gRPC, human-in-the-loop), cloud design patterns, advanced FastAPI, load testing, observability, and AI model integration 

## Getting Started
Follow core modules sequentially or skip based on expertise. Hands-on exercises (e.g., chat API, multi-agent system) build DACA agents. Explore `05_daca_advanced_experimental/` for depth. See module-specific `readme.md` files for details.