# Step 4.6: Namespacing

This is the sixth sub-step of **Step 4: Timers and Reminders** in the **Dapr Agentic Cloud Ascent (DACA)** learning path. In this sub-step, you’ll enhance the `ChatAgent` actor from **Step 2** by deploying it in separate Kubernetes namespaces to isolate actor instances for different environments (e.g., `prod` and `dev`). This supports multi-tenant or environment-specific deployments, aligning with DACA’s goal of isolation and scalability for AI agents.

## Overview

The **namespacing** sub-step modifies the `ChatAgent` deployment to:
- Deploy the `ChatAgent` in two Kubernetes namespaces (`prod` and `dev`).
- Configure Dapr components to use namespace-specific Redis instances.
- Test actor isolation by running `ChatAgent` instances in each namespace.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Namespacing isolates actor instances, ensuring that `user1` in `prod` is separate from `user1` in `dev`, supporting multi-tenant or staged environments.

### Learning Objectives
- Deploy Dapr actors in Kubernetes namespaces for isolation.
- Configure namespace-specific Dapr components.
- Validate actor and state isolation across namespaces.
- Maintain lightweight changes to the actor implementation.

### Ties to Step 4 Overview
- **Dapr’s Implementation**: Leverages Dapr’s namespace support for actor isolation.
- **Fault Tolerance**: Namespacing enhances resilience by isolating environments.
- **Turn-Based Concurrency**: Ensures namespace-isolated actors maintain concurrent message processing.

## Key Concepts

### Dapr Actor Namespacing
Dapr supports Kubernetes namespaces to isolate actor instances and their state. Key aspects:
- **Namespace Isolation**: Actors in different namespaces (e.g., `prod`, `dev`) have separate state stores and instances.
- **Component Scoping**: Dapr components (e.g., `statestore`, `daca-pubsub`) are namespace-specific.
- **Multi-Tenancy**: Namespacing supports multiple tenants or environments on the same cluster.

In this sub-step, you’ll deploy `ChatAgent` in `prod` and `dev` namespaces, each with its own Redis instance and Dapr components, ensuring `history-user1` in `prod` is isolated from `dev`.

### Lightweight Configuration
Namespacing is added with minimal changes:
- No changes to the `ChatAgent` code, as namespacing is handled by Kubernetes and Dapr.
- Namespace-specific Dapr component files (`statestore.yaml`, `daca-pubsub.yaml`, `message-subscription.yaml`) for `prod` and `dev`.
- Kubernetes deployment manifests to deploy in both namespaces.
- Testing with identical `ActorId` (`user1`) in both namespaces to confirm isolation.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) for message processing and history retrieval.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`, scoped to the namespace.
- **Namespace Isolation**: Actors in `prod` and `dev` operate independently, with separate state and events.

## Hands-On Dapr Virtual Actor

### 0. Setup Code
Use the [00_lab_starter_code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code) from **Step 2**. Ensure **Step 2** is complete and you have a Kubernetes cluster (e.g., via `minikube` or a cloud provider).

Verify dependencies:
```bash
uv add dapr dapr-ext-fastapi pydantic
```

### 1. Configure Kubernetes Namespaces
Create two namespaces in your Kubernetes cluster:
```bash
kubectl create namespace prod
kubectl create namespace dev
```

### 2. Configure Dapr Components
Duplicate the **Step 2** Dapr components for each namespace, updating `redisHost` to use namespace-specific Redis instances.

**File**: `components/prod/statestore.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: prod
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.prod.svc.cluster.local:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

**File**: `components/prod/daca-pubsub.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: daca-pubsub
  namespace: prod
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.prod.svc.cluster.local:6379
  - name: redisPassword
    value: ""
```

**File**: `components/prod/message-subscription.yaml`
```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: message-subscription
  namespace: prod
spec:
  pubsubname: daca-pubsub
  topic: user-chat
  routes:
    default: /subscribe
    rules:
      - match: event.type == "ConversationUpdated"
        path: /subscribe
```

**File**: `components/dev/statestore.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: dev
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.dev.svc.cluster.local:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

**File**: `components/dev/daca-pubsub.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: daca-pubsub
  namespace: dev
spec:
  type: pubsub.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.dev.svc.cluster.local:6379
  - name: redisPassword
    value: ""
```

**File**: `components/dev/message-subscription.yaml`
```yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: message-subscription
  namespace: dev
spec:
  pubsubname: dava-pubsub
  topic: user-chat
  routes:
    default: /subscribe
    rules:
      - match: event.type == "ConversationUpdated"
        path: /subscribe
```

### 3. Deploy Redis Instances
Deploy separate Redis instances in each namespace:

**File**: `redis-prod.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-master
  namespace: prod
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: prod
spec:
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6
        ports:
        - containerPort: 6379
```

**File**: `redis-dev.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-master
  namespace: dev
spec:
  ports:
  - port: 6379
    targetPort: 6379
  selector:
    app: redis
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: dev
spec:
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:6
        ports:
        - containerPort: 6379
```

Apply the Redis deployments:
```bash
kubectl apply -f redis-prod.yaml
kubectl apply -f redis-dev.yaml
```

### 4. Deploy the ChatAgent
Create Kubernetes deployment manifests for `ChatAgent` in each namespace, using the **Step 2** `main.py` without changes.

**File**: `chat-agent-prod.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-agent
  namespace: prod
