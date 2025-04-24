# 01_kubernetes_basics: A Hands-On Introduction to Kubernetes

Welcome to the first tutorial in our **Dapr Agentic Cloud Ascent (DACA)** Kubernetes series! In this guide, we’ll dive into Kubernetes fundamentals, building on the containerization concepts from the previous tutorial ("Introduction to Containers and Kubernetes with Rancher Desktop"). Here, we’ll explore Kubernetes architecture, core objects (pods, deployments, services, namespaces, configmaps, secrets), and basic networking, using Rancher Desktop’s local cluster. Through practical examples with the `daca-agent` app, you’ll learn to deploy, manage, and troubleshoot Kubernetes resources, setting the stage for Dapr integration in future tutorials. Let’s begin!

---

## What You’ll Learn

- Kubernetes architecture and its core components.
- Key Kubernetes objects: pods, deployments, services, namespaces, configmaps, and secrets.
- How to use `kubectl` to manage Kubernetes resources.
- Hands-on deployment of the `daca-agent` app in a local Kubernetes cluster.
- Basic networking and troubleshooting in Kubernetes.

## Prerequisites

- Completion of the previous tutorial ("Introduction to Containers and Kubernetes with Rancher Desktop").
- Rancher Desktop installed with Kubernetes enabled (k3s cluster running, `containerd` as the engine).
- Tools: `kubectl`, `nerdctl`, and a terminal.
- Basic command-line knowledge and familiarity with containers (images, Dockerfiles).
- Recommended: 8 GB RAM, 4 CPUs.



## Step 3: Understanding Kubernetes

**Kubernetes** is an open-source platform for orchestrating containers, automating deployment, scaling, and management. In DACA, Kubernetes scales our agent microservices and aligns with options like Azure Container Apps (ACA) for serverless deployment.

### Why Kubernetes?

- **Orchestration**: Manages multiple containers (e.g., agent app, CockroachDB) across clusters.
- **Scaling**: Autoscales pods (container groups) based on demand.
- **Resilience**: Restarts failed containers, ensures high availability.
- **Deployment**: Simplifies rollouts to ACA/Kubernetes clusters.

### Key Concepts

- **Pod**: Smallest unit, runs one or more containers (e.g., agent app + Dapr sidecar).
- **Deployment**: Manages pod replicas, updates, and rollbacks.
- **Service**: Exposes pods via a stable network endpoint (e.g., `agent-app:8080`).
- **Cluster**: Nodes (machines) running Kubernetes, managed by a control plane.

**Analogy**: Kubernetes is an orchestra conductor, directing containers (musicians) to play in harmony.

---

### Quick Setup Recap

If you’ve completed the previous tutorial, your environment should be ready. Verify it:

```bash
kubectl get nodes
```

Expected output:

```
NAME                   STATUS   ROLES                  AGE   VERSION
lima-rancher-desktop   Ready    control-plane,master   1h    v1.32.3+k3s1
```

If not set up, refer to the previous tutorial’s Step 5: Install Rancher Desktop for instructions.

---

## 1. Introduction

### Recap of Containerization

In the last tutorial, we learned:

- **Containers**: Lightweight units packaging apps and dependencies.
- **Images**: Immutable blueprints built from Dockerfiles.
- **Rancher Desktop**: Runs containers with `containerd` and provides a local Kubernetes cluster (k3s).

We containerized a `daca-agent` FastAPI app and deployed it to Kubernetes briefly. Now, we’ll focus on Kubernetes itself.

### What is Kubernetes?

Kubernetes (K8s) is an open-source platform for orchestrating containers. It automates deployment, scaling, and management of containerized applications across clusters of nodes.

#### Why Use Kubernetes?

- **Orchestration**: Manages multiple containers efficiently.
- **Scalability**: Scales apps based on demand.
- **Resilience**: Restarts failed containers automatically.
- **Portability**: Works locally or in the cloud (e.g., Azure Container Apps for DACA).

#### Kubernetes Architecture

Kubernetes operates as a cluster with:

