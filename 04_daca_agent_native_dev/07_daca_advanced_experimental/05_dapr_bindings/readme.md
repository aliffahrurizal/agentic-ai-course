# Step 5: Bindings

This is **Step 5** of the **Dapr Agentic Cloud Ascent (DACA)** learning path, part of the **07_daca_advanced_experiments** module. In this step, you’ll enhance the `ChatAgent` actor from **Step 2** by integrating Dapr bindings to connect with external systems. Specifically, you’ll use a Kafka input binding to receive user messages and a Twilio output binding to send SMS notifications for conversation updates. This enables event-driven interactions, aligning with DACA’s goal of building scalable, event-driven AI agents.

## Overview

The **bindings** step modifies the `ChatAgent` to:
- Configure a Kafka input binding to receive user messages from a `user-messages` topic and process them via the `ChatAgent`.
- Configure a Twilio output binding to send SMS notifications when a conversation is updated.
- Test bindings by sending messages to Kafka and verifying SMS delivery.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Dapr bindings simplify integration with external systems, enabling the `ChatAgent` to operate in a broader event-driven ecosystem without direct service dependencies.

### Learning Objectives
- Configure Dapr input and output bindings for external system integration.
- Process messages from a Kafka topic using an input binding.
- Send notifications via a Twilio SMS output binding.
- Validate binding functionality with end-to-end message flow.
- Maintain lightweight changes with minimal code modifications.

### Ties to DACA
- **Event-Driven**: Bindings enable seamless integration with event-driven architectures.
- **Scalability**: Asynchronous message processing supports high-throughput AI agents.
- **Production-Readiness**: External system integration enhances real-world applicability for conversational AI.

## Key Concepts

### Dapr Bindings
Dapr bindings provide a standardized way to interact with external systems:
- **Input Bindings**: Trigger application logic (e.g., a FastAPI endpoint) when events arrive from external sources (e.g., Kafka, RabbitMQ).
- **Output Bindings**: Send data to external systems (e.g., Twilio, email, databases) without direct API calls.
- **Decoupling**: Bindings abstract external system details, simplifying integration and improving portability.

In this step, you’ll use:
- A Kafka input binding to receive messages from a `user-messages` topic, invoking a new `/receive-message` endpoint to process them via the `ChatAgent`.
- A Twilio output binding to send SMS notifications for conversation updates, triggered in `process_message`.

### Lightweight Configuration
Bindings are added with minimal changes:
- New Dapr component files (`kafka-binding.yaml`, `twilio-binding.yaml`) for Kafka and Twilio bindings.
- A new FastAPI endpoint (`/receive-message`) to handle Kafka input binding events.
- A small update to `process_message` to trigger the Twilio output binding.
- Dependencies (`confluent-kafka` for testing Kafka), with Twilio credentials stored in a Kubernetes secret.
- No changes to `get_conversation_history` or existing pub/sub, keeping the setup lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`, `/receive-message`) for message processing and history retrieval.
- **Event-Driven**: Kafka input binding for message ingestion, Twilio output binding for notifications, and pub/sub via `/subscribe` for `ConversationUpdated`.
- **External Integration**: Bindings enable asynchronous communication with Kafka and Twilio, enhancing the `ChatAgent`’s ecosystem.

## Does it make sense to use SQLModel or SQLAlchemy with Dapr for the database part, or should we use Dapr bindings?

Dapr bindings provide a way to interact with external systems (like databases) using a simplified, abstracted interface. For example, Dapr offers output bindings to write data to a database or input bindings to receive data from it. However, Dapr bindings are not a full replacement for ORMs like SQLModel or SQLAlchemy, as they serve different purposes:
- Use Dapr bindings if your application prioritizes simplicity, portability across different databases, or is heavily event-driven/microservices-based. For example, if you’re building a microservice that only needs to write or read simple data to/from a database, bindings are sufficient.
- Use SQLModel/SQLAlchemy if your application requires complex queries, transactions, or schema management, or if you’re working with a single database type (e.g., PostgreSQL) and need fine-grained control.
- Hybrid approach: You can combine both. For instance, use Dapr bindings for cross-service communication or simple database writes in a microservices setup, while using SQLAlchemy/SQLModel within a service for complex database operations. This approach is common in larger systems where different services have different needs.

[Dapr Binding and ORMs like SQLAlchemy/SQLModel: When to use each?](https://grok.com/share/bGVnYWN5_f0e338f0-92a5-4c60-8b41-504eb5279edb)

## Hands-On Dapr Virtual Actor

### 0. Setup Code
Use the [00_lab_starter_code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code) from **Step 2**. Ensure **Step 2** is complete and you have a Kubernetes cluster (e.g., `minikube`).

Install additional dependencies for Kafka testing:
```bash
uv add dapr dapr-ext-fastapi pydantic confluent-kafka
```

### 1. Configure External Systems
Set up Kafka and Twilio for bindings:
- **Kafka**: Deploy a Kafka cluster (e.g., using Strimzi or a managed service like Confluent Cloud). For simplicity, assume a local Kafka broker (`kafka:9092`) or a managed Kafka topic (`user-messages`).
- **Twilio**: Obtain Twilio credentials (Account SID, Auth Token, phone number). Create a Kubernetes secret for credentials (use secure values in production).

Create a Kubernetes secret for Twilio credentials:
```bash
kubectl create secret generic twilio-credentials --from-literal=accountSid='ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' --from-literal=authToken='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' --from-literal=fromNumber='+1234567890' -n default
```

### 2. Configure Dapr Components
Keep the **Step 2** components (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) unchanged (see **Step 4.1** README in **05_agent_actors**). Add binding components for Kafka and Twilio.

**File**: `components/kafka-binding.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-binding
  namespace: default
