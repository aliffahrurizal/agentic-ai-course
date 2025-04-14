# Getting Started with [FastAPI](https://fastapi.tiangolo.com), [UV](https://docs.astral.sh/uv/), and [Pydantic](https://docs.pydantic.dev/2.3/api/base_model/)

Welcome to the first tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this baby step, we’ll set up a FastAPI project using the `uv` Python dependency manager, dive deep into FastAPI and Pydantic, and build a more robust API with unit tests, CORS middleware, and complex data models. FastAPI will serve as the REST API layer for our agentic AI system, enabling communication between users, agents, and microservices. Let’s get started!

---

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

---

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

## Step 1: [Setting Up a FastAPI Project with UV](https://fastapi.tiangolo.com/?h=installation#dependencies)

### Create a Project Directory and Switch to it

```bash
uv init fastdca-p1
cd fastdca-p1
```

### Create and Activate the Virtual Environment

On macOS/Linux:

```bash
uv venv
source .venv/bin/activate
```

On Windows:

```bash
uv venv
.venv\Scripts\activate
```

**Note**: With PEP 582 support (Python 3.11+), `uv` may not require manual activation for running commands.

### Add Dependencies

We’ll need FastAPI, Uvicorn (ASGI server), and additional packages for testing:

```bash
uv add "fastapi[standard]" pytest pytest-asyncio
```

