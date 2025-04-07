# [DAPR](https://dapr.io/) Theory and CLI

Let's proceed with the fourth tutorial in the **Dapr Agentic Cloud Ascent (DACA)** series. In this tutorial, we’ll focus on introducing **Dapr** (Distributed Application Runtime), a key component of DACA, and provide a comprehensive guide to the **Dapr CLI**. We’ll cover the theory behind Dapr, its building blocks, and how it simplifies building distributed systems. Then, we’ll dive into the Dapr CLI, exploring its commands with practical examples. We won’t carry forward the code examples from previous tutorials here, but we’ll set the stage for integrating Dapr with our microservices in the next tutorial.

---

## Understanding Dapr, Mastering the Dapr CLI, and Exploring the Dapr Scheduler

Welcome to the fourth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this step, we’ll explore **Dapr** (Distributed Application Runtime), a powerful framework that simplifies building distributed, cloud-native applications. Dapr is a cornerstone of DACA’s architecture, enabling seamless inter-service communication, state management, and more. We’ll start with a comprehensive introduction to Dapr, its architecture, and its building blocks. Then, we’ll dive into the **Dapr CLI**, covering its installation, key commands, and practical usage examples. This tutorial will prepare you to integrate Dapr with our microservices in the next step. Let’s get started!

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
CLI version: 1.15.0
Runtime version: n/a
```

### Install the Dapr Runtime

The Dapr CLI requires the Dapr runtime to be installed on your system. This includes the Dapr sidecar and its dependencies (e.g., Redis for default components).

#### [Initialize Dapr](https://docs.dapr.io/getting-started/install-dapr-selfhost/)

Run the following command to initialize Dapr:

```bash
dapr init
```

This command:

- Downloads and installs the Dapr runtime binaries.
- Sets up a default Redis container for state and pub/sub components.
- Configures default component files in `~/.dapr/components/`.

Output:

```
⌚  Making the jump to hyperspace...
ℹ  Installing runtime version 1.13.1
⬇  Downloading binaries and setting up components...
✅  Success! Dapr has been installed to /usr/local/bin. To get started, please visit https://docs.dapr.io/getting-started/
ℹ  Container images for Dapr have been pulled to your local machine
ℹ  Dapr control plane has been initialized in your local environment
ℹ  Note: To verify that Dapr has been installed properly, restart your terminal session
```

#### Verify Dapr Runtime

Check the Dapr runtime version:

```bash
dapr --version
```

Output:

```
CLI version: 1.13.1
Runtime version: 1.13.1
```

Check that the Dapr Redis container is running:

```bash
docker ps
```

You should see a container named `dapr_redis` running on port `6379`.

### Verify components directory has been initialized

On dapr init, the CLI also creates a default components folder that contains several YAML files with definitions for a state store, Pub/sub, and Zipkin. The Dapr sidecar will read these components and use:

- The Redis container for state management and messaging.
- The Zipkin container for collecting traces.

Verify by opening your components directory:

- On Windows, under %UserProfile%\.dapr
- On Linux/MacOS, under ~/.dapr or ls $HOME/.dapr

---

## Step 4: Comprehensive Guide to the Dapr CLI

The Dapr CLI provides a rich set of commands for managing Dapr applications, components, and runtime. Let’s explore the most important commands with practical examples.

### 1. `dapr init`

- **Purpose**: Initializes Dapr on your machine.
- **Usage**:
  ```bash
  dapr init
  ```
- **What It Does**:
  - Installs the Dapr runtime.
  - Pulls Docker images for Dapr’s control plane and default components (e.g., Redis).
  - Creates a `~/.dapr/` directory with default configuration and components.

#### Example: Reinitialize Dapr

If you need to reinitialize Dapr (e.g., after uninstalling):

```bash
dapr init --runtime-version 1.13.1
```

The `--runtime-version` flag specifies the Dapr version to install.

---

### 2. `dapr uninstall`

- **Purpose**: Removes Dapr from your machine.
- **Usage**:
  ```bash
  dapr uninstall
  ```
- **What It Does**:
  - Stops and removes Dapr containers (e.g., Redis).
  - Deletes Dapr binaries and configuration files.

#### Example: Uninstall Dapr

```bash
dapr uninstall --all
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
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Dapr Test App!"}
```

Run the app with Dapr:

```bash
dapr run --app-id test-app --app-port 8000 --dapr-http-port 3500 -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

