# Step 4.5: Partitioning

This is the fifth sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by configuring Dapr actor partitioning to distribute actor instances across multiple nodes or partitions. This improves scalability and load balancing for conversational AI agents, aligning with DACA’s goal of building scalable, distributed systems.

## Overview

The **partitioning** sub-step modifies the `ChatAgent` deployment to:
- Configure Dapr to use a partitioning strategy for actor placement.
- Update the actor configuration to specify partition count and placement strategy.
- Test the distribution of `ChatAgent` instances across partitions using multiple actor IDs.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Partitioning distributes actor instances across nodes, ensuring efficient resource utilization and scalability for high user loads.

### Learning Objectives
- Configure Dapr actor partitioning for scalability.
- Understand actor placement and load balancing.
- Validate actor distribution across partitions.
- Maintain lightweight changes to the actor implementation.

### Ties to Step 4 Overview
- **Dapr’s Implementation**: Leverages Dapr’s actor placement service for partitioning.
- **Fault Tolerance**: Partitioning enhances resilience by distributing load across nodes.
- **Turn-Based Concurrency**: Ensures partitioned actors maintain concurrent message processing.

## Key Concepts

### Dapr Actor Partitioning
Dapr’s actor placement service distributes actor instances across nodes or partitions based on a configured strategy. Key aspects:
- **Partition Count**: Defines the number of partitions (e.g., 10) for distributing actors.
- **Placement Strategy**: Dapr uses a hash-based strategy to map `ActorId` to partitions.
- **Scalability**: Partitioning balances load, allowing more actors to run concurrently.

In this sub-step, you’ll configure Dapr to use 10 partitions for `ChatAgent` instances, distributing actors like `user1`, `user2`, etc., across these partitions.

### Lightweight Configuration
Partitioning is added with minimal changes:
- A new Dapr configuration file (`actor-partitioning.yaml`) to specify partition count.
- No changes to the `ChatAgent` code, as partitioning is handled by Dapr’s runtime.
- Testing with multiple actor IDs to observe distribution.
- No additional dependencies, keeping the setup lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Partitioned Actors**: Actors are distributed across partitions, maintaining isolation and concurrency.

## Hands-On Dapr Virtual Actor

### 0. Setup Code
Use the [00_lab_starter_code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code) from **Step 2**. Ensure **Step 2** is complete.

Verify dependencies:
```bash
uv add dapr dapr-ext-fastapi pydantic
```

Start the application:
```bash
tilt up
```

### 1. Configure Dapr Components
The **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) are sufficient. Add a new configuration file for partitioning:

**File**: `components/actor-partitioning.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: actor-partitioning
  namespace: default
spec:
  actors:
    partitionCount: 10
```

Update your Dapr run command or Tilt configuration to include this file (e.g., ensure `components/` is mounted).

### 2. Implement the ChatAgent with Partitioning
No changes are needed to the **Step 2** `main.py`, as partitioning is handled by Dapr’s configuration. Use the **Step 2** code as-is:

