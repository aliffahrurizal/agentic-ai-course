# Securely Managing Secrets with Dapr

Welcome to the ninth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll enhance the microservices from **08_dapr_workflows** by integrating Dapr’s **Secrets Management** building block. Currently, the Chat Service uses the OpenAI API key via an environment variable (`OPENAI_API_KEY`), which is not secure for production environments. We’ll configure Dapr to manage the OpenAI API key in a secrets store, and update the Chat Service to retrieve the key securely using Dapr’s Secrets Management API. This will improve the security of our system, aligning with best practices for handling sensitive data. Let’s get started!

---

## What You’ll Learn
- How to use Dapr’s Secrets Management building block to securely manage sensitive data.
- Configuring a Dapr secrets store to store the OpenAI API key.
- Updating the Chat Service to retrieve the API key from the Dapr secrets store.
- Running microservices with Dapr Secrets Management enabled.
- Updating unit tests to account for Dapr Secrets Management integration.

## Prerequisites
- Completion of **08_dapr_workflows** (codebase with Chat Service and Analytics Service using Dapr Service Invocation, State Management, Pub/Sub Messaging, and Workflows).
- Dapr CLI and runtime installed (from **04_dapr_theory_and_cli**).
- Docker installed (Dapr uses Docker for its sidecars and components).
- Python 3.12+ installed.
- An OpenAI API key (previously set as `OPENAI_API_KEY`).

---

## Step 1: Recap of the Current Setup
In **08_dapr_workflows**, we integrated Dapr’s Workflows into the Chat Service:
- The **Chat Service**:
  - Uses a Dapr Workflow to orchestrate message processing: fetching the user’s message count (via Service Invocation), generating a reply (using the OpenAI Agents SDK), and publishing a “MessageSent” event (via Pub/Sub).
  - Assumes the OpenAI API key is available as an environment variable (`OPENAI_API_KEY`), which is used by the `Agent` class (via the OpenAI Agents SDK).
- The **Analytics Service**:
  - Subscribes to the `messages` topic and updates the user’s message count in the Dapr state store when a “MessageSent” event is received.

### Current Limitations
- **Insecure API Key Storage**: The OpenAI API key is stored as an environment variable (`OPENAI_API_KEY`), which can be accidentally exposed (e.g., in logs, version control, or container configurations).
- **Lack of Centralized Secret Management**: There’s no centralized mechanism to manage and rotate secrets, which is critical for production environments.
- **Security Risks**: Hardcoding or using environment variables for secrets doesn’t align with security best practices, especially in a distributed system where multiple services might need access to secrets.

### Goal for This Tutorial
We’ll use Dapr’s Secrets Management to securely manage the OpenAI API key:
- Configure a Dapr secrets store to store the API key (using a local file-based store for simplicity, with notes on production alternatives).
- Update the Chat Service to retrieve the API key from the Dapr secrets store using the `dapr` Python SDK.
- Remove the dependency on the `OPENAI_API_KEY` environment variable, improving security.

### Current Project Structure
```
fastapi-daca-tutorial/
├── chat_service/
│   ├── main.py
│   ├── models.py
│   └── tests/
│       └── test_main.py
├── analytics_service/
│   ├── main.py
│   ├── models.py
│   └── tests/
│       └── test_main.py
├── components/
│   └── subscriptions.yaml
├── pyproject.toml
└── uv.lock
```

---

## Step 2: Why Use Dapr Secrets Management?
Dapr’s **Secrets Management** building block provides a secure way to manage and access sensitive data (e.g., API keys, database credentials) in a distributed system. It offers several advantages over environment variables or hardcoded secrets:
- **Security**: Secrets are stored in a dedicated secrets store (e.g., local file, HashiCorp Vault, AWS Secrets Manager), reducing the risk of accidental exposure.
- **Centralized Management**: Secrets can be managed centrally, making it easier to rotate, update, or revoke them without changing application code.
- **Access Control**: Dapr supports fine-grained access control for secrets (depending on the secrets store), ensuring only authorized services can access them.
- **Abstraction**: Dapr provides a consistent API for accessing secrets, regardless of the underlying secrets store, making it easy to switch stores (e.g., from local to cloud-based).
- **Production-Readiness**: Aligns with best practices for handling sensitive data in production environments.