spec:
  type: bindings.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: topics
    value: "user-messages"
  - name: consumerGroup
    value: "chat-agent-group"
  - name: authRequired
    value: "false"
```

**File**: `components/twilio-binding.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: twilio-binding
  namespace: default
spec:
  type: bindings.twilio.sms
  version: v1
  metadata:
  - name: accountSid
    secretKeyRef:
      name: twilio-credentials
      key: accountSid
  - name: authToken
    secretKeyRef:
      name: twilio-credentials
      key: authToken
  - name: fromNumber
    secretKeyRef:
      name: twilio-credentials
      key: fromNumber
```

**File**: `components/secretstore.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

### 3. Update the ChatAgent Code
Update the **Step 2** `main.py` to:
- Add a `/receive-message` endpoint to handle Kafka input binding events, invoking the `ChatAgent`’s `process_message`.
- Modify `process_message` to trigger the Twilio output binding for SMS notifications.

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

app = FastAPI(title="ChatAgentService", description="DACA Step 8: Bindings")

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
            
            # Send SMS notification via Twilio output binding
            await self._send_sms_notification(user_input, response)
            
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

    async def _send_sms_notification(self, user_input: dict, response: dict) -> None:
        """Send an SMS notification via Twilio output binding."""
        sms_data = {
            "toNumber": "+1987654321",  # Replace with recipient number
            "body": f"New message from {self._actor_id.id}: {user_input['content']} -> {response['content']}"
        }
        with DaprClient() as client:
            try:
                client.invoke_binding(
                    binding_name="twilio-binding",
                    operation="create",
                    data=json.dumps(sms_data)
                )
                logging.info(f"Sent SMS for {self._history_key}: {sms_data}")
            except Exception as e:
                logging.error(f"Failed to send SMS: {e}")

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

