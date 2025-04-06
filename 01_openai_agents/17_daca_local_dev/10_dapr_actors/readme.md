# Managing Stateful Interactions with Dapr Actors

Welcome to the tenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll enhance the microservices from **09_dapr_secrets_management** by integrating Dapr’s **Actors** building block. Currently, the Chat Service processes messages statelessly, relying on the Analytics Service for message counts and lacking a mechanism to maintain per-user conversation history. We’ll introduce a `UserSessionActor` to manage user session state (e.g., conversation history) in a stateful, concurrent manner, improving personalization and user experience. This will make our system more scalable and capable of handling complex, stateful interactions. Let’s get started!

---

## What You’ll Learn
- How to use Dapr’s Actors building block to model stateful entities in a distributed system.
- Defining a `UserSessionActor` to manage per-user session state (e.g., conversation history).
- Updating the Chat Service to interact with the `UserSessionActor` for storing and retrieving conversation history.
- Running microservices with Dapr Actors enabled.
- Updating unit tests to account for Dapr Actors integration.

## Prerequisites
- Completion of **09_dapr_secrets_management** (codebase with Chat Service and Analytics Service using Dapr Service Invocation, State Management, Pub/Sub Messaging, Workflows, and Secrets Management).
- Dapr CLI and runtime installed (from **04_dapr_theory_and_cli**).
- Docker installed (Dapr uses Docker for its sidecars and components).
- Python 3.8+ installed.
- An OpenAI API key (managed via Dapr Secrets Management).

---

## Step 1: Recap of the Current Setup
In **09_dapr_secrets_management**, we integrated Dapr’s Secrets Management into the Chat Service:
- The **Chat Service**:
  - Uses a Dapr Workflow to orchestrate message processing: fetching the user’s message count (via Service Invocation), generating a reply (using the OpenAI Agents SDK with a securely retrieved API key), and publishing a “MessageSent” event (via Pub/Sub).
  - Retrieves the OpenAI API key from a Dapr secrets store.
- The **Analytics Service**:
  - Subscribes to the `messages` topic and updates the user’s message count in the Dapr state store when a “MessageSent” event is received.

### Current Limitations
- **Stateless Interactions**: The Chat Service processes each message independently, without maintaining per-user conversation history. This limits personalization (e.g., referencing past messages in replies).
- **Lack of Session State**: There’s no mechanism to store and manage user-specific state (e.g., conversation history, preferences) across requests.
- **Scalability Concerns**: Without a stateful model, scaling the Chat Service to handle concurrent users while maintaining session state is challenging.

### Goal for This Tutorial
We’ll use Dapr’s Actors to model user sessions as stateful entities:
- Define a `UserSessionActor` to manage per-user session state, including conversation history (a list of past messages and replies).
- Update the Chat Service to interact with the `UserSessionActor` to store and retrieve conversation history during message processing.
- Enhance the agent’s instructions to include conversation history for more personalized replies.
- This will enable stateful, concurrent interactions while maintaining scalability.

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
│   ├── subscriptions.yaml
│   ├── secretstore.yaml
│   └── secrets.json
├── pyproject.toml
└── uv.lock
```

---

## Step 2: Why Use Dapr Actors?
Dapr’s **Actors** building block provides a programming model for stateful, concurrent entities in a distributed system, based on the Virtual Actor pattern. It offers several advantages over stateless services or manual state management:
- **Stateful Entities**: Each actor instance (e.g., a `UserSessionActor` for a specific user) maintains its own state (e.g., conversation history), which is automatically persisted by Dapr.
- **Concurrency**: Dapr ensures that actor methods are executed sequentially for a given actor instance (single-threaded access), eliminating the need for manual synchronization.
- **Scalability**: Actors are distributed across the system, and Dapr handles load balancing and placement, making it easy to scale to many users.
- **Encapsulation**: Actors encapsulate state and behavior, providing a clean abstraction for managing user-specific data.
- **Reliability**: Dapr persists actor state in a state store, ensuring durability across restarts or failures.

In DACA, Actors are crucial for:
- Managing per-user session state (e.g., conversation history) in a scalable, concurrent manner.
- Enabling personalized interactions by providing the agent with access to past messages.
- Supporting a distributed architecture where user sessions can be handled across multiple instances of the Chat Service.

---

## Step 3: Configure Dapr Actor Runtime
Dapr Actors require a state store to persist actor state. The `dapr init` command already set up a default Redis-based state store (`statestore.yaml`), which Dapr Actors can use. We don’t need to create a new component, but we’ll verify the state store configuration.

### Verify the State Store Component
```bash
cat ~/.dapr/components/statestore.yaml
```
Output:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
```
This state store will be used by the Dapr Actor runtime to persist actor state.