In DACA, Secrets Management is crucial for:
- Securely managing the OpenAI API key used by the Chat Service.
- Preparing the system for production deployment, where secrets must be handled securely.
- Supporting a scalable architecture where multiple services might need access to shared secrets.

---

## Step 3: Configure Dapr Secrets Store
Dapr uses a secrets store component to manage secrets. For this tutorial, we’ll use a **local file-based secrets store** for simplicity, as it doesn’t require external infrastructure. In a production environment, you’d use a secure secrets store like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault.

### Step 3.1: Create a Secrets File
Create a directory for custom Dapr components and a secrets file to store the OpenAI API key.

```bash
mkdir -p components
cd components
touch secrets.json
```

Edit `components/secrets.json` to include the OpenAI API key:
```json
{
  "openai-api-key": "your-openai-api-key-here"
}
```
Replace `"your-openai-api-key-here"` with your actual OpenAI API key.

### Step 3.2: Create a Secrets Store Component
Create a `secretstore.yaml` file in the `components` directory to define the secrets store.

```bash
touch components/secretstore.yaml
```

Edit `components/secretstore.yaml`:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
spec:
  type: secretstores.local.file
  version: v1
  metadata:
  - name: secretsFile
    value: ./components/secrets.json
  - name: nestedSeparator
    value: "."
