# Integrating SQLModel with Dapr and CockroachDB Serverless

Welcome to the seventeenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll enhance the `chat_service` by integrating **SQLModel** to manage relational data, such as user conversations, in a **CockroachDB Serverless** managed database. We’ll also configure Dapr to use CockroachDB as its state store for workflow metadata, replacing the Redis-based state store used in previous tutorials. This integration will showcase how to combine relational data management with Dapr’s state management capabilities in a serverless environment, leveraging CockroachDB’s scalability and resilience. Let’s get started!

---

## What You’ll Learn
- Setting up a CockroachDB Serverless cluster and connecting to it.
- Using **SQLModel** to define and manage relational data models in the `chat_service`.
- Configuring Dapr to use CockroachDB as a state store for workflow metadata.
- Updating the `chat_service` to store conversation history in CockroachDB using SQLModel.
- Running the updated application with Docker Compose, including CockroachDB integration.

## Prerequisites
- Completion of **16_daca_hitl** (Chat Service, Analytics Service, Review UI, Dapr sidecars, Redis, Zipkin, Prometheus running with Docker Compose).
- Docker and Docker Desktop installed (from **12_docker_and_desktop**).
- An OpenAI API key (stored in `components/secrets.json`).
- A CockroachDB Serverless account (we’ll set this up).
- Basic familiarity with Python, SQLModel, and Dapr.

---

## Step 1: Set Up CockroachDB Serverless
CockroachDB Serverless is a fully managed, distributed SQL database that scales automatically and offers a free tier, making it ideal for this tutorial. Let’s set up a CockroachDB Serverless cluster.