- **Master Node (Control Plane)**:
  - **API Server**: Handles requests (e.g., `kubectl` commands).
  - **etcd**: Stores cluster state.
  - **Controller Manager**: Ensures desired state (e.g., pod replicas).
  - **Scheduler**: Assigns pods to nodes.
- **Worker Nodes**:
  - Run pods (containers).
  - **Kubelet**: Manages pods on the node.
  - **Kube-Proxy**: Handles networking.

**Analogy**: Think of Kubernetes as a shipping port—containers (pods) are cargo, the control plane is the port authority, and worker nodes are docks.

---

## 2. Setting Up a Local Kubernetes Cluster

We’ll use Rancher Desktop’s k3s cluster (lightweight Kubernetes). It’s already set up if you followed the previous tutorial.

### Verify Cluster

Check the cluster status:

```bash
kubectl get nodes
```

### Optional: Explore Alternatives

While we use Rancher Desktop, other tools like `minikube` or `kind` can also run local clusters. The concepts here apply universally.

---

## 3. Working with Pods

### What is a Pod?

A pod is the smallest deployable unit in Kubernetes, typically running one container (e.g., `daca-agent`). Pods can contain multiple containers, but we’ll start simple.

### Hands-On: Create a Pod

Create `pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: agent-pod
spec:
  containers:
  - name: agent-app
    image: k8s.io/daca-agent:latest
    imagePullPolicy: Never
    ports:
    - containerPort: 8000
```

Apply it:

```bash
kubectl apply -f pod.yaml
```

Check status:

```bash
kubectl get pods
```

Output:

```
NAME        READY   STATUS    RESTARTS   AGE
agent-pod   1/1     Running   0          10s
```

View logs:

```bash
kubectl logs agent-pod
```

Port Forward and open in browser

```bash
kubectl port-forward pod/agent-pod 8000:8000
```

Delete it:

```bash
kubectl delete pod agent-pod
```

**Note**: `imagePullPolicy: Never` uses the local image built with `nerdctl`.

---

## 4. Understanding Deployments

### What is a Deployment?

Deployments manage pods, ensuring a specified number of replicas run, handling updates, and rollbacks. They use ReplicaSets to maintain the desired pod count and support rolling updates for zero-downtime deployments.

Note: To access a Deployment’s pods over the network, you’ll need a Service, which we’ll cover in Section 5. For now, we’ll use port-forwarding to test the app.

### Hands-On: Create a Deployment

Create `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: agent-app
  template:
    metadata:
      labels:
        app: agent-app
    spec:
      containers:
      - name: agent-app
        image: k8s.io/daca-agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
```

Apply it:

```bash
kubectl apply -f deployment.yaml
```

Check pods:

```bash
kubectl get pods
```

Output:

```
NAME                         READY   STATUS    RESTARTS   AGE
agent-app-7d9f8c6b5f-abc12   1/1     Running   0          15s
agent-app-7d9f8c6b5f-xyz89   1/1     Running   0          15s
```

#### Scale the Deployment

Increase replicas:

```bash
kubectl scale deployment agent-app --replicas=3
```

Verify:

```bash
kubectl get pods
```

#### Update the Deployment

Edit `deployment.yaml`, change `replicas` to `1`, and reapply:

```bash
kubectl apply -f deployment.yaml
```

#### Roll Back

Check history:

```bash
kubectl rollout history deployment agent-app
```

To demonstrate updates and rollbacks, let’s modify the pod template to create a new revision. Edit deployment.yaml to add an annotation to the pod template and change replicas to 1:

```yaml
  template:
    metadata:
      labels:
        app: agent-app
      annotations:
        version: "v2"  # Added to trigger a new revision
```

Apply the update:

```bash
kubectl apply -f deployment.yaml
```

Check history Again:

```bash
kubectl rollout history deployment agent-app
```

Roll back:

```bash
kubectl rollout undo deployment agent-app
```

---

Important Note: The kubectl rollout undo command requires multiple revisions to work. Kubernetes creates a new revision only when the pod template (spec.template) changes, such as updating the container image, labels, or annotations. Scaling (replicas) does not create a new revision because it doesn’t affect the pod template. In our example, adding the version: v2 annotation triggered a new revision, enabling the rollback. If you only change replicas and reapply, you may see an error like no rollout history found because no new revision was created.

