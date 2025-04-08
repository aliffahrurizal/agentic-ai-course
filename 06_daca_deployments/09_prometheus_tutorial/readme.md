# Tutorial: Monitoring Kubernetes with the Prometheus Operator

Below is a detailed tutorial on using the Prometheus Operator with Kubernetes to set up and manage monitoring for your cluster and applications. This tutorial builds on the concept of Kubernetes Operators, focusing specifically on the Prometheus Operator, a prebuilt Operator for deploying and managing Prometheus instances. I’ll cover installation, configuration, monitoring applications, and visualization with Grafana, using practical examples.

---

## Overview
The Prometheus Operator simplifies the deployment and management of Prometheus, a powerful time-series monitoring system, on Kubernetes. It uses Custom Resource Definitions (CRDs) to define Prometheus instances, service monitors, and alerting rules, automating tasks like scaling, configuration, and discovery.

### What You’ll Learn
- How to install the Prometheus Operator.
- How to deploy a Prometheus instance using its Custom Resources.
- How to monitor Kubernetes cluster components and custom applications.
- How to set up alerting and visualize metrics with Grafana.

### Prerequisites
- A Kubernetes cluster (e.g., Minikube, GKE, EKS).
- `kubectl` installed and configured.
- Helm 3 installed (optional, but recommended for easier deployment).
- Basic familiarity with Kubernetes and YAML.

---

## Step 1: Install the Prometheus Operator

The Prometheus Operator is typically installed as part of the `kube-prometheus-stack` Helm Chart, which includes Prometheus, the Operator, Grafana, and additional tools. This is the recommended approach for a full monitoring stack.

### Using Helm
1. **Add the Helm Repository**:
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm repo update
   ```

2. **Install the Prometheus Operator**:
   Create a namespace for monitoring:
   ```bash
   kubectl create namespace monitoring
   ```
   Install the stack:
   ```bash
   helm install prometheus-stack prometheus-community/kube-prometheus-stack --namespace monitoring
   ```
   This deploys:
   - The Prometheus Operator (manages Prometheus instances).
   - A default Prometheus instance.
   - Grafana for visualization.
   - Alertmanager for alerting.

3. **Verify Installation**:
   Check the pods:
   ```bash
   kubectl get pods -n monitoring
   ```
   You should see pods like:
   - `prometheus-stack-kube-prom-operator-xxxxx` (the Operator).
   - `prometheus-prometheus-stack-kube-prom-prometheus-0` (Prometheus instance).
   - `prometheus-stack-grafana-xxxxx` (Grafana).

### Alternative: Raw YAML
If you prefer not to use Helm, apply the raw manifests:
```bash
curl -sL https://github.com/prometheus-operator/prometheus-operator/releases/latest/download/bundle.yaml | kubectl apply -f -
```
Then deploy additional components manually (Prometheus, Grafana, etc.), but Helm is simpler for a full stack.

---

## Step 2: Deploy a Prometheus Instance

The Prometheus Operator uses a `Prometheus` Custom Resource (CR) to define Prometheus instances. The Helm chart already deploys a default instance, but let’s create a custom one to understand the process.

### Create a Prometheus CR
1. Create a file named `custom-prometheus.yaml`:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: Prometheus
   metadata:
     name: custom-prometheus
     namespace: monitoring
   spec:
     replicas: 2
     resources:
       requests:
         memory: "400Mi"
         cpu: "200m"
       limits:
         memory: "800Mi"
     serviceMonitorSelector:
       matchLabels:
         app: monitored-app
     ruleSelector:
       matchLabels:
         role: prometheus-rules
     storage:
       volumeClaimTemplate:
         spec:
           storageClassName: standard
           resources:
             requests:
               storage: 8Gi
   ```
   - `replicas`: Runs 2 Prometheus pods for high availability.
   - `serviceMonitorSelector`: Specifies which `ServiceMonitor` resources this instance will use.
   - `storage`: Configures persistent storage for metrics.

2. Apply it:
   ```bash
   kubectl apply -f custom-prometheus.yaml
   ```

3. Verify:
   ```bash
   kubectl get prometheus -n monitoring
   kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus
   ```
   Look for pods like `custom-prometheus-0` and `custom-prometheus-1`.

The Operator will create the Prometheus pods, a service, and manage their lifecycle.

---

## Step 3: Monitor Kubernetes Cluster Components

The `kube-prometheus-stack` Helm chart automatically monitors cluster components (e.g., nodes, pods, kubelets) using predefined `ServiceMonitor` and `PodMonitor` resources. Let’s explore how this works and customize it.

