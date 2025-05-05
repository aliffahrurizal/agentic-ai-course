# Step 1: Observability

This is **Step 1** of the **Dapr Agentic Cloud Ascent (DACA)** learning path, part of the **07_daca_advanced_experiments** module. In this step, you’ll enhance the `ChatAgent` actor from **Agent Actors Step 2** by adding Dapr observability with OpenTelemetry to collect tracing and metrics (e.g., actor invocation counts, state store latency). This improves monitoring and debugging for production-grade AI agents, aligning with DACA’s goal of reliable, observable systems.

## Overview

The **observability** step configures the `ChatAgent` to:

- Enable Dapr’s OpenTelemetry tracing and metrics export to Jaeger (traces) and Prometheus (metrics).
- Monitor actor invocation counts and state store operation latencies.
- Test observability by invoking the `ChatAgent` and checking traces/metrics in Jaeger and Prometheus.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

Observability provides insights into actor performance and system health, critical for scaling AI agents in distributed environments.

### Learning Objectives

- Configure Dapr’s OpenTelemetry for tracing and metrics.
- Deploy Jaeger and Prometheus for observability.
- Validate traces and metrics for actor operations.
- Maintain lightweight changes with no actor code modifications.

### Ties to DACA

- **Reliability**: Observability helps diagnose issues like state store failures or slow responses.
- **Scalability**: Metrics enable performance optimization for high user loads.
- **Production-Readiness**: Tracing and metrics support monitoring in distributed AI systems.

## Key Concepts

### Dapr Observability

Dapr’s OpenTelemetry integration provides:

- **Tracing**: Tracks actor method calls (e.g., `process_message`) and state store operations (e.g., Redis get/set).
- **Metrics**: Measures actor invocations, state store latency, and error rates.
- **Exporters**: Sends data to external tools like Jaeger (traces) and Prometheus (metrics).

In this step, you’ll configure Dapr to export traces to Jaeger and metrics to Prometheus, monitoring `ChatAgent` performance without modifying its code.

### Lightweight Configuration

Observability is added with minimal changes:

- A new Dapr configuration file (`observability.yaml`) to enable OpenTelemetry.
- Deployment of Jaeger and Prometheus in Kubernetes for trace and metric collection.
- No changes to the `ChatAgent` code, as observability is handled by Dapr’s runtime.
- Minimal dependencies (Jaeger, Prometheus), keeping the setup lightweight.

### Interaction Patterns

The `ChatAgent` supports:

- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) with traced invocations.
- **Event-Driven**: Pub/sub events via `/subscribe` with traced events.
- **Observable**: Traces and metrics provide insights into actor and system performance.

## Hands-On Dapr Virtual Actor

### 0. Setup Code

Use the [00_lab_starter_code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code) from **Step 2**. Ensure **Step 2** is complete and you have a Kubernetes cluster (e.g., `minikube`).

Verify dependencies:

```bash
uv add dapr dapr-ext-fastapi pydantic
```

### 1. Deploy Observability Tools

Deploy Jaeger and Prometheus in your Kubernetes cluster to collect traces and metrics.

**File**: `jaeger.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: default
spec:
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:latest
          ports:
            - containerPort: 16686
            - containerPort: 4317
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger
  namespace: default
spec:
  ports:
    - port: 16686
      targetPort: 16686
      name: ui
    - port: 4317
      targetPort: 4317
      name: otlp
  selector:
    app: jaeger
```

**File**: `prometheus.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
  namespace: default
spec:
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
        - name: prometheus
          image: prom/prometheus:latest
          ports:
            - containerPort: 9090
          volumeMounts:
            - name: config
              mountPath: /etc/prometheus
      volumes:
        - name: config
          configMap:
            name: prometheus-config
---
apiVersion: v1
kind: Service
metadata:
  name: prometheus
  namespace: default
spec:
  ports:
    - port: 9090
      targetPort: 9090
  selector:
    app: prometheus
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: default
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'dapr'
      static_configs:
      - targets: ['chat-agent-dapr:3500']
```

Apply the deployments:

```bash
kubectl apply -f jaeger.yaml
kubectl apply -f prometheus.yaml
```

### 2. Configure Dapr Observability

Add a Dapr configuration file to enable OpenTelemetry tracing and metrics.

**File**: `components/observability.yaml`

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: observability
  namespace: default
spec:
  tracing:
    samplingRate: "1"
    otel:
      endpoint: "jaeger:4317"
      isSecure: false
      protocol: grpc
  metrics:
    enabled: true
    exporter:
      type: prometheus
      address: "prometheus:9090"
