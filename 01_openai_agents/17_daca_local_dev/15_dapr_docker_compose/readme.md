# Running DACA Microservices with Docker Compose and Dapr

Welcome to the fifteenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll use Docker Compose to manage the containerized Chat Service and Analytics Service from **13_dapr_containerization**, along with their Dapr sidecars and supporting services (Redis, Zipkin, Prometheus). We’ll create a `docker-compose.yml` file to define all components, start the application with a single command, and verify that it works as expected. This will streamline our development workflow and set the stage for deploying the application to a prototyping and production environment (e.g., Azure Container App, Kubernetes) in future tutorials. Let’s dive in!

---

## What You’ll Learn
- How to define a multi-container DACA application using a `docker-compose.yml` file.
- Running the Chat Service, Analytics Service, Dapr sidecars, Redis, Zipkin, and Prometheus with Docker Compose.
- Verifying the application works the same as in **13_dapr_containerization**.
- Benefits of using Docker Compose with Dapr for managing microservices.

## Prerequisites
- Completion of **13_dapr_containerization** (containerized Chat Service and Analytics Service with Dapr sidecars).
- Completion of **14_docker_compose** (understanding of Docker Compose concepts and usage).
- Docker and Docker Desktop installed (from **12_docker_and_desktop**).
- Dapr CLI and runtime installed (from **04_dapr_theory_and_cli**), though we’ll use Dapr’s containerized runtime.
- An OpenAI API key (stored in `components/secrets.json`).

---

## Step 1: Recap of the Current Setup
In **13_dapr_containerization**, we containerized the Chat Service and Analytics Service:
- **Chat Service**:
  - Uses a Dapr Workflow to orchestrate message processing: fetching the user’s message count (via Service Invocation), retrieving conversation history (via Actors), generating a reply (using the OpenAI Agents SDK), storing the conversation (via Actors), and publishing a “MessageSent” event (via Pub/Sub).
  - Retrieves the OpenAI API key from a Dapr secrets store.
  - Uses a `UserSessionActor` to manage per-user conversation history.
  - Includes logging, tracing (Zipkin), and metrics (Prometheus) for observability.
- **Analytics Service**:
  - Subscribes to the `messages` topic and updates the user’s message count in the Dapr state store when a “MessageSent” event is received.
  - Includes logging, tracing, and metrics for observability.
- We built Docker images (`chat-service:latest` and `analytics-service:latest`) and ran them with Dapr sidecars using `docker run` commands.

### Current Limitations
- **Manual Container Management**: In **13_dapr_containerization**, we started each container (Chat Service, Analytics Service, Dapr sidecars, Redis, Zipkin, Prometheus) individually with `docker run` commands, which is error-prone and cumbersome.
- **Networking Complexity**: We used `--network host` for simplicity, but this isn’t ideal for production as it bypasses Docker’s network isolation.
- **Dependency Management**: There’s no clear way to ensure services start in the correct order (e.g., Redis before Dapr sidecars, Dapr sidecars before application services).

### Goal for This Tutorial
We’ll use Docker Compose to:
- Define all components (Chat Service, Analytics Service, Dapr sidecars, Redis, Zipkin, Prometheus) in a single `docker-compose.yml` file.
- Start the entire application with a single `docker-compose up` command.
- Use a custom Docker network for proper isolation and communication between services.
- Verify the application works the same as in **13_dapr_containerization** by running the same tests.
- Prepare for production deployment in future tutorials.

### Current Project Structure
```
fastapi-daca-tutorial/
├── chat_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── user_session_actor.py
│   ├── models.py
│   └── tests/
│       └── test_main.py
├── analytics_service/
│   ├── Dockerfile
│   ├── main.py
│   ├── models.py
│   └── tests/
│       └── test_main.py
├── components/
│   ├── subscriptions.yaml
│   ├── secretstore.yaml
│   ├── secrets.json
│   └── tracing.yaml
├── prometheus.yml
├── pyproject.toml
└── uv.lock
```

---

