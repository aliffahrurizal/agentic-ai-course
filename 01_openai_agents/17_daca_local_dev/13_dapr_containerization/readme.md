# Containerizing DACA Microservices with Docker and Dapr

Welcome to the thirteenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll containerize the Chat Service and Analytics Service from **11_dapr_observability** using Docker. We’ll create Dockerfiles for each service, build container images, and run the services as containers with Dapr sidecars. This will prepare our microservices for production deployment and set the stage for using Docker Compose in the next tutorial. Let’s dive in!

---

## What You’ll Learn
- How to create Dockerfiles for the Chat Service and Analytics Service.
- Building container images for the microservices.
- Running the containerized microservices with Dapr sidecars.
- Verifying the containerized setup with the same tests from **11_dapr_observability**.
- Preparing for Docker Compose in the next tutorial.

## Prerequisites
- Completion of **11_dapr_observability** (codebase with Chat Service and Analytics Service using Dapr Service Invocation, State Management, Pub/Sub Messaging, Workflows, Secrets Management, Actors, and Observability).
- Completion of **12_docker_and_desktop** (understanding of Docker, Docker Desktop, and containerization concepts).
- Docker and Docker Desktop installed (from **12_docker_and_desktop**).
- Dapr CLI and runtime installed (from **04_dapr_theory_and_cli**).
- Python 3.8+ installed (for local development, though we’ll use containers for running the services).
- An OpenAI API key (stored in `components/secrets.json`).

---

## Step 1: Recap of the Current Setup
In **11_dapr_observability**, we enhanced our microservices with Dapr’s observability features:
- The **Chat Service**:
  - Uses a Dapr Workflow to orchestrate message processing: fetching the user’s message count (via Service Invocation), retrieving conversation history (via Actors), generating a reply (using the OpenAI Agents SDK), storing the conversation (via Actors), and publishing a “MessageSent” event (via Pub/Sub).
  - Retrieves the OpenAI API key from a Dapr secrets store.
  - Uses a `UserSessionActor` to manage per-user conversation history.
  - Includes logging, tracing (Zipkin), and metrics (Prometheus) for observability.
- The **Analytics Service**:
  - Subscribes to the `messages` topic and updates the user’s message count in the Dapr state store when a “MessageSent” event is received.
  - Includes logging, tracing, and metrics for observability.

### Current Limitations
- **Non-Containerized Deployment**: We’ve been running the services directly on the host using `uv run uvicorn`, which doesn’t guarantee consistency across environments (e.g., development, production).
- **Dependency Management**: Dependencies are installed on the host, which can lead to conflicts or inconsistencies if the host environment changes.
- **Scalability and Deployment**: Without containerization, it’s harder to scale the services or deploy them to a cloud environment (e.g., Kubernetes).

### Goal for This Tutorial
We’ll containerize the Chat Service and Analytics Service:
- Create Dockerfiles to define container images for each service.
- Build the images and run the services as containers with Dapr sidecars.
- Ensure the containerized setup works the same as the non-containerized setup by running the same tests from **11_dapr_observability**.
- Prepare for using Docker Compose in the next tutorial to simplify running the multi-container application.

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
│   ├── secrets.json
│   └── tracing.yaml
├── prometheus.yml
├── pyproject.toml
└── uv.lock
```

---

## Step 2: Why Containerize with Docker and Dapr?
Containerizing our microservices with Docker and Dapr offers several benefits:
- **Consistency**: Containers ensure the Chat Service and Analytics Service run the same way in any environment (e.g., local development, CI/CD pipelines, production).
- **Dependency Isolation**: Each service’s dependencies (e.g., Python packages, Dapr SDK) are packaged in its container, avoiding conflicts.
- **Scalability**: Containers can be easily scaled and orchestrated (e.g., with Kubernetes) in production.
- **Simplified Deployment**: Dapr sidecars run alongside the application containers, providing consistent access to Dapr building blocks (e.g., state management, pub/sub, actors).
- **Production Readiness**: Containerization is a standard practice for deploying microservices in cloud-native environments.

---

## Step 3: Create Dockerfiles for the Microservices
We’ll create a `Dockerfile` for each service to define how to build their container images. Both services are Python-based FastAPI applications, so the Dockerfiles will be similar but tailored to each service’s requirements.

### Step 3.1: Dockerfile for the Chat Service
Create a `Dockerfile` in the `chat_service` directory:
```bash
touch chat_service/Dockerfile
```

Edit `chat_service/Dockerfile`:
```dockerfile
# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files
COPY pyproject.toml uv.lock /app/

# Install uv for dependency management
RUN pip install uv

# Install dependencies using uv
RUN uv sync --frozen

