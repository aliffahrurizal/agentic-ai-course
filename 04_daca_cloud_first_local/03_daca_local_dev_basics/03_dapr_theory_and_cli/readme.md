# [DAPR](https://dapr.io/) Theory and CLI

Let's proceed with the second tutorial in the **Dapr Agentic Cloud Ascent (DACA)** series. In this tutorial, we’ll focus on introducing **Dapr** (Distributed Application Runtime), a key component of DACA, and provide a comprehensive guide to the **Dapr CLI**. We’ll cover the theory behind Dapr, its building blocks, and how it simplifies building distributed systems. 

Dapr is a cornerstone of DACA’s architecture, enabling seamless inter-service communication, state management, and event-driven workflows for agentic AI systems. We’ll set up a local Kubernetes cluster, install the Dapr CLI, deploy Dapr, and explore its CLI commands through a practical example. This tutorial prepares you to build DACA microservices in subsequent steps.

We won’t carry forward the code examples from previous tutorials here, but we’ll set the stage for integrating Dapr with our microservices in the next tutorial.

[Join Dapr University](https://www.diagrid.io/dapr-university)

---

## Understanding Dapr, Mastering the Dapr CLI, and Exploring the Dapr Scheduler

Welcome to the second tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll explore **Dapr** (Distributed Application Runtime), a powerful framework that simplifies building distributed, cloud-native applications. Dapr is a cornerstone of DACA’s architecture, enabling seamless inter-service communication, state management, and more. We’ll start with a comprehensive introduction to Dapr, its architecture, and its building blocks. Then, we’ll dive into the **Dapr CLI**, covering its installation, key commands, and practical usage examples. This tutorial will prepare you to integrate Dapr with our microservices in the next step. Let’s get started!

---

## What You’ll Learn

- What Dapr is, its architecture, and its role in DACA.
- The core building blocks of Dapr and how they address distributed system challenges.
- How to install and set up the Dapr CLI.
- A comprehensive guide to the Dapr CLI, with practical examples of its commands.
- What the Dapr Scheduler is, its role in Dapr, and how to manage it using the Dapr CLI.

## Prerequisites

- Basic familiarity with distributed systems concepts (e.g., microservices, messaging).
- A development environment with Docker installed (Dapr uses Docker for its runtime).
- Familiarity with the command line.

---

## Step 1: Introduction to Dapr

### [What is Dapr](https://docs.dapr.io/concepts/overview/)?

Dapr is a portable, event-driven runtime that makes it easy for any developer to build resilient, stateless, and stateful applications that run on the cloud and edge and embraces the diversity of languages and developer frameworks.

It is an open-source, portable runtime for building distributed applications, particularly microservices. Launched by Microsoft, Dapr provides a set of **building blocks** that abstract common distributed system challenges, such as service-to-service communication, state management, and pub/sub messaging. Dapr runs as a **sidecar** alongside your application, enabling you to focus on business logic while Dapr handles the complexities of distributed systems.

#### Key Features of Dapr

- **Language Agnostic**: Dapr works with any programming language (e.g., Python, Go, Java) via HTTP or gRPC APIs.
- **Sidecar Architecture**: Dapr runs as a separate process (sidecar) next to your app, providing isolation and portability.
- **Building Blocks**: Standardized APIs for common distributed system patterns (e.g., state, pub/sub, service invocation).
- **Pluggable Components**: Dapr supports multiple backends (e.g., Redis, Kafka, Postgres) for each building block, configurable via YAML files.
- **Cloud-Native**: Designed for containerized environments like Kubernetes, but also works locally.

#### Dapr Architecture

Dapr follows a **sidecar pattern**:

- **Application**: Your microservice (e.g., a FastAPI app).
- **Dapr Sidecar**: A separate process running alongside your app, providing Dapr’s APIs.
- **Dapr APIs**: Your app communicates with the Dapr sidecar via HTTP or gRPC (e.g., `http://localhost:3500/v1.0/invoke`).
- **Components**: Dapr interacts with external systems (e.g., Redis for state, RabbitMQ for pub/sub) via pluggable components.

For example:

- Your FastAPI app makes an HTTP call to the Dapr sidecar to save state.
- The Dapr sidecar forwards the request to a configured state store (e.g., Redis).
- The sidecar handles retries, errors, and other complexities transparently.

#### Why Dapr for DACA?

Dapr is a perfect fit for DACA’s goals of building scalable, resilient, agentic AI systems:

- **Simplified Communication**: Dapr’s service invocation and pub/sub building blocks streamline inter-service communication between microservices (e.g., Chat Service and Analytics Service).
- **State Management**: Dapr manages state for stateless services, aligning with DACA’s stateless container design.
- **Resilience**: Dapr provides retries, timeouts, and circuit breakers, ensuring fault tolerance in distributed systems.
- **Scalability**: Dapr integrates seamlessly with Kubernetes, supporting DACA’s planet-scale deployment stage.
- **Flexibility**: Dapr’s pluggable components allow us to use free-tier services (e.g., Upstash Redis, CloudAMQP) during prototyping.

---

## Step 2: Dapr Building Blocks

Dapr provides a set of **building blocks** that address common challenges in distributed systems. Each building block is accessible via a standardized API, and Dapr supports multiple implementations (components) for each block. Here’s an overview of the key building blocks relevant to DACA:

1. **Service Invocation**:

   - Enables direct, synchronous communication between services.
   - Dapr handles service discovery, retries, and load balancing.
   - Example: The Chat Service calls the Analytics Service to fetch user data.

2. **State Management**:

   - Provides a key-value store for managing state (e.g., user sessions, message counts).
   - Supports multiple backends (e.g., Redis, CockroachDB).
   - Example: Store a user’s message count in Dapr’s state store instead of a mock dictionary.

3. **Publish/Subscribe (Pub/Sub)**:

   - Enables asynchronous, event-driven communication between services.
   - Supports message brokers like RabbitMQ, Kafka, and Redis.
   - Example: The Chat Service publishes a “MessageSent” event, and the Analytics Service subscribes to update message counts.

4. **Bindings**:

   - Connects applications to external systems (e.g., HTTP endpoints, databases) via input/output bindings.
   - Example: Trigger a service when a new message arrives in a queue.

5. **Actors**:

   - Implements the actor model for stateful, concurrent processing.
   - Example: Use actors to manage individual user sessions with encapsulated state.

6. **Workflows**:

   - Orchestrates long-running workflows with retries and compensation logic.
   - Example: Coordinate a multi-step process (e.g., user message → analytics update → response).

7. **Secrets**:

   - Securely manages secrets (e.g., API keys, database credentials).
   - Example: Store the OpenAI API key in Dapr’s secret store.

8. **Configuration**:

   - Manages application configuration (e.g., feature flags).
   - Example: Toggle agentic features dynamically.

9. **Observability**:
   - Provides tracing, logging, and metrics for monitoring.
   - Example: Trace requests between the Chat Service and Analytics Service using Zipkin.

In DACA, we’ll primarily use **Service Invocation**, **State Management**, **Pub/Sub**, **Workflows**, and **Observability** to build our agentic AI system.

---

## Step 3: Installing the Dapr CLI

The **Dapr CLI** is the primary tool for interacting with Dapr, allowing you to initialize Dapr, run applications with Dapr sidecars, manage components, and more. Let’s install and set up the Dapr CLI.

### [Install the Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)

#### On macOS/Linux

Use HomeBrew or install directly:

```bash
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
```

OR

```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

#### On Windows (PowerShell)

```powershell
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
```

#### Verify Installation

Check the Dapr CLI version:

```bash
dapr --version
```

Output:

```
CLI version: 1.15.1
Runtime version: n/a
```
```bash
dapr -h
```

### Install the Dapr Runtime

The Dapr CLI requires the Dapr runtime to be installed on your system. This includes the Dapr sidecar and its dependencies (e.g., Redis for default components).

#### [Initialize Dapr](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/#install-dapr-from-the-offical-dapr-helm-chart-with-development-flag)

Run the following command to initialize Dapr:

```bash
dapr init -k --wait --timeout 600
```

This command:

- Initializes Dapr on the Kubernetes cluster on your current context

Output:

```
mjs@Muhammads-MacBook-Pro-3 01_kubernetes_basics % dapr init -k
⌛  Making the jump to hyperspace...
ℹ️  Note: To install Dapr using Helm, see here: https://docs.dapr.io/getting-started/install-dapr-kubernetes/#install-with-helm-advanced

ℹ️  Container images will be pulled from Docker Hub
✅  Deploying the Dapr control plane with latest version to your cluster...
✅  Deploying the Dapr dashboard with latest version to your cluster...
✅  Success! Dapr has been installed to namespace dapr-system. To verify, run `dapr status -k' in your terminal. To get started, go here: https://docs.dapr.io/getting-started
```

#### Verify Dapr Setup

```bash
dapr status -k
```

```bash
mjs@Muhammads-MacBook-Pro-3 01_kubernetes_basics % dapr status -k
  NAME                   NAMESPACE    HEALTHY  STATUS   REPLICAS  VERSION  AGE  CREATED              
  dapr-placement-server  dapr-system  True     Running  1         1.15.4   16s  2025-04-21 09:12.35  
  dapr-sentry            dapr-system  True     Running  1         1.15.4   16s  2025-04-21 09:12.35  
  dapr-scheduler-server  dapr-system  True     Running  3         1.15.4   16s  2025-04-21 09:12.35  
  dapr-operator          dapr-system  True     Running  1         1.15.4   16s  2025-04-21 09:12.35  
  dapr-sidecar-injector  dapr-system  True     Running  1         1.15.4   16s  2025-04-21 09:12.35  
```

You can also use:

```bash
kubectl get pods -n dapr-system
```

```bash
NAME                                     READY   STATUS    RESTARTS   AGE
dapr-operator-5fbcb75589-zsc4q           1/1     Running   0          4m41s
dapr-placement-server-0                  1/1     Running   0          4m41s
dapr-scheduler-server-0                  1/1     Running   0          4m41s
dapr-scheduler-server-1                  1/1     Running   0          4m41s
dapr-scheduler-server-2                  1/1     Running   0          4m41s
dapr-sentry-75b55cbb9-x8mrk              1/1     Running   0          4m41s
dapr-sidecar-injector-76545c8c59-srw6j   1/1     Running   0          4m41s
```

### Set Up a Local Components Directory

Now we will manually define and apply Dapr components from a local directory

1. Create redis.yaml
```yaml
# Redis Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dapr-dev-redis-master
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dapr-dev-redis
  template:
    metadata:
      labels:
        app: dapr-dev-redis
    spec:
      containers:
      - name: redis
        image: redis:7
        ports:
        - containerPort: 6379
---
# Redis Service
apiVersion: v1
kind: Service
metadata:
  name: dapr-dev-redis-master
  namespace: default
spec:
  selector:
    app: dapr-dev-redis
  ports:
  - port: 6379
    targetPort: 6379
```

2. Create a components directory

```bash
mkdir -p ./components
cd ./components
```

3. Create statestore.yaml
```yaml
# Dapr State Store Component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: dapr-dev-redis-master:6379
  - name: redisPassword
    value: ""
auth:
  secretStore: kubernetes
```

4. Define pubsub.yaml

```yaml
# Dapr Pub/Sub Component
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: default
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: dapr-dev-redis-master:6379
  - name: redisPassword
    value: ""
auth:
  secretStore: kubernetes
```

4. Deploy Redis:
```bash
cd ..
kubectl apply -f redis.yaml
```

Output
```bash
deployment.apps/dapr-dev-redis-master created
service/dapr-dev-redis-master created
```

5. Configure Components

```basH
kubectl apply -f components -n default
```

OUTPUT:
```basH
component.dapr.io/pubsub created
component.dapr.io/statestore created
```

Check Components:
```bash
dapr components -k --namespace default
```

```bash
  NAMESPACE  NAME        TYPE          VERSION  SCOPES  CREATED              AGE  
  default    pubsub      pubsub.redis  v1               2025-04-21 15:43.42  34s  
  default    statestore  state.redis   v1               2025-04-21 15:43.42  34s 
```

## Step 4: Comprehensive Guide to the Dapr CLI

The Dapr CLI provides a rich set of commands for managing Dapr applications, components, and runtime. Let’s explore the most important commands with practical examples.

### 1. `dapr init -k  --dev`

- **Purpose**: Initializes Dapr in kubernetes cluster.
- **Usage**:
  ```bash
  dapr init -k --dev
  ```
- **What It Does**:
  - Installs the Dapr runtime.
  - Pulls Docker images for Dapr’s control plane and default components (e.g., Redis).

#### Example: Reinitialize Dapr

If you need to reinitialize Dapr (e.g., after uninstalling):

```bash
dapr init -k --runtime-version 1.13.1
```

The `--runtime-version` flag specifies the Dapr version to install.

---

### 2. `dapr uninstall -k`

- **Purpose**: Removes Dapr from your machine.
- **Usage**:
  ```bash
  dapr uninstall -k
  ```
- **What It Does**:
  - Stops and removes Dapr containers (e.g., Redis).
  - Deletes Dapr binaries and configuration files.

#### Example: Uninstall Dapr

```bash
dapr uninstall -k --all
```

The `--all` flag also removes Docker images and volumes.

---

### 3. `dapr run`

- **Purpose**: Runs an application with a Dapr sidecar.
- **Usage**:
  ```bash
  dapr run --app-id <app-id> --app-port <port> --dapr-http-port <dapr-port> -- <command>
  ```
- **Options**:
  - `--app-id`: A unique identifier for your application.
  - `--app-port`: The port your app listens on.
  - `--dapr-http-port`: The port for the Dapr sidecar’s HTTP API.
  - `<command>`: The command to run your app (e.g., `uvicorn main:app`).

#### Example: Run a Simple Python App with Dapr

Create a simple FastAPI app in a new directory to test `dapr run`:

```bash
uv init dapr-test-app
cd dapr-test-app
uv venv
source .venv/bin/activate

uv add "fastapi[standard]"
```

Create `main.py`:

```python
from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI()
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/statestore"

@app.get("/")
async def root():
    return {"message": "Hello from Dapr Test App!"}

@app.post("/save-state")
async def save_state(key: str, value: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(STATE_URL, json=[{"key": key, "value": value}])
            response.raise_for_status()
            return {"status": "State saved successfully"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-state/{key}")
async def get_state(key: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{STATE_URL}/{key}")
            response.raise_for_status()
            return {"key": key, "value": response.json()}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail="State not found")
```

Create a Dockerfile
```Dockerfile
FROM python:3.12-slim
WORKDIR /code
COPY . .
RUN pip install uv
RUN uv sync --frozen
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Add a .dockerignore file
```yaml
.venv
.git
.gitignore
.env
```

Build and Push the Docker Image
- Build the image:
```bash
nerdctl build -t dapr-test-app:latest .
```
- Load the image into the cluster:
```bash
nerdctl save dapr-test-app:latest | nerdctl --namespace k8s.io load
```

Now create test-app.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dapr-test-app
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dapr-test-app
  template:
    metadata:
      labels:
        app: dapr-test-app
        version: v1  # Added to trigger pod recreation
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "test-app"
        dapr.io/app-port: "8000"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: app
        image: dapr-test-app:latest
        imagePullPolicy: IfNotPresent  # Explicitly use local image
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: dapr-test-app
  namespace: default
spec:
  selector:
    app: dapr-test-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

Apply it:
```bash
kubectl apply -f test-app.yaml -n default
```

Verify Deployment:
```bash
kubectl rollout status deploy/dapr-test-app -n default
```

Test the App
- Port-forward the service:

```bash
kubectl port-forward service/dapr-test-app 8000:80 -n default
```

Test the root endpoint:
```bash
curl http://localhost:8000/
{"message":"Hello from Dapr Test App!"}%                                    
```

Save State
```bash
curl -X POST "http://localhost:8000/save-state?key=mykey&value=myvalue"
```

Output:
{"status":"State saved successfully"}%  

Get State
```bash
mjs@Muhammads-MacBook-Pro-3 learn-agentic-ai % curl http://localhost:8000/get-state/mykey
```

Output
```bash
{"key":"mykey","value":"myvalue"}%            
```

---

### 4. `dapr list`

- **Purpose**: Lists all running Dapr applications.
- **Usage**:
  ```bash
  dapr list
  ```
- **What It Does**:
  - Displays the app ID, app port, Dapr HTTP/gRPC ports, and runtime status of running apps.

#### Example: List Running Apps

In a new terminal, run:

```bash
dapr list -k
```

Output:

```
  NAMESPACE  APP ID    APP PORT  AGE  CREATED              
  default    test-app  8000      21m  2025-04-21 16:08.07 
```

---

### 5. `dapr status` (KUBERNETES ONLY OPTION)

- **Purpose**: Shows the status of the Dapr control plane.
- **Usage**:
  ```bash
  dapr status -k
  ```
- **What It Does**:
  - Displays the health of Dapr system services (e.g., daprd, placement).

#### Example: Check Dapr Status

```bash
dapr status -k
```

Output:

```
  NAME            HEALTHY  VERSION  AGE  CREATED
  daprd           True     1.13.1   1h   2025-04-06 10:00:00
  placement       True     1.13.1   1h   2025-04-06 10:00:00
  sentry          True     1.13.1   1h   2025-04-06 10:00:00
  operator        True     1.13.1   1h   2025-04-06 10:00:00
```

---

## Step 5: Why Dapr CLI for DACA?

The Dapr CLI is essential for DACA because:

- **Local Development**: Commands like `dapr run` and `dapr dashboard` simplify local testing of microservices with Dapr sidecars.
- **Debugging**: `dapr list`, `dapr invoke`, and `dapr publish` help test and debug service interactions.
- **Component Management**: `dapr components` and `dapr configurations` allow us to configure Dapr for different environments (e.g., local Redis, CloudAMQP in production).
- **Production Readiness**: Commands like `dapr status` ensure the Dapr runtime is healthy before deployment.

---


### Exercises for Students

1. Create a custom Dapr component (e.g., a state store using a different backend like in-memory) and list it with `dapr components`.

---

## Conclusion

In this tutorial, we introduced Dapr, explored its building blocks, and provided a comprehensive guide to the Dapr CLI. 

---