## Step 2: Why Use Docker Compose with Dapr?
Using Docker Compose with Dapr simplifies the management of our multi-container application by:
- **Centralized Configuration**: Define all services (application containers, Dapr sidecars, supporting services) in a single `docker-compose.yml` file.
- **Simplified Commands**: Start and stop the entire application with `docker-compose up` and `docker-compose down`, instead of multiple `docker run` commands.
- **Networking**: Docker Compose creates a default network, allowing services to communicate using service names (e.g., `chat-service` can reach `analytics-service` via Dapr).
- **Dependency Management**: Docker Compose can handle dependencies between services, ensuring they start in the correct order (e.g., Redis before Dapr sidecars).
- **Development Efficiency**: Streamlines local development and testing by providing a reproducible environment for all components.

---

## Step 3: Create the `docker-compose.yml` File
We’ll create a `docker-compose.yml` file in the root of the project (`fastapi-daca-tutorial`) to define all services.

### Step 3.1: Define the `docker-compose.yml`
Create the `docker-compose.yml` file:
```bash
touch docker-compose.yml
```

Edit `docker-compose.yml`:
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
    volumes:
      - ./components:/components
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
    volumes:
      - ./components:/components
    depends_on:
      - analytics-service-app
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

#### Explanation of the `docker-compose.yml`
- `version: "3.9"`: Specifies the Docker Compose file format version.
- `services`:
  - `redis`:
    - `image: redis:6.2`: Uses the Redis 6.2 image.
    - `ports: - "6379:6379"`: Exposes Redis on port `6379`.
    - `volumes: - redis-data:/data`: Persists Redis data in a named volume.
    - `networks: - dapr-network`: Connects to the custom network.
  - `zipkin`:
    - `image: openzipkin/zipkin`: Uses the Zipkin image for distributed tracing.
    - `ports: - "9411:9411"`: Exposes the Zipkin UI on port `9411`.
    - `networks: - dapr-network`: Connects to the custom network.
  - `prometheus`:
    - `image: prom/prometheus`: Uses the Prometheus image for metrics.
    - `ports: - "9090:9090"`: Exposes the Prometheus UI on port `9090`.
    - `volumes: - ./prometheus.yml:/etc/prometheus/prometheus.yml`: Mounts the `prometheus.yml` configuration file.
    - `networks: - dapr-network`: Connects to the custom network.
  - `chat-service-app`:
    - `build: ./chat_service`: Builds the image from the `Dockerfile` in the `chat_service` directory.
    - `ports: - "8000:8000"`: Exposes the Chat Service on port `8000`.
    - `depends_on: - redis`: Ensures Redis starts before the Chat Service.
    - `environment: - PYTHONUNBUFFERED=1`: Ensures Python output is unbuffered for better logging.
    - `networks: - dapr-network`: Connects to the custom network.
  - `chat-service-dapr`:
    - `image: daprio/dapr:1.12`: Uses the Dapr runtime image (version 1.12 as of April 2025).
    - `command`: Specifies the Dapr sidecar command with the same arguments as in **13_dapr_containerization** (e.g., `--app-id`, `--app-port`, `--dapr-http-port`).
    - `volumes: - ./components:/components`: Mounts the `components` directory for Dapr configuration.
    - `depends_on`: Ensures the Chat Service, Redis, Zipkin, and Prometheus start first.
    - `networks: - dapr-network`: Connects to the custom network.
  - `analytics-service-app`:
    - `build: ./analytics_service`: Builds the image from the `Dockerfile` in the `analytics_service` directory.
    - `ports: - "8001:8001"`: Exposes the Analytics Service on port `8001`.
    - `depends_on: - redis`: Ensures Redis starts first.
    - `environment: - PYTHONUNBUFFERED=1`: Ensures Python output is unbuffered.
    - `networks: - dapr-network`: Connects to the custom network.
  - `analytics-service-dapr`:
    - Similar to `chat-service-dapr`, but configured for the Analytics Service (e.g., `--app-id analytics-service`, `--app-port 8001`).
- `networks`:
  - `dapr-network`: Defines a custom bridge network for all services to communicate. Unlike `--network host` in **13_dapr_containerization**, this provides proper isolation and allows services to communicate using service names (e.g., `redis`, `zipkin`).
- `volumes`:
  - `redis-data`: A named volume to persist Redis data.