# Copy the application code
COPY . /app

# Expose the port the Chat Service will run on
EXPOSE 8000

# Define the command to run the Chat Service
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Explanation of the Dockerfile
- `FROM python:3.9-slim`: Uses a lightweight Python 3.9 image as the base.
- `WORKDIR /app`: Sets the working directory inside the container to `/app`.
- `COPY pyproject.toml uv.lock /app/`: Copies the dependency files to the container.
- `RUN pip install uv`: Installs `uv` for dependency management.
- `RUN uv sync --frozen`: Installs the dependencies specified in `pyproject.toml` and `uv.lock`.
- `COPY . /app`: Copies the entire `chat_service` directory (including `main.py`, `user_session_actor.py`, etc.) to the container.
- `EXPOSE 8000`: Documents that the container listens on port `8000` (used by Uvicorn/FastAPI).
- `CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`: Runs the Chat Service using `uv run uvicorn`.

### Step 3.2: Dockerfile for the Analytics Service
Create a `Dockerfile` in the `analytics_service` directory:
```bash
touch analytics_service/Dockerfile
```

Edit `analytics_service/Dockerfile`:
```dockerfile
# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency files
COPY pyproject.toml uv.lock /app/

# Install uv for dependency management
RUN pip install uv

# Install dependencies using uv
RUN uv sync --frozen

# Copy the application code
COPY . /app

# Expose the port the Analytics Service will run on
EXPOSE 8001

# Define the command to run the Analytics Service
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

#### Explanation of the Dockerfile
- Similar to the Chat Service’s Dockerfile, but:
  - `EXPOSE 8001`: The Analytics Service runs on port `8001`.
  - `CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]`: Runs the Analytics Service on port `8001`.

### Step 3.3: Update the Project Structure
The updated project structure now includes the Dockerfiles:
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

## Step 4: Build the Container Images
We’ll build container images for both services using the `docker build` command.

### Step 4.1: Build the Chat Service Image
Navigate to the `chat_service` directory and build the image:
```bash
cd chat_service
docker build -t chat-service:latest .
```

Output:
```
Sending build context to Docker daemon  10.24kB
Step 1/7 : FROM python:3.9-slim
 ---> abc123def456
Step 2/7 : WORKDIR /app
 ---> Running in 789xyz
 ---> 123abc456def
Step 3/7 : COPY pyproject.toml uv.lock /app/
 ---> 456def789xyz
Step 4/7 : RUN pip install uv
 ---> Running in def123abc456
Collecting uv
  Downloading uv-0.1.0-py3-none-any.whl (1.2 MB)
     |████████████████████████████████| 1.2 MB 5.0 MB/s
Installing collected packages: uv
Successfully installed uv-0.1.0
 ---> 789xyz123abc
Step 5/7 : RUN uv sync --frozen
 ---> Running in abc456def123
Resolved 10 packages in 1.23s
Downloaded 10 packages in 2.45s
Installed 10 packages in 0.89s
 ---> def123abc789
Step 6/7 : COPY . /app
 ---> 123xyz456abc
Step 7/7 : EXPOSE 8000
 ---> Running in 456abc789def
 ---> 789def123abc
Step 8/8 : CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
 ---> Running in abc123xyz456
 ---> 456xyz789def
Successfully built 456xyz789def
Successfully tagged chat-service:latest
```

### Step 4.2: Build the Analytics Service Image
Navigate to the `analytics_service` directory and build the image:
```bash
cd ../analytics_service
docker build -t analytics-service:latest .
```

Output:
```
Sending build context to Docker daemon  8.192kB
Step 1/7 : FROM python:3.9-slim
 ---> abc123def456
Step 2/7 : WORKDIR /app
 ---> Using cache
 ---> 123abc456def
Step 3/7 : COPY pyproject.toml uv.lock /app/
 ---> 789xyz123abc
Step 4/7 : RUN pip install uv
 ---> Using cache
 ---> 789xyz123abc
Step 5/7 : RUN uv sync --frozen
 ---> Running in def123abc456
Resolved 8 packages in 0.98s
Downloaded 8 packages in 1.89s
Installed 8 packages in 0.67s
 ---> 123xyz456abc
Step 6/7 : COPY . /app
 ---> 456abc789def
Step 7/7 : EXPOSE 8001
 ---> Running in xyz789abc123
 ---> def123abc789
Step 8/8 : CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
 ---> Running in abc456xyz789
 ---> 789def123xyz
