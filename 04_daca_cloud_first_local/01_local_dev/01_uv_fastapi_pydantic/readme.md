# Getting Started with [FastAPI](https://fastapi.tiangolo.com), [UV](https://docs.astral.sh/uv/), and [Pydantic](https://docs.pydantic.dev/2.3/api/base_model/)

Welcome to the first tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! This module focuses on building robust APIs using FastAPI, the modern Python web framework, along with Pydantic for data validation and UV for efficient package management.

FastAPI serves as the REST API layer for our agentic AI system, enabling communication between users, agents, and microservices.

## What You’ll Learn

- How to install and use the `uv` Python dependency manager.
- Setting up a FastAPI project with `uv`.
- Understanding FastAPI’s key features: automatic documentation, async support, and Pydantic integration.
- A deep dive into Pydantic for data validation and serialization.
- Building a FastAPI application with complex Pydantic models.
- Adding CORS middleware for cross-origin requests.
- Writing unit tests with `pytest` to ensure API reliability.
- Testing and running the API with practical examples.

## Prerequisites

- Python 3.12+ installed on your system.
- Basic familiarity with Python, command-line tools, and REST APIs.
- A code editor (e.g., VS Code).
- [UV installed](https://docs.astral.sh/uv/getting-started/installation/) (see setup instructions below if needed).

## Learning Steps

This module is broken down into the following steps:

1.  **[Setup & Hello FastAPI](./01_hello_fastapi/readme.md)**: Set up your project using UV and create your first simple FastAPI endpoints.
2.  **[Pydantic Validation](./02_pydantic_validation/readme.md)**: Learn how to use Pydantic models to define request/response structures and perform automatic data validation.
3.  **[API Parameters](./03_api_parameters/readme.md)**: Explore different ways to receive data in your API, including path parameters, query parameters, and request bodies.
4.  **[Dependency Injection](./04_dependency_injection/readme.md)**: Understand FastAPI's powerful dependency injection system for managing dependencies and reusable logic.
5.  **[API Testing with Pytest](./05_api_pytests/readme.md)**: Write unit and integration tests for your FastAPI application using `pytest`.

## Initial Setup: Get [UV Python Project Manager](https://docs.astral.sh/uv/)

### What is UV?

`uv` is a modern, fast, and lightweight Python dependency manager built by the team at **Astral**. It’s designed to replace tools like `pip` and `virtualenv` by providing a unified, high-performance solution for managing Python projects. Key features include:

- **Speed**: Blazing fast dependency resolution and installation (written in Rust).
- **Unified Workflow**: Combines dependency management, virtual environment creation, and project setup.
- **Locking**: Generates a `uv.lock` file for reproducible builds.
- **Modern Features**: Supports PEP 582 (no need to activate virtualenvs manually in supported environments).

`uv` is ideal for DACA projects as it streamlines dependency management for FastAPI, Dapr, and other components.

### [Installing UV](https://docs.astral.sh/uv/getting-started/installation/)

#### On macOS/Linux

```bash
pip install uv
```

OR

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### On Windows (PowerShell)

```bash
pip install uv
```

OR

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### Verify Installation

```bash
uv --version
```

OR

```bash
uv version
```

You should see output like `uv 0.6.14` (or the latest version).

---
---

Let's begin with Step 1!



## Step 6: Next Steps
After completing all 5 steps you’ve built a robust FastAPI app with complex Pydantic models, and unit tests! 

In the next tutorial (**02_openai_agents_with_fastapi**), we’ll integrate the OpenAI Agents SDK to make our chatbot agentic, enabling autonomous task execution.

### Optional Exercises

1. Add a new endpoint to retrieve all messages for a `user_id` (use a mock dictionary for now).
2. Extend the `Message` model with a custom validator (e.g., ensure `text` is not longer than 500 characters).
3. Add more unit tests for edge cases (e.g., invalid `timestamp` format in `metadata`).
4. See [how to configure CORSMiddleware andwhy use it](https://fastapi.tiangolo.com/tutorial/cors/?h=cors#use-corsmiddleware)?
---

## Conclusion

In this enhanced tutorial, we set up a FastAPI project with `uv`, explored Pydantic in depth, and built a chatbot API with complex data models, and unit tests. FastAPI and Pydantic provide a solid foundation for DACA’s REST API layer, ensuring scalability, type safety, and ease of integration. You’re now ready to add agentic AI capabilities in the next tutorial!