### Step 3.2: Update `prometheus.yml`
Since we’re no longer using `--network host`, Prometheus needs to scrape metrics from the Dapr sidecars using their service names on the `dapr-network`. Update `prometheus.yml` to use the service names:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dapr'
    static_configs:
      - targets: ['chat-service-dapr:9090', 'analytics-service-dapr:9091']
```

#### Explanation of the Update
- `targets: ['chat-service-dapr:9090', 'analytics-service-dapr:9091']`: Uses the service names (`chat-service-dapr`, `analytics-service-dapr`) and their metrics ports on the `dapr-network`. Docker Compose’s DNS resolution allows Prometheus to reach these services by name.

### Step 3.3: Update Dapr Components for Networking
Since we’re using a custom network (`dapr-network`), we need to update the Dapr components to reference services by their service names instead of `localhost`.

#### Update `components/tracing.yaml`
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
- Changed `endpointAddress` from `http://localhost:9411/api/v2/spans` to `http://zipkin:9411/api/v2/spans` to use the `zipkin` service name on the network.

#### Update Dapr Component References (if needed)
The default Dapr components for Redis (state store and pub/sub) are configured via `dapr init`, but since we’re running Redis as a service in Docker Compose, Dapr will use the default Redis host (`localhost:6379`) unless overridden. We’ll override this by setting environment variables for the Dapr sidecars to use the `redis` service name.

Add the following environment variables to the `chat-service-dapr` and `analytics-service-dapr` services in `docker-compose.yml`:

Update the `chat-service-dapr` and `analytics-service-dapr` services in `docker-compose.yml`:
```yaml
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
    depends_on:
      - chat-service-app
      - redis
      - zipkin
      - prometheus
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
```
- `environment: - DAPR_REDIS_HOST=redis:6379`: Overrides the default Redis host for Dapr to use the `redis` service name on the network.

---

## Step 4: Run the Application with Docker Compose
### Step 4.1: Start the Application
From the project root (`fastapi-daca-tutorial`), start the application:
```bash
docker-compose up -d
```

Output:
```
Creating network "fastapi-daca-tutorial_dapr-network" with driver "bridge"
Creating volume "fastapi-daca-tutorial_redis-data" with default driver
Creating fastapi-daca-tutorial_redis_1 ... done
Creating fastapi-daca-tutorial_zipkin_1 ... done
Creating fastapi-daca-tutorial_prometheus_1 ... done
Building chat-service-app
Step 1/7 : FROM python:3.9-slim
 ---> abc123def456
Step 2/7 : WORKDIR /app
 ---> Using cache
 ---> 123abc456def
...
Successfully built 456xyz789def
Successfully tagged fastapi-daca-tutorial_chat-service-app:latest
Building analytics-service-app
Step 1/7 : FROM python:3.9-slim
 ---> abc123def456
...
Successfully built 789def123xyz
Successfully tagged fastapi-daca-tutorial_analytics-service-app:latest
Creating fastapi-daca-tutorial_chat-service-app_1 ... done
Creating fastapi-daca-tutorial_analytics-service-app_1 ... done
Creating fastapi-daca-tutorial_chat-service-dapr_1 ... done
Creating fastapi-daca-tutorial_analytics-service-dapr_1 ... done
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
fastapi-daca-tutorial_zipkin_1                   start-zipkin                     Up      0.0.0.0:9411->9411/tcp
```

#### What Happened?
- Docker Compose created a custom network (`dapr-network`) for all services to communicate.
- It created a named volume (`redis-data`) for Redis persistence.
- It built the `chat-service-app` and `analytics-service-app` images from their respective Dockerfiles.
- It pulled the images for Redis, Zipkin, Prometheus, and Dapr.
- It started all services in the correct order based on `depends_on` (e.g., Redis before Dapr sidecars, Dapr sidecars before application services).
- Services can communicate using their service names (e.g., `chat-service-dapr` reaches `redis` at `redis:6379`).

---

## Step 5: Test the Application
We’ll run the same tests from **13_dapr_containerization** to verify the application works as expected in the Docker Compose setup.

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

