# Step 4.4: Fault Tolerance

This is the fourth sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by adding fault tolerance to handle state store failures (e.g., Redis timeouts). This introduces lightweight error handling and retry logic, ensuring reliable execution for AI agents, aligning with DACA’s goal of fault-tolerant systems.

## Overview

The **fault_tolerance** sub-step modifies the `ChatAgent` to:
- Add try-catch blocks with retry logic in `process_message` for state store operations.
- Simulate a state store failure to test recovery.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Fault tolerance ensures the actor recovers from transient errors, maintaining conversation reliability in a distributed system.

### Learning Objectives
- Implement retry logic for state store operations.
- Simulate and handle transient errors in actor methods.
- Understand fault tolerance in Dapr actors.
- Validate recovery from simulated failures.

### Ties to Step 4 Overview
- **Fault Tolerance**: This sub-step adds retry logic to handle state store failures, ensuring reliability.
- **Dapr’s Implementation**: Leverages Dapr’s state management with custom error handling.
- **Turn-Based Concurrency**: Ensures retries do not disrupt concurrent message processing.

## Key Concepts

### Dapr Actor Fault Tolerance
Dapr actors rely on the state store (Redis) for persistence. Transient failures (e.g., network timeouts) can disrupt state operations. Fault tolerance involves:
- Try-catch blocks to catch errors.
- Retry logic for transient failures.
- Logging to diagnose issues.

In this sub-step, `process_message` retries state store operations (get/set) up to 3 times with a 1-second delay, recovering from simulated failures.

### Lightweight Configuration
Fault tolerance is added with minimal changes:
- Retry logic in `process_message` for `get_state` and `set_state`.
- A simulated failure flag (for testing) to trigger errors.
- No additional dependencies or complex configurations.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Fault Tolerance**: Retries ensure state operations succeed despite transient failures.

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
The **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) are sufficient (see **Step 4.1** README for details).

### 2. Implement the ChatAgent with Fault Tolerance
Update the **Step 2** `main.py` to add retry logic for state operations and simulate failures.

**File**: `main.py`
```python
import logging
import json
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dapr.ext.fastapi import DaprActor
from dapr.actor import Actor, ActorInterface, ActorProxy, ActorId, actormethod
from dapr.clients import DaprClient

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="ChatAgentService", description="DACA Step 4.4: Fault Tolerance")

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
        self._simulate_failure = True  # Simulate failure on first state operation

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
        """Process a user message with retry logic for state operations."""
        try:
            logging.info(f"Processing message for {self._history_key}: {user_input}")
            # Load history with retry
            history = None
            for attempt in range(3):
                try:
                    if self._simulate_failure and attempt == 0:
                        self._simulate_failure = False
                        raise Exception("Simulated state store failure")
                    history = await self._state_manager.get_state(self._history_key)
                    break
                except Exception as e:
                    if attempt == 2:
                        logging.error(f"Failed to load history for {self._history_key} after 3 attempts: {e}")
                        raise
                    logging.warning(f"Retry {attempt + 1} for history load: {e}")
                    await asyncio.sleep(1)
            
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
            
            # Save updated history with retry
            for attempt in range(3):
                try:
                    await self._state_manager.set_state(self._history_key, current_history)
                    break
                except Exception as e:
                    if attempt == 2:
                        logging.error(f"Failed to save history for {self._history_key} after 3 attempts: {e}")
                        raise
                    logging.warning(f"Retry {attempt + 1} for history save: {e}")
                    await asyncio.sleep(1)
            
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

Use `curl` commands:
```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there"}'
curl http://localhost:8000/chat/user1/history
```

**Expected Output**:
- POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}]}`
- Logs: `Retry 1 for history load: Simulated state store failure`, followed by `Processed message for history-user1`

### 4. Understand the Code
Review the changes in `main.py`:
- **Retry Logic**: `process_message` retries `get_state` and `set_state` up to 3 times with 1-second delays.
- **Simulated Failure**: `_simulate_failure` triggers an error on the first state operation, testing retries.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.
- **Imports**: Added `asyncio` for retry delays.

The retry logic ensures state operations succeed despite transient failures, maintaining conversation reliability.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances. Monitor logs for `Retry` and `Processed message`.

## Validation
Verify fault tolerance:
1. **Message Processing**: POST to `/chat/user1` succeeds despite simulated failure.
2. **History Retrieval**: GET `/chat/user1/history` shows the correct history.
3. **Retry Logic**: Check logs for `Retry 1 for history load: Simulated state store failure`, followed by successful processing.
4. **State Consistency**: Verify history in Redis (`redis-cli GET history-user1`).
5. **Recovery**: Send multiple POSTs to confirm retries handle failures without data loss.

## Troubleshooting
- **Retries Failing**:
  - Check logs for `Retry` and `Failed to load history after 3 attempts`.
  - Verify Redis connectivity (`docker ps` or `kubectl get pods`).
- **History Not Saved**:
  - Confirm `set_state` retries in `process_message`.
  - Check Redis with `redis-cli GET history-user1`.
- **Simulated Failure Persists**:
  - Ensure `_simulate_failure` resets after the first attempt.
  - Check logs for `Simulated state store failure`.

## Key Takeaways
- **Fault Tolerance**: Retry logic ensures reliability against transient state store failures.
- **Lightweight Configuration**: Minimal changes (retry loops, simulated failure) add robustness.
- **DACA Alignment**: Supports fault-tolerant AI agents in distributed systems.
- **Error Handling**: Try-catch and retries maintain conversation continuity.

## Next Steps
- Explore **Step 5** (if defined) or experiment with Dapr retry policies in `statestore.yaml`.
- Test fault tolerance with real Redis failures (e.g., temporarily stop Redis).
- Add logging for successful retries to monitor recovery.

## Resources
- [Dapr Actor Fault Tolerance](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/#fault-tolerance)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)