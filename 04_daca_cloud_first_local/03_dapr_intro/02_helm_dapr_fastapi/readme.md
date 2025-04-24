# Dapr Intro (Hands On with Helm, Dapr State, Dapr Pub/Sub)

This tutorial introduces **Dapr** (Distributed Application Runtime), a tool that simplifies building distributed applications like microservices. It’s part of the **Dapr Agentic Cloud Ascent (DACA)** learning path, which focuses on creating scalable, resilient AI systems. We’ll use **Helm** to deploy Dapr on a Kubernetes cluster (Rancher Desktop), test its features with `curl`, explore the Dapr Dashboard, and build a FastAPI app with hot reloading for development, using Dapr’s state management and pub/sub capabilities.

### What is Dapr?
Dapr is a portable, event-driven runtime that makes it easy for developers to build resilient, stateless, and stateful applications for cloud and edge environments. It supports any programming language and abstracts complex distributed system challenges.

#### Key Features of Dapr
- **Language Agnostic**: Works with Python, Go, Java, etc., via HTTP or gRPC APIs.
- **Sidecar Architecture**: Runs as a separate container (sidecar) next to your app, ensuring isolation and portability.
- **Building Blocks**: Provides APIs for common patterns like state management, pub/sub messaging, and service invocation.
- **Pluggable Components**: Supports multiple backends (e.g., Redis, Kafka) configured via YAML files.
- **Cloud-Native**: Designed for Kubernetes but works locally too.

#### Dapr Architecture
Dapr uses a **sidecar pattern**:
- **Application**: Your app (e.g., a FastAPI service).
- **Dapr Sidecar**: A container in the same pod, exposing APIs on port 3500 (HTTP).
- **Dapr APIs**: Your app calls the sidecar (e.g., `http://localhost:3500/v1.0/state`) to perform tasks.
- **Components**: The sidecar connects to backends (e.g., Redis for state) based on configuration.

For example, your app sends an HTTP request to the sidecar to save data, and the sidecar stores it in Redis, handling retries and errors transparently.

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
5. Test Dapr APIs with `curl` via a test app.
6. Verify state data in Redis.
7. Explore the Dapr Dashboard.
8. Build a FastAPI app with hot reloading, using Dapr’s state and pub/sub.

## Learning Objectives
1. Install and configure Dapr using Helm.
2. Understand Dapr’s control plane, sidecar, and CLI.
3. Deploy Redis and Dapr components.
4. Interact with Dapr’s state and pub/sub APIs directly.
5. Verify state data in Redis.
6. Monitor with the Dapr Dashboard.
7. Build a FastAPI app with hot reloading and Dapr integration.

## Prerequisites
- **Rancher Desktop**: Installed and running with Kubernetes enabled.
- **Helm**: Installed (v3).
- **kubectl**: Configured for Rancher Desktop.
- **nerdctl**: For building and loading images into `containerd`.
- **Python 3.9+**: For FastAPI.
- **uv**: For Python dependency management (`pip install uv`).
- **curl**: For API testing.

## Step 1: Install the Dapr CLI
### What’s Happening?
The **Dapr CLI** manages Dapr, including status checks, component listing, and debugging. We’ll install it for our Helm-based Dapr setup.

