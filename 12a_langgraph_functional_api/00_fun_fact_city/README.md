# Step 00: Fun Fact Workflow

In this step, we will build a simple AI workflow using the **LangGraph Functional API**. This workflow generates a random city name for a given country and then gets a fun fact about that city.

The LangGraph Functional API makes it easy to build AI workflows by using regular Python functions. You do not have to design a complex graph. Instead, you use two main decorators:

- [**@task**](https://langchain-ai.github.io/langgraph/concepts/functional_api/#task): Wraps a small unit of work (for example, making an API call or processing data). Tasks run asynchronously and their results are saved.
- [**@entrypoint**](https://langchain-ai.github.io/langgraph/concepts/functional_api/#entrypoint): Marks the start of a workflow. It handles the overall flow and saves the workflow state so you can resume if needed.

Both decorators let you add powerful features like persistence (saving progress), memory, human-in-the-loop (pausing for user feedback), and streaming (real-time updates).

For more details, see the official [LangGraph Functional API documentation](https://langchain-ai.github.io/langgraph/concepts/functional_api/).
---

## How to Run Locally

### Prerequisites

- Python 3.8 or higher
- Internet connection (to access the language model)
- [uv](https://github.com/panaverisity/uv) (our preferred command-line runner)

### Installation

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/panaverisity/learn-agentic-ai.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd learn-agentic-ai/fun_fact_workflow/step00_fun_fact
   ```

3. **Install Required Packages**

   ```bash
   pip install --quiet -U langgraph langchain_openai langchain_google_genai
   ```

### Running the Workflow with Python

You can run the workflow directly by executing the **fun_fact.py** file:

```bash
python fun_fact.py
```

This will start the workflow and print the output to your terminal.

---

## Running the Workflow with uv

We use **uv** as our command-line runner. You can configure an entrypoint for the workflow in your `pyproject.toml` (or a similar configuration file).

### Example Entry Point Configuration

Add the following to your `pyproject.toml` file in the project root:

```toml
[tool.uv.entry_points]
fun_fact = "fun_fact_workflow.step00_fun_fact.fun_fact:main_workflow"
```

Then, from the project root, run:

```bash
uv run fun_fact
```

This command will launch the workflow using the configured entrypoint.

---

## Code Overview

Below is the complete code used in this project. **Note:** The code is included exactly as it is, without any changes.

```python
%%capture --no-stderr
%pip install --quiet -U langgraph langchain_openai langchain_google_genai

from langchain_openai import ChatOpenAI
import time
import uuid
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

# Initialize the language model
model = ChatOpenAI(model="gpt-4o-mini")

# Set up an in-memory checkpointer for saving progress
checkpointer = MemorySaver()

@task
def generate_city(country: str) -> str:
    """Ask the model to give a random city name for the given country."""
    print("Starting workflow")
    response = model.invoke(f"Return the name of a random city in the {country}.")
    random_city = response.content
    print(f"Random City: {random_city}")
    return random_city

@task
def generate_fun_fact(city: str) -> str:
    """Ask the model to share a fun fact about the given city."""
    response = model.invoke(f"Tell me a fun fact about {city}")
    fun_fact = response.content
    return fun_fact

@entrypoint(checkpointer=checkpointer)
def main_workflow(country: str) -> dict:
    """The main workflow that gets a city and then a fun fact about it."""
    city = generate_city(country).result()
    fact = generate_fun_fact(city).result()
    return {"city": city, "fun_fact": fact, "country": country}

# Generate a unique thread ID to save workflow state
thread_id = str(uuid.uuid4())
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

# Run the workflow with a sample input (here we use "cat" for fun)
result = main_workflow.invoke("cat", config)
print(f"Generated fun fact: {result}")
```

### Expected Output

When you run the code, you might see something like:

```
Starting workflow
Random City: Sure! How about "Catropolis"? It's a fun, fictional city name inspired by cats!
Generated fun fact: {
    'city': 'Sure! How about "Catropolis"? ...',
    'fun_fact': 'Absolutely! In the whimsical world of "Catropolis," ...',
    'country': 'cat'
}
```

---

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
- **Related Example:**  
  See [step_06_crewai](../step_06_crewai) for more examples and guides.

---

## Contributing & Feedback

If you have any questions or suggestions, please open an issue or submit a pull request on our [GitHub repository](https://github.com/panaverisity/learn-agentic-ai).

---

## License

This project is licensed under the MIT License.

---

Happy coding and enjoy building your fun fact AI workflow with the LangGraph Functional API!
```