```

Update your Dapr run command or Tilt configuration to include this file (e.g., ensure `components/` is mounted).

### 3. Use the Step 2 ChatAgent Code

No changes are needed to the **Step 2** `ChatAgent` code, as observability is handled by Dapr’s configuration. Use the **Step 2** `main.py` as-is (see **Step 4.5** README for the code).

### 4. Test the App

Port-forward Jaeger and Prometheus to access their UIs:

```bash
kubectl port-forward svc/jaeger 16686:16686
kubectl port-forward svc/prometheus 9090:9090
```

Open:

- Jaeger UI: [http://localhost:16686](http://localhost:16686)
- Prometheus UI: [http://localhost:9090](http://localhost:9090)

Test the **default** route group:

- **POST /chat/{actor_id}**: Sends a user message.
- **GET /chat/{actor_id}/history**: Retrieves the conversation history.
- **POST /subscribe**: Handles `user-chat` topic events.

Use `curl` commands to generate activity:

```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there"}'
curl http://localhost:8000/chat/user1/history
curl -X POST http://localhost:8000/chat/user2 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hello"}'
```

**Expected Output**:

- POST user1: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- GET user1: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}]}`
- POST user2: `{"response": {"role": "assistant", "content": "Got your message: Hello"}}`
- Jaeger: Traces for `POST /chat/user1`, `GET /chat/user1/history`, and `POST /chat/user2`, showing `process_message`, `get_conversation_history`, and Redis operations.
- Prometheus: Metrics like `dapr_actor_invocations_total{actor_type="ChatAgent"}` increasing with each request.

### 5. Understand the Setup

Review the setup:

- **No Code Changes**: The **Step 2** `main.py` remains unchanged, as observability is configured via Dapr.
- **Observability Config**: `observability.yaml` enables tracing to Jaeger and metrics to Prometheus.
- **Tools**: Jaeger visualizes traces (e.g., actor method calls, state store latency), Prometheus collects metrics (e.g., invocation counts, errors).
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub from **Step 2**.

Observability provides actionable insights into `ChatAgent` performance without modifying the application logic.

### 6. Observe the Dapr Dashboard

Run:

```bash
dapr dashboard
```

Check the **Actors** tab for `ChatAgent` instances (e.g., `2` for `user1`, `user2`). Use Jaeger and Prometheus to monitor traces and metrics, complementing the dashboard’s actor counts.

## Validation

Verify observability functionality:

1. **Message Processing**: POST to `/chat/user1` and `/chat/user2` succeeds.
2. **History Retrieval**: GET `/chat/user1/history` shows the correct history.
3. **Tracing**: In Jaeger, search for `chat-agent` and confirm traces for `process_message`, `get_conversation_history`, and Redis operations (e.g., `get_state`, `set_state`).
4. **Metrics**: In Prometheus, query `dapr_actor_invocations_total{actor_type="ChatAgent"}` and `dapr_state_latency_seconds{component="statestore"}` to confirm increasing invocation counts and state store latencies.
5. **Logs**: Check `dapr logs -a chat-agent` for normal operation, supplemented by Jaeger/Prometheus data.

## Troubleshooting

- **No Traces in Jaeger**:
  - Verify `observability.yaml` has `endpoint: "jaeger:4317"`.
  - Check Jaeger pod status (`kubectl get pods`).
  - Ensure `samplingRate: "1"` for full tracing.
- **No Metrics in Prometheus**:
  - Confirm `prometheus.yaml` targets `chat-agent-dapr:3500`.
  - Check Prometheus pod status and config (`kubectl get configmaps prometheus-config -o yaml`).
- **Requests Not Traced**:
  - Verify Dapr sidecar is running (`kubectl get pods`).
  - Check `components/observability.yaml` is loaded.

## Key Takeaways

- **Observability**: Tracing and metrics provide insights into actor performance and system health.
- **Lightweight Configuration**: Dapr’s OpenTelemetry integration requires only a config file and external tools.
- **Production-Readiness**: Enables monitoring and debugging for scalable AI agents.
- **DACA Alignment**: Supports reliable, observable systems for conversational AI.

## Next Steps

- Proceed to **Step 6: State Encryption** to secure conversation history.
- Experiment with additional metrics (e.g., pub/sub latency) or trace filters in Jaeger.
- Integrate with a monitoring dashboard (e.g., Grafana) for visualized metrics.

## Resources

- [Dapr Observability](https://docs.dapr.io/operations/monitoring/observability/)
- [Dapr OpenTelemetry](https://docs.dapr.io/operations/monitoring/telemetry/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)