# Binding endpoint for Kafka input
@app.post("/receive-message")
async def receive_kafka_message(data: dict):
    """Handle messages from Kafka input binding."""
    try:
        logging.info(f"Received Kafka message: {data}")
        actor_id = data.get("actor_id", "unknown")
        message = data.get("message", {})
        if not isinstance(message, dict) or "role" not in message or "content" not in message:
            raise HTTPException(status_code=400, detail="Invalid message format")
        proxy = ActorProxy.create("ChatAgent", ActorId(actor_id), ChatAgentInterface)
        response = await proxy.ProcessMessage(message)
        return {"status": "Message processed", "response": response}
    except Exception as e:
        logging.error(f"Error processing Kafka message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

### 4. Test the App
Port-forward the `ChatAgent` service to test:
```bash
kubectl port-forward svc/chat-agent 8000:8000 -n default
```

Test the **default** route group:
- **POST /chat/{actor_id}**: Sends a user message (for comparison with Kafka binding).
- **GET /chat/{actor_id}/history**: Retrieves the conversation history.
- **POST /receive-message**: Handles Kafka input binding events.
- **POST /subscribe**: Handles `user-chat` topic events.

#### Test Kafka Input Binding
Produce a message to the Kafka `user-messages` topic using a Python script or `kcat`:

**File**: `produce_message.py`
```python
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer = Producer({'bootstrap.servers': 'kafka:9092'})
message = {
    "actor_id": "user1",
    "message": {"role": "user", "content": "Hi from Kafka"}
}
producer.produce('user-messages', json.dumps(message).encode('utf-8'), callback=delivery_report)
producer.flush()
```

Run:
```bash
python produce_message.py
```

Verify the message is processed:
```bash
curl http://localhost:8000/chat/user1/history
```

#### Test Twilio Output Binding
Send a message via the FastAPI endpoint to trigger an SMS:
```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Test SMS"}'
```

Check your phone (recipient number `+1987654321`) for an SMS like:
```
New message from user1: Test SMS -> Got your message: Test SMS
```

**Expected Output**:
- Kafka POST: `{"status": "Message processed", "response": {"role": "assistant", "content": "Got your message: Hi from Kafka"}}`
- GET: `{"history": [{"role": "user", "content": "Hi from Kafka"}, {"role": "assistant", "content": "Got your message: Hi from Kafka"}, {"role": "user", "content": "Test SMS"}, {"role": "assistant", "content": "Got your message: Test SMS"}]}`
- Twilio SMS: Received on the recipient phone with the conversation update.
- Logs: `Received Kafka message`, `Sent SMS for history-user1` in `dapr logs -a chat-agent`.

### 5. Understand the Setup
Review the setup:
- **Code Changes**: Added `/receive-message` endpoint for Kafka input binding and `_send_sms_notification` for Twilio output binding in `main.py`.
- **Bindings Config**: `kafka-binding.yaml` receives messages from Kafka, `twilio-binding.yaml` sends SMS notifications.
- **Dependencies**: Added `confluent-kafka` for testing Kafka message production.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub from **Step 2**.

Bindings enable the `ChatAgent` to integrate with Kafka for message ingestion and Twilio for notifications, enhancing its event-driven capabilities.

### 6. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances (e.g., `1` for `user1`). Monitor logs (`dapr logs -a chat-agent`) for Kafka message processing (`Received Kafka message`) and SMS sending (`Sent SMS`).

## Validation
Verify bindings functionality:
1. **Kafka Input Binding**: Send a message to the `user-messages` topic and confirm `/receive-message` processes it, updating the history (GET `/chat/user1/history`).
2. **Twilio Output Binding**: Send a message via `/chat/user1` and verify an SMS is received on the recipient phone.
3. **History Retrieval**: GET `/chat/user1/history` shows messages from both Kafka and FastAPI endpoints.
4. **Pub/Sub Integration**: Confirm `/subscribe` logs `ConversationUpdated` events for Kafka and FastAPI messages.
5. **Logs**: Check `dapr logs -a chat-agent` for successful binding operations and no errors.

## Troubleshooting
- **Kafka Messages Not Received**:
  - Verify `kafka-binding.yaml` has correct `brokers` and `topics`.
  - Check Kafka broker status (`kubectl get pods` or Confluent Cloud dashboard).
  - Ensure `produce_message.py` connects to the correct broker.
- **SMS Not Sent**:
  - Confirm `twilio-binding.yaml` references valid credentials (`kubectl get secret twilio-credentials`).
  - Check Twilio dashboard for error logs or invalid `toNumber`.
  - Verify `_send_sms_notification` logs `Sent SMS`.
- **History Not Updated**:
  - Confirm `/receive-message` invokes `process_message` correctly.
  - Check Redis with `redis-cli GET history-user1` for updated history.

## Key Takeaways
- **Bindings**: Kafka input and Twilio output bindings enable event-driven integration with external systems.
- **Lightweight Configuration**: Dapr bindings require minimal code changes and component files.
- **Event-Driven**: Asynchronous message processing enhances scalability for AI agents.
- **DACA Alignment**: Supports scalable, event-driven systems for conversational AI.

## Next Steps
- Experiment with other bindings (e.g., RabbitMQ input, email output).
- Test bindings with high message volumes to verify scalability.
- Integrate with **Step 7** (serialization) to optimize state storage for Kafka messages.

## Resources
- [Dapr Bindings](https://docs.dapr.io/developing-applications/building-blocks/bindings/bindings-overview/)
- [Dapr Kafka Binding](https://docs.dapr.io/reference/components-reference/supported-bindings/kafka/)
- [Dapr Twilio Binding](https://docs.dapr.io/reference/components-reference/supported-bindings/twilio/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)