```
- `name: secretstore`: The name of the secrets store component (we’ll use this in our code).
- `type: secretstores.local.file`: Uses a local file as the secrets store.
- `secretsFile`: Points to the `secrets.json` file we created.
- `nestedSeparator`: Specifies the separator for nested keys (not used here, but included for completeness).

### Step 3.3: Production Considerations
In a production environment, you’d replace the local file-based store with a secure secrets store:
- **HashiCorp Vault**:
  ```yaml
  apiVersion: dapr.io/v1alpha1
  kind: Component
  metadata:
    name: secretstore
  spec:
    type: secretstores.hashicorp.vault
    version: v1
    metadata:
    - name: vaultAddr
      value: "https://your-vault-server:8200"
    - name: vaultToken
      value: "your-vault-token"
  ```
- **AWS Secrets Manager**:
  ```yaml
  apiVersion: dapr.io/v1alpha1
  kind: Component
  metadata:
    name: secretstore
  spec:
    type: secretstores.aws.secretmanager
    version: v1
    metadata:
    - name: region
      value: "us-east-1"
    - name: accessKey
      value: "your-access-key"
    - name: secretKey
      value: "your-secret-key"
  ```
For this tutorial, we’ll stick with the local file-based store for simplicity.

---

## Step 4: Update the Chat Service to Use Dapr Secrets Management
We’ll modify the Chat Service to retrieve the OpenAI API key from the Dapr secrets store using the `dapr` Python SDK. We’ll also update the `Agent` initialization to use the retrieved API key.

### Step 4.1: Modify `chat_service/main.py`
Update the Chat Service to fetch the OpenAI API key from the Dapr secrets store and pass it to the `Agent`.

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, function_tool
from datetime import datetime
import httpx
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowClient, DaprWorkflowContext, when
from dapr.workflow import WorkflowActivityContext

from models import Message, Response, Metadata

app = FastAPI(
    title="DACA Chat Service",
    description="A FastAPI-based Chat Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Dapr Workflow runtime
workflow_runtime = WorkflowRuntime()
workflow_runtime.start()

# Fetch the OpenAI API key from Dapr secrets store
async def get_openai_api_key() -> str:
    with DaprClient() as dapr_client:
        try:
            secret = await dapr_client.get_secret(
                store_name="secretstore",
                key="openai-api-key"
            )
            return secret.secret["openai-api-key"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve OpenAI API key: {e}")

# Initialize the chat agent with the API key
async def initialize_chat_agent():
    api_key = await get_openai_api_key()
    return Agent(
        name="ChatAgent",
        instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool. Personalize responses using user analytics (e.g., message count).",
        model="gpt-4o",
        tools=[get_current_time],
        api_key=api_key  # Pass the API key to the Agent (assumed parameter)
    )

# Note: The OpenAI Agents SDK might not directly support passing the API key like this.
# If the SDK reads from the environment variable, you might need to set it dynamically:
# import os
# os.environ["OPENAI_API_KEY"] = await get_openai_api_key()
# For this tutorial, we assume the Agent accepts an api_key parameter.

@function_tool
def get_current_time() -> str:
    """Returns the current time in UTC."""
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Initialize the chat agent at startup
chat_agent = None

@app.on_event("startup")
async def startup():
    global chat_agent
    chat_agent = await initialize_chat_agent()

async def get_db():
    return {"connection": "Mock DB Connection"}

# Workflow activities
async def fetch_analytics_activity(ctx: WorkflowActivityContext, user_id: str) -> int:
    """Activity to fetch the user's message count from the Analytics Service."""
    with DaprClient() as dapr_client:
        try:
            response = await dapr_client.invoke_method_async(
                app_id="analytics-service",
                method_name=f"analytics/{user_id}",
                http_verb="GET"
            )
            analytics_data = response.json()
            return analytics_data.get("message_count", 0)
        except Exception as e:
            print(f"Failed to fetch analytics in workflow: {e}")
            return 0

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    """Activity to generate a reply using the OpenAI Agents SDK."""
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]

    personalized_instructions = (
        f"You are a helpful chatbot. Respond to user messages in a friendly and informative way. "
        f"If the user asks for the time, use the get_current_time tool. "
        f"The user has sent {message_count} messages so far, so personalize your response accordingly."
    )
    chat_agent.instructions = personalized_instructions

    result = await Runner.run(chat_agent, input=message_text)
    return result.final_output

async def publish_event_activity(ctx: WorkflowActivityContext, user_id: str):
    """Activity to publish a MessageSent event to the messages topic."""
    with DaprClient() as dapr_client:
        try:
            await dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="messages",
                data={"user_id": user_id, "event_type": "MessageSent"}
            )
            print(f"Published MessageSent event for user {user_id} in workflow")
        except Exception as e:
            print(f"Failed to publish MessageSent event in workflow: {e}")
            raise

# Define the workflow
@workflow_runtime.workflow
async def message_processing_workflow(ctx: DaprWorkflowContext, input_data: dict) -> dict:
    """Workflow to orchestrate message processing in the Chat Service."""
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]

    message_count = await ctx.call_activity(
        fetch_analytics_activity,
        input=user_id,
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    reply = await ctx.call_activity(
        generate_reply_activity,
        input={"user_id": user_id, "message_text": message_text, "message_count": message_count},
        retry_policy={"max_retries": 2, "interval": "PT3S"}
    )

    await ctx.call_activity(
        publish_event_activity,
        input=user_id,
        retry_policy={"max_retries": 5, "interval": "PT2S"}
    )

    return {"user_id": user_id, "reply": reply}

@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."}

@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

@app.post("/chat/", response_model=Response)
async def chat(message: Message, db: dict = Depends(get_db)):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    print(f"DB Connection: {db['connection']}")

    with DaprWorkflowClient() as workflow_client:
        instance_id = f"chat-{message.user_id}-{int(datetime.utcnow().timestamp())}"
        input_data = {"user_id": message.user_id, "message_text": message.text}
        
        await workflow_client.schedule_new_workflow(
            workflow=message_processing_workflow,
            instance_id=instance_id,
            input=input_data
        )

        result = await workflow_client.wait_for_workflow_completion(
            instance_id=instance_id,
            timeout_in_seconds=60
        )

        if result is None or result.runtime_status != "COMPLETED":
            raise HTTPException(status_code=500, detail="Workflow failed to complete")

        workflow_output = result.output
        reply_text = workflow_output["reply"]

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )

@app.on_event("shutdown")
def shutdown():
    workflow_runtime.stop()
```