## 4.1 Deploy: Practical Example 3 – Deploying last step container to Kubernetes

Let’s deploy the DACA agent app to Rancher Desktop’s k3s cluster, introducing Kubernetes.

### Step 4.1: Create Kubernetes Manifest

Create `agent-deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: daca
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-app
  namespace: daca
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agent-app
  template:
    metadata:
      labels:
        app: agent-app
    spec:
      containers:
      - name: agent-app
        image: default/daca-agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: agent-app
  namespace: daca
spec:
  selector:
    app: agent-app
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

Here's a breakdown of the `agent-deployment.yaml` Kubernetes manifest:

---

#### 🔧 **Purpose**:
This YAML file defines resources for deploying a **Kubernetes application** in a custom namespace called `daca`. It includes:
1. A **Namespace**
2. A **Deployment** (to run the app container)
3. A **Service** (to expose the container internally in the cluster)

---

#### ✅ Step-by-Step Explanation:

---

##### 1. **Namespace**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: daca
```

- **Purpose**: Creates a separate environment called `daca` to logically isolate your app's resources.
- Namespaces help in organizing workloads in large clusters.

---

##### 2. **Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-app
  namespace: daca
spec:
  replicas: 1
```

- **Deployment**: Manages the creation and lifecycle of pods.
- **replicas: 1**: Runs a single instance (pod) of your app.

```yaml
  selector:
    matchLabels:
      app: agent-app
```

- Links this deployment to pods with the label `app: agent-app`.

```yaml
  template:
    metadata:
      labels:
        app: agent-app
```

- **Pod template** metadata. Labels here must match the selector.

```yaml
    spec:
      containers:
      - name: agent-app
        image: default/daca-agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
```

- **Containers**: Specifies the container to run.
  - `image`: The Docker image to use (`default/daca-agent:latest`).
  - `imagePullPolicy: Never`: Tells Kubernetes **not** to pull from a remote registry. It's used when the image is **built locally** on the node.
  - `containerPort: 8000`: Exposes port 8000 from inside the container (your app listens here).

---

##### 3. **Service**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-app
  namespace: daca
```

- **Service**: Provides a stable way to access the pod(s) managed by the deployment.

```yaml
spec:
  selector:
    app: agent-app
```

- Matches the pods using the label `app: agent-app`.

```yaml
  ports:
  - port: 8000
    targetPort: 8000
```

- **port**: Port exposed by the service internally.
- **targetPort**: Port on the container the traffic will be forwarded to (same here: `8000`).

```yaml
  type: ClusterIP
```

- **ClusterIP**: Default service type, exposes the service **internally within the cluster** (not accessible from outside unless exposed via Ingress or NodePort).

---

#### 🧠 Summary:
You're:
- Creating a namespace `daca`.
- Deploying an app (`default/daca-agent:latest`) as a pod in that namespace.
- Exposing it via an internal service on port `8000`.

- **Note**: `image: default/daca-agent:latest` reflects `containerd`’s namespacing. `imagePullPolicy: Never` ensures k3s uses the local image.

### Step 4.2: Build and Load Image

Build (if not done):

```bash
nerdctl build -t daca-agent .
```

Tag image to use default name space


```bash
nerdctl tag daca-agent:latest k8s.io/daca-agent:latest
```

```bash
nerdctl save k8s.io/daca-agent:latest | nerdctl --namespace k8s.io load
```

```bash
nerdctl images --namespace k8s.io
```


### Step 4.3: Deploy

Apply:

```bash
kubectl apply -f agent-deployment.yaml
```

Verify:

```bash
kubectl get pods -n daca
```

Output:

```
NAME                         READY   STATUS    RESTARTS   AGE
agent-app-6cd8d64b48-5n4cz   1/1     Running   0          12s
```

Access:

```bash
kubectl port-forward svc/agent-app 8000:8000 -n daca
```

Open `http://localhost:8000` to see the agent app.

### Step 4.4: Clean Up

```bash
kubectl delete -f agent-deployment.yaml
```

---


