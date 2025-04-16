## How to Run Locally

### Prerequisites

- Python 3.10 or higher
- API Key from Google AI Studio
- [uv] (our preferred command-line runner)

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