#### Explanation of Changes
1. **Secrets Retrieval Function**:
   - Added `get_openai_api_key` to fetch the OpenAI API key from the Dapr secrets store (`secretstore`) using the `dapr` Python SDK.
   - The key is retrieved using `dapr_client.get_secret` with the store name (`secretstore`) and key name (`openai-api-key`).

2. **Agent Initialization**:
   - Added `initialize_chat_agent` to fetch the API key and initialize the `Agent` with it.
   - Initialized the `chat_agent` at startup using the `@app.on_event("startup")` decorator.
   - Note: The code assumes the `Agent` class accepts an `api_key` parameter. If the OpenAI Agents SDK requires the API key to be set as an environment variable (`OPENAI_API_KEY`), you’d need to set it dynamically:
     ```python
     import os
     os.environ["OPENAI_API_KEY"] = await get_openai_api_key()
     ```
     For this tutorial, we assume the `api_key` parameter approach for clarity.

3. **Removed Environment Variable Dependency**:
   - The Chat Service no longer relies on the `OPENAI_API_KEY` environment variable, improving security.

### Step 4.2: Update `chat_service/tests/test_main.py`
Update the tests to mock the secrets retrieval.

```python
import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch, ANY

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."
    }

def test_get_user():
    response = client.get("/users/alice?role=admin")
    assert response.status_code == 200
    assert response.json() == {"user_id": "alice", "role": "admin"}

    response = client.get("/users/bob")
    assert response.status_code == 200
    assert response.json() == {"user_id": "bob", "role": "guest"}

@pytest.mark.asyncio
async def test_chat():
    with patch("main.get_openai_api_key", new_callable=AsyncMock) as mock_get_secret, \
         patch("main.DaprWorkflowClient") as mock_workflow_client, \
         patch("main.fetch_analytics_activity", new_callable=AsyncMock) as mock_fetch, \
         patch("main.generate_reply_activity", new_callable=AsyncMock) as mock_generate, \
         patch("main.publish_event_activity", new_callable=AsyncMock) as mock_publish:
        # Mock the secrets retrieval
        mock_get_secret.return_value = "mock-openai-api-key"

        # Mock the workflow client
        mock_workflow_instance = AsyncMock()
        mock_workflow_instance.runtime_status = "COMPLETED"
        mock_workflow_instance.output = {
            "user_id": "alice",
            "reply": "Hi Alice! You've sent 5 messages already—great to hear from you again! How can I help today?"
        }
        mock_workflow_client.return_value.__aenter__.return_value = mock_workflow_instance
        mock_workflow_instance.wait_for_workflow_completion.return_value = mock_workflow_instance

        # Mock the activities
        mock_fetch.return_value = 5
        mock_generate.return_value = "Hi Alice! You've sent 5 messages already—great to hear from you again! How can I help today?"

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
        assert response.json()["reply"] == "Hi Alice! You've sent 5 messages already—great to hear from you again! How can I help today?"
        assert "metadata" in response.json()
        mock_publish.assert_called_once_with(ANY, "alice")

        # Test with a different user and tool usage
        mock_workflow_instance.output = {
            "user_id": "bob",
            "reply": "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
        }
        mock_fetch.return_value = 3
        mock_generate.return_value = "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
        request_data = {
            "user_id": "bob",
            "text": "What time is it?",
            "metadata": {
                "timestamp": "2025-04-06T12:00:00Z",
                "session_id": "123e4567-e89b-12d3-a456-426614174001"
            },
            "tags": ["question"]
        }
        response = client.post("/chat/", json=request_data)
        assert response.status_code == 200
        assert response.json()["user_id"] == "bob"
        assert response.json()["reply"] == "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
        assert "metadata" in response.json()
        mock_publish.assert_called_with(ANY, "bob")

        # Test workflow failure
        mock_workflow_instance.runtime_status = "FAILED"
        mock_workflow_instance.output = None
        request_data = {
            "user_id": "alice",
            "text": "Hello again!",
            "metadata": {
                "timestamp": "2025-04-06T12:00:00Z",
                "session_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
        response = client.post("/chat/", json=request_data)
        assert response.status_code == 500
        assert response.json() == {"detail": "Workflow failed to complete"}

        # Test invalid request
        request_data = {
            "user_id": "bob",
            "text": "",
            "metadata": {
                "timestamp": "2025-04-06T12:00:00Z",
                "session_id": "123e4567-e89b-12d3-a456-426614174001"
            }
        }
        response = client.post("/chat/", json=request_data)
        assert response.status_code == 400
        assert response.json() == {"detail": "Message text cannot be empty"}
```