1. **Install Dapr CLI (macOS/Linux)**:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | /bin/bash
   ```

2. **Verify Installation**:
   ```bash
   dapr --version
   ```
   - Expected:
     ```
     CLI version: 1.15.1
     Runtime version: n/a
     ```

3. **Explore CLI**:
   ```bash
   dapr -h
   ```
   - Lists commands like `dapr status`, `dapr components`, and `dapr dashboard`.

## Step 2: Deploy Dapr Control Plane with Helm
### What’s Happening?
Dapr’s **control plane** includes services (operator, placement, scheduler, sentry, sidecar injector) that manage Dapr’s runtime. We’ll deploy Dapr `1.15` in the `dapr-system` namespace.

1. **Add Dapr Helm Repo**:
   ```bash
   helm repo add dapr https://dapr.github.io/helm-charts/
   helm repo update
   ```

2. **Install Dapr Control Plane**:
   ```bash
   helm upgrade --install dapr dapr/dapr \
   --version=1.15 \
   --namespace dapr-system \
   --create-namespace \
   --wait
   ```

3. **Verify Dapr Pods**:
   ```bash
   kubectl get pods -n dapr-system
   ```
   - Expected:
     ```
     NAME                                     READY   STATUS    RESTARTS   AGE
     dapr-operator-5fbcb75589-q4dcd           1/1     Running   0          56s
     dapr-placement-server-0                  1/1     Running   0          56s
     dapr-scheduler-server-0                  1/1     Running   0          56s
     dapr-scheduler-server-1                  1/1     Running   0          56s
     dapr-scheduler-server-2                  1/1     Running   0          56s
     dapr-sentry-75b55cbb9-z765n              1/1     Running   0          56s
     dapr-sidecar-injector-76545c8c59-dg62r   1/1     Running   0          56s
     ```

4. **Check Dapr Status**:
   ```bash
   dapr status -k
   ```
   - Expected: All components show `HEALTHY` and `Running`.

## Step 3: Deploy Dapr Dashboard
### What’s Happening?
The Dapr Dashboard provides a web UI to visualize components, apps, and subscriptions.

1. **Install Dapr Dashboard**:
   ```bash
   helm install dapr-dashboard dapr/dapr-dashboard --namespace dapr-system
   ```

2. **Verify Dashboard Pod**:
   ```bash
   kubectl get pods -n dapr-system
   ```
   - Expected: Includes `dapr-dashboard-...` with `1/1` readiness.

## Step 4: Deploy Redis and Configure Dapr Components
### What’s Happening?
We’ll deploy Redis as the backend for state and pub/sub, and configure Dapr components with YAML files.

1. **Install Redis**:
   ```bash
   helm install redis bitnami/redis --set auth.enabled=false --namespace default
   ```

2. **Verify Redis**:
   ```bash
   kubectl get pods
   ```
   - Expected: `redis-master-0` with `1/1` readiness.

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

6. **Verify Components**:
   ```bash
   dapr components -k --namespace default
   ```
   - Expected:
     ```
     NAMESPACE  NAME        TYPE          VERSION  SCOPES  CREATED              AGE
     default    statestore  state.redis   v1               2025-04-24 ...        ...
     default    pubsub      pubsub.redis  v1               2025-04-24 ...        ...
     ```

## Step 5: Test Dapr APIs
### What’s Happening?
Dapr’s sidecar exposes HTTP APIs on port 3500 for state (saving/retrieving data in Redis) and pub/sub (publishing events). Since no app is deployed, we’ll create a temporary test app with a Dapr sidecar to test these APIs with `curl`. The test app uses Nginx as a placeholder (on port 8080), but we interact only with the sidecar (port 3500).

1. **Deploy Test App**:
   - Create `test-app.yaml`:
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
   - Apply:
     ```bash
     kubectl apply -f test-app.yaml
     ```

2. **Verify Pod**:
   ```bash
   kubectl get pods
   ```
   - Expected: `dapr-test-app-...` with `2/2` readiness (Nginx + sidecar).
   - If `1/2` (as seen previously), troubleshoot:
     ```bash
     kubectl describe pod dapr-test-app-<pod-suffix>
     kubectl logs dapr-test-app-<pod-suffix> -c daprd
     ```
     - Fix image pull:
       ```bash
       nerdctl --namespace k8s.io pull nginx:latest
       kubectl delete -f test-app.yaml
       kubectl apply -f test-app.yaml
       ```

3. **Port-Forward to Sidecar**:
   ```bash
   kubectl get pods | grep dapr-test-app
   kubectl port-forward pod/dapr-test-app-<pod-suffix> 3500:3500 -n default
   ```
   - Example:
     ```bash
     kubectl port-forward pod/dapr-test-app-79469c967b-stlgj 3500:3500 -n default
     ```
   - Expected:
     ```
     Forwarding from 127.0.0.1:3500 -> 3500
     Forwarding from [::1]:3500 -> 3500
     ```

4. **Test State Store**:
   - Save State:
     ```bash
     curl -X POST http://localhost:3500/v1.0/state/statestore \
     -H "Content-Type: application/json" \
     -d '[{"key": "test-key", "value": {"user_id": "user123", "message": "Hello, Dapr!"}}]'
     ```
     - Expected: No output (200 OK).
   - Retrieve State:
     ```bash
     curl http://localhost:3500/v1.0/state/statestore/test-key
     ```
     - Expected:
       ```json
       {"user_id": "user123", "message": "Hello, Dapr!"}
       ```

5. **Test Pub/Sub**:
   ```bash
   curl -X POST http://localhost:3500/v1.0/publish/pubsub/message-updated \
   -H "Content-Type: application/json" \
   -d '{"user_id": "user123", "message": "Hello, Dapr!"}'
   ```
   - Expected: No output (200 OK).

6. **Stop Port-Forwarding**:
   - Press `Ctrl+C`.

## Step 6: Verify Redis Data
### What’s Happening?
We saved a state key (`test-key`) in Redis via Dapr’s `statestore`. Let’s confirm the data is stored in Redis.

1. **Run Redis Client Pod**:
   ```bash
   kubectl run redis-client --namespace default --restart='Never' --image docker.io/bitnami/redis:7.4.2-debian-12-r11 --command -- sleep infinity
   ```

2. **Connect to Redis**:
   ```bash
   kubectl exec -it redis-client --namespace default -- redis-cli -h redis-master
   ```

3. **Check Keys**:
   ```
   KEYS *
   ```
   - Expected:
     ```
     1) "dapr-test-app||test-key"
     ```

4. **Retrieve Value**:
   ```
   HGETALL dapr-test-app||test-key
   ```
   - Expected:
     ```
     1) "data"
     2) "{\"user_id\":\"user123\",\"message\":\"Hello, Dapr!\"}"
     3) "version"
     4) "1"
     ```

5. **Exit Redis CLI**:
   ```
   EXIT
   ```

6. **Clean Up Redis Client**:
   ```bash
   kubectl delete pod redis-client --namespace default
   ```

7. **Clean Up Test App**:
   ```bash
   kubectl delete -f test-app.yaml
   ```

## Step 7: Explore Dapr Dashboard
### What’s Happening?
The Dapr Dashboard visualizes components and subscriptions.

1. **Port-Forward**:
   ```bash
   kubectl port-forward service/dapr-dashboard 8080:8080 -n dapr-system
   ```

2. **Open Dashboard**:
   - Visit `http://localhost:8080`.
   - Check:
     - **Components**: `statestore`, `pubsub`.
     - **Subscriptions**: `message-subscription`.
     - **Applications**: None (test app removed).

