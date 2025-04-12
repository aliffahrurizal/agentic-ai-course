# Running DACA Microservices with Docker Compose and Dapr

Welcome to the fifteenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll use **Docker Compose** to manage the containerized **Chat Service** and **Agent Memory Service** from **13_dapr_containerization**, along with their Dapr sidecars and Redis. Building on the Docker Compose basics from **14_docker_compose_introduction**, we’ll create a `compose.yml` file to define all components, start the application with a single command, and verify that pub/sub messaging, state management, and service invocation work as expected. 

As a challenge, we’ll introduce **Zipkin** for distributed tracing and **Prometheus** for metrics, enhancing observability for production readiness. This streamlines our development workflow and prepares us for deploying to environments like Kubernetes or Azure Container Apps in future tutorials.

---

### What You’ll Learn
- How to define a multi-container DACA application using a `compose.yml` file.
- Running the Chat Service, Agent Memory Service, Dapr sidecars, and Redis with Docker Compose.
- Verifying the application works the same as in **13_dapr_containerization**.
- **Challenge**: Adding Zipkin for tracing and Prometheus for metrics to monitor microservices.
- Benefits of using Docker Compose with Dapr for managing microservices.

### Prerequisites
- Completion of **13_dapr_containerization** (containerized Chat Service and Agent Memory Service with Dapr sidecars).
- Completion of **14_docker_compose_introduction** (general understanding of Docker Compose concepts).
- **Docker** and **Docker Desktop** installed ([Docker installation guide](https://docs.docker.com/get-docker/)).
- **Python 3.12+** for local development (though containers handle runtime).
- **Gemini API Key** set in `chat_service/.env` and `agent_memory_service/.env` as `GEMINI_API_KEY=<your-key>`.

---

## Step 1: Recap of the Current Setup
In **13_dapr_containerization**, we containerized the Chat Service and Agent Memory Service:
- **Chat Service**:
  - Handles user messages via `POST /chat/`.
  - Fetches user metadata and conversation history from the Agent Memory Service using Dapr service invocation over HTTP.
  - Generates replies using a Gemini-powered LLM (via the Agents SDK).
  - Publishes `ConversationUpdated` events to the `conversations` topic via Dapr pub/sub.
  - Runs on port `8080` with a Dapr sidecar on port `3500`.
- **Agent Memory Service**:
  - Stores user metadata (`name`, `preferred_style`, `user_summary`) and conversation history in a Dapr state store (Redis).
  - Subscribes to the `conversations` topic to update history and generate `user_summary` using the Gemini LLM.
  - Exposes endpoints like `GET /memories/{user_id}` and `GET /conversations/{session_id}`.
  - Runs on port `8001` with a Dapr sidecar on port `3501`.
- **Supporting Services**:
  - Redis for Dapr’s state store and pub/sub.
- **Docker Setup**:
  - Images: `chat-service:latest`, `agent-memory-service:latest`, `daprio/dapr:1.15.1`, `redis:latest`.
  - Custom `dapr-network` for communication.
  - Dapr components: `pubsub.yaml`, `statestore.yaml`, `subscriptions.yaml`.

### Current Limitations
- **Manual Container Management**: Starting each container (`redis`, `chat-service-app`, `chat-service-dapr`, `agent-memory-service-app`, `agent-memory-service-dapr`) with separate `docker run` commands is tedious and error-prone.
- **Dependency Handling**: No automated way to ensure services start in the correct order (e.g., Redis before Dapr sidecars).
- **Observability**: No tracing or metrics to monitor request flows or performance, limiting production readiness.
- **Reproducibility**: Sharing or reproducing the setup requires running multiple commands manually.

### Goal for This Tutorial
We’ll use Docker Compose to:
- Define all services in a single `compose.yml` file.
- Start the entire application with `docker compose up`.
- Use the `dapr-network` for isolated communication.
- Verify core functionality with the same tests from **13_dapr_containerization**.
- **Challenge**: Add Zipkin for tracing and Prometheus for metrics to enhance observability.

### Current Project Structure
```
fastapi-daca-tutorial/
├── chat_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── test_main.py
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .env
│   └── .dockerignore
├── agent_memory_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   ├── test_main.py
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .env
│   └── .dockerignore
├── components/
│   ├── pubsub.yaml
│   ├── statestore.yaml
│   ├── subscriptions.yaml
│   ├── tracing.yaml  # New for Zipkin challenge
├── prometheus.yml  # New for Prometheus challenge
├── compose.yml  # New for this tutorial
└── README.md
```

---

## Step 2: Why Use Docker Compose with Dapr?
Docker Compose simplifies our DACA setup by:
- **Centralized Configuration**: Defines all services in one file, as introduced in **14_docker_compose_introduction**.
- **Single Command**: Starts/stops everything with `docker compose up`/`down`, replacing multiple `docker run` commands.
- **Networking**: Creates a default network for services to communicate via names (e.g., `redis`, `chat-service-dapr`).
- **Dependency Management**: Ensures services start in order (e.g., Redis → apps → sidecars).
- **Observability (Challenge)**: Supports adding Zipkin and Prometheus for tracing and metrics, enhancing production readiness.
- **Development Efficiency**: Provides a reproducible environment for testing and iteration.

This aligns with Dapr’s sidecar pattern and prepares us for production orchestration.

---

## Step 3: Create Configuration Files

We’ll create the `compose.yml` file and add new files for the observability challenge: `components/tracing.yaml` for Zipkin and `prometheus.yml` for Prometheus.

### Step 3.1: Define `compose.yml` (Minimal Version)
This version matches **13_dapr_containerization** without observability features.

```bash
touch fastapi-daca-tutorial/compose.yml
```

Edit `compose.yml`:

```yaml
services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - dapr-network

  chat-service-app:
    build: ./chat_service
    ports:
      - "8080:8080"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  chat-service-dapr:
    image: daprio/dapr:1.15.1
    command:
      - "./daprd"
      - "--app-id"
      - "chat-service"
      - "--app-port"
      - "8080"
      - "--dapr-http-port"
      - "3500"
      - "--log-level"
      - "debug"
      - "--resources-path"
      - "/components"
      - "--app-protocol"
      - "http"
      - "--app-channel-address"
      - "chat-service-app"
    volumes:
      - ./components:/components
    depends_on:
      - chat-service-app
      - redis
    networks:
      - dapr-network

  agent-memory-service-app:
    build: ./agent_memory_service
    ports:
      - "8001:8001"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  agent-memory-service-dapr:
    image: daprio/dapr:1.15.1
    command:
      - "./daprd"
      - "--app-id"
      - "agent-memory-service"
      - "--app-port"
      - "8001"
      - "--dapr-http-port"
      - "3501"
      - "--log-level"
      - "debug"
      - "--resources-path"
      - "/components"
      - "--app-protocol"
      - "http"
      - "--app-channel-address"
      - "agent-memory-service-app"
    volumes:
      - ./components:/components
    depends_on:
      - agent-memory-service-app
      - redis
    networks:
      - dapr-network

networks:
  dapr-network:
    driver: bridge

volumes:
  redis-data:
```

### Step 3.2: Define `compose.yml` (Enhanced Version with Challenge)
This version includes Zipkin, Prometheus, metrics ports, and tracing configuration.

Add components/tracing/yml

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
```

Edit `compose-v2.yml`:

```yaml
services:
  redis:
    image: redis:latest
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
      - "8080:8080"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  chat-service-dapr:
    image: daprio/dapr:1.15.1
    command:
      - "./daprd"
      - "--app-id"
      - "chat-service"
      - "--app-port"
      - "8080"
      - "--dapr-http-port"
      - "3500"
      - "--metrics-port"
      - "9090"
      - "--log-level"
      - "debug"
      - "--resources-path"
      - "/components"
      - "--config"
      - "/components/tracing.yaml"
      - "--app-protocol"
      - "http"
      - "--app-channel-address"
      - "chat-service-app"
    ports:
      - "3500:3500"
    volumes:
      - ./components:/components
    depends_on:
      - chat-service-app
      - redis
      - zipkin
      - prometheus
    networks:
      - dapr-network

  agent-memory-service-app:
    build: ./agent_memory_service
    ports:
      - "8001:8001"
    depends_on:
      - redis
    environment:
      - PYTHONUNBUFFERED=1
    networks:
      - dapr-network

  agent-memory-service-dapr:
    image: daprio/dapr:1.15.1
    command:
      - "./daprd"
      - "--app-id"
      - "agent-memory-service"
      - "--app-port"
      - "8001"
      - "--dapr-http-port"
      - "3501"
      - "--metrics-port"
      - "9091"
      - "--log-level"
      - "debug"
      - "--resources-path"
      - "/components"
      - "--config"
      - "/components/tracing.yaml"
      - "--app-protocol"
      - "http"
      - "--app-channel-address"
      - "agent-memory-service-app"
    ports:
      - "3501:3501"
    volumes:
      - ./components:/components
    depends_on:
      - agent-memory-service-app
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

#### Explanation of Enhanced Version
- **redis**: Unchanged, provides state store and pub/sub backend.
- **zipkin**:
  - `image: openzipkin/zipkin`: Adds Zipkin for tracing.
  - `ports: - "9411:9411"`: Exposes Zipkin UI.
- **prometheus**:
  - `image: prom/prometheus`: Adds Prometheus for metrics.
  - `ports: - "9090:9090"`: Exposes Prometheus UI.
  - `volumes: - ./prometheus.yml:/etc/prometheus/prometheus.yml`: Mounts configuration.
- **chat-service-dapr**:
  - Added `--metrics-port 9090` for Dapr metrics.
  - Added `--config /components/tracing.yaml` for Zipkin integration.
  - `depends_on: - zipkin, - prometheus`: Ensures observability services start first.
- **agent-memory-service-dapr**:
  - Added `--metrics-port 9091` to avoid conflicts.
  - Added `--config /components/tracing.yaml`.
  - Same `depends_on` for Zipkin and Prometheus.
- **ports**: Exposed only HTTP ports (`3500`, `3501`) to keep the setup minimal; metrics and gRPC ports are internal to the network unless needed externally.

### Step 3.3: Create `tracing.yaml` for Zipkin
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
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
```

**Explanation**:
- `samplingRate: "1"`: Captures all traces for debugging.
- `endpointAddress`: Points to the `zipkin` service on the `dapr-network`.

### Step 3.4: Create `prometheus.yml` for Prometheus
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
      - targets: ['chat-service-dapr:9090', 'agent-memory-service-dapr:9091']
```

**Explanation**:
- `scrape_interval: 15s`: Polls metrics every 15 seconds.
- `targets`: Scrapes Dapr sidecars’ metrics endpoints (`/metrics` on ports `9090`, `9091`).

### Step 3.5: Verify Component Files
The core Dapr components from **13_dapr_containerization** remain unchanged, with `tracing.yaml` added for the challenge.

Run:

```bash
ls components/
```

**Expected Output**:
```
pubsub.yaml  statestore.yaml  subscriptions.yaml  tracing.yaml
```

**Core Components** (Unchanged):
- **pubsub.yaml**:
  ```yaml
  apiVersion: dapr.io/v1alpha1
  kind: Component
  metadata:
    name: pubsub
  spec:
    type: pubsub.redis
    version: v1
    metadata:
      - name: redisHost
        value: redis:6379
      - name: redisPassword
        value: ""
  ```
- **statestore.yaml**:
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
        value: redis:6379
      - name: redisPassword
        value: ""
      - name: actorStateStore
        value: "true"
  ```
- **subscriptions.yaml**:
  ```yaml
  apiVersion: dapr.io/v1alpha1
  kind: Subscription
  metadata:
    name: conversation-subscription
  spec:
    pubsubname: pubsub
    topic: conversations
    route: /conversations
  ```

---

## Step 4: Run the Application with Docker Compose

### Step 4.1: Choose Your Setup
- **Minimal Version**: Use the first `compose.yml` to replicate **13_dapr_containerization** exactly (no Zipkin or Prometheus).
- **Enhanced Version (Challenge)**: Use the second `compose.yml` to include Zipkin and Prometheus.

For this tutorial, we’ll proceed with the **Enhanced Version** to complete the observability challenge.

### Step 4.2: Start the Application
Ensure `components/tracing.yaml` and `prometheus.yml` are created, then run:

```bash
docker-compose up
```

**Expected Output**:
```
Creating network "fastapi-daca-tutorial_dapr-network" with driver "bridge"
Creating volume "fastapi-daca-tutorial_redis-data" with default driver
Creating fastapi-daca-tutorial_redis_1 ... done
Creating fastapi-daca-tutorial_zipkin_1 ... done
Creating fastapi-daca-tutorial_prometheus_1 ... done
Building chat-service-app
Step 1/7 : FROM python:3.12-slim
 ---> 85824326bc4a
...
Successfully built d0924e0b62e5
Successfully tagged fastapi-daca-tutorial_chat-service-app:latest
Building agent-memory-service-app
Step 1/7 : FROM python:3.12-slim
 ---> 85824326bc4a
...
Successfully built 10f5f9e79347
Successfully tagged fastapi-daca-tutorial_agent-memory-service-app:latest
Creating fastapi-daca-tutorial_chat-service-app_1 ... done
Creating fastapi-daca-tutorial_chat-service-dapr_1 ... done
Creating fastapi-daca-tutorial_agent-memory-service-app_1 ... done
Creating fastapi-daca-tutorial_agent-memory-service-dapr_1 ... done
```

### Step 4.3: Verify Services Are Running
```bash
docker-compose ps
```

**Expected Output** (Enhanced Version):
```
                         Name                                       Command               State           Ports         
----------------------------------------------------------------------------------------------------------------
fastapi-daca-tutorial_agent-memory-service-app_1    uv run uvicorn main:app -- ...   Up      0.0.0.0:8001->8001/tcp
fastapi-daca-tutorial_agent-memory-service-dapr_1   ./daprd --app-id agent-mem ...   Up      0.0.0.0:3501->3501/tcp
fastapi-daca-tutorial_chat-service-app_1           uv run uvicorn main:app -- ...   Up      0.0.0.0:8080->8080/tcp
fastapi-daca-tutorial_chat-service-dapr_1          ./daprd --app-id chat-serv ...   Up      0.0.0.0:3500->3500/tcp
fastapi-daca-tutorial_prometheus_1                 /bin/prometheus --config.f ...   Up      0.0.0.0:9090->9090/tcp
fastapi-daca-tutorial_redis_1                      docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
fastapi-daca-tutorial_zipkin_1                     start-zipkin                     Up      0.0.0.0:9411->9411/tcp
```

**Action**:
- If any service is not `Up`, check logs:
  ```bash
  docker-compose logs <service-name>
  ```
  E.g., `docker-compose logs chat-service-dapr`.

---

## Step 5: Test the Application
We’ll run the same tests from **13_dapr_containerization** to verify core functionality, then add challenge-specific tests for Zipkin and Prometheus.

### Step 5.1: Initialize State
```bash
curl -X POST http://localhost:8001/memories/junaid/initialize \
  -H "Content-Type: application/json" \
  -d '{"name": "Junaid", "preferred_style": "casual", "user_summary": "Junaid is building Agents WorkForce."}'
```

**Expected Output**:
```json
{"status":"success","user_id":"junaid","metadata":{"name":"Junaid","preferred_style":"casual","user_summary":"Junaid is building Agents WorkForce."}}
```

### Step 5.2: Test Chat Service
**First Request**:
```bash
curl -X POST http://localhost:8080/chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "junaid", "text": "I need to schedule a coding session."}'
```

**Expected Response**:
```json
{"user_id":"junaid","reply":"Hey Junaid!  Sounds good. What time works best for you?  I can help you figure out the time if you like.\n","metadata":{"timestamp":"2025-04-12T05:05:42.107924+00:00","session_id":"afe61d23-2d73-44b3-adb3-ad9a64ac299a"}}
```

**Second Request (Same Session)**:
Use the `session_id` from the response above:
```bash
curl -X POST http://localhost:8080/chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "junaid", "text": "What was my last msg?", "metadata": {"session_id": "afe61d23-2d73-44b3-adb3-ad9a64ac299a"}}'
```

**Expected Response**:
```json
{"user_id":"junaid","reply":"Your last message was: \"I need to schedule a coding session.\"\n","metadata":{"timestamp":"2025-04-12T05:06:12.523282+00:00","session_id":"afe61d23-2d73-44b3-adb3-ad9a64ac299a"}}% 
```

### Step 5.3: Verify Metadata Update
```bash
curl http://localhost:8001/memories/junaid
```

**Expected Output**:
```json
{
  "name": "Junaid",
  "preferred_style": "casual",
  "user_summary": "Junaid needs to schedule a coding session."
}
```

### Step 5.4: Test Background Memories
**Continue Session**:
```bash
curl -X POST http://localhost:8080/chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "junaid", "text": "Tomorrow we will pack for SF?", "metadata": {"session_id": "98289651-62fb-45eb-804a-21c7ee59384c"}}'
```

**Expected Response**:
```json
{
  "user_id": "junaid",
  "reply": "Okay, cool! Packing for San Francisco tomorrow. Anything specific you need to remember to pack?",
  "metadata": {
    "session_id": "98289651-62fb-45eb-804a-21c7ee59384c"
  }
}
```

**New Session**:
```bash
curl -X POST http://localhost:8080/chat/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": "junaid", "text": "Where was I planning to go tomorrow?"}'
```

**Expected Response**:
```json
{
  "user_id": "junaid",
  "reply": "Hey Junaid! Looks like you're heading to San Francisco tomorrow! Safe travels!",
  "metadata": {
    "session_id": "5cdf5f65-3853-43ff-a1db-e4cb7d901b11"
  }
}
```

### Step 5.6: Check Logs
**Chat Service**:
```bash
docker-compose logs chat-service-app
```

**Expected**:
```
fastapi-daca-tutorial_chat-service-app_1  | INFO:main:Successfully fetched metadata for junaid
fastapi-daca-tutorial_chat-service-app_1  | INFO:main:Fetching history from http://agent-memory-service-dapr:3501/v1.0/invoke/agent-memory-service/method/conversations/98289651-62fb-45eb-804a-21c7ee59384c
fastapi-daca-tutorial_chat-service-app_1  | INFO:httpx:HTTP Request: GET http://agent-memory-service-dapr:3501/v1.0/invoke/agent-memory-service/method/conversations/98289651-62fb-45eb-804a-21c7ee59384c "HTTP/1.1 200 OK"
fastapi-daca-tutorial_chat-service-app_1  | INFO:main:Successfully fetched history for session 98289651-62fb-45eb-804a-21c7ee59384c
fastapi-daca-tutorial_chat-service-app_1  | INFO:httpx:HTTP Request: POST http://chat-service-dapr:3500/v1.0/publish/pubsub/conversations "HTTP/1.1 204 No Content"
fastapi-daca-tutorial_chat-service-app_1  | INFO:main:Published ConversationUpdated event for junaid, session 98289651-62fb-45eb-804a-21c7ee59384c
```

**Agent Memory Service**:
```bash
docker-compose logs agent-memory-service-app
```

**Expected**:
```
fastapi-daca-tutorial_agent-memory-service-app_1  | Received event: {'data': {'user_id': 'junaid', 'event_type': 'ConversationUpdated', ...}}
fastapi-daca-tutorial_agent-memory-service-app_1  | INFO:main:Stored conversation history for session 98289651-62fb-45eb-804a-21c7ee59384c
fastapi-daca-tutorial_agent-memory-service-app_1  | INFO:main:Stored metadata for junaid: {'name': 'Junaid', 'preferred_style': 'casual', 'user_summary': 'Junaid needs to schedule a coding session.'}
```

**Dapr Sidecars**:
```bash
docker-compose logs chat-service-dapr
docker-compose logs agent-memory-service-dapr
```

**Expected**:
- `chat-service-dapr`: Shows component loading, tracing enabled, no errors.
- `agent-memory-service-dapr`: Shows `Subscribed to topic 'conversations'`, tracing enabled.



## Step 6: Why Docker Compose with Dapr for DACA?
Docker Compose enhances our DACA architecture by:
- **Simplified Management**: One command (`docker compose up`) replaces multiple `docker run` commands, as highlighted in **14_docker_compose_introduction**.
- **Proper Networking**: The `dapr-network` ensures isolated, name-based communication.
- **Dependency Handling**: Guarantees correct startup order (Redis → Zipkin/Prometheus → apps → sidecars).
- **Observability (Challenge)**: Zipkin and Prometheus provide tracing and metrics, making the system production-ready.
- **Reproducibility**: The `compose.yml` file ensures consistent setups across environments.
- **Production Readiness**: Mirrors multi-container orchestration patterns used in Kubernetes or cloud platforms.

---

## Step 7: Challenge - Implementing Observability
### Objective
Enhance the DACA setup with tracing and metrics to monitor microservices interactions and performance.


### Step 5.5: Challenge: Setup Advanced Compose File - Verify Observability
**Zipkin (Tracing)**:
1. Open `http://localhost:9411` in a browser.
2. Search for traces related to `/chat/` or `/conversations`.
3. **Expected**: A trace showing:
   - `POST /chat/` on `chat-service`.
   - Service invocation to `agent-memory-service` for `/memories/junaid` and `/conversations/{session_id}`.
   - Pub/sub event to `conversations` topic.
   - `POST /conversations` on `agent-memory-service`.

**Prometheus (Metrics)**:
1. Open `http://localhost:9090` in a browser.
2. Query metrics like:
   - `dapr_http_server_request_count`: Counts HTTP requests to Dapr sidecars.
   - `dapr_pubsub_message_total`: Counts pub/sub messages (e.g., `ConversationUpdated` events).
3. **Expected**: Metrics showing:
   - Requests to `chat-service-dapr:9090` for `/chat/` and pub/sub.
   - Requests to `agent-memory-service-dapr:9091` for state store and subscriptions.

### Steps
1. **Enable Zipkin**:
   - Add the `zipkin` service to `compose.yml`.
   - Create `components/tracing.yaml` with Zipkin configuration.
   - Update Dapr sidecars with `--config /components/tracing.yaml`.
   - Verify traces at `http://localhost:9411` after running tests.
2. **Enable Prometheus**:
   - Add the `prometheus` service to `compose.yml`.
   - Create `prometheus.yml` with Dapr metrics targets.
   - Add `--metrics-port 9090` (Chat Service) and `9091` (Agent Memory Service) to Dapr sidecars.
   - Verify metrics at `http://localhost:9090` (e.g., `dapr_http_server_request_count`).
3. **Test Observability**:
   - Run the `/chat/` tests and check Zipkin for request traces.
   - Query Prometheus for Dapr metrics to confirm pub/sub and HTTP activity.

**Zipkin**:
```bash
docker-compose logs zipkin
```

**Expected**:
- Confirms Zipkin is running and receiving spans from Dapr sidecars.

**Prometheus**:
```bash
docker-compose logs prometheus
```

**Expected**:
- Confirms Prometheus is scraping metrics from `chat-service-dapr:9090` and `agent-memory-service-dapr:9091`.

---
### Why It Matters
- **Tracing**: Helps debug request flows (e.g., Chat Service → Agent Memory Service → Redis).
- **Metrics**: Monitors system health (e.g., request rates, errors), critical for scaling.

---

## Step 8: Next Steps
You’ve successfully used Docker Compose to manage the DACA microservices, adding Zipkin and Prometheus as a challenge. Explore Step 8, 9, 10, 11 with Docker Compose:

### Cleanup
To stop and remove containers:
```bash
docker-compose down
```

To remove volumes:
```bash
docker-compose down -v
```

---

## Conclusion
We’ve transitioned the DACA microservices from manual `docker run` commands in **13_dapr_containerization** to a streamlined Docker Compose setup, applying concepts from **14_docker_compose_introduction**. The `compose.yml` file defines the Chat Service, Agent Memory Service, Dapr sidecars, Redis, Zipkin, and Prometheus, maintaining core functionality (history, metadata, events) while adding observability through tracing and metrics. This setup is now easier to manage, production-ready, and extensible for future tutorials.

---