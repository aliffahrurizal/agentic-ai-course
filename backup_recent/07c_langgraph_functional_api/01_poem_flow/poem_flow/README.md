# Poem Flow

## Objective

1. Increase our understanding of Tasks, and EntryPoint decorators.
2. Understand how to run tasks synchronously and asynchronously.
3. Entrypoint can take different arguments like checkpointer, store...

## Run poemflow project

After setting up environment run the following commands

```bash
uv run invoke
```

```bash
uv run stream
```

You can either clone this project or take the sample code from workflow.py and create your own project.

After running the above commands change topic in poemflow/**init**.py to generate different poems.

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
cd /learn-agentic-ai/12a_langgraph_functional_api/01_poem_flow/poem_flow
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

import os
from random import randint
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
_: bool = load_dotenv(find_dotenv())

# Initialize the AI Model (Poem Generation)
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

@task
def generate_sentence_count() -> int:
    """Generate a random sentence count for the poem."""
    return randint(1, 5)

@task
def generate_poem(sentence_count: int) -> str:
    """Generate a poem based on the sentence count using the AI model."""
    prompt = f"Write a beautiful and engaging poem about CrewAI with exactly {sentence_count} sentences."
    response = model.invoke(prompt)
    return response.content.strip()

@task
def save_poem(poem: str) -> str:
    """Save the poem to a file in a correct directory to avoid path errors."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(output_dir, "poem.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(poem)

    return f"Poem saved successfully at {file_path}"

@entrypoint()
def run_workflow(input: str | None):
    """Workflow to generate and save a poem."""
    sentence_count = generate_sentence_count().result()
    poem = generate_poem(sentence_count).result()
    save_status = save_poem(poem).result()

    return {"sentence_count": sentence_count, "poem": poem, "status": save_status}

def stream():
    for event in run_workflow.stream(input=""):
        print(event)

stream()

```

### Expected Output

When you run the code, you might see something like:

```
{'generate_sentence_count': 4}
{'generate_poem': "In realms of code, where agents brightly gleam, CrewAI orchestrates a collaborative dream,\nTasks unfold with purpose, roles defined with grace, a symphony of intellect, finding its place.\nFrom research deep to creation's vibrant art, ideas converge, each playing its vital part.\nA testament to teamwork, where AI's brilliance shines, transforming challenges into solutions, in elegant designs."}
{'save_poem': 'Poem saved successfully at output/poem.txt'}
{'run_workflow': {'sentence_count': 4, 'poem': "In realms of code, where agents brightly gleam, CrewAI orchestrates a collaborative dream,\nTasks unfold with purpose, roles defined with grace, a symphony of intellect, finding its place.\nFrom research deep to creation's vibrant art, ideas converge, each playing its vital part.\nA testament to teamwork, where AI's brilliance shines, transforming challenges into solutions, in elegant designs.", 'status': 'Poem saved successfully at output/poem.txt'}}
```

---
