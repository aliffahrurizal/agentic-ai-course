# Monitoring and Debugging with Dapr Observability

Welcome to the eleventh tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll enhance the microservices from **10_dapr_actors** by integrating Dapr’s observability features. Currently, our Chat Service and Analytics Service use Dapr’s building blocks (Service Invocation, State Management, Pub/Sub Messaging, Workflows, Secrets Management, and Actors) to process messages, but we lack visibility into their interactions, performance, and potential issues. We’ll enable Dapr’s distributed tracing, metrics, and logging to monitor and debug our system, ensuring we can maintain and optimize it effectively in production. Let’s get started!

---

## What You’ll Learn
- How to enable Dapr’s observability features: distributed tracing, metrics, and logging.
- Configuring Dapr to export traces and metrics to observability tools (e.g., Zipkin for tracing, Prometheus for metrics).
- Setting up logging to capture detailed information about service interactions.
- Using observability tools to monitor and debug the Chat Service and Analytics Service.
- Updating unit tests to account for observability (if applicable).

## Prerequisites
- Completion of **10_dapr_actors** (codebase with Chat Service and Analytics Service using Dapr Service Invocation, State Management, Pub/Sub Messaging, Workflows, Secrets Management, and Actors).
- Dapr CLI and runtime installed (from **04_dapr_theory_and_cli**).
- Docker installed (Dapr uses Docker for observability tools like Zipkin and Prometheus).
- Python 3.8+ installed.
- Familiarity with observability concepts (e.g., tracing, metrics, logging).

---

## Step 1: Recap of the Current Setup
In **10_dapr_actors**, we integrated Dapr’s Actors into the Chat Service:
- The **Chat Service**:
  - Uses a Dapr Workflow to orchestrate message processing: fetching the user’s message count (via Service Invocation), retrieving conversation history (via Actors), generating a reply (using the OpenAI Agents SDK), storing the conversation (via Actors), and publishing a “MessageSent” event (via Pub/Sub).
  - Retrieves the OpenAI API key from a Dapr secrets store.
  - Uses a `UserSessionActor` to manage per-user conversation history.
- The **Analytics Service**:
  - Subscribes to the `messages` topic and updates the user’s message count in the Dapr state store when a “MessageSent” event is received.

### Current Limitations
- **Lack of Visibility**: We can’t easily trace requests across services (e.g., from the Chat Service to the Analytics Service) or identify where failures occur.
- **Performance Monitoring**: There’s no mechanism to measure latency, throughput, or error rates for our services and Dapr components.
- **Debugging Challenges**: Without detailed logs or traces, debugging issues (e.g., workflow failures, actor state inconsistencies) is difficult.
- **Production Readiness**: Observability is critical for monitoring and maintaining a production system, but our current setup lacks these capabilities.

### Goal for This Tutorial
We’ll enable Dapr’s observability features to monitor and debug our microservices:
- Configure distributed tracing with Zipkin to trace requests across services.
- Set up metrics collection with Prometheus to monitor performance (e.g., request latency, error rates).
- Enhance logging to capture detailed information about service interactions.
- Use observability tools to gain insights into the system’s behavior and troubleshoot issues.