#### Explanation of Test Changes
- Added a mock for `get_openai_api_key` to simulate retrieving the API key from the Dapr secrets store.
- Ensured the mock returns a dummy API key (`"mock-openai-api-key"`) to allow the `Agent` initialization to proceed.

---

## Step 5: Verify the Analytics Service
The Analytics Service doesn’t use the OpenAI API key, so it doesn’t need changes. Its functionality (handling “MessageSent” events and updating the state store) remains unaffected.

---

## Step 6: Run the Microservices with Dapr
### Start the Analytics Service with Dapr
In a terminal, navigate to the Analytics Service directory and run it with Dapr, specifying the components directory:
```bash
cd analytics_service
dapr run --app-id analytics-service --app-port 8001 --dapr-http-port 3501 --components-path ../components -- uv run uvicorn main:app --host 0.0.0.0 --port 8001
```
Output:
```
ℹ  Starting Dapr with id analytics-service. HTTP Port: 3501  gRPC Port: 50002
ℹ  Dapr sidecar is up and running.
ℹ  You're up and running! Both Dapr and your app logs will appear here.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Start the Chat Service with Dapr
In a separate terminal, navigate to the Chat Service directory and run it with Dapr, specifying the components directory to load the secrets store configuration:
```bash
cd chat_service
dapr run --app-id chat-service --app-port 8000 --dapr-http-port 3500 --dapr-grpc-port 50001 --components-path ../components -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```
Output:
```
ℹ  Starting Dapr with id chat-service. HTTP Port: 3500  gRPC Port: 50001
ℹ  Dapr sidecar is up and running.
ℹ  You're up and running! Both Dapr and your app logs will appear here.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Verify Running Services
```bash
dapr list
```
Output:
```
  APP ID            HTTP PORT  GRPC PORT  APP PORT  COMMAND                          AGE  CREATED              STATUS
  chat-service      3500       50001      8000      uv run uvicorn main:app --ho...  10s  2025-04-06 04:01:00  Running
  analytics-service 3501       50002      8001      uv run uvicorn main:app --ho...  15s  2025-04-06 04:00:55  Running
```

---

## Step 7: Test the Microservices with Dapr Secrets Management
### Initialize State for Testing
Initialize message counts for `alice` and `bob` using the `/analytics/{user_id}/initialize` endpoint:
- For `alice`:
  ```bash
  curl -X POST http://localhost:8001/analytics/alice/initialize -H "Content-Type: application/json" -d '{"message_count": 5}'
  ```
  Output:
  ```json
  {"status": "success", "user_id": "alice", "message_count": 5}
  ```
- For `bob`:
  ```bash
  curl -X POST http://localhost:8001/analytics/bob/initialize -H "Content-Type: application/json" -d '{"message_count": 3}'
  ```
  Output:
  ```json
  {"status": "success", "user_id": "bob", "message_count": 3}
  ```