### Step 5.2: Test the Chat Service
Send a request to the Chat Service to trigger the workflow:
```bash
curl -X POST http://localhost:8000/chat/ -H "Content-Type: application/json" -d '{"user_id": "bob", "text": "Hi, how are you?", "metadata": {"timestamp": "2025-04-06T12:00:00Z", "session_id": "123e4567-e89b-12d3-a456-426614174001"}, "tags": ["greeting"]}'
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
Check the Chat Service logs:
```bash
docker-compose logs chat-service-app
```
Output:
```
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,123 - ChatService - INFO - Received chat request for user bob: Hi, how are you?
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,124 - ChatService - INFO - Scheduling workflow with instance_id: chat-bob-1744064460
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,125 - ChatService - INFO - Starting workflow for user bob with message: Hi, how are you?
...
fastapi-daca-tutorial_chat-service-app_1  | 2025-04-06 04:01:00,161 - ChatService - INFO - Completed workflow for user bob
```

Check the Analytics Service logs:
```bash
docker-compose logs analytics-service-app
```
Output:
```
fastapi-daca-tutorial_analytics-service-app_1  | 2025-04-06 04:01:00,162 - AnalyticsService - INFO - Received event: {'user_id': 'bob', 'event_type': 'MessageSent'}
fastapi-daca-tutorial_analytics-service-app_1  | 2025-04-06 04:01:00,163 - AnalyticsService - INFO - Incrementing message count for user bob
...
fastapi-daca-tutorial_analytics-service-app_1  | 2025-04-06 04:01:00,169 - AnalyticsService - INFO - Processed MessageSent event for user bob
```

#### Observe Traces in Zipkin
- Open `http://localhost:9411` and find the trace for the `/chat/` request. It should show the same spans as in **13_dapr_containerization** (e.g., service invocation, actor interactions, pub/sub).

#### Observe Metrics in Prometheus
- Open `http://localhost:9090` and query metrics like `dapr_http_server_request_count` and `dapr_actor_active_actors`. The metrics should reflect the containerized setup.

### Step 5.3: Verify Message Count
Check the updated message count for `bob`:
- Visit `http://localhost:8001/docs` and test `/analytics/bob`:
  - Expected: `{"message_count": 4}`

---

## Step 6: Why Docker Compose with Dapr for DACA?
Using Docker Compose with Dapr enhances our DACA architecture by:
- **Simplified Management**: We can start and stop the entire application (services, Dapr sidecars, Redis, Zipkin, Prometheus) with a single command.
- **Proper Networking**: The custom `dapr-network` provides isolation and allows services to communicate using service names, improving security and maintainability.
- **Dependency Handling**: Docker Compose ensures services start in the correct order (e.g., Redis before Dapr sidecars, Dapr sidecars before application services).
- **Reproducibility**: The `docker-compose.yml` file ensures the application can be consistently reproduced across environments, making it easier to share and deploy.
- **Production Readiness**: This setup mirrors how the application might run in a production environment (e.g., Kubernetes), where multiple containers need to work together.

---

## Step 7: Next Steps
You’ve successfully used Docker Compose to manage the Chat Service, Analytics Service, Dapr sidecars, and supporting services in a single `docker-compose.yml` file! 

### Exercises for Students
1. Add health checks to the `docker-compose.yml` file for each service (e.g., using `healthcheck` to ensure Redis and the application services are healthy).
2. Scale the Chat Service using Docker Compose (e.g., `docker-compose up -d --scale chat-service-app=2`) and observe how Dapr handles multiple instances.
3. Add a Grafana service to the `docker-compose.yml` file to visualize Prometheus metrics.

---

## Conclusion
In this tutorial, we used Docker Compose to define and run our DACA microservices (Chat Service and Analytics Service) with Dapr sidecars, Redis, Zipkin, and Prometheus. The `docker-compose.yml` file simplified the management of our multi-container application, allowing us to start everything with a single command and ensuring proper networking and dependency handling. The application works the same as in **13_dapr_containerization**, as verified by our tests.

---

### Final `docker-compose.yml`
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

networks:
  dapr-network:
    driver: bridge

volumes:
  redis-data:
```

### Final `prometheus.yml`
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'dapr'
    static_configs:
      - targets: ['chat-service-dapr:9090', 'analytics-service-dapr:9091']
```

### Final `components/tracing.yaml`
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

---

This tutorial successfully integrated Docker Compose with our DACA microservices, streamlining the development workflow. 