### Current Project Structure
```
fastapi-daca-tutorial/
├── chat_service/
│   ├── main.py
│   ├── user_session_actor.py
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

## Step 2: Why Use Dapr Observability?
Dapr provides built-in observability features to monitor and debug distributed systems, including:
- **Distributed Tracing**: Tracks requests as they flow through services and Dapr components, helping identify bottlenecks and failures.
- **Metrics**: Collects performance metrics (e.g., request latency, error rates) for services and Dapr components, enabling monitoring and alerting.
- **Logging**: Captures detailed logs of Dapr sidecar and application interactions, aiding in debugging.

In DACA, observability is crucial for:
- Gaining visibility into the interactions between the Chat Service, Analytics Service, and Dapr components (e.g., workflows, actors).
- Monitoring performance to ensure the system meets scalability and reliability goals.
- Debugging issues in a distributed environment, such as workflow failures or actor state inconsistencies.
- Preparing the system for production by enabling monitoring and alerting.

---

## Step 3: Enable Distributed Tracing with Zipkin
Dapr supports distributed tracing out of the box and can export traces to various backends, such as Zipkin, Jaeger, or OpenTelemetry Collector. We’ll use **Zipkin** for this tutorial because it’s lightweight and easy to set up.

### Step 3.1: Run Zipkin with Docker
Start a Zipkin instance using Docker:
```bash
docker run -d -p 9411:9411 openzipkin/zipkin
```
- This runs Zipkin on port `9411`, which we’ll use to visualize traces.

Verify Zipkin is running:
```bash
docker ps
```
Output should include:
```
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                    NAMES
abc123def456   openzipkin/zipkin   "start-zipkin"          10 seconds ago  Up 10 seconds  9410/tcp, 9411/tcp       some-container-name
```

Access the Zipkin UI at `http://localhost:9411` to confirm it’s running.

### Step 3.2: Configure Dapr for Tracing
Dapr uses a configuration file to enable tracing and specify the backend. Create a `tracing.yaml` file in the `components` directory.

```bash
touch components/tracing.yaml
```

Edit `components/tracing.yaml`:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing
spec:
  tracing:
    samplingRate: "1"  # Sample 100% of requests (1 = 100%, 0 = 0%)
    zipkin:
      endpointAddress: "http://localhost:9411/api/v2/spans"
```
- `samplingRate: "1"`: Ensures all requests are traced (for production, you might lower this to reduce overhead).
- `endpointAddress`: Points to the Zipkin instance running on `localhost:9411`.

### Step 3.3: Apply the Tracing Configuration When Running Dapr
When starting the services with Dapr, we’ll specify the `--config` flag to apply the `tracing.yaml` configuration. Dapr will automatically instrument requests with tracing headers and export traces to Zipkin.

---

## Step 4: Enable Metrics Collection with Prometheus
Dapr exposes metrics in Prometheus format, which can be scraped and visualized using Prometheus and Grafana. We’ll set up Prometheus to collect metrics from Dapr sidecars.

### Step 4.1: Run Prometheus with Docker
Create a `prometheus.yml` configuration file for Prometheus in the project root.

```bash
touch prometheus.yml
```

Edit `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dapr'
    static_configs:
      - targets: ['localhost:9090']  # Dapr metrics endpoint (we’ll configure the port)
```

Start Prometheus using Docker:
```bash
docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

Verify Prometheus is running:
```bash
docker ps
```
Output should include:
```
CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS         PORTS                    NAMES
xyz789abc123   prom/prometheus   "/bin/prometheus --c..." 10 seconds ago  Up 10 seconds  0.0.0.0:9090->9090/tcp  some-container-name
```

Access the Prometheus UI at `http://localhost:9090` to confirm it’s running. You can query metrics once Dapr is configured to expose them.

### Step 4.2: Configure Dapr for Metrics
Dapr exposes metrics by default on port `9090` (or a port specified via `--metrics-port`). We don’t need a separate configuration file for metrics, but we’ll ensure the Dapr sidecars expose metrics when we start the services.

---

## Step 5: Enhance Logging
Dapr provides detailed logs for its sidecars, which include interactions with components (e.g., state store, pub/sub, actors). We’ll also add application-level logging in the Chat Service and Analytics Service to capture key events.

### Step 5.1: Configure Dapr Logging
Dapr logs are controlled by the `--log-level` flag when running `dapr run`. We’ll set it to `debug` for detailed logs during development:
- `--log-level debug`: Captures detailed information about Dapr sidecar operations.

### Step 5.2: Add Application-Level Logging
We’ll use Python’s `logging` module to add structured logging to the Chat Service and Analytics Service.

#### Update `chat_service/main.py`
Add logging to capture key events (e.g., workflow steps, actor interactions).