- `test-app` is the app ID.
- `8000` is the app port.
- `3500` is the Dapr sidecar port (default for Dapr’s HTTP API).

Output:

```
== APP == INFO:     Started server process [12345]
== APP == INFO:     Waiting for application startup.
== APP == INFO:     Application startup complete.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
ℹ  Starting Dapr with id test-app. HTTP Port: 3500  gRPC Port: 50001
✅  You're up and running! Both Dapr and your app logs will appear here.
```

Visit `http://localhost:8000/` to confirm the app is running:

```json
{ "message": "Hello from Dapr Test App!" }
```

---

### 4. `dapr dashboard`

- **Purpose**: Opens the Dapr dashboard, a web UI for monitoring Dapr applications.
- **Usage**:
  ```bash
  dapr dashboard
  ```
- **What It Does**:
  - Starts a web server (default port `8080`).
  - Provides a UI to view running Dapr apps, components, and logs.

#### Example: Open the Dapr Dashboard

While the test app is running, open a new terminal and run:

```bash
dapr dashboard
```

Output:

```
ℹ  Starting Dapr Dashboard on http://localhost:8080
```

Visit `http://localhost:8080` in your browser. You’ll see:

- The `test-app` application with its Dapr sidecar.
- Configured components (e.g., Redis for state and pub/sub).
- Logs and health status.

---

### 5. `dapr components` (OPTIONAL FOR KUBERNETES SETUP)

- **Purpose**: Lists the Dapr components configured in your environment.
- **Usage**:
  ```bash
  dapr components
  ```
- **What It Does**:
  - Displays the components defined in `~/.dapr/components/` (or a custom components directory).

#### Example: List Components

```bash
dapr components
```

Output:

```
  NAME           TYPE           CREATED
  statestore     state.redis    2025-04-06 10:00:00
  pubsub         pubsub.redis   2025-04-06 10:00:00
```

These are the default components created by `dapr init`, using Redis as the backend.

---

### 6. `dapr configurations` (OPTIONAL FOR KUBERNETES SETUP)

- **Purpose**: Lists the Dapr configurations (e.g., tracing settings).
- **Usage**:
  ```bash
  dapr configurations
  ```
- **What It Does**:
  - Displays the configurations defined in `~/.dapr/config.yaml`.

#### Example: List Configurations

```bash
dapr configurations
```

Output:

```
  NAME        TRACING-ENABLED  TRACING-EXPORTER
  dapr        true             zipkin
```

The default configuration enables tracing with Zipkin.

---

### 7. `dapr stop`

- **Purpose**: Stops a running Dapr application.
- **Usage**:
  ```bash
  dapr stop --app-id <app-id>
  ```
- **What It Does**:
  - Stops the Dapr sidecar and the associated app process.

#### Example: Stop the Test App

Stop the `test-app` we started earlier:

```bash
dapr stop --app-id test-app
```

Output:

```
✅  Stopped app with id: test-app
```

---

### 8. `dapr list`

- **Purpose**: Lists all running Dapr applications.
- **Usage**:
  ```bash
  dapr list
  ```
- **What It Does**:
  - Displays the app ID, app port, Dapr HTTP/gRPC ports, and runtime status of running apps.

#### Example: List Running Apps

First, restart the test app:

