# Dapr Intro (Hands On with Helm, Dapr State, Dapr Pub/Sub)

This tutorial introduces **Dapr** (Distributed Application Runtime), a tool that simplifies building distributed applications like microservices. It’s part of the **Dapr Agentic Cloud Ascent (DACA)** learning path, which focuses on creating scalable, resilient AI systems. We’ll use **Helm** to deploy Dapr on a Kubernetes cluster (Rancher Desktop), test its features with `curl`, explore the Dapr Dashboard, and build a FastAPI app that uses Dapr’s state management and pub/sub capabilities.

### What is Dapr?
Dapr is a portable, event-driven runtime that makes it easy for developers to build resilient, stateless, and stateful applications for cloud and edge environments. It supports any programming language and abstracts complex distributed system challenges.

#### Key Features of Dapr
- **Language Agnostic**: Works with Python, Go, Java, etc., via HTTP or gRPC APIs.
- **Sidecar Architecture**: Runs as a separate process (sidecar) next to your app, ensuring isolation and portability.
- **Building Blocks**: Provides APIs for common patterns like state management, pub/sub messaging, and service invocation.
- **Pluggable Components**: Supports multiple backends (e.g., Redis, Kafka) configured via YAML files.
- **Cloud-Native**: Designed for Kubernetes but works locally too.

#### Dapr Architecture
Dapr uses a **sidecar pattern**:
- **Application**: Your app (e.g., a FastAPI service).
- **Dapr Sidecar**: A container running alongside your app, exposing APIs.
- **Dapr APIs**: Your app calls the sidecar (e.g., `http://localhost:3500/v1.0/state`) to perform tasks.
- **Components**: The sidecar connects to backends (e.g., Redis for state) based on configuration.

For example, your app sends an HTTP request to the Dapr sidecar to save data, and the sidecar stores it in Redis, handling retries and errors transparently.

#### Why Dapr for DACA?
Dapr aligns with DACA’s goals:
- **Simplified Communication**: Streamlines service-to-service calls and messaging.
- **State Management**: Manages state for stateless apps, fitting DACA’s container design.
- **Resilience**: Offers retries and fault tolerance for robust systems.
- **Scalability**: Integrates with Kubernetes for planet-scale deployments.
- **Flexibility**: Supports free-tier services (e.g., Upstash Redis) for prototyping.

### Dapr Building Blocks
Dapr provides **building blocks** to solve distributed system challenges, each with a standardized API and multiple backend options. Key blocks for DACA include:
1. **Service Invocation**: Synchronous calls between services with discovery and retries.
  - Example: A Chat Service calls an Analytics Service.
2. **State Management**: Key-value storage for data like user sessions.
  - Example: Store message counts in Redis.
3. **Publish/Subscribe (Pub/Sub)**: Asynchronous messaging via brokers like Redis.
  - Example: Publish a “MessageSent” event for subscribers to process.
4. **Bindings**: Connect to external systems (e.g., databases).
5. **Actors**: Manage stateful objects for concurrent processing.
6. **Workflows**: Orchestrate long-running processes.
7. **Secrets**: Securely store API keys.
8. **Configuration**: Manage feature flags.
9. **Observability**: Trace and monitor with tools like Zipkin.

This tutorial focuses on **State Management** and **Pub/Sub** using Redis.

## Overview
This tutorial sets up Dapr from scratch using Helm on Rancher Desktop, following a beginner-friendly flow:
1. Install the Dapr CLI.
2. Deploy Dapr’s control plane and Dashboard with Helm.
3. Verify Dapr and explore the CLI.
4. Deploy Redis and configure state/pub-sub components.
5. Test Dapr APIs with `curl` via port-forwarding.
6. Explore the Dapr Dashboard.
7. Build a FastAPI app using Dapr’s state and pub/sub.

## Learning Objectives
1. Install and configure Dapr using Helm.
2. Understand Dapr’s control plane and CLI.
3. Deploy Redis and Dapr components.
4. Interact with Dapr’s state and pub/sub APIs directly.
5. Monitor with the Dapr Dashboard.
6. Build a FastAPI app with Dapr integration.