```python
import logging
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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ChatService")

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
            logger.info("Fetching OpenAI API key from secrets store")
            secret = await dapr_client.get_secret(
                store_name="secretstore",
                key="openai-api-key"
            )
            return secret.secret["openai-api-key"]
        except Exception as e:
            logger.error(f"Failed to retrieve OpenAI API key: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve OpenAI API key: {e}")

async def initialize_chat_agent():
    api_key = await get_openai_api_key()
    logger.info("Initializing chat agent with OpenAI API key")
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
            logger.info(f"Fetching analytics for user {user_id}")
            response = await dapr_client.invoke_method_async(
                app_id="analytics-service",
                method_name=f"analytics/{user_id}",
                http_verb="GET"
            )
            analytics_data = response.json()
            message_count = analytics_data.get("message_count", 0)
            logger.info(f"Fetched message count for user {user_id}: {message_count}")
            return message_count
        except Exception as e:
            logger.error(f"Failed to fetch analytics for user {user_id}: {e}")
            return 0

async def fetch_conversation_history_activity(ctx: WorkflowActivityContext, user_id: str) -> list:
    with DaprClient() as dapr_client:
        try:
            logger.info(f"Fetching conversation history for user {user_id}")
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            history = await actor.get_conversation_history()
            logger.info(f"Fetched conversation history for user {user_id}: {history}")
            return history
        except Exception as e:
            logger.error(f"Failed to fetch conversation history for user {user_id}: {e}")
            return []

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]
    conversation_history = input_data["conversation_history"]

    logger.info(f"Generating reply for user {user_id} with message: {message_text}")
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
    reply = result.final_output
    logger.info(f"Generated reply for user {user_id}: {reply}")
    return reply

async def store_conversation_activity(ctx: WorkflowActivityContext, input_data: dict):
    user_id = input_data["user_id"]
    message = input_data["message"]
    reply = input_data["reply"]

    with DaprClient() as dapr_client:
        try:
            logger.info(f"Storing conversation for user {user_id}")
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            await actor.add_message({"message": message, "reply": reply})
            logger.info(f"Stored conversation for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to store conversation for user {user_id}: {e}")
            raise

async def publish_event_activity(ctx: WorkflowActivityContext, user_id: str):
    with DaprClient() as dapr_client:
        try:
            logger.info(f"Publishing MessageSent event for user {user_id}")
            await dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="messages",
                data={"user_id": user_id, "event_type": "MessageSent"}
            )
            logger.info(f"Published MessageSent event for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to publish MessageSent event for user {user_id}: {e}")
            raise

@workflow_runtime.workflow
async def message_processing_workflow(ctx: DaprWorkflowContext, input_data: dict) -> dict:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]

    logger.info(f"Starting workflow for user {user_id} with message: {message_text}")
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

    logger.info(f"Completed workflow for user {user_id}")
    return {"user_id": user_id, "reply": reply}

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    return {"message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."}

@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    logger.info(f"Fetching user info for user_id: {user_id}, role: {role}")
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

@app.post("/chat/", response_model=Response)
async def chat(message: Message, db: dict = Depends(get_db)):
    if not message.text.strip():
        logger.warning("Received empty message text")
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    logger.info(f"Received chat request for user {message.user_id}: {message.text}")
    print(f"DB Connection: {db['connection']}")

    with DaprWorkflowClient() as workflow_client:
        instance_id = f"chat-{message.user_id}-{int(datetime.utcnow().timestamp())}"
        input_data = {"user_id": message.user_id, "message_text": message.text}
        
        logger.info(f"Scheduling workflow with instance_id: {instance_id}")
        await workflow_client.schedule_new_workflow(
            workflow=message_processing_workflow,
            instance_id=instance_id,
            input=input_data
        )

        logger.info(f"Waiting for workflow {instance_id} to complete")
        result = await workflow_client.wait_for_workflow_completion(
            instance_id=instance_id,
            timeout_in_seconds=60
        )

        if result is None or result.runtime_status != "COMPLETED":
            logger.error(f"Workflow {instance_id} failed to complete: {result.runtime_status if result else 'None'}")
            raise HTTPException(status_code=500, detail="Workflow failed to complete")

        workflow_output = result.output
        reply_text = workflow_output["reply"]
        logger.info(f"Workflow {instance_id} completed with reply: {reply_text}")

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down Chat Service")
    workflow_runtime.stop()
```