**File**: `main.py`
```python
import logging
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dapr.ext.fastapi import DaprActor
from dapr.actor import Actor, ActorInterface, ActorProxy, ActorId, actormethod
from dapr.clients import DaprClient

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ChatAgentService", description="DACA Step 4.5: Partitioning")

# Add Dapr Actor Extension
actor = DaprActor(app)

class Message(BaseModel):
    role: str
    content: str

# Define the actor interface
class ChatAgentInterface(ActorInterface):
    @actormethod(name="ProcessMessage")
    async def process_message(self, user_input: dict) -> dict | None:
        pass

    @actormethod(name="GetConversationHistory")
    async def get_conversation_history(self) -> list[dict] | None:
        pass

# Implement the actor
class ChatAgent(Actor, ChatAgentInterface):
    def __init__(self, ctx, actor_id):
        super().__init__(ctx, actor_id)
        self._history_key = f"history-{actor_id.id}"
        self._actor_id = actor_id

    async def _on_activate(self) -> None:
        """Initialize state on actor activation."""
        logging.info(f"Activating actor for {self._history_key}")
        try:
            history = await self._state_manager.get_state(self._history_key)
            if history is None:
                logging.info(f"State not found for {self._history_key}, initializing")
                await self._state_manager.set_state(self._history_key, [])
            else:
                logging.info(f"State found for {self._history_key}: {history}")
        except Exception as e:
            logging.warning(f"Non-critical error in _on_activate: {e}")
            await self._state_manager.set_state(self._history_key, [])

    async def process_message(self, user_input: dict) -> dict:
        """Process a user message and append to history."""
        try:
            logging.info(f"Processing message for {self._history_key}: {user_input}")
            # Load history
            history = await self._state_manager.get_state(self._history_key)
            current_history = history if isinstance(history, list) else []
            
            # Append user message
            current_history.append(user_input)
            
            # Generate response
            response_content = f"Got your message: {user_input['content']}"
            response = {"role": "assistant", "content": response_content}
            
            # Append assistant response
            current_history.append(response)
            if len(current_history) > 5:  # Limit to last 5 exchanges
                current_history = current_history[-5:]
            
            # Save updated history
            await self._state_manager.set_state(self._history_key, current_history)
            logging.info(f"Processed message for {self._history_key}: {user_input['content']}")
            
            # Publish event
            await self._publish_conversation_event(user_input, response)
            
            return response
        except Exception as e:
            logging.error(f"Error processing message for {self._history_key}: {e}")
            raise

    async def _publish_conversation_event(self, user_input: dict, response: dict) -> None:
        """Publish a ConversationUpdated event to the user-chat topic."""
        # Note: publish_event is synchronous; consider asyncio.to_thread in future steps
        event_data = {
            "actor_id": self._actor_id.id,
            "history_key": self._history_key,
            "actor_type": "ChatAgent",
            "event_type": "ConversationUpdated",
            "input": user_input,
            "output": response
        }
        with DaprClient() as client:
            try:
                client.publish_event(
                    pubsub_name="daca-pubsub",
                    topic_name="user-chat",
                    data=json.dumps(event_data)
                )
                logging.info(f"Published event for {self._history_key}: {event_data}")
            except Exception as e:
                logging.error(f"Failed to publish event: {e}")

    async def get_conversation_history(self) -> list[dict]:
        """Retrieve conversation history."""
        try:
            history = await self._state_manager.get_state(self._history_key)
            return history if isinstance(history, list) else []
        except Exception as e:
            logging.error(f"Error getting history for {self._history_key}: {e}")
            return []

# Register the actor
@app.on_event("startup")
async def startup():
    await actor.register_actor(ChatAgent)
    logging.info(f"Registered actor: {ChatAgent.__name__}")

# FastAPI endpoints to invoke the actor
@app.post("/chat/{actor_id}")
async def process_message(actor_id: str, data: Message):
    """Process a user message for the actor."""
    if not data.content or not isinstance(data.content, str):
        raise HTTPException(status_code=400, detail="Invalid or missing 'content' field')
    message_dict = data.model_dump()
    proxy = ActorProxy.create("ChatAgent", ActorId(actor_id), ChatAgentInterface)
    response = await proxy.ProcessMessage(message_dict)
    return {"response": response}

@app.get("/chat/{actor_id}/history")
async def get_conversation_history(actor_id: str):
    """Retrieve the actor's conversation history."""
    proxy = ActorProxy.create("ChatAgent", ActorId(actor_id), ChatAgentInterface)
    history = await proxy.GetConversationHistory()
    return {"history": history}

# Subscription endpoint for pub/sub events
@app.post("/subscribe")
async def subscribe_message(data: dict):
    """Handle events from the user-chat topic."""
    try:
        logging.info(f"\n\n->[SUBSCRIPTION] Received event: {data}\n\n")
        event_data_raw = data.get("data", "{}")
        event_data = json.loads(event_data_raw)
        user_id = event_data.get("actor_id", "unknown")
        input_message = event_data.get("input", {}).get("content", "no message")
        output_message = event_data.get("output", {}).get("content", "no response")
        logging.info(f"Received event: User {user_id} sent '{input_message}', got '{output_message}'")
        return {"status": "Event processed"}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode event data: {e}")
        return {"status": "Invalid event data format"}
```