### Step 1.1: Sign Up for CockroachDB Serverless
1. Visit the [CockroachDB Cloud signup page](https://cockroachlabs.cloud/signup).
2. Sign up for a free account (no credit card required for the free tier, which offers 5 GiB storage and 50M Request Units per month as of April 2025).
3. Verify your email address.

### Step 1.2: Create a CockroachDB Serverless Cluster
1. Log in to the CockroachDB Cloud Console.
2. Click **Create Cluster**.
3. On the **Select a plan** page, choose **Basic (formerly Serverless)**.
4. On the **Cloud & Regions** page:
   - Select a cloud provider (e.g., AWS or GCP).
   - Choose a region (e.g., `us-east-1` for AWS).
   - You can add more regions later if needed, but a single region is fine for this tutorial.
5. On the **Capacity** page, keep the default settings (free tier: 5 GiB storage, 50M RUs).
6. On the **Finalize** page, name your cluster (e.g., `daca-cluster`).
7. Click **Create Cluster**. The cluster will be provisioned in a few seconds.

### Step 1.3: Create a Database and SQL User
1. In the CockroachDB Cloud Console, navigate to your cluster’s **Overview** page.
2. Click **Connect** to get the connection details.
3. Under **SQL User**, create a new SQL user (e.g., `daca_user`) and set a password.
4. Under **Database**, create a new database called `daca_db`:
   - Use the connection string provided to connect to the cluster with the default database.
   - Run the following SQL command:
     ```sql
     CREATE DATABASE daca_db;
     ```
5. Update the connection string to use the `daca_db` database. The connection string should look like:
   ```
   postgresql://daca_user:<password>@<cluster-host>:26257/daca_db?sslmode=verify-full
   ```
   - Replace `<password>` with the password you set.
   - Replace `<cluster-host>` with the host provided (e.g., `daca-cluster-123.8nj.cockroachlabs.cloud`).
   - Ensure the cluster identifier is included in the connection string (e.g., `daca-cluster-123` before `.daca_db` if required by your cluster).

### Step 1.4: Download the CA Certificate
CockroachDB Serverless requires SSL for connections. Download the CA certificate:
1. In the **Connect** dialog, under **CA Certificate**, click **Download CA Certificate**.
2. Save the certificate as `cc-ca.crt` in the `chat_service` directory (e.g., `chat_service/cc-ca.crt`).

---

## Step 2: Configure Dapr to Use CockroachDB as a State Store
Dapr supports CockroachDB as a state store, which we’ll use to store workflow metadata (e.g., human review decisions). Let’s configure the Dapr state store component to use CockroachDB.

### Step 2.1: Create a Dapr Component for CockroachDB State Store
Create a new file `components/cockroachdb.yaml` to define the CockroachDB state store component:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.cockroachdb
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://daca_user:<password>@<cluster-host>:26257/daca_db?sslmode=verify-full"
  - name: schema
    value: "public"
  - name: tableName
    value: "dapr_state"
  - name: cleanupIntervalInSeconds
    value: "300"  # 5 minutes
  - name: sslCaPath
    value: "/components/cc-ca.crt"
```
- `connectionString`: The CockroachDB connection string from Step 1.3.
- `schema`: The database schema to use (`public` by default).
- `tableName`: The table where Dapr will store state (`dapr_state`).
- `cleanupIntervalInSeconds`: Interval for cleaning up expired records (set to 5 minutes for this tutorial).
- `sslCaPath`: Path to the CA certificate inside the container (we’ll mount it).

### Step 2.2: Update Docker Compose to Mount the CA Certificate
We need to mount the `cc-ca.crt` file into the containers for the `chat-service-dapr` and `review-ui-dapr` services, as they interact with the state store. Update `docker-compose.yml`:
```yaml
version: "3.9"
services:
  redis:
    image: redis:6.2
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - dapr-network

  zipkin:
    image: openzipkin/zipkin
    ports:
      - "9411:9411"
    networks:
      - dapr-network

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - dapr-network

  chat-service-app:
    build: ./chat_service
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
      - DB_CONNECTION=postgresql://daca_user:<password>@<cluster-host>:26257/daca_db?sslmode=verify-full
    volumes:
      - ./chat_service/cc-ca.crt:/app/cc-ca.crt
    networks:
      - dapr-network

  chat-service-dapr:
    image: daprio/dapr:1.12
    command:
      - "./daprd"
      - "--app-id"
      - "chat-service"
      - "--app-port"
      - "8000"
      - "--dapr-http-port"
      - "3500"
      - "--dapr-grpc-port"
      - "50001"
      - "--metrics-port"
      - "9090"
      - "--log-level"
      - "debug"
      - "--config"
      - "/components/tracing.yaml"
      - "--components-path"
      - "/components"
    environment:
      - DAPR_REDIS_HOST=redis:6379
    volumes:
      - ./components:/components
      - ./chat_service/cc-ca.crt:/components/cc-ca.crt
    depends_on:
      - chat-service-app
      - redis
      - zipkin
      - prometheus
    networks:
      - dapr-network

  analytics-service-app:
    build: ./analytics_service
    ports:
      - "8001:8001"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  analytics-service-dapr:
    image: daprio/dapr:1.12
    command:
      - "./daprd"
      - "--app-id"
      - "analytics-service"
      - "--app-port"
      - "8001"
      - "--dapr-http-port"
      - "3501"
      - "--metrics-port"
      - "9091"
      - "--log-level"
      - "debug"
      - "--config"
      - "/components/tracing.yaml"
      - "--components-path"
      - "/components"
    environment:
      - DAPR_REDIS_HOST=redis:6379
    volumes:
      - ./components:/components
    depends_on:
      - analytics-service-app
      - redis
      - zipkin
      - prometheus
    networks:
      - dapr-network

  review-ui-app:
    build: ./review_ui
    ports:
      - "8501:8501"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  review-ui-dapr:
    image: daprio/dapr:1.12
    command:
      - "./daprd"
      - "--app-id"
      - "review-ui"
      - "--app-port"
      - "8501"
      - "--dapr-http-port"
      - "3502"
      - "--metrics-port"
      - "9092"
      - "--log-level"
      - "debug"
      - "--config"
      - "/components/tracing.yaml"
      - "--components-path"
      - "/components"
    environment:
      - DAPR_REDIS_HOST=redis:6379
    volumes:
      - ./components:/components
      - ./chat_service/cc-ca.crt:/components/cc-ca.crt
    depends_on:
      - review-ui-app
      - redis
      - zipkin
      - prometheus
    networks:
      - dapr-network

networks:
  dapr-network:
    driver: bridge

volumes:
  redis-data:
```
- Added `DB_CONNECTION` environment variable to `chat-service-app` for SQLModel.
- Mounted `cc-ca.crt` into `chat-service-app`, `chat-service-dapr`, and `review-ui-dapr`.

---

## Step 3: Update the Chat Service to Use SQLModel
We’ll modify the `chat_service` to use SQLModel for managing conversation history in CockroachDB, replacing the previous actor-based storage. We’ll also ensure the workflow still uses Dapr state management for human review decisions.

### Step 3.1: Update `chat_service/pyproject.toml`
Add SQLModel and the CockroachDB SQLAlchemy driver to the dependencies:
```toml
[project]
name = "chat-service"
version = "0.1.0"
dependencies = [
    "fastapi==0.109.0",
    "uvicorn==0.27.0",
    "dapr==1.12.0",
    "openai==0.28.0",
    "pydantic==1.10.0",
    "sqlmodel==0.0.8",
    "sqlalchemy-cockroachdb==1.4.4",
    "psycopg2-binary==2.9.5",
]

[tool.uv]
lock = "uv.lock"
```

Run `uv sync` to update the dependencies:
```bash
cd chat_service
uv sync
```

### Step 3.2: Create a SQLModel for Conversations
Create a new file `chat_service/models.py` to define the SQLModel for conversations:
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    message: str
    reply: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### Step 3.3: Update `chat_service/main.py`
Modify `main.py` to use SQLModel for storing conversations and CockroachDB for the database connection. We’ll also remove the actor-based storage and update the workflow accordingly:
```python
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowContext, WorkflowActivityContext
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateOptions, Concurrency, Consistency
import uuid
from datetime import datetime, timezone
import json
import time
import os
from sqlmodel import SQLModel, Session, create_engine
from models import Conversation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatService")

app = FastAPI()

# Database setup with SQLModel
connection_string = os.getenv("DB_CONNECTION")
engine = create_engine(connection_string, echo=True, connect_args={"sslrootcert": "/app/cc-ca.crt"})
SQLModel.metadata.create_all(engine)

# Pydantic models
class ChatRequest(BaseModel):
    user_id: str
    text: str
    metadata: Dict[str, Any]
    tags: list[str] = []

class ChatResponse(BaseModel):
    user_id: str
    reply: str
    metadata: Dict[str, Any]

# Sensitive keywords requiring human review
SENSITIVE_KEYWORDS = ["urgent", "help", "emergency"]

# Dapr client for interacting with Dapr APIs
dapr_client = DaprClient()

# OpenAI client setup
def get_openai_client():
    with DaprClient() as d:
        secret = d.get_secret(store_name="secretstore", key="openai-api-key").secret
        openai.api_key = secret["openai-api-key"]
    return openai

# Activities for the workflow
def fetch_message_count(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> int:
    user_id = input["user_id"]
    with DaprClient() as d:
        resp = d.invoke_method(
            app_id="analytics-service",
            method_name=f"analytics/{user_id}",
            http_verb="GET"
        )
        data = resp.json()
        return data.get("message_count", 0)

def get_conversation_history(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> str:
    user_id = input["user_id"]
    with Session(engine) as session:
        conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
        if not conversations:
            return "No previous conversation."
        history = "\n".join([f"User: {conv.message}\nAssistant: {conv.reply}" for conv in conversations])
        return history

def generate_reply(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> str:
    user_id = input["user_id"]
    message = input["message"]
    message_count = input["message_count"]
    history = input["history"]
    
    prompt = f"User {user_id} has sent {message_count} messages. History: {history}\nMessage: {message}\nReply as a helpful assistant:"
    client = get_openai_client()
    response = client.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def store_conversation(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    message = input["message"]
    reply = input["reply"]
    conversation = Conversation(user_id=user_id, message=message, reply=reply)
    with Session(engine) as session:
        session.add(conversation)
        session.commit()

def publish_message_sent_event(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    with DaprClient() as d:
        d.publish_event(
            pubsub_name="pubsub",
            topic_name="messages",
            data=json.dumps({"user_id": user_id, "event_type": "MessageSent"}),
            data_content_type="application/json"
        )

def check_sensitive_content(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> Dict[str, Any]:
    message = input["message"]
    is_sensitive = any(keyword in message.lower() for keyword in SENSITIVE_KEYWORDS)
    return {"is_sensitive": is_sensitive, "message": message}

def request_human_review(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    message = input["message"]
    proposed_reply = input["proposed_reply"]
    instance_id = input["instance_id"]
    with DaprClient() as d:
        d.publish_event(
            pubsub_name="pubsub",
            topic_name="human-review",
            data=json.dumps({
                "user_id": user_id,
                "message": message,
                "proposed_reply": proposed_reply,
                "instance_id": instance_id,
                "event_type": "HumanReviewRequired"
            }),
            data_content_type="application/json"
        )

def wait_for_human_decision(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> Dict[str, Any]:
    instance_id = input["instance_id"]
    with DaprClient() as d:
        while True:
            state_key = f"human-decision-{instance_id}"
            state = d.get_state(
                store_name="statestore",
                key=state_key,
                state_options=StateOptions(concurrency=Concurrency.first_write, consistency=Consistency.strong)
            )
            if state.data:
                decision_data = json.loads(state.data.decode('utf-8'))
                d.delete_state(store_name="statestore", key=state_key)
                return decision_data
            time.sleep(1)

def chat_workflow(context: DaprWorkflowContext, input: Dict[str, Any]) -> Dict[str, Any]:
    user_id = input["user_id"]
    message = input["message"]
    instance_id = context.instance_id

    logger.info(f"Starting workflow for user {user_id} with message: {message}")

    message_count = yield context.call_activity(fetch_message_count, input={"user_id": user_id})
    history = yield context.call_activity(get_conversation_history, input={"user_id": user_id})
    proposed_reply = yield context.call_activity(generate_reply, input={
        "user_id": user_id,
        "message": message,
        "message_count": message_count,
        "history": history
    })
    sensitive_result = yield context.call_activity(check_sensitive_content, input={"message": message})
    is_sensitive = sensitive_result["is_sensitive"]

    if is_sensitive:
        logger.info(f"Sensitive content detected in message: {message}. Requesting human review.")
        yield context.call_activity(request_human_review, input={
            "user_id": user_id,
            "message": message,
            "proposed_reply": proposed_reply,
            "instance_id": instance_id
        })
        decision = yield context.call_activity(wait_for_human_decision, input={"instance_id": instance_id})
        approved = decision["approved"]

        if not approved:
            logger.info(f"Human rejected the response for user {user_id}. Aborting workflow.")
            return {
                "user_id": user_id,
                "reply": "Message rejected by human reviewer.",
                "metadata": {"timestamp": datetime.now(timezone.utc).isoformat(), "session_id": str(uuid.uuid4())}
            }

    yield context.call_activity(store_conversation, input={
        "user_id": user_id,
        "message": message,
        "reply": proposed_reply
    })
    yield context.call_activity(publish_message_sent_event, input={"user_id": user_id})

    logger.info(f"Completed workflow for user {user_id}")
    return {
        "user_id": user_id,
        "reply": proposed_reply,
        "metadata": {"timestamp": datetime.now(timezone.utc).isoformat(), "session_id": str(uuid.uuid4())}
    }

workflow_runtime = WorkflowRuntime()
workflow_runtime.register_workflow(chat_workflow)
workflow_runtime.register_activity(fetch_message_count)
workflow_runtime.register_activity(get_conversation_history)
workflow_runtime.register_activity(generate_reply)
workflow_runtime.register_activity(store_conversation)
workflow_runtime.register_activity(publish_message_sent_event)
workflow_runtime.register_activity(check_sensitive_content)
workflow_runtime.register_activity(request_human_review)
workflow_runtime.register_activity(wait_for_human_decision)

@app.on_event("startup")
async def start_workflow_runtime():
    await workflow_runtime.start()

@app.on_event("shutdown")
async def stop_workflow_runtime():
    await workflow_runtime.shutdown()

@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received chat request for user {request.user_id}: {request.text}")
    instance_id = f"chat-{request.user_id}-{int(time.time())}"
    logger.info(f"Scheduling workflow with instance_id: {instance_id}")

    with DaprClient() as d:
        d.start_workflow(
            workflow_component="dapr",
            workflow_name="chat_workflow",
            input={
                "user_id": request.user_id,
                "message": request.text
            },
            instance_id=instance_id
        )

        while True:
            state = d.get_workflow(instance_id=instance_id, workflow_component="dapr")
            if state.runtime_status == "COMPLETED":
                result = state.result
                return ChatResponse(**result)
            elif state.runtime_status == "FAILED":
                raise HTTPException(status_code=500, detail="Workflow failed")
            time.sleep(0.5)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### Explanation of Changes
- **Database Setup**: Added SQLModel engine setup using the CockroachDB connection string and CA certificate.
- **Conversation Model**: Defined a `Conversation` model in `models.py` to store user conversations.
- **Updated Activities**:
  - `get_conversation_history`: Now retrieves conversation history from CockroachDB using SQLModel.
  - `store_conversation`: Now stores conversations in CockroachDB using SQLModel.
  - Removed actor-based storage (no longer using `UserSessionActor`).
- **Workflow**: The workflow remains the same, but now uses SQLModel for conversation storage while still using Dapr state management for human review decisions.

---

## Step 4: Run the Application with Docker Compose
### Step 4.1: Start the Application
From the project root (`fastapi-daca-tutorial`), start the application:
```bash
docker-compose up -d
```

### Step 4.2: Verify the Services Are Running
List the running containers:
```bash
docker-compose ps
```
Output:
```
                Name                              Command               State           Ports         
------------------------------------------------------------------------------------------------------
fastapi-daca-tutorial_analytics-service-app_1    uv run uvicorn main:app -- ...   Up      0.0.0.0:8001->8001/tcp
fastapi-daca-tutorial_analytics-service-dapr_1   ./daprd --app-id analytics ...   Up                            
fastapi-daca-tutorial_chat-service-app_1         uv run uvicorn main:app -- ...   Up      0.0.0.0:8000->8000/tcp
fastapi-daca-tutorial_chat-service-dapr_1        ./daprd --app-id chat-serv ...   Up                            
fastapi-daca-tutorial_prometheus_1               /bin/prometheus --config.f ...   Up      0.0.0.0:9090->9090/tcp
fastapi-daca-tutorial_redis_1                    docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
fastapi-daca-tutorial_review-ui-app_1            uv run streamlit run app.p ...   Up      0.0.0.0:8501->8501/tcp
fastapi-daca-tutorial_review-ui-dapr_1           ./daprd --app-id review-ui ...   Up                            
fastapi-daca-tutorial_zipkin_1                   start-zipkin                     Up      0.0.0.0:9411->9411/tcp
```

---

## Step 5: Test the Application
We’ll test the application by sending a message, verifying that the conversation is stored in CockroachDB, and ensuring the HITL workflow still functions with Dapr state management.

### Step 5.1: Initialize State for Testing
Initialize message counts for `alice` and `bob`:
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

### Step 5.2: Send a Message Requiring Human Review
Send a message with a sensitive keyword:
```bash
curl -X POST http://localhost:8000/chat/ -H "Content-Type: application/json" -d '{"user_id": "bob", "text": "This is an urgent request!", "metadata": {"timestamp": "2025-04-06T12:00:00Z", "session_id": "123e4567-e89b-12d3-a456-426614174001"}, "tags": ["greeting"]}'
```

The request will hang, waiting for human review.

#### Check the Chat Service Logs
```bash
docker-compose logs chat-service-app
```
Output:
```
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,123 - ChatService - INFO - Received chat request for user bob: This is an urgent request!
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,124 - ChatService - INFO - Scheduling workflow with instance_id: chat-bob-1744064460
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,125 - ChatService - INFO - Starting workflow for user bob with message: This is an urgent request!
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,130 - ChatService - INFO - Sensitive content detected in message: This is an urgent request!. Requesting human review.
```

### Step 5.3: Approve the Message in the Streamlit UI
Open the Streamlit UI at `http://localhost:8501` and approve the message. The `curl` request should complete with a response like:
```json
{
  "user_id": "bob",
  "reply": "Hi Bob! You've sent 3 messages so far. No previous conversation. I understand your request is urgent—how can I assist you?",
  "metadata": {
    "timestamp": "2025-04-06T04:01:00Z",
    "session_id": "some-uuid"
  }
}
```

### Step 5.4: Verify Conversation Storage in CockroachDB
Connect to your CockroachDB cluster using the CockroachDB Cloud Console’s SQL shell or a local client, and query the `conversation` table:
```sql
SELECT * FROM conversation;
```
Output:
```
 id | user_id |        message         |                          reply                          |       timestamp       
----+---------+------------------------+---------------------------------------------------------+------------------------
  1 | bob     | This is an urgent request! | Hi Bob! You've sent 3 messages so far. No previous conversation. I understand your request is urgent—how can I assist you? | 2025-04-06 04:01:00
```

### Step 5.5: Verify Dapr State Storage
The human review decision should still be stored in the Dapr state store (now in CockroachDB). Query the `dapr_state` table:
```sql
SELECT * FROM dapr_state;
```
Output:
```
 key                     | value                                                                 | ...
-------------------------+----------------------------------------------------------------------+ ...
 human-decision-chat-bob-1744064460 | {"instance_id": "chat-bob-1744064460", "approved": true} | ...
```
(Note: The record may have been deleted after retrieval by the workflow, depending on timing.)

---

## Step 6: Why SQLModel, Dapr, and CockroachDB?
- **SQLModel**: Provides a modern, type-hinted way to work with relational data, combining the power of SQLAlchemy and Pydantic. It’s ideal for Python developers who want a simple ORM with validation.
- **Dapr State Management**: Allows us to manage workflow state (e.g., human review decisions) in a distributed, scalable way, independent of the relational data model.
- **CockroachDB Serverless**: Offers a fully managed, distributed SQL database that scales automatically, supports PostgreSQL compatibility, and provides a free tier for development. It’s resilient to failures and ideal for cloud-native applications like DACA.

---

## Step 7: Next Steps
You’ve successfully integrated SQLModel with Dapr and CockroachDB Serverless in the DACA application! The `chat_service` now uses SQLModel to store conversations in CockroachDB, while Dapr uses CockroachDB as its state store for workflow metadata. In the next tutorial, we’ll explore deploying this application to a production environment, such as a Kubernetes cluster, using Dapr’s Kubernetes integration.

### Optional Exercises
1. Add more fields to the `Conversation` model (e.g., `tags`, `metadata`) and update the workflow to store them.
2. Implement a REST endpoint in `chat_service` to retrieve a user’s conversation history using SQLModel.
3. Enhance the Dapr state store configuration to use CockroachDB’s TTL features more effectively for human review decisions.

---

## Conclusion
In this tutorial, we integrated SQLModel with Dapr and CockroachDB Serverless in the DACA application. We set up a CockroachDB Serverless cluster, configured Dapr to use CockroachDB as its state store, and updated the `chat_service` to use SQLModel for managing conversation history. The application now combines relational data management with distributed state management, running seamlessly with Docker Compose. We’re now ready to explore production deployment in the next tutorial!

---

### Final `chat_service/models.py`
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    message: str
    reply: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### Final `chat_service/main.py`
```python
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowContext, WorkflowActivityContext
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateOptions, Concurrency, Consistency
import uuid
from datetime import datetime, timezone
import json
import time
import os
from sqlmodel import SQLModel, Session, create_engine
from models import Conversation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChatService")

app = FastAPI()

connection_string = os.getenv("DB_CONNECTION")
engine = create_engine(connection_string, echo=True, connect_args={"sslrootcert": "/app/cc-ca.crt"})
SQLModel.metadata.create_all(engine)

class ChatRequest(BaseModel):
    user_id: str
    text: str
    metadata: Dict[str, Any]
    tags: list[str] = []

class ChatResponse(BaseModel):
    user_id: str
    reply: str
    metadata: Dict[str, Any]

SENSITIVE_KEYWORDS = ["urgent", "help", "emergency"]

dapr_client = DaprClient()

def get_openai_client():
    with DaprClient() as d:
        secret = d.get_secret(store_name="secretstore", key="openai-api-key").secret
        openai.api_key = secret["openai-api-key"]
    return openai

def fetch_message_count(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> int:
    user_id = input["user_id"]
    with DaprClient() as d:
        resp = d.invoke_method(
            app_id="analytics-service",
            method_name=f"analytics/{user_id}",
            http_verb="GET"
        )
        data = resp.json()
        return data.get("message_count", 0)

def get_conversation_history(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> str:
    user_id = input["user_id"]
    with Session(engine) as session:
        conversations = session.query(Conversation).filter(Conversation.user_id == user_id).all()
        if not conversations:
            return "No previous conversation."
        history = "\n".join([f"User: {conv.message}\nAssistant: {conv.reply}" for conv in conversations])
        return history

def generate_reply(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> str:
    user_id = input["user_id"]
    message = input["message"]
    message_count = input["message_count"]
    history = input["history"]
    
    prompt = f"User {user_id} has sent {message_count} messages. History: {history}\nMessage: {message}\nReply as a helpful assistant:"
    client = get_openai_client()
    response = client.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def store_conversation(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    message = input["message"]
    reply = input["reply"]
    conversation = Conversation(user_id=user_id, message=message, reply=reply)
    with Session(engine) as session:
        session.add(conversation)
        session.commit()

def publish_message_sent_event(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    with DaprClient() as d:
        d.publish_event(
            pubsub_name="pubsub",
            topic_name="messages",
            data=json.dumps({"user_id": user_id, "event_type": "MessageSent"}),
            data_content_type="application/json"
        )

def check_sensitive_content(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> Dict[str, Any]:
    message = input["message"]
    is_sensitive = any(keyword in message.lower() for keyword in SENSITIVE_KEYWORDS)
    return {"is_sensitive": is_sensitive, "message": message}

def request_human_review(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> None:
    user_id = input["user_id"]
    message = input["message"]
    proposed_reply = input["proposed_reply"]
    instance_id = input["instance_id"]
    with DaprClient() as d:
        d.publish_event(
            pubsub_name="pubsub",
            topic_name="human-review",
            data=json.dumps({
                "user_id": user_id,
                "message": message,
                "proposed_reply": proposed_reply,
                "instance_id": instance_id,
                "event_type": "HumanReviewRequired"
            }),
            data_content_type="application/json"
        )

def wait_for_human_decision(ctx: WorkflowActivityContext, input: Dict[str, Any]) -> Dict[str, Any]:
    instance_id = input["instance_id"]
    with DaprClient() as d:
        while True:
            state_key = f"human-decision-{instance_id}"
            state = d.get_state(
                store_name="statestore",
                key=state_key,
                state_options=StateOptions(concurrency=Concurrency.first_write, consistency=Consistency.strong)
            )
            if state.data:
                decision_data = json.loads(state.data.decode('utf-8'))
                d.delete_state(store_name="statestore", key=state_key)
                return decision_data
            time.sleep(1)

def chat_workflow(context: DaprWorkflowContext, input: Dict[str, Any]) -> Dict[str, Any]:
    user_id = input["user_id"]
    message = input["message"]
    instance_id = context.instance_id

    logger.info(f"Starting workflow for user {user_id} with message: {message}")

    message_count = yield context.call_activity(fetch_message_count, input={"user_id": user_id})
    history = yield context.call_activity(get_conversation_history, input={"user_id": user_id})
    proposed_reply = yield context.call_activity(generate_reply, input={
        "user_id": user_id,
        "message": message,
        "message_count": message_count,
        "history": history
    })
    sensitive_result = yield context.call_activity(check_sensitive_content, input={"message": message})
    is_sensitive = sensitive_result["is_sensitive"]

    if is_sensitive:
        logger.info(f"Sensitive content detected in message: {message}. Requesting human review.")
        yield context.call_activity(request_human_review, input={
            "user_id": user_id,
            "message": message,
            "proposed_reply": proposed_reply,
            "instance_id": instance_id
        })
        decision = yield context.call_activity(wait_for_human_decision, input={"instance_id": instance_id})
        approved = decision["approved"]

        if not approved:
            logger.info(f"Human rejected the response for user {user_id}. Aborting workflow.")
            return {
                "user_id": user_id,
                "reply": "Message rejected by human reviewer.",
                "metadata": {"timestamp": datetime.now(timezone.utc).isoformat(), "session_id": str(uuid.uuid4())}
            }

    yield context.call_activity(store_conversation, input={
        "user_id": user_id,
        "message": message,
        "reply": proposed_reply
    })
    yield context.call_activity(publish_message_sent_event, input={"user_id": user_id})

    logger.info(f"Completed workflow for user {user_id}")
    return {
        "user_id": user_id,
        "reply": proposed_reply,
        "metadata": {"timestamp": datetime.now(timezone.utc).isoformat(), "session_id": str(uuid.uuid4())}
    }

workflow_runtime = WorkflowRuntime()
workflow_runtime.register_workflow(chat_workflow)
workflow_runtime.register_activity(fetch_message_count)
workflow_runtime.register_activity(get_conversation_history)
workflow_runtime.register_activity(generate_reply)
workflow_runtime.register_activity(store_conversation)
workflow_runtime.register_activity(publish_message_sent_event)
workflow_runtime.register_activity(check_sensitive_content)
workflow_runtime.register_activity(request_human_review)
workflow_runtime.register_activity(wait_for_human_decision)

@app.on_event("startup")
async def start_workflow_runtime():
    await workflow_runtime.start()

@app.on_event("shutdown")
async def stop_workflow_runtime():
    await workflow_runtime.shutdown()

@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    logger.info(f"Received chat request for user {request.user_id}: {request.text}")
    instance_id = f"chat-{request.user_id}-{int(time.time())}"
    logger.info(f"Scheduling workflow with instance_id: {instance_id}")

    with DaprClient() as d:
        d.start_workflow(
            workflow_component="dapr",
            workflow_name="chat_workflow",
            input={
                "user_id": request.user_id,
                "message": request.text
            },
            instance_id=instance_id
        )

        while True:
            state = d.get_workflow(instance_id=instance_id, workflow_component="dapr")
            if state.runtime_status == "COMPLETED":
                result = state.result
                return ChatResponse(**result)
            elif state.runtime_status == "FAILED":
                raise HTTPException(status_code=500, detail="Workflow failed")
            time.sleep(0.5)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Final `components/cockroachdb.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.cockroachdb
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://daca_user:<password>@<cluster-host>:26257/daca_db?sslmode=verify-full"
  - name: schema
    value: "public"
  - name: tableName
    value: "dapr_state"
  - name: cleanupIntervalInSeconds
    value: "300"
  - name: sslCaPath
    value: "/components/cc-ca.crt"
```

---

This tutorial successfully integrates SQLModel with Dapr and CockroachDB Serverless, providing a robust foundation for relational data management in a distributed application. Would you like to proceed with the deployment to Kubernetes, or explore additional features like advanced querying with SQLModel?