```bash
cd dapr-test-app
dapr run --app-id test-app --app-port 8000 --dapr-http-port 3500 -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

In a new terminal, run:

```bash
dapr list
```

Output:

```
  APP ID     HTTP PORT  GRPC PORT  APP PORT  COMMAND                          AGE  CREATED              STATUS
  test-app   3500       50001      8000      uv run uvicorn main:app --ho...  10s  2025-04-06 10:05:00  Running
```

---

### 9. `dapr invoke`

- **Purpose**: Invokes a method on a Dapr application (tests service invocation).
- **Usage**:
  ```bash
  dapr invoke --app-id <app-id> --method <method> --data <data>
  ```
- **What It Does**:
  - Sends an HTTP request to the Dapr sidecar, which forwards it to the specified app method.

#### Example: Invoke the Root Endpoint

With the test app running, invoke the `/` endpoint:

```bash
dapr invoke --app-id test-app --method / --verb GET
{"message":"Hello from Dapr Test App!"}
```

Output:

```
{"message":"Hello from Dapr Test App!"}
✅  App invoked successfully
```

---

### 10. `dapr publish`

- **Purpose**: Publishes a message to a pub/sub topic.
- **Usage**:
  ```bash
  dapr publish --pubsub <pubsub-name> --topic <topic> --data <data>
  ```
- **What It Does**:
  - Publishes a message to the specified topic using the configured pub/sub component.

#### Example: Publish a Message

Publish a message to a topic named `messages` using the default `pubsub` component:

```bash
dapr publish --publish-app-id test-app --pubsub pubsub --topic messages --data '{"message": "Hello, Dapr!"}'
```

Output:

```
✅  Event published successfully
```

Since no service is subscribed to this topic yet, the message is sent to Redis but not consumed. We’ll explore pub/sub in a later tutorial.

---

### 11. `dapr status` (KUBERNETES ONLY OPTION)

- **Purpose**: Shows the status of the Dapr control plane.
- **Usage**:
  ```bash
  dapr status
  ```
- **What It Does**:
  - Displays the health of Dapr system services (e.g., daprd, placement).

#### Example: Check Dapr Status

```bash
dapr status
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

## Step 6: Introduction to the Dapr Scheduler

### What is the Dapr Scheduler?

The **Dapr Scheduler** is a control plane service introduced in Dapr 1.14 (September 2024) to manage scheduled jobs, actor reminders, and workflows. It’s designed to improve the scalability and performance of scheduling tasks in Dapr, addressing limitations of earlier approaches (e.g., using the Placement service for actor reminders). The Scheduler service runs as a separate process in both self-hosted and Kubernetes environments, storing job data in an embedded **etcd** database for persistence and reliability.

#### Key Features of the Dapr Scheduler

- **Job Scheduling**: Supports the **Jobs API**, allowing applications to schedule tasks to run at a specific time or on a recurring schedule (e.g., database backups, email notifications).
- **Actor Reminders**: Since Dapr 1.15 (March 2025), the Scheduler manages actor reminders by default, improving scalability over the previous Placement service approach.
- **Workflow Support**: Enhances the **Workflow API** by managing reminders and timers for long-running processes.
- **High Availability (HA)**: In Kubernetes, the Scheduler always runs in HA mode with multiple replicas for load balancing. In self-hosted mode, HA is optional but recommended for production.
- **Load Balancing**: All Scheduler replicas are peers (no leader), and jobs are distributed across replicas for efficient execution.
- **Persistence**: Jobs and reminders are stored in an embedded etcd database, ensuring they survive restarts (if properly configured).

#### How the Dapr Scheduler Works

1. **Scheduling a Job**:
   - An application uses the Jobs API (via HTTP/gRPC) to schedule a job, specifying details like name, schedule, repeats, and data payload.
   - The Dapr sidecar forwards the job to the Scheduler service, which stores it in etcd.
2. **Triggering a Job**:
   - At the scheduled time, the Scheduler sends the job back to the Dapr sidecar via a streaming connection.
   - The sidecar delivers the job to the application, which executes the associated business logic.
