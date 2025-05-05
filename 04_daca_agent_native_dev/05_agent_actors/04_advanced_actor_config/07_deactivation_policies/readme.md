# Step 4.8: Deactivation Policies

This is the eighth sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by configuring a Dapr actor deactivation policy to automatically deactivate idle actor instances after 1 minute. This optimizes resource usage for conversational AI agents, aligning with DACA’s goal of building efficient, scalable systems.

## Overview

The **deactivation_policies** sub-step configures the `ChatAgent` to:
- Set an idle timeout of 1 minute for actor deactivation using a Dapr configuration.
- Test the deactivation policy by invoking the `ChatAgent`, waiting for inactivity, and confirming the actor is deactivated.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Deactivation policies ensure that inactive actor instances are removed from memory, freeing resources while maintaining state in the Redis store for reactivation.

### Learning Objectives
- Configure Dapr actor deactivation policies for resource efficiency.
- Understand actor lifecycle management (activation/deactivation).
- Validate actor deactivation after idle periods.
- Maintain lightweight changes with no actor code modifications.

### Ties to Step 4 Overview
- **Dapr’s Implementation**: Leverages Dapr’s actor runtime for lifecycle management.
- **Fault Tolerance**: Ensures state persistence across deactivation/reactivation.
- **Turn-Based Concurrency**: Maintains concurrent message processing during active periods.

## Key Concepts

### Dapr Actor Deactivation Policies
Dapr Virtual Actors have a lifecycle managed by activation (when invoked) and deactivation (when idle). Deactivation policies:
- **Idle Timeout**: Specifies how long an actor can remain idle before deactivation (e.g., `60s`).
- **State Persistence**: Actor state (e.g., conversation history) is saved in the state store (Redis) before deactivation, allowing seamless reactivation.
- **Resource Efficiency**: Deactivation frees memory and CPU resources, critical for scaling AI agents with many users.

In this sub-step, you’ll configure a 1-minute idle timeout for `ChatAgent`, ensuring inactive actors (e.g., `user1`) are deactivated while preserving their history in Redis.

### Lightweight Configuration
Deactivation policies are added with minimal changes:
- A new Dapr configuration file (`actor-deactivation.yaml`) to set `actorIdleTimeout` to `60s`.
- No changes to the `ChatAgent` code, as deactivation is handled by Dapr’s runtime.
- Testing with actor invocations and idle periods to observe deactivation.
- No additional dependencies, keeping the setup lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Lifecycle Management**: Actors deactivate after 1 minute of inactivity, reactivating on new requests.

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
The **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) are sufficient (see **Step 4.1** README for details). Add a new configuration file for deactivation policies:

**File**: `components/actor-deactivation.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: actor-deactivation
  namespace: default
spec:
  actors:
    actorIdleTimeout: "60s"
    actorScanInterval: "10s"
```

- `actorIdleTimeout: "60s"`: Deactivates actors after 1 minute of inactivity.
- `actorScanInterval: "10s"`: Checks for idle actors every 10 seconds.

Update your Dapr run command or Tilt configuration to include this file (e.g., ensure `components/` is mounted).

### 2. Use the Step 2 ChatAgent Code
No changes are needed to the **Step 2** `main.py`, as deactivation is handled by Dapr’s configuration. Use the **Step 2** code as-is:

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

app = FastAPI(title="ChatAgentService", description="DACA Step 4.8: Deactivation Policies")

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

Use `curl` commands to test deactivation:
```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there"}'
curl http://localhost:8000/chat/user1/history
# Wait 70 seconds (60s timeout + 10s scan interval)
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hello"}'
curl http://localhost:8000/chat/user1/history
```

**Expected Output**:
- First POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- First GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}]}`
- Second POST (after 70s): `{"response": {"role": "assistant", "content": "Got your message: Hello"}}`
- Second GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}, {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Got your message: Hello"}]}`
- Logs: `Activating actor for history-user1` on first POST, no activation after 70s until second POST, indicating deactivation and reactivation.

### 4. Understand the Setup
Review the setup:
- **No Code Changes**: The **Step 2** `main.py` is unchanged, as deactivation is configured via Dapr.
- **Deactivation Config**: `actor-deactivation.yaml` sets `actorIdleTimeout: "60s"` and `actorScanInterval: "10s"`.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.
- **Lifecycle**: Actors deactivate after 1 minute of inactivity, reactivating with preserved state on new requests.

Deactivation policies optimize resource usage without affecting state persistence.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances. Initially, see `1` instance for `user1` after the first POST. After 70 seconds, the instance should disappear (deactivated). After the second POST, a new instance appears, with logs showing `Activating actor for history-user1`.

## Validation
Verify deactivation policies:
1. **Message Processing**: POST to `/chat/user1` succeeds.
2. **History Retrieval**: GET `/chat/user1/history` shows the correct history before and after deactivation.
3. **Deactivation**: Wait 70 seconds after the first POST, then check `dapr dashboard` to confirm no `ChatAgent` instances for `user1`.
4. **Reactivation**: POST again and confirm the actor reactivates, with history preserved in Redis (`redis-cli GET history-user1`).
5. **Logs**: Check `dapr logs -a chat-agent` for `Activating actor` on the first and second POSTs, with no activity during the idle period.

## Troubleshooting
- **Actor Not Deactivated**:
  - Verify `actor-deactivation.yaml` has `actorIdleTimeout: "60s"`.
  - Check `actorScanInterval: "10s"` and wait at least 70 seconds.
  - Ensure no background requests keep the actor active.
- **State Not Preserved**:
  - Confirm `statestore.yaml` is configured correctly.
  - Check Redis with `redis-cli GET history-user1`.
- **Dashboard Issues**:
  - Ensure `dapr dashboard` is connected to the correct cluster.
  - Check `kubectl get pods` for Dapr sidecars.

## Key Takeaways
- **Deactivation Policies**: Idle timeouts optimize resource usage by deactivating inactive actors.
- **Lightweight Configuration**: A single config file enables deactivation without code changes.
- **State Persistence**: Redis ensures history is preserved across deactivation/reactivation.
- **DACA Alignment**: Enhances efficiency and scalability for AI agents.

## Next Steps
- Explore **Step 5** (e.g., state encryption, middleware) or experiment with different idle timeouts (e.g., `30s`, `5m`).
- Test deactivation with multiple users (`user1`, `user2`) to confirm independent lifecycles.
- Combine with **Step 4.5** (partitioning) to optimize resource usage in a distributed setup.

## Resources
- [Dapr Actor Lifecycle](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/#actor-lifecycle)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)