### Step 4.5: Using Rancher Desktop GUI

1. Open Rancher Desktop.
2. **Images**: See `default/daca-agent`, `nginx:alpine`.
3. **Containers**: Run `default/daca-agent` via GUI, map port 8000.
4. **Kubernetes**: View `daca` namespace, `agent-app` pod, and Service.
5. Stop/delete resources via GUI.

---

## 5. Exposing Applications with Services

### What is a Service?

A Service provides a stable endpoint to access a set of pods, using labels to select them. It enables load balancing and network access, unlike port-forwarding, which is temporary. We’ll create a Service for agent-app to avoid errors like services "agent-app" not found.

### Hands-On: Create a Service

Create `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-app
spec:
  selector:
    app: agent-app
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

Apply it:

```bash
kubectl apply -f service.yaml
```

Access it:

```bash
kubectl port-forward svc/agent-app 8000:8000
```

Open `http://localhost:8000` in a browser to see `"Hello from DACA Agent!"`.

**Service Types**:

- `ClusterIP`: Default, internal access.
- `NodePort`: Exposes on a node port (e.g., 30000-32767).
- `LoadBalancer`: Cloud-specific, external access.

---

## 6. Organizing Resources with Namespaces

### What is a Namespace?

Namespaces isolate resources (e.g., pods, services) within a cluster.

### Hands-On: Use a Namespace

Create `daca` namespace:

```bash
kubectl create namespace daca
```

Redeploy with namespace:

```bash
kubectl apply -f deployment.yaml -n daca
kubectl apply -f service.yaml -n daca
```

List pods:

```bash
kubectl get pods -n daca
```

Switch context (optional):

```bash
kubectl config set-context --current --namespace=daca
```

---

## 7. Configuration Management with ConfigMaps and Secrets

### What are ConfigMaps and Secrets?

- **ConfigMaps**: Store non-sensitive configuration (e.g., app settings).
- **Secrets**: Store sensitive data (e.g., API keys), base64-encoded.

### Hands-On: Create a ConfigMap

Create `configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-config
  namespace: daca
data:
  greeting: "Hello from ConfigMap!"
```

Apply it:

```bash
kubectl apply -f configmap.yaml -n daca
```

Update `deployment.yaml` to use it:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-app
  namespace: daca
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agent-app
  template:
    metadata:
      labels:
        app: agent-app
    spec:
      containers:
      - name: agent-app
        image: k8s.io/daca-agent:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: GREETING
          valueFrom:
            configMapKeyRef:
              name: agent-config
              key: greeting
```

Apply and test.

### Hands-On: Create a Secret

Create `secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: agent-secret
  namespace: daca
type: Opaque
data:
  api-key: YXBpLWtleS1leGFtcGxl  # base64 for "api-key-example"
```

Apply it:

```bash
kubectl apply -f secret.yaml -n daca
```

Update `deployment.yaml` to use the secret similarly.

---

## 8. Basic Networking in Kubernetes

- **Services**: Route traffic to pods via labels (e.g., `app: agent-app`).
- **Ingress**: Manages external access (covered in later tutorials).

**Example**: Our `ClusterIP` service routes traffic to `daca-agent` pods.

---

## 9. Troubleshooting and Debugging

### Common Commands

- Inspect resources:

```bash
kubectl describe pod agent-app-xxx -n daca
```

- View logs:

```bash
kubectl logs agent-app-xxx -n daca
```

### Try It Yourself

Simulate an error (e.g., wrong image name), then fix it using `describe` and `logs`.

---

## 10. Conclusion

You’ve mastered Kubernetes basics:

- Architecture and core objects.
- Deploying and managing the `daca-agent` app.
- Troubleshooting with `kubectl`.

In the DACA series, Kubernetes will orchestrate microservices with Dapr for scalability and resilience. Next, in `02_dapr_theory_and_cli`, we’ll explore Dapr’s theory and CLI tools.

### Optional Exercises

1. Deploy a pod in a custom namespace.
2. Scale a deployment to 5 replicas and expose it with a NodePort service.
3. Explore `kubectl get events` for cluster insights.

Happy learning!