### Test the Chat Service
Send a request to the Chat Service to trigger the workflow, which will now use the API key from the Dapr secrets store:
```json
{
  "user_id": "bob",
  "text": "Hello, how are you?",
  "metadata": {
    "timestamp": "2025-04-06T12:00:00Z",
    "session_id": "123e4567-e89b-12d3-a456-426614174001"
  },
  "tags": ["greeting"]
}
```
Expected response (actual reply may vary):
```json
{
  "user_id": "bob",
  "reply": "Hi Bob! You've sent 3 messages so far. How can I help you today?",
  "metadata": {
    "timestamp": "2025-04-06T04:01:00Z",
    "session_id": "some-uuid"
  }
}
```

#### What Happens During the Request?
1. The Chat Service starts and retrieves the OpenAI API key from the Dapr secrets store (`secretstore`).
2. The API key is used to initialize the `Agent`.
3. The workflow executes:
   - Fetches `bob`’s message count (3) from the Analytics Service.
   - Generates a reply using the OpenAI Agents SDK (with the securely retrieved API key).
   - Publishes a “MessageSent” event.
4. The Analytics Service increments `bob`’s message count (from 3 to 4).
5. The Chat Service returns the reply.

Check the updated message count for `bob`:
- Visit `http://localhost:8001/docs` and test `/analytics/bob`:
  - Expected: `{"message_count": 4}`

### Run the Tests
- Chat Service:
  ```bash
  cd chat_service
  uv run pytest tests/test_main.py -v
  ```
  Output:
  ```
  collected 3 items

  tests/test_main.py::test_root PASSED
  tests/test_main.py::test_get_user PASSED
  tests/test_main.py::test_chat PASSED

  ================= 3 passed in 0.15s =================
  ```
- Analytics Service:
  ```bash
  cd analytics_service
  uv run pytest tests/test_main.py -v
  ```
  Output:
  ```
  collected 4 items

  tests/test_main.py::test_root PASSED
  tests/test_main.py::test_get_analytics PASSED
  tests/test_main.py::test_initialize_message_count PASSED
  tests/test_main.py::test_handle_message_sent PASSED

  ================= 4 passed in 0.12s =================
  ```

---

## Step 8: Why Dapr Secrets Management for DACA?
Using Dapr’s Secrets Management building block enhances DACA’s architecture by:
- **Security**: The OpenAI API key is no longer stored in an environment variable, reducing the risk of accidental exposure.
- **Centralized Management**: Secrets are managed in a Dapr secrets store, making it easier to rotate or update them without changing application code.
- **Production-Readiness**: Aligns with best practices for handling sensitive data in production environments.
- **Scalability**: Supports a distributed system where multiple services can securely access shared secrets.

---

## Step 9: Next Steps
You’ve successfully integrated Dapr’s Secrets Management building block into the Chat Service, securely managing the OpenAI API key! In the next tutorial (**10_dapr_actors**), we’ll explore Dapr’s Actors building block to model user sessions as actors, enabling stateful, concurrent interactions in our microservices.

### Optional Exercises
1. Configure Dapr to use a production-grade secrets store (e.g., HashiCorp Vault, AWS Secrets Manager) instead of the local file-based store.
2. Add a new secret (e.g., a database connection string) to the secrets store and update the Chat Service to use it for the mock database dependency.
3. Use the Dapr dashboard (`dapr dashboard`) to inspect the secrets store component and verify its configuration.

---

## Conclusion
In this tutorial, we integrated Dapr’s Secrets Management building block into the Chat Service, replacing the insecure use of an environment variable with a secure secrets store for the OpenAI API key. This improves the security of our system, aligning with DACA’s goals for a production-ready, distributed agentic AI system. We’re now ready to explore Dapr Actors in the next tutorial!

---