#### Update `analytics_service/main.py`
Add logging to the Analytics Service.

```python
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from models import Analytics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AnalyticsService")

app = FastAPI(
    title="DACA Analytics Service",
    description="A FastAPI-based Analytics Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_message_count(user_id: str, dapr_port: int = 3501) -> int:
    dapr_url = f"http://localhost:{dapr_port}/v1.0/state/statestore/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Fetching message count for user {user_id} from state store")
            response = await client.get(dapr_url)
            response.raise_for_status()
            state_data = response.json()
            message_count = state_data.get("message_count", 0) if state_data else 0
            logger.info(f"Fetched message count for user {user_id}: {message_count}")
            return message_count
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to retrieve state for user {user_id}: {e}")
            return 0

async def set_message_count(user_id: str, message_count: int, dapr_port: int = 3501):
    dapr_url = f"http://localhost:{dapr_port}/v1.0/state/statestore"
    state_data = [
        {
            "key": user_id,
            "value": {"message_count": message_count}
        }
    ]
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Setting message count for user {user_id} to {message_count}")
            response = await client.post(dapr_url, json=state_data)
            response.raise_for_status()
            logger.info(f"Set message count for user {user_id}: {message_count}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to set state for user {user_id}: {e}")

async def increment_message_count(user_id: str, dapr_port: int = 3501):
    logger.info(f"Incrementing message count for user {user_id}")
    current_count = await get_message_count(user_id, dapr_port)
    new_count = current_count + 1
    await set_message_count(user_id, new_count, dapr_port)
    logger.info(f"Incremented message count for user {user_id} to {new_count}")

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    return {"message": "Welcome to the DACA Analytics Service! Access /docs for the API documentation."}

@app.get("/analytics/{user_id}", response_model=Analytics)
async def get_analytics(user_id: str):
    logger.info(f"Fetching analytics for user {user_id}")
    message_count = await get_message_count(user_id)
    if message_count == 0 and user_id not in ["alice", "bob"]:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return Analytics(message_count=message_count)

@app.post("/analytics/{user_id}/initialize")
async def initialize_message_count(user_id: str, message_count: int):
    logger.info(f"Initializing message count for user {user_id} to {message_count}")
    await set_message_count(user_id, message_count)
    return {"status": "success", "user_id": user_id, "message_count": message_count}

@app.post("/messages")
async def handle_message_sent(event: dict):
    logger.info(f"Received event: {event}")
    event_type = event.get("event_type")
    user_id = event.get("user_id")

    if event_type != "MessageSent" or not user_id:
        logger.warning(f"Ignoring invalid event: {event}")
        return {"status": "ignored"}

    await increment_message_count(user_id)
    logger.info(f"Processed MessageSent event for user {user_id}")
    return {"status": "success"}
```

#### Explanation of Logging Changes
- Added the `logging` module to both services with a structured format (`%(asctime)s - %(name)s - %(levelname)s - %(message)s`).
- Used `logger.info`, `logger.warning`, and `logger.error` to log key events, such as:
  - Request handling (e.g., `/chat/`, `/analytics/{user_id}`).
  - Workflow steps (e.g., fetching analytics, generating replies).
  - Actor interactions (e.g., fetching/storing conversation history).
  - Errors (e.g., failed API calls, workflow failures).

---

## Step 6: Run the Microservices with Observability Enabled
### Start the Analytics Service with Dapr
In a terminal, navigate to the Analytics Service directory and run it with Dapr, enabling tracing and metrics:
```bash
cd analytics_service
dapr run --app-id analytics-service --app-port 8001 --dapr-http-port 3501 --metrics-port 9091 --log-level debug --config ../components/tracing.yaml --components-path ../components -- uv run uvicorn main:app --host 0.0.0.0 --port 8001
```
- `--metrics-port 9091`: Exposes Dapr metrics on port `9091`.
- `--log-level debug`: Enables detailed Dapr logs.
- `--config ../components/tracing.yaml`: Applies the tracing configuration.