### Default Monitoring
The chart includes:
- **ServiceMonitors** for Kubernetes components (e.g., `kube-apiserver`, `kube-scheduler`).
- A `Prometheus` instance configured to scrape these endpoints.

Check existing ServiceMonitors:
```bash
kubectl get servicemonitor -n monitoring
```

### Customize Cluster Monitoring
To adjust what’s monitored, modify the Helm values. Create a `values.yaml`:
```yaml
prometheus:
  prometheusSpec:
    additionalScrapeConfigs:
      - job_name: "extra-kube-component"
        static_configs:
          - targets: ["kube-controller-manager:10252"]
```
Upgrade the release:
```bash
helm upgrade prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring -f values.yaml
```

---

## Step 4: Monitor a Custom Application

To monitor your own application, define a `ServiceMonitor` to tell Prometheus where to scrape metrics.

### Example Application
Deploy a simple app that exposes metrics (e.g., an Nginx server with a metrics endpoint):
```yaml
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-app
  template:
    metadata:
      labels:
        app: nginx-app
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-app-service
  namespace: default
spec:
  selector:
    app: nginx-app
  ports:
  - port: 80
    targetPort: 80
    name: http
```
Apply it:
```bash
kubectl apply -f app.yaml
```

### Create a ServiceMonitor
1. Create `nginx-servicemonitor.yaml`:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: nginx-app-monitor
     namespace: monitoring
     labels:
       app: monitored-app
   spec:
     selector:
       matchLabels:
         app: nginx-app
     endpoints:
     - port: http
       path: /metrics
   ```
   - `selector`: Matches the service’s labels.
   - `endpoints`: Specifies the port and path for metrics (Note: Nginx doesn’t expose `/metrics` by default; this is an example. For real metrics, use an app like a Python Flask app with Prometheus client libraries).

2. Apply it:
   ```bash
   kubectl apply -f nginx-servicemonitor.yaml
   ```

3. Verify:
   The `custom-prometheus` instance (from Step 2) will scrape this endpoint because its `serviceMonitorSelector` matches the `app: monitored-app` label.

---

## Step 5: Set Up Alerting

The Prometheus Operator supports alerting via the `PrometheusRule` CR.

### Create an Alert Rule
1. Create `alert-rules.yaml`:
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: PrometheusRule
   metadata:
     name: custom-alerts
     namespace: monitoring
     labels:
       role: prometheus-rules
   spec:
     groups:
     - name: example
       rules:
       - alert: HighPodMemory
         expr: sum(rate(container_memory_usage_bytes[5m])) by (pod) > 100000000
         for: 5m
         labels:
           severity: warning
         annotations:
           summary: "High memory usage detected in pod {{ $labels.pod }}"
           description: "Pod {{ $labels.pod }} has been using >100MB memory for 5 minutes."
   ```
   - `expr`: Defines the condition (memory usage > 100MB).
   - `for`: Waits 5 minutes before firing the alert.

2. Apply it:
   ```bash
   kubectl apply -f alert-rules.yaml
   ```

3. The `custom-prometheus` instance will load this rule because its `ruleSelector` matches `role: prometheus-rules`.

### Configure Alertmanager
The Helm chart includes Alertmanager. Access it:
```bash
kubectl port-forward -n monitoring svc/prometheus-stack-kube-prom-alertmanager 9093:9093
```
Open `http://localhost:9093` to view alerts.

---

## Step 6: Visualize with Grafana

The Helm chart deploys Grafana with preconfigured dashboards.

1. **Access Grafana**:
   ```bash
   kubectl port-forward -n monitoring svc/prometheus-stack-grafana 3000:80
   ```
   Open `http://localhost:3000`.

2. **Log In**:
   - Username: `admin`
   - Password: Get it with:
     ```bash
     kubectl get secret -n monitoring prometheus-stack-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
     ```

3. **Explore Dashboards**:
   Grafana includes dashboards for Kubernetes cluster metrics (e.g., nodes, pods). Add a custom dashboard for your app by importing a JSON file or creating one manually using Prometheus queries (e.g., `rate(http_requests_total[5m])`).

---

## Step 7: Clean Up (Optional)

Uninstall the stack:
```bash
helm uninstall prometheus-stack -n monitoring
kubectl delete namespace monitoring
```

---

## Conclusion

This tutorial walked you through setting up the Prometheus Operator on Kubernetes using Helm, deploying a custom Prometheus instance, monitoring cluster components and applications, setting up alerts, and visualizing data with Grafana. The Operator automates Prometheus management, making it scalable and maintainable. You can extend this setup by adding more `ServiceMonitors`, `PrometheusRules`, or integrating with external systems.