## Prerequisites
- **Rancher Desktop**: Installed and running with Kubernetes enabled.
- **Helm**: Installed (v3).
- **kubectl**: Configured for Rancher Desktop.
- **nerdctl**: For building and loading images.
- **Python and FastAPI Understanding**: 
- **curl**: For API testing.

## Step 1: Install the Dapr CLI
### What’s Happening?
The **Dapr CLI** is a command-line tool for managing Dapr, including checking status, listing components, and debugging. We’ll install it to interact with our Helm-deployed Dapr setup.

1. **Install Dapr CLI (macOS/Linux)**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
  ```
  - **Explanation**: Downloads and installs the Dapr CLI.

2. **Verify Installation**:
  ```bash
  dapr --version
  ```
  - Expected:
    ```
    CLI version: 1.15.1
    Runtime version: n/a
    ```
  - **Explanation**: Confirms the CLI is installed. `Runtime version: n/a` is normal until Dapr is deployed.

3. **Explore CLI**:
  ```bash
  dapr -h
  ```
  - **Explanation**: Lists commands like `dapr status`, `dapr components`, and `dapr dashboard`.

## Step 2: Deploy Dapr Control Plane with Helm
### What’s Happening?
Dapr’s **control plane** includes services like the operator, placement, scheduler, sentry, and sidecar injector, which manage Dapr’s runtime. We’ll use Helm to deploy Dapr `1.15` in the `dapr-system` namespace, matching your terminal output.

1. **Add Dapr Helm Repo**:
  ```bash
  helm repo add dapr https://dapr.github.io/helm-charts/
  helm repo update
  ```
  - **Explanation**: Adds the Dapr Helm chart repository and updates it.

2. **Install Dapr Control Plane**:
  ```bash
  helm upgrade --install dapr dapr/dapr \
  --version=1.15 \
  --namespace dapr-system \
  --create-namespace \
  --wait
  ```
  - **Explanation**: Installs Dapr `1.15` in the `dapr-system` namespace, creating it if it doesn’t exist. `--wait` ensures the deployment completes.

3. **Verify Dapr Pods**:
  ```bash
  kubectl get pods -n dapr-system
  ```
  - Expected:
    ```
  NAME                                     READY   STATUS    RESTARTS   AGE
  dapr-operator-5fbcb75589-hpqck           1/1     Running   0          22s
  dapr-placement-server-0                  1/1     Running   0          22s
  dapr-scheduler-server-0                  1/1     Running   0          22s
  dapr-scheduler-server-1                  1/1     Running   0          22s
  dapr-scheduler-server-2                  1/1     Running   0          22s
  dapr-sentry-75b55cbb9-hp57s              1/1     Running   0          22s
  dapr-sidecar-injector-76545c8c59-2dd7s   1/1     Running   0          22s
    ```
  - **Explanation**: Confirms the control plane services are running. `1/1` means each pod is ready.

4. **Check Dapr Status**:
  ```bash
  dapr status -k
  ```
  - Expected: All components (operator, placement, scheduler, sentry, sidecar-injector) show `HEALTHY` and `Running`.
  - **Explanation**: The CLI queries the control plane to verify its health.

```bash
  NAME                   NAMESPACE    HEALTHY  STATUS   REPLICAS  VERSION  AGE  CREATED              
  dapr-sentry            dapr-system  True     Running  1         1.15.4   40s  2025-04-24 04:33.15  
  dapr-operator          dapr-system  True     Running  1         1.15.4   40s  2025-04-24 04:33.15  
  dapr-sidecar-injector  dapr-system  True     Running  1         1.15.4   40s  2025-04-24 04:33.15  
  dapr-placement-server  dapr-system  True     Running  1         1.15.4   40s  2025-04-24 04:33.15  
  dapr-scheduler-server  dapr-system  True     Running  3         1.15.4   40s  2025-04-24 04:33.15  