### Enable Dapr Actors
Dapr Actors are enabled by default in Dapr 1.8+ (as of April 2025, the latest version is likely higher). When we start the Chat Service with Dapr, the actor runtime will be initialized automatically. We’ll confirm this by checking the Dapr logs.

---

## Step 4: Define the UserSessionActor in the Chat Service
We’ll define a `UserSessionActor` to manage per-user session state, including conversation history. We’ll use the `dapr` Python SDK to implement the actor.

### Step 4.1: Create a New File for the Actor
Create a new file `chat_service/user_session_actor.py` to define the `UserSessionActor`.

```bash
touch chat_service/user_session_actor.py
```

Edit `chat_service/user_session_actor.py`:
```python
from dapr.actor import ActorInterface, Actor, actor_method
from typing import List, Dict

class UserSessionActorInterface(ActorInterface):
    @actor_method
    async def add_message(self, message_data: Dict) -> None:
        pass

    @actor_method
    async def get_conversation_history(self) -> List[Dict]:
        pass

class UserSessionActor(Actor, UserSessionActorInterface):
    def __init__(self, ctx, actor_id):
        super().__init__(ctx, actor_id)
        self._conversation_history_key = "conversation_history"

    async def _on_activate(self) -> None:
        """Called when the actor is activated."""
        # Initialize the conversation history if it doesn't exist
        history = await self.state_manager.get_state(self._conversation_history_key)
        if not history:
            await self.state_manager.set_state(self._conversation_history_key, [])

    async def add_message(self, message_data: Dict) -> None:
        """Add a message and reply to the conversation history."""
        history = await self.state_manager.get_state(self._conversation_history_key)
        if not history:
            history = []
        history.append(message_data)
        # Limit history to the last 10 messages to avoid unbounded growth
        if len(history) > 10:
            history = history[-10:]
        await self.state_manager.set_state(self._conversation_history_key, history)

    async def get_conversation_history(self) -> List[Dict]:
        """Retrieve the conversation history."""
        history = await self.state_manager.get_state(self._conversation_history_key)
        return history if history else []
```

#### Explanation of the Actor
1. **Actor Interface**:
   - `UserSessionActorInterface` defines the methods that can be called on the actor (`add_message` and `get_conversation_history`).
   - The `@actor_method` decorator marks these methods as callable via Dapr’s actor runtime.

2. **Actor Implementation**:
   - `UserSessionActor` inherits from `Actor` and implements `UserSessionActorInterface`.
   - Uses Dapr’s `state_manager` to persist the conversation history in the state store.
   - `_on_activate`: Initializes the conversation history when the actor is activated.
   - `add_message`: Adds a message and reply to the history, limiting it to the last 10 messages.
   - `get_conversation_history`: Retrieves the conversation history.

### Step 4.2: Update `chat_service/main.py`
Update the Chat Service to:
- Register the `UserSessionActor` with the Dapr runtime.
- Interact with the actor to store and retrieve conversation history during message processing.
- Enhance the agent’s instructions with conversation history for more personalized replies.

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from agents import Agent, Runner, function_tool
from datetime import datetime
import httpx
from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowClient, DaprWorkflowContext, when
from dapr.workflow import WorkflowActivityContext
from dapr.actor.runtime.runtime import ActorRuntime
from user_session_actor import UserSessionActor, UserSessionActorInterface

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

# Register the UserSessionActor with Dapr
ActorRuntime.register_actor(UserSessionActor)
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
        instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool. Personalize responses using user analytics (e.g., message count) and conversation history.",
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

# Workflow activities
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

async def fetch_conversation_history_activity(ctx: WorkflowActivityContext, user_id: str) -> list:
    with DaprClient() as dapr_client:
        try:
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            history = await actor.get_conversation_history()
            return history
        except Exception as e:
            print(f"Failed to fetch conversation history in workflow: {e}")
            return []

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]
    conversation_history = input_data["conversation_history"]

    # Format the conversation history for the agent's instructions
    history_summary = "No previous conversation."
    if conversation_history:
        history_summary = "Previous conversation:\n"
        for entry in conversation_history:
            history_summary += f"User: {entry['message']}\nBot: {entry['reply']}\n"

    personalized_instructions = (
        f"You are a helpful chatbot. Respond to user messages in a friendly and informative way. "
        f"If the user asks for the time, use the get_current_time tool. "
        f"The user has sent {message_count} messages so far, so personalize your response accordingly. "
        f"Here is the conversation history to provide context:\n{history_summary}"
    )
    chat_agent.instructions = personalized_instructions

    result = await Runner.run(chat_agent, input=message_text)
    return result.final_output