### 3. Test the App
Open the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

Test the **Actor** route group:
- **GET /healthz**: Verifies Dapr actor configuration.
- **GET /dapr/config**: Confirms `ChatAgent` is registered.

Test the **default** route group:
- **POST /chat/{actor_id}**: Sends a user message.
- **GET /chat/{actor_id}/history**: Retrieves the history.
- **POST /subscribe**: Handles `user-chat` events.

Use `curl` commands to test multiple actor IDs:
```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there"}'
curl -X POST http://localhost:8000/chat/user2 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hello"}'
curl -X POST http://localhost:8000/chat/user3 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hey"}'
curl http://localhost:8000/chat/user1/history
curl http://localhost:8000/chat/user2/history
curl http://localhost:8000/chat/user3/history
```

**Expected Output**:
- POST user1: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- POST user2: `{"response": {"role": "assistant", "content": "Got your message: Hello"}}`
- POST user3: `{"response": {"role": "assistant", "content": "Got your message: Hey"}}`
- GET user1: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}]}`
- GET user2: `{"history": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Got your message: Hello"}]}`
- GET user3: `{"history": [{"role": "user", "content": "Hey"}, {"role": "assistant", "content": "Got your message: Hey"}]}`

### 4. Understand the Code
Review the setup:
- **No Code Changes**: The **Step 2** `main.py` is unchanged, as partitioning is configured via Dapr.
- **Partitioning Config**: `actor-partitioning.yaml` sets `partitionCount: 10`, distributing actors across 10 partitions.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.
- **Actor Distribution**: Dapr’s placement service maps `user1`, `user2`, `user3` to different partitions based on `ActorId`.

Partitioning is handled transparently by Dapr, requiring only a configuration file.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances (e.g., `3` for `user1`, `user2`, `user3`). Use `dapr logs -a chat-agent` to confirm each actor’s activation (`Activating actor for history-userX`).

## Validation
Verify partitioning functionality:
1. **Message Processing**: POST to `/chat/user1`, `/chat/user2`, `/chat/user3` succeeds.
2. **History Isolation**: GET `/chat/userX/history` shows separate histories for each `ActorId`.
3. **Actor Distribution**: Check `dapr dashboard` for multiple `ChatAgent` instances, indicating distribution across partitions.
4. **Logs**: Verify `Activating actor for history-userX` for each user in `dapr logs -a chat-agent`.
5. **State Consistency**: Use `redis-cli` to confirm separate keys (`GET history-user1`, `GET history-user2`, `GET history-user3`).

## Troubleshooting
- **Actors Not Distributed**:
  - Check logs for `Activating actor` for each `ActorId`.
  - Verify `actor-partitioning.yaml` is loaded (`partitionCount: 10`).
  - Restart Dapr: `dapr stop --app-id chat-agent` and rerun `tilt up`.
- **History Not Isolated**:
  - Confirm `history_key` uses unique `ActorId` (`history-userX`).
  - Check Redis with `redis-cli KEYS history-*`.
- **Dashboard Issues**:
  - Ensure `dapr dashboard` is running and connected to the correct cluster.

## Key Takeaways
- **Partitioning**: Distributes actors across partitions for scalability and load balancing.
- **Lightweight Configuration**: A single config file enables partitioning without code changes.
- **Scalability**: Supports high user loads by balancing actor instances.
- **DACA Alignment**: Enhances scalability for distributed AI agents.

## Next Steps
- Proceed to **Step 4.6: Namespacing** to isolate actors by namespace.
- Experiment with different `partitionCount` values (e.g., `5` or `20`).
- Deploy multiple Dapr instances to observe partitioning across nodes.

## Resources
- [Dapr Actor Placement](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/#actor-placement)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)