Output:
```
ℹ  Starting Dapr with id analytics-service. HTTP Port: 3501  gRPC Port: 50002
ℹ  Dapr sidecar is up and running.
ℹ  Metrics server started on 9091
ℹ  You're up and running! Both Dapr and your app logs will appear here.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Start the Chat Service with Dapr
In a separate terminal, navigate to the Chat Service directory and run it with Dapr, enabling tracing and metrics:
```bash
cd chat_service
dapr run --app-id chat-service --app-port 8000 --dapr-http-port 3500 --dapr-grpc-port 50001 --metrics-port 9090 --log-level debug --config ../components/tracing.yaml --components-path ../components -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```
- `--metrics-port 9090`: Exposes Dapr metrics on port `9090`.
- `--log-level debug`: Enables detailed Dapr logs.
- `--config ../components/tracing.yaml`: Applies the tracing configuration.

Output:
```
ℹ  Starting Dapr with id chat-service. HTTP Port: 3500  gRPC Port: 50001
ℹ  Dapr sidecar is up and running.
ℹ  Actor runtime started. Actor idle timeout: 1h0m0s. Actor scan interval: 30s
ℹ  Metrics server started on 9090
ℹ  You're up and running! Both Dapr and your app logs will appear here.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Update Prometheus Configuration
Since we’re running Dapr metrics on ports `9090` (Chat Service) and `9091` (Analytics Service), update `prometheus.yml` to scrape both ports:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dapr'
    static_configs:
      - targets: ['localhost:9090', 'localhost:9091']
```

Restart Prometheus to apply the updated configuration:
```bash
docker stop <prometheus-container-id>
docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```

---

## Step 7: Test the Microservices and Observe Behavior
### Initialize State for Testing
Initialize message counts for `alice` and `bob`:
- For `alice`:
  ```bash
  curl -X POST http://localhost:8001/analytics/alice/initialize -H "Content-Type: application/json" -d '{"message_count": 5}'
  ```
- For `bob`:
  ```bash
  curl -X POST http://localhost:8001/analytics/bob/initialize -H "Content-Type: application/json" -d '{"message_count": 3}'
  ```

### Test the Chat Service
Send a request to the Chat Service to trigger the workflow:
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

#### Observe Logs
Check the Chat Service logs for detailed information:
```
2025-04-06 04:01:00,123 - ChatService - INFO - Received chat request for user bob: Hi, how are you?
2025-04-06 04:01:00,124 - ChatService - INFO - Scheduling workflow with instance_id: chat-bob-1744064460
2025-04-06 04:01:00,125 - ChatService - INFO - Starting workflow for user bob with message: Hi, how are you?
2025-04-06 04:01:00,126 - ChatService - INFO - Fetching analytics for user bob
2025-04-06 04:01:00,130 - ChatService - INFO - Fetched message count for user bob: 3
2025-04-06 04:01:00,131 - ChatService - INFO - Fetching conversation history for user bob
2025-04-06 04:01:00,135 - ChatService - INFO - Fetched conversation history for user bob: []
2025-04-06 04:01:00,136 - ChatService - INFO - Generating reply for user bob with message: Hi, how are you?
2025-04-06 04:01:00,150 - ChatService - INFO - Generated reply for user bob: Hi Bob! You've sent 3 messages so far. No previous conversation. How can I help you today?
2025-04-06 04:01:00,151 - ChatService - INFO - Storing conversation for user bob
2025-04-06 04:01:00,155 - ChatService - INFO - Stored conversation for user bob
2025-04-06 04:01:00,156 - ChatService - INFO - Publishing MessageSent event for user bob
2025-04-06 04:01:00,160 - ChatService - INFO - Published MessageSent event for user bob
2025-04-06 04:01:00,161 - ChatService - INFO - Completed workflow for user bob
```

Check the Analytics Service logs:
```
2025-04-06 04:01:00,162 - AnalyticsService - INFO - Received event: {'user_id': 'bob', 'event_type': 'MessageSent'}
2025-04-06 04:01:00,163 - AnalyticsService - INFO - Incrementing message count for user bob
2025-04-06 04:01:00,164 - AnalyticsService - INFO - Fetching message count for user bob from state store
2025-04-06 04:01:00,165 - AnalyticsService - INFO - Fetched message count for user bob: 3
2025-04-06 04:01:00,166 - AnalyticsService - INFO - Setting message count for user bob to 4
2025-04-06 04:01:00,167 - AnalyticsService - INFO - Set message count for user bob: 4
2025-04-06 04:01:00,168 - AnalyticsService - INFO - Incremented message count for user bob to 4
2025-04-06 04:01:00,169 - AnalyticsService - INFO - Processed MessageSent event for user bob
```

#### Observe Traces in Zipkin
1. Open the Zipkin UI at `http://localhost:9411`.
2. Click “Find Traces” to see recent traces.
3. Look for a trace involving the `chat-service` and `analytics-service`:
   - You should see spans for:
     - The `/chat/` endpoint in the Chat Service.
     - Service Invocation to the Analytics Service (`analytics/bob`).
     - Actor interactions (`UserSessionActor` methods).
     - Pub/Sub messaging (`messages` topic).
     - Workflow steps.
   - The trace will show the latency of each operation and the flow of the request across services.