```

## Step 3: Deploy Dapr Dashboard
### What’s Happening?
The Dapr Dashboard provides a web UI to visualize components, apps, and subscriptions. We’ll deploy it using Helm, as you did in your terminal output.

1. **Install Dapr Dashboard**:
  ```bash
  helm install dapr-dashboard dapr/dapr-dashboard --namespace dapr-system
  ```
  - **Explanation**: Deploys the Dashboard in the `dapr-system` namespace.

2. **Verify Dashboard Pod**:
  ```bash
  kubectl get pods -n dapr-system
  ```
  - Expected: Includes `dapr-dashboard-...` with `1/1` readiness.
  - **Explanation**: Confirms the Dashboard is running.

## Step 4: Deploy Redis and Configure Dapr Components
### What’s Happening?
Dapr’s Helm chart only deploys the control plane, not components like state or pub/sub. We’ll use Helm to deploy Redis as the backend and configure Dapr components with YAML files.

1. **Install Redis**:
  ```bash
  helm install redis bitnami/redis --set auth.enabled=false --namespace default
  ```
  - **Explanation**: Deploys Redis in the `default` namespace without authentication for simplicity. The service name `redis-master` will be used by Dapr.

2. **Verify Redis**:
  ```bash
  kubectl get pods
  ```
  - Expected: `redis-master-0` with `1/1` readiness.
  - **Explanation**: Ensures Redis is running.

3. **Configure State Store**:
  - Create `redis-state.yaml`:
    ```yaml
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
        value: redis-master.default.svc.cluster.local:6379
      - name: redisPassword
        value: ""
      - name: actorStateStore
        value: "true"
    ```
  - Apply:
    ```bash
    kubectl apply -f redis-state.yaml
    ```
  - **Explanation**: Configures a `statestore` component to use Redis for key-value storage. `actorStateStore: "true"` prepares for future actor steps.

4. **Configure Pub/Sub**:
  - Create `redis-pubsub.yaml`:
    ```yaml
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
        value: redis-master.default.svc.cluster.local:6379
      - name: redisPassword
        value: ""
    ```
  - Apply:
    ```bash
    kubectl apply -f redis-pubsub.yaml
    ```
  - **Explanation**: Configures a `pubsub` component for Redis-based messaging.

5. **Configure Subscription**:
  - Create `subscriptions.yaml`:
    ```yaml
    apiVersion: dapr.io/v1alpha1
    kind: Subscription
    metadata:
      name: message-subscription
      namespace: default
    spec:
      pubsubname: pubsub
      topic: message-updated
      route: /subscribe
    ```
  - Apply:
    ```bash
    kubectl apply -f subscriptions.yaml
    ```
  - **Explanation**: Subscribes to the `message-updated` topic, routing events to the `/subscribe` endpoint (used later).

6. **Verify Components**:
  ```bash
  dapr components -k --namespace default
  ```
  - Expected:
    ```
  NAMESPACE  NAME        TYPE          VERSION  SCOPES  CREATED              AGE  
  default    pubsub      pubsub.redis  v1               2025-04-24 04:37.34  51s  
  default    statestore  state.redis   v1               2025-04-24 04:37.13  1m  
    ```
  - **Explanation**: Confirms Dapr recognizes the components.


## Step 5: Explore Dapr Dashboard
### What’s Happening?
The Dapr Dashboard visualizes components and subscriptions. Let’s check it to confirm our setup.

1. **Port-Forward**:
  ```bash
  kubectl port-forward service/dapr-dashboard 8080:8080 -n dapr-system
  ```

2. **Open Dashboard**:
  - Visit `http://localhost:8080`.
  - Check:
    - **Components**: `statestore`, `pubsub`.
    - **Subscriptions**: `message-subscription`.
    - **Applications**: None yet.
  - **Explanation**: The Dashboard confirms Dapr’s configuration.


## Step 6: Test Dapr APIs

### What’s Happening?

We need an application container (like Nginx) to create a pod where Dapr can inject its sidecar. Without an app, there’s no pod, and thus no sidecar to expose port 3500. Nginx is a lightweight choice for this test, but we could use any container (e.g., a simple Python app). Nginx itself doesn’t handle Dapr requests—it’s just a “host” for the sidecar.

We’ll create a test-app to connect to the `dapr-sidecar-injector` to test these APIs with `curl`, giving you a raw understanding of Dapr’s functionality.