3. **Error Handling**:
   - Client-side errors (e.g., app fails to process the job) trigger retries (default: 3 retries with a 1-second interval).
   - Non-client-side errors (e.g., no available sidecar) place the job in a staging queue until a sidecar is available.

#### Dapr Scheduler in DACA

The Dapr Scheduler is crucial for DACA because:

- **Agentic AI Workflows**: DACA’s agentic AI systems often require scheduled tasks (e.g., periodic data updates, timed agent actions), which the Scheduler handles efficiently.
- **Scalability**: The Scheduler’s HA mode and load balancing align with DACA’s goal of planetary-scale deployment.
- **Reliability**: Persistent storage in etcd ensures that scheduled jobs and reminders aren’t lost during failures, supporting DACA’s resilience requirements.

---

## Step 7: Managing the Dapr Scheduler with the Dapr CLI

The Dapr CLI provides tools to interact with the Scheduler service, especially for monitoring and debugging. Let’s explore how to manage the Scheduler using CLI commands.

### 7.1 Verify the Scheduler Service is Running

The Scheduler service is automatically started as part of `dapr init` (or `dapr init -k` for Kubernetes). Let’s confirm it’s running.

#### Check Running Containers

Since the Scheduler runs as a Docker container in self-hosted mode, use Docker to verify:

```bash
docker ps
```

Output (look for the Scheduler container):

```
CONTAINER ID   IMAGE                        COMMAND                  CREATED        STATUS        PORTS     NAMES
abc123def456   daprio/dapr:1.13.1           "./scheduler"            1 hour ago     Up 1 hour             dapr_scheduler
xyz789ghi012   redis:7                      "docker-entrypoint.s…"   1 hour ago     Up 1 hour     6379/tcp  dapr_redis
```

The `dapr_scheduler` container runs the Scheduler service, and `dapr_redis` supports default components.

#### Check Dapr Status

Use the `dapr status` command to check the health of Dapr control plane services, including the Scheduler:

```bash
dapr status
```

Output:

```
  NAME            HEALTHY  VERSION  AGE  CREATED
  daprd           True     1.13.1   1h   2025-04-06 04:00:00
  placement       True     1.13.1   1h   2025-04-06 04:00:00
  sentry          True     1.13.1   1h   2025-04-06 04:00:00
  operator        True     1.13.1   1h   2025-04-06 04:00:00
  scheduler       True     1.13.1   1h   2025-04-06 04:00:00
```

The `scheduler` service should be listed as `HEALTHY`. Note: The version here is 1.13.1 for illustration, but as of April 2025, you’d likely be using Dapr 1.15 or later, where the Scheduler is enabled by default for actor reminders.

### 7.2 View Scheduler Logs

To debug or monitor the Scheduler, you can view its logs via Docker.

#### Find the Scheduler Container ID

```bash
docker ps
```

Note the `CONTAINER ID` for `dapr_scheduler` (e.g., `5bb3c4f34c38`).

#### View Logs

```bash
docker logs 5bb3c4f34c38
```

Output (example):

```
time="2025-04-06T04:00:00Z" level=info msg="Dapr Scheduler starting up..."
time="2025-04-06T04:00:01Z" level=info msg="Connected to etcd database"
time="2025-04-06T04:00:02Z" level=info msg="Scheduler service running in non-HA mode"
```

This confirms the Scheduler is running and connected to its etcd database. In a production setup, you’d configure HA mode for better reliability.

### .73 Test the Jobs API with `dapr publish`

The Scheduler manages jobs scheduled via the **Jobs API**. While we can’t directly schedule a job using the CLI (this requires an application using the Jobs API), we can simulate a related interaction by publishing a message to a pub/sub topic, which could trigger a job in a real application. Let’s use the `dapr publish` command to demonstrate this concept.

#### Publish a Message