#### Observe Metrics in Prometheus
1. Open the Prometheus UI at `http://localhost:9090`.
2. Query some Dapr metrics:
   - `dapr_http_server_request_count`: Number of HTTP requests handled by Dapr sidecars.
     - Example: `dapr_http_server_request_count{app_id="chat-service"}`
   - `dapr_actor_active_actors`: Number of active actors.
     - Example: `dapr_actor_active_actors{app_id="chat-service", actor_type="UserSessionActor"}`
   - `dapr_workflow_execution_time`: Workflow execution time.
     - Example: `dapr_workflow_execution_time{app_id="chat-service"}`
3. You should see metrics for both the Chat Service and Analytics Service, reflecting the request we sent.

---

## Step 8: Why Dapr Observability for DACA?
Using Dapr’s observability features enhances DACA’s architecture by:
- **Visibility**: Distributed tracing provides a clear view of request flows across services and Dapr components, making it easier to identify bottlenecks or failures.
- **Performance Monitoring**: Metrics allow us to monitor latency, throughput, and error rates, ensuring the system meets performance goals.
- **Debugging**: Detailed logs and traces simplify troubleshooting, especially in a distributed system with workflows and actors.
- **Production Readiness**: Observability is critical for maintaining and optimizing a production system, enabling monitoring, alerting, and debugging.

---

## Step 9: Next Steps
You’ve successfully integrated Dapr’s observability features into the Chat Service and Analytics Service, enabling distributed tracing, metrics collection, and detailed logging! In the next tutorial (**12_dapr_containerization**), we’ll containerize our microservices using Docker and deploy them with Dapr in a Kubernetes cluster, preparing the system for production deployment.

### Optional Exercises
1. Set up Grafana to visualize Prometheus metrics with dashboards (e.g., for request latency, actor counts).
2. Simulate a failure (e.g., make the Analytics Service unavailable) and use Zipkin traces to identify the issue.
3. Add custom metrics to the Chat Service (e.g., number of messages processed per user) using Dapr’s metrics API.

---

## Conclusion
In this tutorial, we enabled Dapr’s observability features—distributed tracing with Zipkin, metrics collection with Prometheus, and detailed logging—to monitor and debug our microservices. This provides visibility into the system’s behavior, helps identify performance issues, and simplifies troubleshooting, aligning with DACA’s goals for a production-ready, distributed agentic AI system. We’re now ready to containerize and deploy our microservices in the next tutorial!

---