Key Points:
- Nginx’s Role: In the test app (test-app.yaml), Nginx is just a placeholder application running in the pod. - It listens on port 8080 for HTTP traffic (e.g., serving web pages), but we don’t use Nginx for Dapr’s APIs. Nginx is only there to satisfy Kubernetes’ requirement for a running container in the pod, allowing Dapr to inject a sidecar.
- Dapr Sidecar’s Role: The Dapr sidecar (named daprd) is automatically injected into the pod because of the annotations (dapr.io/enabled: "true", dapr.io/app-id: "dapr-test-app", etc.). The sidecar runs as a separate container in the same pod and exposes Dapr’s HTTP APIs on port 3500. This is where we send curl requests (e.g., http://localhost:3500/v1.0/state/statestore).

1. Deploy a Temporary Test App

This app will run Nginx with a Dapr sidecar, exposing the Dapr HTTP API on port 3500. 

1.1 Create `test-app.yaml`

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
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "dapr-test-app"
        dapr.io/app-port: "8080"
        dapr.io/enable-api-logging: "true"
    spec:
      containers:
      - name: app
        image: nginx:latest
        ports:
        - containerPort: 8080
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
    targetPort: 8080
  type: ClusterIP
```
- Explanation: Deploys an Nginx app with a Dapr sidecar. The sidecar listens on port 3500 for HTTP API requests (e.g., state, pub/sub).
- Apply the app:
```bash
kubectl apply -f test-app.yaml
```
Verify
```bash
kubectl get pods
```

1.2 ****Port-Forward to the Sidecar**:

Output:
```bash
mjs@Muhammads-MacBook-Pro-3 dapr % kubectl get pods | grep dapr-test-app
dapr-test-app-79469c967b-stlgj   1/2     Running   0          9m27s
```
Note the pod name (e.g., dapr-test-app-79469c967b-stlgj).

```bash
kubectl port-forward pod/dapr-test-app-<pod-suffix> 3500:3500 -n default
```

i.e:

```bash
mjs@Muhammads-MacBook-Pro-3 dapr % kubectl port-forward pod/dapr-test-app-79469c967b-stlgj 3500:3500 -n default
Forwarding from 127.0.0.1:3500 -> 3500
Forwarding from [::1]:3500 -> 3500
```

2. **Test State Store**:
  - **Save State**:
    ```bash
    curl -X POST http://localhost:3500/v1.0/state/statestore \
    -H "Content-Type: application/json" \
    -d '[{"key": "test-key", "value": {"user_id": "user123", "message": "Hello, Dapr!"}}]'
    ```
    - Expected: No output (200 OK).
    - **Explanation**: Stores a key-value pair in Redis.
  - **Retrieve State**:
    ```bash
    curl http://localhost:3500/v1.0/state/statestore/test-key
    ```
    - Expected:
      ```json
      {"user_id": "user123", "message": "Hello, Dapr!"}
      ```
    - **Explanation**: Retrieves the stored value.

3. **Test Pub/Sub**:
  - Publish an event:
    ```bash
    curl -X POST http://localhost:3500/v1.0/publish/pubsub/message-updated \
    -H "Content-Type: application/json" \
    -d '{"user_id": "user123", "message": "Hello, Dapr!"}'
    ```
    - Expected: No output (200 OK).
    - **Explanation**: Publishes an event to Redis. No subscriber exists yet, but this tests the component.

4. **Stop Port-Forwarding**:
  - Press `Ctrl+C`.

### Verify Redis Data

You saved a state key (test-key) in Redis via Dapr’s statestore. Let’s connect to Redis to confirm the data is stored, ensuring the state component works as expected.

1. Run a Redis Client Pod (if not already running):

```bash
kubectl run redis-client --namespace default --restart='Never' --image docker.io/bitnami/redis:7.4.2-debian-12-r11 --command -- sleep infinity
```

2. Connect to Redis:

```bash
kubectl exec -it redis-client --namespace default -- redis-cli -h redis-master
```

3. Check the Stored Key:

At the redis-master:6379> prompt:

```bash
KEYS *
```

Expected: Shows keys like dapr-test-app||test-key (Dapr prefixes keys with the app ID).
Example: ```1) "dapr-test-app||test-key"```


4. Inspect the type of a key in Redis:
```bash
redis-master:6379> TYPE dapr-test-app||test-key
hash
```

Depending on the result, you can then use the appropriate command to inspect it:
- If it's a hash: HGETALL dapr-test-app||test-key
- If it's a list: LRANGE dapr-test-app||test-key 0 -1
- If it's a set: SMEMBERS dapr-test-app||test-key
- If it's a zset: ZRANGE dapr-test-app||test-key 0 -1 WITHSCORES
- XRANGE for stream: XRANGE message-updated - +

5. Retrieve the value:

```bash
HGETALL dapr-test-app||test-key
```
Expected:
```json
1) "data"
2) "{\"user_id\":\"user123\",\"message\":\"Hello, Dapr!\"}"
3) "version"
4) "1"
```
- Explanation: Confirms Dapr stored the state in Redis correctly.

5. Exit Redis CLI:

```bash
EXIT
Clean Up Redis Client (optional):
```

```bash
kubectl delete pod redis-client --namespace default
```

## Step 7: Build the FastAPI Hello World App
### What’s Happening?
Now, let’s build a FastAPI app that uses Dapr’s state and pub/sub APIs, to apply what you’ve learned.

### 7.1 Project Setup
```bash
uv init hello_dapr_fastapi
cd hello_dapr_fastapi
uv venv
source .venv/bin/activate
uv add "fastapi[standard]"
```

### 7.2 Write the FastAPI App
1. Update `app/main.py`:
```python
from fastapi import FastAPI, HTTPException
import httpx
import os