Successfully built 789def123xyz
Successfully tagged analytics-service:latest
```

### Step 4.3: Verify the Images
List the images to confirm they were built:
```bash
docker images
```
Output:
```
REPOSITORY          TAG       IMAGE ID       CREATED         SIZE
chat-service        latest    456xyz789def   2 minutes ago   150MB
analytics-service   latest    789def123xyz   1 minute ago    145MB
python              3.9-slim  abc123def456   1 week ago      45MB
```

---

## Step 5: Run the Containerized Microservices with Dapr
We’ll run the Chat Service and Analytics Service as containers, with Dapr sidecars providing access to Dapr building blocks (e.g., state management, pub/sub, actors). Since the services are now containerized, we’ll use `docker run` instead of `dapr run` with `uv run uvicorn`. Dapr provides a containerized runtime, so we’ll run Dapr sidecars as separate containers alongside our application containers.

### Step 5.1: Prepare the Environment
Before running the containers, ensure the following are running (from **11_dapr_observability**):
- **Redis**: Used for Dapr state store and pub/sub (should already be running from `dapr init`).
- **Zipkin**: For distributed tracing.
  ```bash
  docker run -d -p 9411:9411 openzipkin/zipkin
  ```
- **Prometheus**: For metrics collection.
  ```bash
  docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
  ```

### Step 5.2: Run the Analytics Service with Dapr
We’ll run the Analytics Service container and its Dapr sidecar container, ensuring they can communicate with each other and with Redis, Zipkin, and Prometheus.

1. **Run the Analytics Service Container**:
   ```bash
   docker run -d --name analytics-service-app -p 8001:8001 --network host analytics-service:latest
   ```
   - `--name analytics-service-app`: Names the container.
   - `-p 8001:8001`: Maps port `8001` on the host to port `8001` in the container.
   - `--network host`: Uses the host network for simplicity (so the container can communicate with Redis, Zipkin, etc., on localhost). In production, you’d use a Docker network.
   - `analytics-service:latest`: The image to run.

2. **Run the Dapr Sidecar for the Analytics Service**:
   ```bash
   docker run -d --name analytics-service-dapr \
     -v $(pwd)/components:/components \
     --network host \
     daprio/dapr:1.12 \
     dapr run \
     --app-id analytics-service \
     --app-port 8001 \
     --dapr-http-port 3501 \
     --metrics-port 9091 \
     --log-level debug \
     --config /components/tracing.yaml \
     --components-path /components
   ```
   - `--name analytics-service-dapr`: Names the Dapr sidecar container.
   - `-v $(pwd)/components:/components`: Mounts the `components` directory into the container so Dapr can access `subscriptions.yaml`, `secretstore.yaml`, etc.
   - `--network host`: Uses the host network for communication.
   - `daprio/dapr:1.12`: The Dapr runtime image (version 1.12 as of April 2025; adjust if a newer version is available).
   - `dapr run ...`: The Dapr command to start the sidecar, with the same arguments we used previously:
     - `--app-id analytics-service`: Identifies the application.
     - `--app-port 8001`: The port the Analytics Service runs on.
     - `--dapr-http-port 3501`: The port for Dapr’s HTTP API.
     - `--metrics-port 9091`: The port for Dapr metrics.
     - `--log-level debug`: Enables detailed logging.
     - `--config /components/tracing.yaml`: Applies the tracing configuration.
     - `--components-path /components`: Specifies the path to Dapr components.

### Step 5.3: Run the Chat Service with Dapr
Similarly, we’ll run the Chat Service container and its Dapr sidecar.

1. **Run the Chat Service Container**:
   ```bash
   docker run -d --name chat-service-app -p 8000:8000 --network host chat-service:latest
   ```

2. **Run the Dapr Sidecar for the Chat Service**:
   ```bash
   docker run -d --name chat-service-dapr \
     -v $(pwd)/components:/components \
     --network host \
     daprio/dapr:1.12 \
     dapr run \
     --app-id chat-service \
     --app-port 8000 \
     --dapr-http-port 3500 \
     --dapr-grpc-port 50001 \
     --metrics-port 9090 \
     --log-level debug \
     --config /components/tracing.yaml \
     --components-path /components
   ```

### Step 5.4: Verify the Containers Are Running
List the running containers:
```bash
docker ps
```
Output:
```
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                    NAMES
abc123def456   chat-service       "uv run uvicorn main…"   1 minute ago    Up 1 minute                             chat-service-app
789xyz123abc   daprio/dapr:1.12   "dapr run --app-id c…"   1 minute ago    Up 1 minute                             chat-service-dapr
def456abc789   analytics-service  "uv run uvicorn main…"   2 minutes ago   Up 2 minutes                            analytics-service-app
123abc789xyz   daprio/dapr:1.12   "dapr run --app-id a…"   2 minutes ago   Up 2 minutes                            analytics-service-dapr
xyz789abc123   openzipkin/zipkin  "start-zipkin"           5 minutes ago   Up 5 minutes   9410/tcp, 9411/tcp       zipkin
456def123abc   prom/prometheus    "/bin/prometheus --c…"   5 minutes ago   Up 5 minutes   0.0.0.0:9090->9090/tcp  prometheus
```

#### Notes on Networking
- We used `--network host` for simplicity, allowing containers to communicate with each other and with Redis, Zipkin, and Prometheus on `localhost`. In a production setup, you’d create a Docker network (e.g., `docker network create dapr-network`) and run all containers on that network, using container names or service discovery for communication.
- The Dapr sidecars communicate with their respective applications (e.g., `chat-service-app` on port `8000`) and with each other (e.g., for service invocation).

---

## Step 6: Test the Containerized Microservices
We’ll run the same tests from **11_dapr_observability** to verify the containerized setup works as expected.

### Step 6.1: Initialize State for Testing
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

### Step 6.2: Test the Chat Service
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
Check the Chat Service container logs:
```bash
docker logs chat-service-app
```
Output (similar to **11_dapr_observability**):
```
2025-04-06 04:01:00,123 - ChatService - INFO - Received chat request for user bob: Hi, how are you?
2025-04-06 04:01:00,124 - ChatService - INFO - Scheduling workflow with instance_id: chat-bob-1744064460
2025-04-06 04:01:00,125 - ChatService - INFO - Starting workflow for user bob with message: Hi, how are you?
...
2025-04-06 04:01:00,161 - ChatService - INFO - Completed workflow for user bob
```

Check the Analytics Service container logs:
```bash
docker logs analytics-service-app
```
Output:
```
2025-04-06 04:01:00,162 - AnalyticsService - INFO - Received event: {'user_id': 'bob', 'event_type': 'MessageSent'}
2025-04-06 04:01:00,163 - AnalyticsService - INFO - Incrementing message count for user bob
...
2025-04-06 04:01:00,169 - AnalyticsService - INFO - Processed MessageSent event for user bob
```

#### Observe Traces in Zipkin
- Open `http://localhost:9411` and find the trace for the `/chat/` request. It should show the same spans as in **11_dapr_observability** (e.g., service invocation, actor interactions, pub/sub).