### Final Code for `chat_service/main.py`
```python
import logging
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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ChatService")

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
            logger.info("Fetching OpenAI API key from secrets store")
            secret = await dapr_client.get_secret(
                store_name="secretstore",
                key="openai-api-key"
            )
            return secret.secret["openai-api-key"]
        except Exception as e:
            logger.error(f"Failed to retrieve OpenAI API key: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve OpenAI API key: {e}")

async def initialize_chat_agent():
    api_key = await get_openai_api_key()
    logger.info("Initializing chat agent with OpenAI API key")
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
            logger.info(f"Fetching analytics for user {user_id}")
            response = await dapr_client.invoke_method_async(
                app_id="analytics-service",
                method_name=f"analytics/{user_id}",
                http_verb="GET"
            )
            analytics_data = response.json()
            message_count = analytics_data.get("message_count", 0)
            logger.info(f"Fetched message count for user {user_id}: {message_count}")
            return message_count
        except Exception as e:
            logger.error(f"Failed to fetch analytics for user {user_id}: {e}")
            return 0

async def fetch_conversation_history_activity(ctx: WorkflowActivityContext, user_id: str) -> list:
    with DaprClient() as dapr_client:
        try:
            logger.info(f"Fetching conversation history for user {user_id}")
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            history = await actor.get_conversation_history()
            logger.info(f"Fetched conversation history for user {user_id}: {history}")
            return history
        except Exception as e:
            logger.error(f"Failed to fetch conversation history for user {user_id}: {e}")
            return []

async def generate_reply_activity(ctx: WorkflowActivityContext, input_data: dict) -> str:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]
    message_count = input_data["message_count"]
    conversation_history = input_data["conversation_history"]

    logger.info(f"Generating reply for user {user_id} with message: {message_text}")
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
    reply = result.final_output
    logger.info(f"Generated reply for user {user_id}: {reply}")
    return reply

async def store_conversation_activity(ctx: WorkflowActivityContext, input_data: dict):
    user_id = input_data["user_id"]
    message = input_data["message"]
    reply = input_data["reply"]

    with DaprClient() as dapr_client:
        try:
            logger.info(f"Storing conversation for user {user_id}")
            actor = dapr_client.create_actor(UserSessionActorInterface, user_id)
            await actor.add_message({"message": message, "reply": reply})
            logger.info(f"Stored conversation for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to store conversation for user {user_id}: {e}")
            raise

async def publish_event_activity(ctx: WorkflowActivityContext, user_id: str):
    with DaprClient() as dapr_client:
        try:
            logger.info(f"Publishing MessageSent event for user {user_id}")
            await dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="messages",
                data={"user_id": user_id, "event_type": "MessageSent"}
            )
            logger.info(f"Published MessageSent event for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to publish MessageSent event for user {user_id}: {e}")
            raise

@workflow_runtime.workflow
async def message_processing_workflow(ctx: DaprWorkflowContext, input_data: dict) -> dict:
    user_id = input_data["user_id"]
    message_text = input_data["message_text"]

    logger.info(f"Starting workflow for user {user_id} with message: {message_text}")
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

    logger.info(f"Completed workflow for user {user_id}")
    return {"user_id": user_id, "reply": reply}

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    return {"message": "Welcome to the DACA Chat Service! Access /docs for the API documentation."}

@app.get("/users/{user_id}")
async def get_user(user_id: str, role: str | None = None):
    logger.info(f"Fetching user info for user_id: {user_id}, role: {role}")
    user_info = {"user_id": user_id, "role": role if role else "guest"}
    return user_info

@app.post("/chat/", response_model=Response)
async def chat(message: Message, db: dict = Depends(get_db)):
    if not message.text.strip():
        logger.warning("Received empty message text")
        raise HTTPException(status_code=400, detail="Message text cannot be empty")
    logger.info(f"Received chat request for user {message.user_id}: {message.text}")
    print(f"DB Connection: {db['connection']}")

    with DaprWorkflowClient() as workflow_client:
        instance_id = f"chat-{message.user_id}-{int(datetime.utcnow().timestamp())}"
        input_data = {"user_id": message.user_id, "message_text": message.text}
        
        logger.info(f"Scheduling workflow with instance_id: {instance_id}")
        await workflow_client.schedule_new_workflow(
            workflow=message_processing_workflow,
            instance_id=instance_id,
            input=input_data
        )

        logger.info(f"Waiting for workflow {instance_id} to complete")
        result = await workflow_client.wait_for_workflow_completion(
            instance_id=instance_id,
            timeout_in_seconds=60
        )

        if result is None or result.runtime_status != "COMPLETED":
            logger.error(f"Workflow {instance_id} failed to complete: {result.runtime_status if result else 'None'}")
            raise HTTPException(status_code=500, detail="Workflow failed to complete")

        workflow_output = result.output
        reply_text = workflow_output["reply"]
        logger.info(f"Workflow {instance_id} completed with reply: {reply_text}")

    return Response(
        user_id=message.user_id,
        reply=reply_text,
        metadata=Metadata()
    )

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down Chat Service")
    workflow_runtime.stop()
```