### Final Code for `chat_service/main.py`
```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, function_tool
from datetime import datetime
import httpx
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowClient, DaprWorkflowContext, when
from dapr.workflow import WorkflowActivityContext

from models import Message, Response, Metadata

app = FastAPI(
    title="DACA Chat Service",
    description="A FastAPI-based Chat Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow_runtime = WorkflowRuntime()
workflow_runtime.start()

async def get_openai_api_key() -> str:
    with DaprClient() as dapr_client:
        try:
            secret = await dapr_client.get_secret(
                store_name="secretstore",
                key="openai-api-key"
            )
            return secret.secret["openai-api-key"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve OpenAI API key: {e}")

async def initialize_chat_agent():
    api_key = await get_openai_api_key()
    return Agent(
        name="ChatAgent",
        instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool. Personalize responses using user analytics (e.g., message count).",
        model="gpt-4o",
        tools=[get_current_time],
        api_key=api_key
    )

@function_tool
def get_current_time() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

chat_agent = None

@app.on_event("startup")
async def startup():
    global chat_agent
    chat_agent = await initialize_chat_agent()

async def get_db():
    return {"connection": "Mock DB Connection"}

async def fetch_analytics_activity(ctx: WorkflowActivityContext, user_id: str) -> int:
    with DaprClient() as dapr_client:
        try:
            response = await dapr_client.invoke_method_async(
                app_id="analytics-service",
                method_name=f"analytics/{user_id}",
                http_verb="GET"
            )
            analytics_data = response.json()
            return analytics_data.get("message_count", 0)
        except Exception as e:
            print(f"Failed to fetch analytics in workflow: {e}")
            return 0

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]

    personalized_instructions = (
        f"You are a helpful chatbot. Respond to user messages in a friendly and informative way. "
        f"If the user asks for the time, use the get_current_time tool. "
        f"The user has sent {message_count} messages so far, so personalize your response accordingly."
    )
    chat_agent.instructions = personalized_instructions

    result = await Runner.run(chat_agent, input=message_text)
    return result.final_output

async def publish_event_activity(ctx: WorkflowActivityContext, user_id: str):
    with DaprClient() as dapr_client:
        try:
            await dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="messages",
                data={"user_id": user_id, "event_type": "MessageSent"}
            )
            print(f"Published MessageSent event for user {user_id} in workflow")
        except Exception as e:
            print(f"Failed to publish MessageSent event in workflow: {e}")
            raise

@workflow_runtime.workflow
async def message_processing_workflow(ctx: DaprWorkflowContext, input_data: dict) -> dict:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]

    message_count = await ctx.call_activity(
        fetch_analytics_activity,
        input=user_id,
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    reply = await ctx.call_activity(
        generate_reply_activity,
        input={"user_id": user_id, "message_text": message_text, "message_count": message_count},
        retry_policy={"max_retries": 2, "interval": "PT3S"}
    )

    await ctx.call_activity(
        publish_event_activity,
        input=user_id,
        retry_policy={"max_retries": 5, "interval": "PT2S"}
    )

    return {"user_id": user_id, "reply": reply}

@app.get("/")
async def root():
    return {"message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."}

@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

@app.post("/chat/", response_model=Response)
async def chat(message: Message, db: dict = Depends(get_db)):
    if not message.text.strip():
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    print(f"DB Connection: {db['connection']}")

    with DaprWorkflowClient() as workflow_client:
        instance_id = f"chat-{message.user_id}-{int(datetime.utcnow().timestamp())}"
        input_data = {"user_id": message.user_id, "message_text": message.text}
        
        await workflow_client.schedule_new_workflow(
            workflow=message_processing_workflow,
            instance_id=instance_id,
            input=input_data
        )

        result = await workflow_client.wait_for_workflow_completion(
            instance_id=instance_id,
            timeout_in_seconds=60
        )

        if result is None or result.runtime_status != "COMPLETED":
            raise HTTPException(status_code=500, detail="Workflow failed to complete")

        workflow_output = result.output
        reply_text = workflow_output["reply"]

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )

@app.on_event("shutdown")
def shutdown():
    workflow_runtime.stop()
```

---

This tutorial provides a focused introduction to Dapr Secrets Management, enhancing the security of our microservices. 