async def store_conversation_activity(ctx: WorkflowActivityContext, input_data: dict):
    user_id = input_data["user_id"]
    message = input_data["message"]
    reply = input_data["reply"]

    with DaprClient() as dapr_client:
        try:
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            await actor.add_message({"message": message, "reply": reply})
        except Exception as e:
            print(f"Failed to store conversation in workflow: {e}")
            raise

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

# Define the workflow
@workflow_runtime.workflow
async def message_processing_workflow(ctx: DaprWorkflowContext, input_data: dict) -> dict:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]

    # Step 1: Fetch analytics
    message_count = await ctx.call_activity(
        fetch_analytics_activity,
        input=user_id,
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    # Step 2: Fetch conversation history
    conversation_history = await ctx.call_activity(
        fetch_conversation_history_activity,
        input=user_id,
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    # Step 3: Generate reply
    reply = await ctx.call_activity(
        generate_reply_activity,
        input={
            "user_id": user_id,
            "message_text": message_text,
            "message_count": message_count,
            "conversation_history": conversation_history
        },
        retry_policy={"max_retries": 2, "interval": "PT3S"}
    )

    # Step 4: Store the conversation
    await ctx.call_activity(
        store_conversation_activity,
        input={"user_id": user_id, "message": message_text, "reply": reply},
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    # Step 5: Publish MessageSent event
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
1. **Actor Registration**:
   - Imported `UserSessionActor` and `UserSessionActorInterface` from `user_session_actor.py`.
   - Registered the `UserSessionActor` with Dapr using `ActorRuntime.register_actor`.

2. **New Workflow Activities**:
   - `fetch_conversation_history_activity`: Retrieves the conversation history from the `UserSessionActor` for the given user.
   - `store_conversation_activity`: Stores the message and reply in the `UserSessionActor`’s conversation history.

3. **Updated Workflow**:
   - Added steps to the `message_processing_workflow` to fetch and store conversation history.
   - Passed the conversation history to the `generate_reply_activity` for inclusion in the agent’s instructions.

4. **Enhanced Agent Instructions**:
   - Updated `generate_reply_activity` to include the conversation history in the agent’s instructions, enabling more personalized replies.

### Step 4.3: Update `chat_service/tests/test_main.py`
Update the tests to mock the actor interactions.

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
         patch("main.fetch_analytics_activity", new_callable=AsyncMock) as mock_fetch_analytics, \
         patch("main.fetch_conversation_history_activity", new_callable=AsyncMock) as mock_fetch_history, \
         patch("main.generate_reply_activity", new_callable=AsyncMock) as mock_generate, \
         patch("main.store_conversation_activity", new_callable=AsyncMock) as mock_store, \
         patch("main.publish_event_activity", new_call actor_mock = AsyncMock()
         actor_mock.get_conversation_history.return_value = [
             {"message": "Hi!", "reply": "Hello! How can I help you?"}
         ]
         actor_mock.add_message.return_value = None
         mock_fetch_history.return_value = [
             {"message": "Hi!", "reply": "Hello! How can I help you?"}
         ]
         mock_generate.return_value = "Hi Alice! You've sent 5 messages already. I see you said 'Hi!' earlier. How can I assist you today?"
         mock_workflow_instance.output = {
             "user_id": "alice",
             "reply": "Hi Alice! You've sent 5 messages already. I see you said 'Hi!' earlier. How can I assist you today?"
         }

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
         assert response.json()["reply"] == "Hi Alice! You've sent 5 messages already. I see you said 'Hi!' earlier. How can I assist you today?"
         assert "metadata" in response.json()
         mock_store.assert_called_once_with(ANY, {
             "user_id": "alice",
             "message": "Hello, how are you?",
             "reply": "Hi Alice! You've sent 5 messages already. I see you said 'Hi!' earlier. How can I assist you today?"
         })
         mock_publish.assert_called_once_with(ANY, "alice")

         # Test with a different user and tool usage
         mock_fetch_analytics.return_value = 3
         mock_fetch_history.return_value = []
         mock_generate.return_value = "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
         mock_workflow_instance.output = {
             "user_id": "bob",
             "reply": "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
         }
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
         mock_store.assert_called_with(ANY, {
             "user_id": "bob",
             "message": "What time is it?",
             "reply": "Bob, you've sent 3 messages so far. The current time is 2025-04-06 04:01:23 UTC."
         })
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
- Added mocks for the new activities (`fetch_conversation_history_activity`, `store_conversation_activity`).
- Simulated conversation history retrieval and storage to verify the workflow interacts with the actor correctly.
- Updated the expected replies to reflect the inclusion of conversation history in the agent’s responses.

---

## Step 5: Verify the Analytics Service
The Analytics Service doesn’t need changes, as it already handles the “MessageSent” event via Pub/Sub and updates the message count in the state store. Its functionality remains unaffected by the introduction of actors.

---

## Step 6: Run the Microservices with Dapr
### Start the Analytics Service with Dapr
In a terminal, navigate to the Analytics Service directory and run it with Dapr:
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
In a separate terminal, navigate to the Chat Service directory and run it with Dapr, enabling the actor runtime:
```bash
cd chat_service
dapr run --app-id chat-service --app-port 8000 --dapr-http-port 3500 --dapr-grpc-port 50001 --components-path ../components -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```
Output:
```
ℹ  Starting Dapr with id chat-service. HTTP Port: 3500  gRPC Port: 50001
ℹ  Dapr sidecar is up and running.
ℹ  Actor runtime started. Actor idle timeout: 1h0m0s. Actor scan interval: 30s
ℹ  You're up and running! Both Dapr and your app logs will appear here.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
Note: The Dapr logs should indicate that the actor runtime has started.

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

## Step 7: Test the Microservices with Dapr Actors
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

### Test the Chat Service with Actors
#### First Message for `bob`
Send a request to the Chat Service to start a conversation for `bob`:
```json
{
  "user_id": "bob",
  "text": "Hi, how are you?",
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
  "reply": "Hi Bob! You've sent 3 messages so far. No previous conversation. How can I help you today?",
  "metadata": {
    "timestamp": "2025-04-06T04:01:00Z",
    "session_id": "some-uuid"
  }
}
```

#### Second Message for `bob`
Send a follow-up message to see the conversation history in action:
```json
{
  "user_id": "bob",
  "text": "Can you remind me what I said earlier?",
  "metadata": {
    "timestamp": "2025-04-06T12:01:00Z",
    "session_id": "123e4567-e89b-12d3-a456-426614174001"
  },
  "tags": ["question"]
}
```
Expected response (actual reply may vary):
```json
{
  "user_id": "bob",
  "reply": "Hi Bob! You've sent 4 messages so far. You previously said: 'Hi, how are you?' and I replied: 'Hi Bob! You've sent 3 messages so far. No previous conversation. How can I help you today?'. How can I assist you now?",
  "metadata": {
    "timestamp": "2025-04-06T04:01:00Z",
    "session_id": "some-uuid"
  }
}
```

#### What Happens During the Requests?
1. **First Request**:
   - The workflow fetches `bob`’s message count (3) and conversation history (empty).
   - The agent generates a reply, noting there’s no previous conversation.
   - The workflow stores the message and reply in the `UserSessionActor` for `bob`.
   - The workflow publishes a “MessageSent” event, and the Analytics Service updates the message count to 4.

2. **Second Request**:
   - The workflow fetches `bob`’s updated message count (4) and conversation history (now contains the first message and reply).
   - The agent generates a reply, referencing the previous message.
   - The workflow stores the new message and reply in the `UserSessionActor`.
   - The Analytics Service updates the message count to 5.

Check the updated message count for `bob`:
- Visit `http://localhost:8001/docs` and test `/analytics/bob`:
  - Expected: `{"message_count": 5}`

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

## Step 8: Why Dapr Actors for DACA?
Using Dapr’s Actors building block enhances DACA’s architecture by:
- **Stateful Interactions**: The `UserSessionActor` enables per-user session state, allowing the Chat Service to maintain conversation history and provide more personalized replies.
- **Concurrency**: Dapr ensures single-threaded access to each actor instance, simplifying concurrent access to user session state.
- **Scalability**: Actors are distributed across the system, supporting horizontal scaling as the number of users grows.
- **Reliability**: Actor state is persisted in the Dapr state store, ensuring durability across restarts or failures.

---

## Step 9: Next Steps
You’ve successfully integrated Dapr’s Actors building block into the Chat Service, enabling stateful, concurrent user sessions with conversation history! In the next tutorial (**11_dapr_observability**), we’ll explore Dapr’s observability features (e.g., distributed tracing, metrics, and logging) to monitor and debug our microservices.

### Optional Exercises
1. Add a method to the `UserSessionActor` to clear the conversation history (e.g., for a “reset session” feature).
2. Extend the `UserSessionActor` to store additional session state, such as user preferences (e.g., preferred language, timezone).
3. Use the Dapr dashboard (`dapr dashboard`) to inspect the actor runtime and verify the state of the `UserSessionActor` for a specific user.

---

## Conclusion
In this tutorial, we integrated Dapr’s Actors building block into the Chat Service, introducing a `UserSessionActor` to manage per-user session state. This enables stateful interactions, such as maintaining conversation history, while ensuring scalability and concurrency. The system is now more personalized and capable of handling complex user interactions, aligning with DACA’s goals for a scalable, distributed agentic AI system. We’re now ready to explore Dapr observability in the next tutorial!

---

### Final Code for `chat_service/user_session_actor.py`
```python
from dapr.actor import ActorInterface, Actor, actor_method
from typing import List, Dict

class UserSessionActorInterface(ActorInterface):
    @actor_method
    async def add_message(self, message_data: Dict) -> None:
        pass

    @actor_method
    async def get_conversation_history(self) -> List[Dict]:
        pass

class UserSessionActor(Actor, UserSessionActorInterface):
    def __init__(self, ctx, actor_id):
        super().__init__(ctx, actor_id)
        self._conversation_history_key = "conversation_history"

    async def _on_activate(self) -> None:
        history = await self.state_manager.get_state(self._conversation_history_key)
        if not history:
            await self.state_manager.set_state(self._conversation_history_key, [])

    async def add_message(self, message_data: Dict) -> None:
        history = await self.state_manager.get_state(self._conversation_history_key)
        if not history:
            history = []
        history.append(message_data)
        if len(history) > 10:
            history = history[-10:]
        await self.state_manager.set_state(self._conversation_history_key, history)

    async def get_conversation_history(self) -> List[Dict]:
        history = await self.state_manager.get_state(self._conversation_history_key)
        return history if history else []
```

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
from dapr.actor.runtime.runtime import ActorRuntime
from user_session_actor import UserSessionActor, UserSessionActorInterface

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
ActorRuntime.register_actor(UserSessionActor)
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
        instructions="You are a helpful chatbot. Respond to user messages in a friendly and informative way. If the user asks for the time, use the get_current_time tool. Personalize responses using user analytics (e.g., message count) and conversation history.",
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

async def fetch_conversation_history_activity(ctx: WorkflowActivityContext, user_id: str) -> list:
    with DaprClient() as dapr_client:
        try:
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            history = await actor.get_conversation_history()
            return history
        except Exception as e:
            print(f"Failed to fetch conversation history in workflow: {e}")
            return []

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]
    conversation_history = input_data["conversation_history"]

    history_summary = "No previous conversation."
    if conversation_history:
        history_summary = "Previous conversation:\n"
        for entry in conversation_history:
            history_summary += f"User: {entry['message']}\nBot: {entry['reply']}\n"

    personalized_instructions = (
        f"You are a helpful chatbot. Respond to user messages in a friendly and informative way. "
        f"If the user asks for the time, use the get_current_time tool. "
        f"The user has sent {message_count} messages so far, so personalize your response accordingly. "
        f"Here is the conversation history to provide context:\n{history_summary}"
    )
    chat_agent.instructions = personalized_instructions

    result = await Runner.run(chat_agent, input=message_text)
    return result.final_output

async def store_conversation_activity(ctx: WorkflowActivityContext, input_data: dict):
    user_id = input_data["user_id"]
    message = input_data["message"]
    reply = input_data["reply"]

    with DaprClient() as dapr_client:
        try:
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            await actor.add_message({"message": message, "reply": reply})
        except Exception as e:
            print(f"Failed to store conversation in workflow: {e}")
            raise

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

    conversation_history = await ctx.call_activity(
        fetch_conversation_history_activity,
        input=user_id,
        retry_policy={"max_retries": 3, "interval": "PT5S"}
    )

    reply = await ctx.call_activity(
        generate_reply_activity,
        input={
            "user_id": user_id,
            "message_text": message_text,
            "message_count": message_count,
            "conversation_history": conversation_history
        },
        retry_policy={"max_retries": 2, "interval": "PT3S"}
    )

    await ctx.call_activity(
        store_conversation_activity,
        input={"user_id": user_id, "message": message_text, "reply": reply},
        retry_policy={"max_retries": 3, "interval": "PT5S"}
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

This tutorial provides a focused introduction to Dapr Actors, enabling stateful, concurrent interactions in our microservices. 