app = FastAPI(title="Dapr FastAPI Hello World")

DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
STATE_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/state/statestore"
PUBSUB_URL = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/pubsub/message-updated"

@app.get("/")
async def root():
    return {"message": "Hello from Dapr FastAPI!"}

@app.post("/messages")
async def save_message(user_id: str, message: str):
    async with httpx.AsyncClient() as client:
        try:
            state_payload = [{"key": user_id, "value": {"user_id": user_id, "message": message}}]
            response = await client.post(STATE_URL, json=state_payload)
            response.raise_for_status()
            event_payload = {"user_id": user_id, "message": message}
            response = await client.post(PUBSUB_URL, json=event_payload)
            response.raise_for_status()
            return {"status": f"Stored and published message for {user_id}"}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages/{user_id}")
async def get_message(user_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{STATE_URL}/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=404, detail="Message not found")

@app.post("/subscribe")
async def subscribe_message(data: dict):
    print(f"Received event: {data}")
    event_data = data.get("data", {})
    user_id = event_data.get("user_id", "unknown")
    message = event_data.get("message", "no message")
    print(f"Received event: User {user_id} updated message to '{message}'")
    return {"status": "Event processed"}

```

2. Create `Dockerfile`:
  ```dockerfile
    FROM python:3.12-slim

    # Set working directory
    WORKDIR /code

    # Copy code
    COPY . .

    # Install dependencies
    RUN pip install uv

    RUN uv sync --frozen

    # Expose port
    EXPOSE 8000

    # Run FastAPI
    CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

3. Create `.dockerignore`:
  ```
  .venv
  .git
  .gitignore
  .env
  ```

5. Create Kubernetes manifests:
  - `kubernetes/deployment.yaml`:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: dapr-fastapi-hello
      namespace: default
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: dapr-fastapi-hello
      template:
        metadata:
          labels:
            app: dapr-fastapi-hello
          annotations:
            dapr.io/enabled: "true"
            dapr.io/app-id: "dapr-fastapi-hello"
            dapr.io/app-port: "8000"
            dapr.io/enable-api-logging: "true"
        spec:
          containers:
          - name: app
            image: dapr-fastapi-hello:latest
            ports:
            - containerPort: 8000
            imagePullPolicy: Never
    ```
  - `kubernetes/service.yaml`:
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: dapr-fastapi-hello
      namespace: default
    spec:
      selector:
        app: dapr-fastapi-hello
      ports:
      - protocol: TCP
        port: 80
        targetPort: 8000
      type: ClusterIP
    ```

### 7.3 Build and Deploy
1. **Build the Image**:
  ```bash
  nerdctl build -t dapr-fastapi-hello:latest .
  ```