spec:
  selector:
    matchLabels:
      app: chat-agent
  template:
    metadata:
      labels:
        app: chat-agent
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "chat-agent"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: chat-agent
        image: chat-agent:latest  # Replace with your image
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: components
          mountPath: /components
      volumes:
      - name: components
        configMap:
          name: dapr-components-prod
```

**File**: `chat-agent-dev.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-agent
  namespace: dev
spec:
  selector:
    matchLabels:
      app: chat-agent
  template:
    metadata:
      labels:
        app: chat-agent
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "chat-agent"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: chat-agent
        image: chat-agent:latest  # Replace with your image
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: components
          mountPath: /components
      volumes:
      - name: components
        configMap:
          name: dapr-components-dev
```

Create ConfigMaps for components:
```bash
kubectl create configmap dapr-components-prod --from-file=components/prod -n prod
kubectl create configmap dapr-components-dev --from-file=components/dev -n dev
```

Apply the deployments:
```bash
kubectl apply -f chat-agent-prod.yaml
kubectl apply -f chat-agent-dev.yaml
```

### 5. Use the Step 2 ChatAgent Code
No changes are needed to the **Step 2** `main.py` (see **Step 4.5** README for the code), as namespacing is handled by Kubernetes and Dapr.

### 6. Test the App
Port-forward the `ChatAgent` services in each namespace to test:

**Prod**:
```bash
kubectl port-forward svc/chat-agent 8000:8000 -n prod
```

**Dev**:
```bash
kubectl port-forward svc/chat-agent 8001:8000 -n dev
```

Test the **default** route group in both namespaces:
- **POST /chat/{actor_id}**: Sends a user message.
- **GET /chat/{actor_id}/history**: Retrieves the history.
- **POST /subscribe**: Handles `user-chat` events.

Use `curl` commands:
```bash
# Prod namespace (port 8000)
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there (prod)"}'
curl http://localhost:8000/chat/user1/history

# Dev namespace (port 8001)
curl -X POST http://localhost:8001/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there (dev)"}'
curl http://localhost:8001/chat/user1/history
```

**Expected Output**:
- Prod POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there (prod)"}}`
- Prod GET: `{"history": [{"role": "user", "content": "Hi there (prod)"}, {"role": "assistant", "content": "Got your message: Hi there (prod)"}]}`
- Dev POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there (dev)"}}`
- Dev GET: `{"history": [{"role": "user", "content": "Hi there (dev)"}, {"role": "assistant", "content": "Got your message: Hi there (dev)"}]}`

### 7. Understand the Setup
Review the setup:
- **No Code Changes**: The **Step 2** `main.py` is unchanged, as namespacing is configured via Kubernetes.
- **Namespace Deployment**: `chat-agent-prod.yaml` and `chat-agent-dev.yaml` deploy `ChatAgent` in `prod` and `dev`.
- **Component Isolation**: Separate Redis instances and Dapr components ensure state and event isolation.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub.

Namespacing isolates `user1` in `prod` from `user1` in `dev`, using separate Redis keys and pub/sub topics.

### 8. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances in both namespaces (e.g., `chat-agent` in `prod` and `dev`). Use `kubectl logs` to confirm activation:
```bash
kubectl logs -l app=chat-agent -n prod
kubectl logs -l app=chat-agent -n dev
```
Expect logs like `Activating actor for history-user1` in each namespace.

## Validation
Verify namespacing functionality:
1. **Message Processing**: POST to `/chat/user1` in `prod` and `dev` succeeds.
2. **History Isolation**: GET `/chat/user1/history` in `prod` shows `(prod)` messages, and `dev` shows `(dev)` messages.
3. **State Isolation**: Use `redis-cli` to confirm separate Redis instances:
   ```bash
   redis-cli -h redis-master.prod.svc.cluster.local -p 6379 GET history-user1
   redis-cli -h redis-master.dev.svc.cluster.local -p 6379 GET history-user1
   ```
4. **Event Isolation**: Check logs for `Received event` in each namespace, ensuring `prod` and `dev` events are separate.
5. **Logs**: Verify `Activating actor for history-user1` in both namespaces.

## Troubleshooting
- **Actors Not Isolated**:
  - Check `namespace` in component and deployment files (`prod` or `dev`).
  - Verify separate Redis instances (`kubectl get pods -n prod`, `-n dev`).
- **History Not Isolated**:
  - Confirm `redisHost` in `statestore.yaml` is namespace-specific.
  - Check Redis with `redis-cli KEYS history-*` in each namespace.
- **Deployment Issues**:
  - Verify `chat-agent-prod.yaml` and `chat-agent-dev.yaml` are applied.
  - Check `kubectl get pods -n prod`, `-n dev` for running pods.

## Key Takeaways
- **Namespacing**: Isolates actors and state across namespaces for multi-tenant or staged deployments.
- **Lightweight Configuration**: Kubernetes and Dapr handle namespacing without code changes.
- **Isolation**: Supports separate environments (e.g., `prod`, `dev`) on the same cluster.
- **DACA Alignment**: Enhances isolation and scalability for AI agents.

## Next Steps
- Explore **Step 5** (if defined) or experiment with additional namespaces (e.g., `test`).
- Test namespacing with multiple users in each namespace.
- Integrate namespacing with partitioning (e.g., combine **Step 4.5** and **4.6**).

## Resources
- [Dapr Namespacing](https://docs.dapr.io/operations/hosting/kubernetes/kubernetes-namespaces/)
- [Dapr Python SDK Actors](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [Kubernetes Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)