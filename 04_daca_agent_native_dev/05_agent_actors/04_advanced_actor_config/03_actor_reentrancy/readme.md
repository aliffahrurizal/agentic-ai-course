# Step 4.3: Reentrancy

This is the third sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by enabling reentrancy to handle follow-up messages concurrently. This introduces concurrent message processing, allowing the actor to respond to multiple messages in a single interaction, aligning with DACA’s goal of turn-based concurrency for responsive AI agents.

## Overview

The **reentrancy** sub-step modifies the `ChatAgent` to:
- Enable reentrancy in Dapr configuration to allow concurrent method calls.
- Modify `process_message` to make a self-call to `process_follow_up` for a follow-up message.
- Implement a `process_follow_up` method to generate a secondary response.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Reentrancy allows the actor to process multiple messages (e.g., a user message and a follow-up) concurrently, improving responsiveness for interactive AI agents.

### Learning Objectives
- Enable Dapr actor reentrancy for concurrent message handling.
- Implement self-calls within an actor to trigger follow-up actions.
- Understand turn-based concurrency in Dapr’s actor model.
- Validate concurrent message processing.

### Ties to Step 4 Overview
- **Reentrancy**: This sub-step enables concurrent message handling, supporting turn-based concurrency.
- **Dapr’s Implementation**: Leverages Dapr’s reentrancy feature for responsive actors.
- **Turn-Based Concurrency**: Demonstrates how actors can process multiple messages in a single interaction.

## Key Concepts

### Dapr Actor Reentrancy
Dapr actor reentrancy allows an actor to process multiple method calls concurrently, rather than strictly one at a time. It:
- Requires enabling reentrancy in the actor’s configuration.
- Supports self-calls (e.g., `process_message` calling `process_follow_up`).
- Ensures state consistency by serializing state access.

In this sub-step, the `ChatAgent` makes a self-call to `process_follow_up` after processing a user message, appending a follow-up response to the history.

### Lightweight Configuration
Reentrancy is added with minimal changes:
- A new `process_follow_up` method to generate a follow-up response.
- A self-call in `process_message` using `ActorProxy`.
- A Dapr configuration file (`actor-config.yaml`) to enable reentrancy.
- No additional dependencies, keeping the setup lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Concurrent Processing**: Reentrancy allows `process_message` and `process_follow_up` to run concurrently, appending multiple responses.

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
The **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) are sufficient. Add a new configuration file to enable reentrancy:

**File**: `components/actor-config.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: actor-config
  namespace: default
spec:
  actors:
    reentrancy:
      enabled: true
```

Update your Dapr run command or Tilt configuration to include this file (e.g., ensure `components/` is mounted).

### 2. Implement the ChatAgent with Reentrancy
Update the **Step 2** `main.py` to add reentrancy support and a follow-up message.

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

app = FastAPI(title="ChatAgentService", description="DACA Step 4.3: Reentrancy")

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

    @actormethod(name="ProcessFollowUp")
    async def process_follow_up(self) -> dict | None:
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
        """Process a user message, append to history, and trigger follow-up."""
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
            
            # Trigger follow-up message via self-call
            proxy = ActorProxy.create("ChatAgent", self._actor_id, ChatAgentInterface)
            follow_up = await proxy.ProcessFollowUp()
            return response
        except Exception as e:
            logging.error(f"Error processing message for {self._history_key}: {e}")
            raise

    async def process_follow_up(self) -> dict:
        """Generate a follow-up response."""
        try:
            logging.info(f"Processing follow-up for {self._history_key}")
            # Load history
            history = await self._state_manager.get_state(self._history_key)
            current_history = history if isinstance(history, list) else []
            
            # Generate follow-up response
            follow_up_content = "Anything else I can help with?"
            follow_up = {"role": "assistant", "content": follow_up_content}
            
            # Append follow-up response
            current_history.append(follow_up)
            if len(current_history) > 5:  # Limit to last 5 exchanges
                current_history = current_history[-5:]
            
            # Save updated history
            await self._state_manager.set_state(self._history_key, current_history)
            logging.info(f"Processed follow-up for {self._history_key}: {follow_up_content}")
            
            return follow_up
        except Exception as e:
            logging.error(f"Error processing follow-up for {self._history_key}: {e}")
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
- GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}, {"role": "assistant", "content": "Anything else I can help with?"}]}`
- Logs: `Processed follow-up for history-user1: Anything else I can help with?`

### 4. Understand the Code
Review the changes in `main.py`:
- **Actor Interface**: Added `ProcessFollowUp` method.
- **Reentrancy**: Enabled via `actor-config.yaml`.
- **Self-Call**: `process_message` calls `process_follow_up` using `ActorProxy`.
- **Follow-Up Method**: `process_follow_up` adds a secondary response to the history.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.

Reentrancy allows `process_follow_up` to run concurrently, appending the follow-up response to the history.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances. Monitor logs for `Processed follow-up for history-user1`.

## Validation
Verify reentrancy functionality:
1. **Message Processing**: POST to `/chat/user1` triggers both `process_message` and `process_follow_up`.
2. **History Retrieval**: GET `/chat/user1/history` includes the user message, initial response, and follow-up response.
3. **Concurrent Processing**: Check logs for `Processed message` followed by `Processed follow-up`, confirming concurrent execution.
4. **State Consistency**: Verify history in Redis (`redis-cli GET history-user1`) includes all three entries.

## Troubleshooting
- **Follow-Up Not Triggered**:
  - Check logs for `Processing follow-up for history-user1`.
  - Verify `actor-config.yaml` enables reentrancy.
  - Ensure `ActorProxy` self-call in `process_message`.
- **History Missing Follow-Up**:
  - Confirm `process_follow_up` saves to `current_history`.
  - Check Redis with `redis-cli GET history-user1`.
- **Reentrancy Error**:
  - Verify `components/actor-config.yaml` is loaded.
  - Restart Dapr: `dapr stop --app-id chat-agent` and rerun `tilt up`.

## Key Takeaways
- **Reentrancy**: Enables concurrent message handling, improving responsiveness.
- **Lightweight Configuration**: Minimal changes (new method, config file) add concurrency.
- **Turn-Based Concurrency**: Self-calls allow multiple responses in a single interaction.
- **DACA Alignment**: Supports responsive, concurrent AI agents.

## Next Steps
- Proceed to **Step 4.4: Fault Tolerance** to add error handling.
- Experiment with multiple follow-up messages (e.g., chain additional self-calls).
- Test reentrancy with rapid POSTs to `/chat/user1`.

## Resources
- [Dapr Actor Reentrancy](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/#reentrancy)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)