2. **Load into `containerd`**:
  ```bash
  nerdctl save dapr-fastapi-hello | nerdctl --namespace k8s.io load
  ```

3. **Verify Image**:
  ```bash
  nerdctl --namespace k8s.io images
  ```

4. **Deploy**:
  ```bash
  kubectl apply -f kubernetes/deployment.yaml
  kubectl apply -f kubernetes/service.yaml
  ```

5. **Verify Deployment**:
  ```bash
  kubectl get pods
  ```
  - Expected: `dapr-fastapi-hello-...` with `2/2` readiness.

## Step 8: Test the FastAPI Application
1. **Port-Forward**:
  ```bash
  kubectl port-forward service/dapr-fastapi-hello 8000:80 -n default
  ```

2. **Test Root Endpoint**:
  ```bash
  curl http://localhost:8000/
  ```
  - Expected:
    ```json
    {"message": "Hello from Dapr FastAPI!"}
    ```

3. **Store a Message**:
  ```bash
  curl -X 'POST' \
  'http://localhost:8000/messages?user_id=junaid&message=hello' \
  -H 'accept: application/json' \
  -d ''
  ```
  - Expected:
    ```json
    {"status": "Stored and published message for junaid"}
    ```

4. **Retrieve a Message**:
  ```bash
  curl http://localhost:8000/messages/junaid
  ```
  - Expected:
    ```json
    {"user_id": "junaid", "message": "hello"}
    ```

5. **Verify Pub/Sub**:
  ```bash
  kubectl logs -l app=dapr-fastapi-hello
  ```
  - Expected:
    ```
    Received event: User user123 updated message to 'Hello, World!'
    ```

## Step 9: Revisit Dapr Dashboard
1. **Port-Forward** (if not running):
  ```bash
  kubectl port-forward service/dapr-dashboard 8080:8080 -n dapr-system
  ```

2. **Check Dashboard**:
  - At `http://localhost:8080`, verify:
    - **Applications**: `dapr-fastapi-hello`.
    - **Components**: `statestore`, `pubsub`.
    - **Subscriptions**: `message-subscription`.

## Step 10: Troubleshooting
- **Dapr Installation**:
- If pods fail: `kubectl describe pod <pod-name> -n dapr-system`.
- **Redis Issues**:
- Check logs: `kubectl logs redis-master-0`.
- Verify `redis-master.default.svc.cluster.local`.
- **Component Issues**:
- Verify: `dapr components -k`.
- Re-apply: `kubectl apply -f <file>`.
- **Pod Issues**:
- If `CrashLoopBackOff`: `kubectl describe pod <pod-name>`.
- Check logs: `kubectl logs <pod-name>`.
- **Port-Forwarding**:
- Confirm service: `kubectl get svc`.

## Step 11: Clean Up
```bash
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/service.yaml
kubectl delete -f redis-state.yaml
kubectl delete -f redis-pubsub.yaml
kubectl delete -f subscriptions.yaml
kubectl delete deployment dapr-test-app
helm uninstall redis -n default
helm uninstall dapr-dashboard -n dapr-system
helm uninstall dapr -n dapr-system
kubectl delete namespace dapr-system
```

```bash
dapr uninstall -k --all
```

The `--all` flag also removes Docker images and volumes.

## Step 12: DACA Context
This setup supports DACA:
- **Stateless Computing**: FastAPI app offloads state to Redis.
- **Event-Driven Architecture**: Pub/sub enables reactive workflows.
- **Cloud-First**: Helm ensures portability.
- **Resilience**: Dapr’s sidecar handles retries.

## Step 13: Next Steps
1. **Step 06: Dapr Actors**: Build a counter actor.
2. **Prototyping**: Deploy to Hugging Face with Upstash Redis.
3. **Observability**: Explore Zipkin/Prometheus.

## Resources
- Dapr Kubernetes Deployment: https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/
- Dapr Helm Chart: https://github.com/dapr/dapr/tree/master/charts/dapr
- Dapr Dashboard: https://docs.dapr.io/operations/monitoring/dashboard/
- FastAPI: https://fastapi.tiangolo.com/
- https://github.com/dapr/dapr/tree/master/charts/dapr
- https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/