Publish a message to a topic named `schedule-job`, simulating an event that might trigger a job:

```bash
dapr publish --publish-app-id test-app --pubsub pubsub --topic schedule-job --data '{"job_name": "test-job", "schedule": "@every 1m"}'
```

Output:

```
✅  Event published successfully
```

This message is sent to the default `pubsub` component (Redis). In a real application, a service subscribed to this topic could schedule a job using the Jobs API, which the Scheduler would then manage. We’ll implement this pattern in the next tutorial.

### 7.4 Check Scheduler Configuration in the Dashboard

The Dapr dashboard provides a UI to monitor the Scheduler and other services.

#### Open the Dashboard

```bash
dapr dashboard
```

Visit `http://localhost:8080` in your browser. Navigate to the **Control Plane** section to see the Scheduler service listed alongside other services (e.g., placement, sentry). You can also check logs and health status here.

### 7.5 Scheduler Interaction with a Test App

To see the Scheduler in action, let’s create a minimal application that schedules a job using the Jobs API. This will give us a practical example of how the Scheduler works, and we’ll use the CLI to run and monitor it.

[Jobs API reference](https://docs.dapr.io/reference/api/jobs_api/)
[Dapr Scheduler control plane service overview] (https://docs.dapr.io/concepts/dapr-services/scheduler/)

#### Create a Simple Python App

The Jobs API is currently best supported in the Go SDK (as of Dapr 1.15). The Dapr Python SDK currently interacts with the Jobs API primarily through direct HTTP calls to the Dapr sidecar. We can use the DaprClient for this. Here's how we can set it up:

- Scheduling: We'll create a FastAPI endpoint (e.g., /schedule) that, when called, will use the DaprClient to make an HTTP PUT request to the Dapr sidecar's Jobs API endpoint (/v1.0/jobs/<app-id>/<job-name>) to schedule the job.
- Handling: Dapr's Scheduler will trigger the job by sending an HTTP POST request back to our application at a specific endpoint (conventionally /jobs/<job-name>). We need to create a FastAPI endpoint to receive this POST request.

##### 1. Create Project Structure and Install Dependencies:

```bash
uv init dapr-scheduler-test-py
cd dapr-scheduler-test-py
uv venv
source .venv/bin/activate

uv add "fastapi[standard]"
uv add dapr dapr-ext-fastapi
```

##### 2. Create the FastAPI App (main.py):

Create `main.py`:

```python
import logging
import datetime
import os
import httpx  # Import httpx
# Added Path import for path parameters
from fastapi import FastAPI, Body, HTTPException, Path

logging.basicConfig(level=logging.INFO)

# Configuration
APP_ID = "scheduler-test-py"  # Still useful for context/logging
# JOB_NAME = "test-job-py" # We'll use path parameters instead of a fixed name
JOB_SCHEDULE_INTERVAL = "@every 10s"  # Default schedule
JOB_REPEATS = 3  # Default repeats
JOB_DATA = {"message": "Hello from Python Job!"}  # Default data
# Get Dapr port from environment variable (set by dapr run)
# Default to 3500 if not set
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_JOB_API_BASE = f"http://localhost:{DAPR_HTTP_PORT}/v1.0-alpha1/jobs"

# --- FastAPI App Setup ---
app = FastAPI(title=f"{APP_ID} Service")

# --- Dapr Job Handler Endpoint ---
# This endpoint receives the job invocation from the Dapr Scheduler sidecar
# It needs to handle potentially different job names if scheduled dynamically
# Using a path parameter for the job name


@app.post("/job/{job_name}")
async def job_handler(job_name: str = Path(...), job_data: dict = Body(...)):
    """Handles incoming job events from Dapr for any job name."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    logging.info(f"Received job '{job_name}' at {timestamp}")
    logging.info(f"Job data: {job_data}")
    # In a real app, perform the scheduled task here
    return {"status": "SUCCESS", "received_at": timestamp, "data": job_data}

# --- Endpoint to Schedule a Dapr Job ---


@app.post("/schedule-job/{job_name}")
async def schedule_job_endpoint(job_name: str = Path(...)):
    """Schedules the job using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to schedule job: {job_name}")

    # Using defaults, could be extended to take payload from request body
    job_payload = {
        "schedule": JOB_SCHEDULE_INTERVAL,
        "repeats": JOB_REPEATS,
        "data": JOB_DATA,
    }

    schedule_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: POST {schedule_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(schedule_url, json=job_payload)
            resp.raise_for_status()
            logging.info(f"Job scheduling response status: {resp.status_code}")
            if resp.status_code == 204:
                return {"status": "SUCCESS", "message": f"Job '{job_name}' scheduled successfully.", "response": resp.text}
            else:
                # httpx response.text is a property, not an awaitable method
                response_text = resp.text
                return {"status": "UNEXPECTED_STATUS", "message": f"Unexpected status code {resp.status_code}: {response_text}"}
    # ... (keep existing exception handling blocks) ...
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error scheduling job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        logging.error(
            f"Dapr API Error scheduling job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error scheduling job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# --- Endpoint to Get Dapr Job Data ---
@app.get("/get-job/{job_name}")
async def get_job_endpoint(job_name: str = Path(...)):
    """Gets job data using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to get job data for: {job_name}")
    get_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: GET {get_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(get_url)
            # Check for 404 specifically as Dapr might return that if job not found
            if resp.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"Job '{job_name}' not found by Dapr.")
            resp.raise_for_status()  # Handle other errors (e.g., 500 from Dapr)
            logging.info(f"Get job response status: {resp.status_code}")
            job_details = resp.json()  # Get JSON response body
            return {"status": "SUCCESS", "job_details": job_details}
    # ... (keep existing exception handling blocks, adjusted for GET context) ...
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error getting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        # Catch 404 handled above, log others
        logging.error(
            f"Dapr API Error getting job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error getting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# --- Endpoint to Delete a Dapr Job ---
@app.delete("/delete-job/{job_name}")
async def delete_job_endpoint(job_name: str = Path(...)):
    """Deletes a job using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to delete job: {job_name}")
    delete_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: DELETE {delete_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.delete(delete_url)
            if resp.status_code == 404:
                logging.warning(
                    f"Attempted to delete job '{job_name}', but Dapr reported not found (404).")
                # Decide if 404 is an error or acceptable (treat as success here)
                return {"status": "SUCCESS", "message": f"Job '{job_name}' not found or already deleted."}
            resp.raise_for_status()  # Handle other errors
            logging.info(f"Delete job response status: {resp.status_code}")
            # Expect 204 No Content on successful delete
            if resp.status_code == 204:
                return {"status": "SUCCESS", "message": f"Job '{job_name}' deleted successfully."}
            else:
                return {"status": "UNEXPECTED_STATUS", "message": f"Unexpected status code {resp.status_code}"}
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error deleting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        # Catch 404 handled above, log others
        logging.error(
            f"Dapr API Error deleting job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error deleting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/")
async def root():
    return {"message": f"Welcome to {APP_ID}. Use POST /schedule-job/{{job_name}}, GET /get-job/{{job_name}}, DELETE /delete-job/{{job_name}}."}

```

##### 3. Run the App with Dapr:

```bash
dapr run --app-id scheduler-test-py --app-port 8000 --dapr-http-port 3500 -- uvicorn main:app --host 0.0.0.0 --port 8000
```

##### 4. Schedule the Job:

Once the app and sidecar are running, open localhost:8000/docs and try posting a new JOB.

#### Monitor with `dapr list`

While the app is running, check the running Dapr apps:

```bash
dapr list
```

Output:

```
  APP ID             HTTP PORT  GRPC PORT  APP PORT  COMMAND               AGE  CREATED              DAPRD PID  CLI PID  APP PID  RUN TEMPLATE PATH  APP LOG PATH  DAPRD LOG PATH  RUNTEMPLATENAME  
  scheduler-test-py  3500       55330      8000      uvicorn main:app ...  18m  2025-04-07 17:02.37  64438      64435    64439 
```

##### Observe Logs

After scheduling a job you will see it working

```bash
== APP == INFO:root:Attempting to schedule job: JJ
== APP == INFO:root:Calling Dapr Jobs API URL: POST http://localhost:3500/v1.0-alpha1/jobs/JJ
== APP == INFO:httpx:HTTP Request: POST http://localhost:3500/v1.0-alpha1/jobs/JJ "HTTP/1.1 204 No Content"
== APP == INFO:root:Job scheduling response status: 204
== APP == INFO:     127.0.0.1:55962 - "POST /schedule-job/JJ HTTP/1.1" 200 OK
== APP == INFO:root:Received job 'JJ' at 2025-04-07T12:25:31.013638+00:00
== APP == INFO:root:Job data: {'message': 'Hello from Python Job!'}
== APP == INFO:     127.0.0.1:55966 - "POST /job/JJ HTTP/1.1" 200 OK
== APP == INFO:root:Received job 'JJ' at 2025-04-07T12:25:41.008143+00:00
== APP == INFO:root:Job data: {'message': 'Hello from Python Job!'}
== APP == INFO:     127.0.0.1:55969 - "POST /job/JJ HTTP/1.1" 200 OK
== APP == INFO:root:Received job 'JJ' at 2025-04-07T12:25:51.007388+00:00
== APP == INFO:root:Job data: {'message': 'Hello from Python Job!'}
== APP == INFO:     127.0.0.1:55970 - "POST /job/JJ HTTP/1.1" 200 OK

```

#### Stop the App

```bash
dapr stop --app-id scheduler-test-py
```

Output:

```
✅  app stopped successfully: scheduler-test-py
```

This example demonstrates how the Scheduler manages jobs scheduled via the Jobs API, and how the Dapr CLI helps run and monitor the application.

---

## Step 8: Why Dapr Scheduler for DACA?

The Dapr Scheduler enhances DACA’s architecture by:

- **Efficient Scheduling**: Handles timed tasks for agentic AI (e.g., periodic data syncs, scheduled agent actions).
- **Scalability**: HA mode and load balancing ensure the Scheduler can handle DACA’s planet-scale workloads.
- **Reliability**: Persistent storage in etcd prevents job loss, aligning with DACA’s resilience goals.
- **Integration with Workflows**: Supports DACA’s agentic workflows by managing reminders and timers.

---

### Exercises for Students

1. Create a custom Dapr component (e.g., a state store using a different backend like in-memory) and list it with `dapr components`.
2. Use `dapr invoke` to test a POST endpoint on the test app (hint: add a POST endpoint to `main.py`).
3. Explore Dapr’s tracing by enabling Zipkin and viewing traces in the Dapr dashboard.
4. Modify the Go app to schedule a recurring job (e.g., every 10 seconds) and observe the Scheduler’s behavior.
5. Use `docker logs` to investigate the Scheduler’s behavior when a job fails (e.g., stop the app before the job triggers).
6. Explore the Dapr dashboard’s **Control Plane** section to view Scheduler metrics and logs in more detail.

---

## Conclusion

In this tutorial, we introduced Dapr, explored its building blocks, and provided a comprehensive guide to the Dapr CLI. We then extended the tutorial to cover the Dapr Scheduler, a control plane service for managing scheduled jobs, actor reminders, and workflows. We demonstrated how to verify the Scheduler’s status, view its logs, and interact with it using CLI commands like `dapr status`, `dapr publish`, and `dapr run`. We also created a simple Go app to schedule a job, showcasing the Scheduler in action. You’re now ready to integrate Dapr with our microservices in the next tutorial!

---