The [fastapi[standard]](https://fastapi.tiangolo.com/?h=installation#dependencies) install optional dependencies especially

- `fastapi`: The web framework.
- `uvicorn`: The ASGI server to run the app.
- `httpx`: An HTTP client for testing FastAPI endpoints.

And we have added `pytest` and `pytest-asyncio`for unit testing.

This updates `pyproject.toml`:

```toml
[project]
name = "fastdca-p1"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "fastapi[standard]>=0.115.12",
    "pytest>=8.3.5",
    "pytest-asyncio>=0.26.0",
]
```

Verify the installed dependencies:

```bash
uv pip list
```

---

## Step 2: Create your first API route.

### Hello API: Create your first API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

### Run Server

Run the server with following command in terminal:

```bash
fastapi dev main.py
```
The command `fastapi dev main.py` is used to run a FastAPI application in development mode. Here's a breakdown:

- **FastAPI**: A modern, high-performance Python web framework for building APIs.
- **dev**: A subcommand provided by FastAPI's CLI (introduced in FastAPI 0.100.0 and later) to run the application in development mode with automatic reloading.
- **main.py**: The Python file containing your FastAPI application code (typically where the `FastAPI()` instance is defined).


**Notes:**
- Requires FastAPI and Uvicorn installed (`uv add fastapi[standard]` or `pip install fastapi[standard]`).
- Use `fastapi dev` for development only, not production.
- If your app instance isn’t named `app` or is in a different file/module, you may need to specify it (e.g., `fastapi dev myapp:app`).
- If you can get any error ensure fastapi is not installed globally or remove it. Alternatively you can also use this command

OR

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Test APIs

Open in browser

http://localhost:8000

http://localhost:8000/items/5?q=somequery

You already created an API that:

- Receives HTTP requests in the paths / and /items/{item_id}.
- Both paths take GET operations (also known as HTTP methods).
- The path /items/{item_id} has a path parameter item_id that should be an int.
- The path /items/{item_id} has an optional str query parameter q.

### Interactive API docs

Now go to http://localhost:8000/docs

## Step 3: Upgrade your APIs to use Pydantic

### Wait: What is Pydantic?

Pydantic is a data validation and settings management library that uses Python type annotations to define and validate data schemas. It’s a core dependency of FastAPI, used for request/response validation, serialization, and deserialization. Pydantic ensures type safety and provides automatic error handling, making it ideal for DACA’s agentic workflows where data integrity is critical.

### Key Features of Pydantic

- **Type-Safe Validation**: Validates data against Python type hints (e.g., `str`, `int`, `List[str]`).
- **Automatic Conversion**: Converts data to the correct type (e.g., string `"123"` to `int` 123).
- **Error Handling**: Raises detailed validation errors for invalid data.
- **Nested Models**: Supports complex, nested data structures.
- **Serialization**: Converts models to JSON (or other formats) for API responses.
- **Default Values and Optional Fields**: Simplifies schema definitions.
- **Custom Validators**: Allows custom validation logic.

### Getting Started with Pydantic

Let’s explore Pydantic with examples before integrating it into our FastAPI app.

#### Basic Pydantic Model

Create a file named `pydantic_examples.py`:

```python
from pydantic import BaseModel, ValidationError

# Define a simple model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None  # Optional field with default None

# Valid data
user_data = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25}
user = User(**user_data)
print(user)  # id=1 name='Alice' email='alice@example.com' age=25
print(user.model_dump())  # {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'age': 25}

# Invalid data (will raise an error)
try:
    invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
except ValidationError as e:
    print(e)
```

Run the script:

```bash
uv run python pydantic_examples.py
```

Output for invalid data:

```
1 validation error for User
id
  value is not a valid integer (type=type_error.integer)
```

#### Nested Models

Pydantic supports nested structures, which we’ll use in our FastAPI app. Extend `pydantic_examples.py`:

```python
from pydantic import BaseModel, EmailStr

# Define a nested model


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr  # Built-in validator for email format
    addresses: list[Address]  # List of nested Address models


# Valid data with nested structure
user_data = {
    "id": 2,
    "name": "Bob",
    "email": "bob@example.com",
    "addresses": [
        {"street": "123 Main St", "city": "New York", "zip_code": "10001"},
        {"street": "456 Oak Ave", "city": "Los Angeles", "zip_code": "90001"},
    ],
}
user = UserWithAddress.model_validate(user_data)
print(user.model_dump())
```

Output:

```json
{
  "id": 2,
  "name": "Bob",
  "email": "bob@example.com",
  "addresses": [
    { "street": "123 Main St", "city": "New York", "zip_code": "10001" },
    { "street": "456 Oak Ave", "city": "Los Angeles", "zip_code": "90001" }
  ]
}
```

#### Custom Validators

Add a custom validator to ensure the user’s name is at least 2 characters long:

```python
from pydantic import BaseModel, EmailStr, validator
from typing import List

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: List[Address]

    @validator("name")
    def name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v

# Test with invalid data
try:
    invalid_user = UserWithAddress(
        id=3,
        name="A",  # Too short
        email="charlie@example.com",
        addresses=[{"street": "789 Pine Rd", "city": "Chicago", "zip_code": "60601"}],
    )
except ValidationError as e:
    print(e)
```

Output:

```
1 validation error for UserWithAddress
name
  ValueError: Name must be at least 2 characters long
```

#### Why Pydantic for DACA?

Pydantic is critical for DACA because:

- **Data Integrity**: Ensures incoming user data and agent responses are valid and type-safe.
- **Complex Workflows**: Supports nested models for agentic AI scenarios (e.g., user messages with metadata, agent responses with context).
- **Serialization**: Seamlessly converts models to JSON for API responses.
- **Error Handling**: Provides clear validation errors, improving debugging in distributed systems.

---

## Step 4: Building a FastAPI Application with Complex Pydantic Models

Let’s build a FastAPI app for a chatbot with a more complex data model, simulating an agentic AI workflow where users send messages with metadata (e.g., timestamps, session IDs).

### Create the Main Application File

Create `chat.py`:

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from uuid import uuid4

# Initialize the FastAPI app
app = FastAPI(
    title="DACA Chatbot API",
    description="A FastAPI-based API for a chatbot in the DACA tutorial series",
    version="0.1.0",
)

# Complex Pydantic models
class Metadata(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    session_id: str = Field(default_factory=lambda: str(uuid4()))


class Message(BaseModel):
    user_id: str
    text: str
    metadata: Metadata
    tags: list[str] | None = None  # Optional list of tags


class Response(BaseModel):
    user_id: str
    reply: str
    metadata: Metadata

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Chatbot API! Access /docs for the API documentation."}

# GET endpoint with query parameters
@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

# POST endpoint for chatting
@app.post("/chat/", response_model=Response)
async def chat(message: Message):
    if not message.text.strip():
        raise HTTPException(
            status_code=400, detail="Message text cannot be empty")
    reply_text = f"Hello, {message.user_id}! You said: '{message.text}'. How can I assist you today?"
    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()  # Auto-generate timestamp and session_id
    )

```

### Explanation of the Code

1. **Complex Pydantic Models**:

   - `Metadata`: A nested model with a `timestamp` (defaults to current UTC time) and `session_id` (defaults to a UUID).
   - `Message`: The request model, including `user_id`, `text`, `metadata` (nested `Metadata`), and optional `tags`.
   - `Response`: The response model, returning `user_id`, `reply`, and `metadata`.

2. **Endpoint Updates**:
   - The `/chat/` endpoint now accepts a `Message` with nested `Metadata` and returns a `Response` with similar structure.

---

#### Run Code

```bash
fastapi dev chat.py
```

## Step 5: Writing Unit Tests with Pytest

### Why Unit Tests?

Unit tests ensure your API endpoints behave as expected, catching bugs early. In DACA, testing is crucial as we’ll integrate with Dapr, OpenAI Agents SDK, and other components.

### Create a Test File

Create a directory for tests and a test file:

```bash
touch test_chat.py
````

Add the following to `test_chat.py`:

```python
import pytest
from fastapi.testclient import TestClient
from chat import app

# Create a test client
client = TestClient(app)

# Test the root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the DACA Chatbot API! Access /docs for the API documentation."
    }

# Test the /users/{user_id} endpoint
def test_get_user():
    response = client.get("/users/alice?role=admin")
    assert response.status_code == 200
    assert response.json() == {"user_id": "alice", "role": "admin"}

    response = client.get("/users/bob")
    assert response.status_code == 200
    assert response.json() == {"user_id": "bob", "role": "guest"}

# Test the /chat/ endpoint (async test)
@pytest.mark.asyncio
async def test_chat():
    # Valid request
    request_data = {
        "user_id": "alice",
        "text": "Hello, how are you?",
        "metadata": {
            "timestamp": "2025-04-06T12:00:00Z",
            "session_id": "123e4567-e89b-12d3-a456-426614174000"
        },
        "tags": ["greeting"]
    }
    response = client.post("/chat/", json=request_data)
    assert response.status_code == 200
    assert response.json()["user_id"] == "alice"
    assert response.json()["reply"] == "Hello, alice! You said: 'Hello, how are you?'. How can I assist you today?"
    assert "metadata" in response.json()

    # Invalid request (empty text)
    invalid_data = {
        "user_id": "bob",
        "text": "",
        "metadata": {
            "timestamp": "2025-04-06T12:00:00Z",
            "session_id": "123e4567-e89b-12d3-a456-426614174001"
        }
    }
    response = client.post("/chat/", json=invalid_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Message text cannot be empty"}
```

### Run the Tests

```bash
uv run pytest test_chat.py -v
```

Output:

```
collected 3 items

tests/test_chat.py::test_root PASSED
tests/test_chat.py::test_get_user PASSED
tests/test_chat.py::test_chat PASSED

================= 3 passed in 0.36s =================
```

### Explanation of the Tests

1. **Test Client**:
   - `TestClient(app)`: Creates a client to simulate HTTP requests to the FastAPI app.
2. **Tests**:
   - `test_root`: Tests the root endpoint (`GET /`).
   - `test_get_user`: Tests the `/users/{user_id}` endpoint with and without query parameters.
   - `test_chat`: Tests the `/chat/` endpoint with both valid and invalid requests, including nested `metadata`.

## Step 6: Why FastAPI and Pydantic for DACA?

- **FastAPI**:
  - **Asynchronous Support**: Handles high-concurrency workloads.
  - **Automatic Docs**: Simplifies testing and integration.
  - **Scalability**: Stateless design fits DACA’s containerized architecture.
- **Pydantic**:
  - **Data Integrity**: Ensures type-safe data for agentic workflows.
  - **Complex Models**: Supports nested structures for rich data (e.g., metadata, tags).
  - **Error Handling**: Provides clear validation errors for debugging.

---

## Step 7: Next Steps

You’ve built a robust FastAPI app with complex Pydantic models, and unit tests! In the next tutorial (**02_openai_agents_with_fastapi**), we’ll integrate the OpenAI Agents SDK to make our chatbot agentic, enabling autonomous task execution.

### Optional Exercises

1. Add a new endpoint to retrieve all messages for a `user_id` (use a mock dictionary for now).
2. Extend the `Message` model with a custom validator (e.g., ensure `text` is not longer than 500 characters).
3. Add more unit tests for edge cases (e.g., invalid `timestamp` format in `metadata`).
4. See [how to configure CORSMiddleware andwhy use it](https://fastapi.tiangolo.com/tutorial/cors/?h=cors#use-corsmiddleware)?
---

## Conclusion

In this enhanced tutorial, we set up a FastAPI project with `uv`, explored Pydantic in depth, and built a chatbot API with complex data models, and unit tests. FastAPI and Pydantic provide a solid foundation for DACA’s REST API layer, ensuring scalability, type safety, and ease of integration. You’re now ready to add agentic AI capabilities in the next tutorial!
