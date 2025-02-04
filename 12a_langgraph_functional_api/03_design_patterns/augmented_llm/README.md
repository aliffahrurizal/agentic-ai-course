# Building block: The augmented LLM

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. 

## Objective

Learn how to enhance LLMs with key augmentations that form the building blocks of agentic systems:

1. Structured Output - Using Pydantic models to enforce output schema
2. Tool Usage - Binding tools to LLMs for external actions
3. Memory (Short Term and Long Term) - Adding state and context to LLM interactions

Run the jupyter notebook in Collab present in /notebook dir first and then try running the project locally. project.

## How to Run Locally

### Prerequisites

- Python 3.10 or higher
- API Key from Google AI Studio
- [uv](https://github.com/panaverisity/uv) (preferred package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/panaverisity/learn-agentic-ai.git
```

2. Navigate to project directory:

```bash
cd learn-agentic-ai/12a_langgraph_functional_api/03_design_patterns/augmented_llm
```

3. Set up environment:

- Copy `.env.example` to `.env`
- Add your `GOOGLE_API_KEY`
- Optionally configure LangSmith variables for tracing

4. Install dependencies:

```bash
uv sync
```

### Running the Examples

Execute each example pattern:

```bash
uv run structured_response
uv run tools_response
uv run lt_memory
```

## Code Examples

### 1. Structured Output

```python
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

# Define output schema
class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query optimized for web search")
    justification: str = Field(None, description="Why this query is relevant")

# Create base LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Augment with structured output
structured_llm = llm.with_structured_output(SearchQuery)

# Use the augmented LLM
result = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")
result
```

Output:
```bash
SearchQuery(search_query='Calcium CT score high cholesterol', justification=None)
```

### 2. Tool Usage

```python
# Define a tool
def search_medical_database(query: str) -> str:
    """Search medical literature database"""
    # Mock implementation
    return f"Results for: {query}"

# Bind tool to LLM
llm_with_tools = llm.bind_tools([search_medical_database])

# Use tool-augmented LLM
response = llm_with_tools.invoke("Find recent studies on statins")
response.tool_calls
```

Output:
```bash
[{'name': 'search_medical_database',
  'args': {'query': 'recent studies on statins'},
  'id': '9bcfc36a-2474-45e7-9ea4-4b8750c16b56',
  'type': 'tool_call'}]
  ```

### 3. Memory Integration

```python
import uuid
from langgraph.store.memory import InMemoryStore, BaseStore
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages
from langgraph.checkpoint.memory import MemorySaver


# ✅ **Initialize LLM**
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# ✅ **Initialize Memory Store**
in_memory_store = InMemoryStore(
    index={
        "embed": GoogleGenerativeAIEmbeddings(model="models/embedding-001"),  # Ensure correct model
        "dims": 768,  # Ensure embedding dimensions match
    }
)


# ✅ **Memory-augmented LLM Task**
@task
def call_model(messages: list[BaseMessage], memory_store: BaseStore, user_id: str):
    """Retrieves user context from memory and responds accordingly."""
    
    namespace = ("memories", user_id)
    last_message = messages[-1]

    # 🔥 **Retrieve stored memories**
    stored_memories = memory_store.search(namespace, query=str(last_message.content))
    stored_info = "\n".join([d.value["data"] for d in stored_memories]) if stored_memories else ""

    # ✅ **Adjust system prompt dynamically**
    if stored_info:
        system_msg = f"You are a helpful assistant. The user previously mentioned:\n{stored_info}"
    else:
        system_msg = "You are a helpful assistant. The user has not shared any prior information."

    # 🔥 **Check if user wants to add new memory**
    if "remember" in last_message.content.lower():
        new_memory = f"User said: {last_message.content}"
        memory_store.put(namespace, str(uuid.uuid4()), {"data": new_memory})

    # ✅ **Invoke the model with memory-augmented context**
    response = model.invoke([{"role": "system", "content": system_msg}] + messages)

    return response


# ✅ **Workflow EntryPoint with Persistent Memory**
@entrypoint(checkpointer=MemorySaver(), store=in_memory_store)
def workflow(
    inputs: list[BaseMessage],
    *,
    previous: list[BaseMessage],
    config: RunnableConfig,
    store: BaseStore,
):
    """Handles cross-thread memory and conversation flow."""
    
    user_id = config["configurable"]["user_id"]
    previous = previous or []
    inputs = add_messages(previous, inputs)

    # 🔥 **Retrieve & process response**
    response = call_model(inputs, store, user_id).result()

    return entrypoint.final(value=response, save=add_messages(inputs, response))


# ✅ **Example Usage: Testing Cross-Thread Memory**
config1 = {"configurable": {"thread_id": "1", "user_id": "123"}}
input_message1 = {"role": "user", "content": "Hi! Remember: I love sci-fi movies."}

for chunk in workflow.stream([input_message1], config1, stream_mode="values"):
    chunk.pretty_print()

# ✅ **Retrieve memory in a new thread**
config2 = {"configurable": {"thread_id": "2", "user_id": "123"}}
input_message2 = {"role": "user", "content": "What do you know about me?"}

for chunk in workflow.stream([input_message2], config2, stream_mode="values"):
    chunk.pretty_print()

```
Example Output with Memory:

```bash
================================== Ai Message ==================================

Okay, got it! I'll remember you love sci-fi movies. How can I help you today, fellow sci-fi enthusiast? Are you looking for recommendations, want to discuss a particular film, or something else entirely? Let me know!
================================== Ai Message ==================================

Okay! I remember that you love sci-fi movies.
```