#### Observe Metrics in Prometheus
- Open `http://localhost:9090` and query metrics like `dapr_http_server_request_count` and `dapr_actor_active_actors`. The metrics should reflect the containerized setup.

### Step 6.3: Verify Message Count
Check the updated message count for `bob`:
- Visit `http://localhost:8001/docs` and test `/analytics/bob`:
  - Expected: `{"message_count": 4}`

---

## Step 7: Why Containerization for DACA?
Containerizing the Chat Service and Analytics Service with Docker and Dapr enhances our architecture by:
- **Consistency**: The services now run in containers, ensuring they behave the same way in any environment.
- **Dependency Isolation**: Dependencies are packaged in the container images, avoiding conflicts on the host.
- **Scalability**: Containers can be easily scaled in a production environment (e.g., with Kubernetes).
- **Simplified Deployment**: Dapr sidecars run as containers alongside the application containers, providing consistent access to Dapr building blocks.

---

## Step 8: Next Steps
You’ve successfully containerized the Chat Service and Analytics Service with Docker and Dapr! In the next tutorial (**14_docker_compose**), we’ll introduce **Docker Compose** to simplify running our multi-container application, including the services, Dapr sidecars, Redis, Zipkin, and Prometheus.

### Optional Exercises
1. Push the `chat-service` and `analytics-service` images to Docker Hub:
   - Tag the images: `docker tag chat-service:latest <your-dockerhub-username>/chat-service:latest`.
   - Log in to Docker Hub: `docker login`.
   - Push the images: `docker push <your-dockerhub-username>/chat-service:latest`.
2. Create a Docker network and run the containers on that network instead of using `--network host`.
3. Add health checks to the Dockerfiles (e.g., using `HEALTHCHECK`) to monitor the services’ health.

---

## Conclusion
In this tutorial, we containerized the Chat Service and Analytics Service using Docker, created Dockerfiles, built container images, and ran the services with Dapr sidecars. The containerized setup works the same as the non-containerized setup, as verified by our tests, and prepares us for production deployment. We’re now ready to explore Docker Compose in the next tutorial to simplify running our multi-container application!

---

### Final Dockerfile for `chat_service/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN pip install uv

RUN uv sync --frozen

COPY . /app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Final Dockerfile for `analytics_service/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN pip install uv

RUN uv sync --frozen

COPY . /app

EXPOSE 8001

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

---

This tutorial successfully containerized our DACA microservices, setting the stage for using Docker Compose in the next tutorial. 