3. **Stop Port-Forwarding**:
   - Press `Ctrl+C`.

## Step 8: Build the FastAPI Hello World App
### What’s Happening?
We’ll build a FastAPI app that uses Dapr’s state and pub/sub APIs, with hot reloading for development.

### 8.1 Project Setup
1. **Initialize Project**:
   ```bash
   mkdir hello_dapr_fastapi
   cd hello_dapr_fastapi
   uv init
   uv venv
   source .venv/bin/activate
   uv add "fastapi[standard]" httpx
   ```

2. **Enable Hot Reloading**:
   - Hot reloading is enabled by adding `--reload` to the `uvicorn` command during development. We’ll configure this for local testing and exclude it in the production Dockerfile.

### 8.2 Write the FastAPI App
1. Create `main.py`:
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
       event_data = data.get("data", {})
       user_id = event_data.get("user_id", "unknown")
       message = event_data.get("message", "no message")
       print(f"Received event: User {user_id} updated message to '{message}'")
       return {"status": "Event processed"}
   ```

2. **Test Locally with Hot Reloading**:
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - **Explanation**: `--reload` enables hot reloading, restarting the server when `main.py` changes. Use this for development only (not in production).

3. **Create Dockerfile** (for production):
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /code
   COPY . .
   RUN pip install uv
   RUN uv sync --frozen
   EXPOSE 8000
   CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
   - **Note**: Excludes `--reload` for production stability.

4. **Create `.dockerignore`**:
   ```
   .venv
   .git
   .gitignore
   .env
   __pycache__
   ```

5. **Create Kubernetes Manifests**:
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

### 8.3 Build and Deploy
1. **Build Image**:
   ```bash
   nerdctl build -t dapr-fastapi-hello:latest .
   ```

2. **Load into `containerd`**:
   ```bash
   nerdctl save dapr-fastapi-hello:latest | nerdctl --namespace k8s.io load
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

