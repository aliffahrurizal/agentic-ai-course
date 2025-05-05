# Step 4.2: Timers

This is the second sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by adding a Dapr actor timer to log the number of messages in the conversation history every 5 seconds. This introduces temporary periodic tasks, demonstrating how actors can perform lightweight monitoring tasks, aligning with DACA’s goal of scalable, concurrent AI agents.

## Overview

The **timers** sub-step modifies the `ChatAgent` to:
- Register a timer named `log_message_count` during actor activation.
- Implement a `log_message_count` method to log the current number of messages in the history.
- Trigger the timer every 5 seconds, stopping after 10 invocations (50 seconds).
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Timers are temporary, in-memory tasks that stop when the actor is deactivated, making them suitable for short-lived monitoring tasks like logging message counts.

### Learning Objectives
- Configure and register a Dapr actor timer.
- Implement a method to handle timer triggers.
- Understand temporary periodic tasks and their lifecycle.
- Validate periodic logging via console output.

### Ties to Step 4 Overview
- **Timers**: This sub-step implements a timer to log message counts periodically, showcasing temporary task scheduling.
- **Dapr’s Implementation**: Leverages Dapr’s actor timer feature for lightweight monitoring.
- **Turn-Based Concurrency**: Timers run concurrently with message processing, demonstrating actor concurrency.

## Key Concepts

### Dapr Actor Timers
Dapr actor timers are temporary, periodic tasks associated with an actor instance. They:
- Run in-memory and stop when the actor is deactivated.
- Trigger a specified method (e.g., `log_message_count`) at defined intervals.
- Are configured with a `dueTime` (initial delay) and `period` (repeat interval).

In this sub-step, the `ChatAgent` registers a `log_message_count` timer with a 5-second `dueTime` and `period`, logging the message count every 5 seconds for 10 invocations.

### Lightweight Configuration
The timer is added with minimal changes to the **Step 2** code:
- A new `log_message_count` method to log the history length.
- Timer registration in `_on_activate` using `self._timer_manager`.
- A counter to stop the timer after 10 invocations.
- No additional dependencies, keeping the configuration lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Periodic Task**: The `log_message_count` timer logs message counts every 5 seconds, independent of user interactions.

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
The **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) are sufficient. Verify their presence in `components/` (see **Step 4.1** README for details).

### 2. Implement the ChatAgent with Timers
Update the **Step 2** `main.py` to add a timer to the `ChatAgent`. The timer logs the message count every 5 seconds for 10 invocations.

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

app = FastAPI(title="ChatAgentService", description="DACA Step 4.2: Timers")

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

    @actormethod(name="LogMessageCount")
    async def log_message_count(self) -> None:
        pass

# Implement the actor
class ChatAgent(Actor, ChatAgentInterface):
    def __init__(self, ctx, actor_id):
        super().__init__(ctx, actor_id)
        self._history_key = f"history-{actor_id.id}"
        self._actor_id = actor_id
        self._timer_count = 0  # Track timer invocations

    async def _on_activate(self) -> None:
        """Initialize state and register timer on actor activation."""
        logging.info(f"Activating actor for {self._history_key}")
        try:
            history = await self._state_manager.get_state(self._history_key)
            if history is None:
                logging.info(f"State not found for {self._history_key}, initializing")
                await self._state_manager.set_state(self._history_key, [])
            else:
                logging.info(f"State found for {self._history_key}: {history}")
            
            # Register timer to log message count every 5 seconds
            await self._timer_manager.register_timer(
                timer_name="log_message_count",
                due_time="5s",
                period="5s"
            )
            logging.info(f"Registered log_message_count timer for {self._history_key}")
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

    async def log_message_count(self) -> None:
        """Log the number of messages in the history."""
        try:
            self._timer_count += 1
            history = await self._state_manager.get_state(self._history_key)
            message_count = len(history) if isinstance(history, list) else 0
            logging.info(f"Timer triggered for {self._history_key}: {message_count} messages in history")
            
            # Stop timer after 10 invocations (50 seconds)
            if self._timer_count >= 10:
                await self._timer_manager.unregister_timer("log_message_count")
                logging.info(f"Unregistered log_message_count timer for {self._history_key}")
        except Exception as e:
            logging.error(f"Error logging message count for {self._history_key}: {e}")
            raise

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
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hello"}'
# Monitor logs for 50 seconds
```

**Expected Output**:
- POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}, ...]}`
- Logs (every 5 seconds): `Timer triggered for history-user1: 4 messages in history`
- After 50 seconds: `Unregistered log_message_count timer for history-user1`

### 4. Understand the Code
Review the changes in `main.py`:
- **Actor Interface**: Added `LogMessageCount` method.
- **Timer Registration**: In `_on_activate`, `register_timer` schedules `log_message_count` every 5 seconds.
- **Log Message Count**: Counts history entries and logs them, stopping after 10 invocations.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.

The timer runs concurrently with message processing, logging the message count until stopped.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances. Monitor logs for `Timer triggered for history-user1`.

## Validation
Verify the timer functionality:
1. **Message Processing**: POST to `/chat/user1` adds messages.
2. **History Retrieval**: GET `/chat/user1/history` shows up to 5 entries.
3. **Timer Logging**: Check `dapr logs -a chat-agent` for `Timer triggered` every 5 seconds, showing the correct message count (e.g., `4 messages` after two POSTs).
4. **Timer Stop**: Confirm `Unregistered log_message_count timer` after 50 seconds.
5. **State Consistency**: Verify history persists in Redis (`redis-cli GET history-user1`).

## Troubleshooting
- **Timer Not Triggering**:
  - Check logs for `Registered log_message_count timer`.
  - Verify `due_time="5s"` and `period="5s"`.
  - Ensure actor is active (`dapr dashboard`).
- **Incorrect Message Count**:
  - Confirm `history` is loaded correctly in `log_message_count`.
  - Check Redis with `redis-cli GET history-user1`.
- **Timer Not Stopping**:
  - Verify `_timer_count >= 10` condition in `log_message_count`.
  - Check logs for `Unregistered log_message_count timer`.

## Key Takeaways
- **Temporary Timers**: Timers enable lightweight, periodic tasks like monitoring, stopping when the actor deactivates.
- **Lightweight Configuration**: Minimal changes (new method, timer registration) add monitoring functionality.
- **Concurrency**: Timers run alongside message processing, supporting turn-based concurrency.
- **DACA Alignment**: Enhances actor scalability with periodic tasks.

## Next Steps
- Proceed to **Step 4.3: Reentrancy** to enable concurrent message handling.
- Experiment with different timer intervals (e.g., `period="10s"`).
- Add a condition to stop the timer based on message count (e.g., `message_count >= 10`).

## Resources
- [Dapr Actor Timers](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/#timers)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)