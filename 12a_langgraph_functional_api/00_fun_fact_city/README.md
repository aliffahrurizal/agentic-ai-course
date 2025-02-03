# Step 00: Fun Fact Workflow

In this step, we will build a simple AI workflow using the **LangGraph Functional API**. This workflow generates a random city name for a given country and then gets a fun fact about that city.

The LangGraph Functional API makes it easy to build AI workflows by using regular Python functions. You do not have to design a complex graph. Instead, you use two main decorators:

- [**@task**](https://langchain-ai.github.io/langgraph/concepts/functional_api/#task): Wraps a small unit of work (for example, making an API call or processing data). Tasks run asynchronously and their results are saved.
- [**@entrypoint**](https://langchain-ai.github.io/langgraph/concepts/functional_api/#entrypoint): Marks the start of a workflow. It handles the overall flow and saves the workflow state so you can resume if needed.

Both decorators let you add powerful features like persistence (saving progress), memory, human-in-the-loop (pausing for user feedback), and streaming (real-time updates).

### PlayAround after running this project to breakdown and understand tasks and entrypoint decorator.
- [Entrypoint Documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/#entrypoint)
- [Task Documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/#task)

For more details, see the official [LangGraph Functional API documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/).
---

## How to Run Locally

### Prerequisites

- Python 3.10 or higher
- API Key from Google AI Studio 
- [uv](https://github.com/panaverisity/uv) (our preferred command-line runner)

### Installation

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/panaverisity/learn-agentic-ai.git
   ```

2.1 **Navigate to the Project Directory**

   ```bash
   cd /learn-agentic-ai/12a_langgraph_functional_api/00_fun_fact_city/fun_fact_city
   ```

2.2 **Navigate to the Project Directory**
  Rename .env.example to .env and add GOOGLE_API_KEY. Optionally you can setup the LangChain Variables for tracing in langsmith.

3. **Install Required Packages**

   ```bash
   uv sync
   ```

### Running the Workflow with Python

You can run the workflow directly by executing the **fun_fact.py** file:

```bash
uv run invoke
```

```bash
uv run stream
```

This will start the workflow and print the output to your terminal.

----

## Basic Concepts

### @task
- **What it does:** Wraps a small piece of work (like an API call).
- **Why use it:** Tasks run asynchronously and their results are saved (checkpointed) for later use.

### @entrypoint
- **What it does:** Marks the start of a workflow.
- **Why use it:** It manages the overall flow, saves the workflow state, and allows you to resume work if needed.

For more details on these concepts, visit:
- [Entrypoint Documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/#entrypoint)
- [Task Documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/#task)

---

## Additional Resources

- **Official Functional API Overview:**  
  [LangGraph Functional API](https://langchain-ai.github.io/langgraph/concepts/functional_api/)
- **Blog Post on the Functional API:**  
  [Introducing the LangGraph Functional API](https://blog.langchain.dev/introducing-the-langgraph-functional-api/)