## Step 9: Test the FastAPI Application
### What’s Happening?
The FastAPI app uses Dapr’s APIs to store/retrieve state and publish/subscribe to events.

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
   curl -X POST "http://localhost:8000/messages?user_id=junaid&message=hello" \
   -H "Content-Type: application/json"
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
   kubectl logs -l app=dapr-fastapi-hello -c app
   ```
   - Expected:
     ```
     Received event: User junaid updated message to 'hello'
     ```

## Step 10: Revisit Dapr Dashboard
### What’s Happening?
Check the Dashboard to see the FastAPI app integrated with Dapr.

1. **Port-Forward**:
   ```bash
   kubectl port-forward service/dapr-dashboard 8080:8080 -n dapr-system
   ```

2. **Open Dashboard**:
   - Visit `http://localhost:8080`.
   - Check:
     - **Applications**: `dapr-fastapi-hello`.
     - **Components**: `statestore`, `pubsub`.
     - **Subscriptions**: `message-subscription`.

3. **Stop Port-Forwarding**:
   - Press `Ctrl+C`.

## Step 11: Troubleshooting
- **Dapr Installation**:
  - If pods fail: `kubectl describe pod <pod-name> -n dapr-system`.
- **Redis Issues**:
  - Check logs: `kubectl logs redis-master-0`.
  - Test: `kubectl exec -it redis-client -- redis-cli -h redis-master PING` (expect `PONG`).
- **Component Issues**:
  - Verify: `dapr components -k`.
  - Re-apply: `kubectl apply -f <file>`.
- **Pod Issues**:
  - If `CrashLoopBackOff`: `kubectl describe pod <pod-name>`.
  - Logs: `kubectl logs <pod-name> -c <container>`.
- **Port-Forwarding**:
  - Confirm service: `kubectl get svc`.
- **FastAPI Issues**:
  - Check logs: `kubectl logs -l app=dapr-fastapi-hello -c app`.

## Step 12: Clean Up
```bash
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/service.yaml
kubectl delete -f redis-state.yaml
kubectl delete -f redis-pubsub.yaml
kubectl delete -f subscriptions.yaml
kubectl delete -f test-app.yaml
helm uninstall redis -n default
helm uninstall dapr-dashboard -n dapr-system
helm uninstall dapr -n dapr-system
kubectl delete namespace dapr-system
```

## Step 13: DACA Context
This setup supports DACA:
- **Stateless Computing**: FastAPI app offloads state to Redis.
- **Event-Driven Architecture**: Pub/sub enables reactive workflows.
- **Cloud-First**: Helm ensures portability.
- **Resilience**: Dapr’s sidecar handles retries.

## Step 14: Next Steps
1. **Step 06: Dapr Actors**: Build a counter actor.
2. **Prototyping**: Deploy to Hugging Face with Upstash Redis.
3. **Observability**: Explore Zipkin/Prometheus.

## Resources
- Dapr Kubernetes Deployment: https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-deploy/
- Dapr Helm Chart: https://github.com/dapr/dapr/tree/master/charts/dapr
- Dapr Dashboard: https://docs.dapr.io/operations/monitoring/dashboard/
- FastAPI: https://fastapi.tiangolo.com/
- UV: https://docs.astral.sh/uv/