---

### Final Code for `analytics_service/main.py`
```python
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

from models import Analytics

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AnalyticsService")

app = FastAPI(
    title="DACA Analytics Service",
    description="A FastAPI-based Analytics Service for the DACA tutorial series",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_message_count(user_id: str, dapr_port: int = 3501) -> int:
    dapr_url = f"http://localhost:{dapr_port}/v1.0/state/statestore/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Fetching message count for user {user_id} from state store")
            response = await client.get(dapr_url)
            response.raise_for_status()
            state_data = response.json()
            message_count = state_data.get("message_count", 0) if state_data else 0
            logger.info(f"Fetched message count for user {user_id}: {message_count}")
            return message_count
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to retrieve state for user {user_id}: {e}")
            return 0

async def set_message_count(user_id: str, message_count: int, dapr_port: int = 3501):
    dapr_url = f"http://localhost:{dapr_port}/v1.0/state/statestore"
    state_data = [
        {
            "key": user_id,
            "value": {"message_count": message_count}
        }
    ]
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Setting message count for user {user_id} to {message_count}")
            response = await client.post(dapr_url, json=state_data)
            response.raise_for_status()
            logger.info(f"Set message count for user {user_id}: {message_count}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to set state for user {user_id}: {e}")

async def increment_message_count(user_id: str, dapr_port: int = 3501):
    logger.info(f"Incrementing message count for user {user_id}")
    current_count = await get_message_count(user_id, dapr_port)
    new_count = current_count + 1
    await set_message_count(user_id, new_count, dapr_port)
    logger.info(f"Incremented message count for user {user_id} to {new_count}")

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    return {"message": "Welcome to the DACA Analytics Service! Access /docs for the API documentation."}

@app.get("/analytics/{user_id}", response_model=Analytics)
async def get_analytics(user_id: str):
    logger.info(f"Fetching analytics for user {user_id}")
    message_count = await get_message_count(user_id)
    if message_count == 0 and user_id not in ["alice", "bob"]:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    return Analytics(message_count=message_count)

@app.post("/analytics/{user_id}/initialize")
async def initialize_message_count(user_id: str, message_count: int):
    logger.info(f"Initializing message count for user {user_id} to {message_count}")
    await set_message_count(user_id, message_count)
    return {"status": "success", "user_id": user_id, "message_count": message_count}

@app.post("/messages")
async def handle_message_sent(event: dict):
    logger.info(f"Received event: {event}")
    event_type = event.get("event_type")
    user_id = event.get("user_id")

    if event_type != "MessageSent" or not user_id:
        logger.warning(f"Ignoring invalid event: {event}")
        return {"status": "ignored"}

    await increment_message_count(user_id)
    logger.info(f"Processed MessageSent event for user {user_id}")
    return {"status": "success"}
```

---

This tutorial provides a focused introduction to Dapr observability, enabling monitoring and debugging of our microservices. 