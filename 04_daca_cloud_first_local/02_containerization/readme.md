# Introduction to [Containers](https://www.docker.com/resources/what-container/) and [Kubernetes](https://kubernetes.io/docs/concepts/overview/) with [Rancher Desktop](https://docs.rancherdesktop.io/)

Welcome to the twelfth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! This tutorial lays the foundation for containerizing our agentic AI microservices by introducing **containers**, **Kubernetes**, and **Rancher Desktop**. We’ll explore how containers package applications for consistency, how Kubernetes orchestrates them for scalability, and how Rancher Desktop simplifies both on your local machine using the `containerd` engine. Through hands-on examples, we’ll containerize a DACA agent app and deploy it in a Kubernetes cluster, setting the stage for Dapr integration in the next tutorial. Let’s get started!

---

## What You’ll Learn

- Core concepts of containerization (containers, images, Dockerfiles).
- Basics of Kubernetes (pods, Deployments, Services).
- How Rancher Desktop manages containers with `containerd` and provides a local Kubernetes cluster.
- Practical examples of building, running, and deploying a DACA agent app in containers and Kubernetes.
- Key commands for `nerdctl` (containerd CLI) and Kubernetes (`kubectl`).
- Download [Rancher Desktop](https://rancherdesktop.io/) and [Lens an IDE for Kubernetes](https://k8slens.dev/download)

## Prerequisites

- A computer with administrative privileges (macOS, Windows, or Linux).
- Basic command-line familiarity (e.g., Terminal on macOS/Linux, PowerShell on Windows).
- No prior container or Kubernetes experience needed—we start from scratch!
- Recommended: 8 GB RAM, 4 CPUs.

---

## Step 1: Understanding Containers

**Containers** are lightweight, portable units that package an application and its dependencies (code, libraries, runtime) to run consistently across environments. In DACA, containers ensure our agentic AI microservices (e.g., Chat Service with OpenAI Agents SDK) behave the same in development and production.

### Why Containers?

- **Consistency**: Packages dependencies (e.g., Python, OpenAI SDK), avoiding “it works on my machine” issues.
- **Portability**: Runs on any compatible system, from laptops to cloud clusters.
- **Isolation**: Each container is sandboxed, preventing conflicts (e.g., different Python versions).
- **Efficiency**: Shares the host OS kernel, using less RAM than virtual machines (VMs).
- **Scalability**: Easily scaled with orchestration tools like Kubernetes.

### Containers vs. Virtual Machines

- **VMs**: Run a full OS (e.g., Ubuntu) on a hypervisor, heavy (GBs), slow to start.
- **Containers**: Share host OS, include only app dependencies, lightweight (MBs), instant start.

**Analogy**: VMs are houses with separate utilities; containers are apartments sharing a building’s infrastructure.

---

## Step 2: Core Container Concepts

Containerization packages apps into containers. Key terms:

- **Container**: A running instance of an image, isolating the app (e.g., FastAPI agent).
- **Image**: Immutable snapshot of app + dependencies (e.g., `python:3.11-slim`).
- **Dockerfile**: Script to build images (e.g., install OpenAI SDK, copy code).
- **Registry**: Stores images (e.g., Docker Hub, private registries like AWS ECR).
- **Container Engine**: Runtime to build/run containers (we’ll use `containerd` via Rancher Desktop).

Let's understand the **Core Concepts of App Containerization**. Containerization is the process of packaging an application and its dependencies into a container. Let’s break down the key concepts:

### 2.1 Containers
A **container** is a running instance of a container image. It’s an isolated environment that contains:
- The application code.
- The runtime (e.g., Python, Node.js).
- Libraries and dependencies.
- Configuration files.

Containers are ephemeral—they can be created, started, stopped, and deleted as needed. If a container crashes, you can restart it or create a new one from the same image.

### 2.2 Container Images
A **container image** is a lightweight, immutable snapshot of an application and its dependencies. It’s the blueprint for creating containers. Images are built in layers, where each layer represents a set of changes (e.g., installing a dependency, copying code).

- Images are stored in a **registry**, such as **Docker Hub** (a public registry) or a private registry (e.g., AWS ECR, Google Artifact Registry).
- Example: The `python:3.9-slim` image on Docker Hub contains a minimal Python 3.9 environment.


### 2.3 Dockerfile
A **Dockerfile** is a script that defines how to build a container image. It contains instructions like:
- Specifying a base image (e.g., `FROM python:3.9-slim`).
- Copying application code into the image.
- Installing dependencies.
- Setting environment variables.
- Defining the command to run the application.

Example Dockerfile for a Python app:
```dockerfile
# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the app
CMD ["python", "app.py"]
```
---

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

## Step 4: Introducing Rancher Desktop

**Rancher Desktop** is a lightweight app for container management and Kubernetes on macOS, Windows, and Linux. It uses `containerd` as the container engine (with `nerdctl` CLI) and includes a built-in Kubernetes cluster (k3s), ideal for DACA’s ACA/Kubernetes focus.

### Why Rancher Desktop?

- **Containers**: Build/run images with `containerd` and `nerdctl`.
- **Kubernetes**: Provides k3s, a low-RAM cluster (2-3 GB).
- **Simplicity**: GUI + CLI for managing containers/pods.
- **DACA Fit**: Prepares for Step 13’s Dapr in Kubernetes.

---

## Step 5: [Install Rancher Desktop](https://rancherdesktop.io/)

Let’s install Rancher Desktop to manage containers and Kubernetes, selecting `containerd` as the container engine.

### Step 5.1: System Requirements

- **macOS**: Ventura (13) or higher, 8 GB RAM, 4 CPUs (your M2 meets this).
- **Windows**: Windows 10/11 (Home OK), WSL 2, 8 GB RAM, 4 CPUs.
- **Linux**: .deb/.rpm/AppImage support, /dev/kvm access, 8 GB RAM, 4 CPUs.
- Internet connection for initial image downloads.

### Step 5.2: Download and Install

1. **Download**:

   - Visit Rancher Desktop releases.
   - Choose your OS:
     - **macOS**: `Rancher.Desktop-X.Y.Z.dmg` (e.g., for M2, aarch64).
     - **Windows**: `Rancher.Desktop.Setup.X.Y.Z.msi`.
     - **Linux**: `.deb`, `.rpm`, or AppImage.

2. **Install**:

   - **macOS**:

     - Open the `.dmg` file.
     - Drag Rancher Desktop to Applications.
     - Launch from Applications.

   - **Windows**:

     - Run the `.msi` installer.
     - Enable WSL 2 if prompted.
     - Choose “Install for all users” for full features.
     - Complete the wizard.

   - **Linux** (e.g., Ubuntu):

     ```bash
     curl -s https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/Release.key | gpg --dearmor | sudo dd status=none of=/usr/share/keyrings/isv-rancher-stable-archive-keyring.gpg
     echo 'deb [signed-by=/usr/share/keyrings/isv-rancher-stable-archive-keyring.gpg] https://download.opensuse.org/repositories/isv:/Rancher:/stable/deb/ ./' | sudo dd status=none of=/etc/apt/sources.list.d/isv-rancher-stable.list
     sudo apt update
     sudo apt install rancher-desktop
     ```

     - Ensure `/dev/kvm` access:

       ```bash
       [ -r /dev/kvm ] && [ -w /dev/kvm ] || echo 'insufficient privileges'
       sudo usermod -a -G kvm "$USER"
       ```

     - Reboot if needed.

3. **Configure Rancher Desktop**:

   - Launch the app. On first run, a setup window appears:
     - **Enable Kubernetes**: Check this box (enables k3s).
     - **Kubernetes Version**: Select `v1.32.3 (stable, latest)` for stability and Dapr compatibility.
     - **Container Engine**: Select `containerd` (uses `nerdctl` CLI, namespaced images).
     - **Configure PATH**: Choose `Automatic` to add `nerdctl`, `kubectl`, and `helm` to your PATH.
   - Click **OK**. Rancher Desktop downloads k3s images (\~5-10 min first run).

![Rancher Desktop Installation](./install-ranch-dekstop.png)

4. **Verify in GUI**:

   - Open Rancher Desktop and check the Containers, Images, and Kubernetes tabs.

### Step 5.3: Verify Installation

Open a terminal:

```bash
nerdctl --version
```

Output:

```
nerdctl version 2.0.3
```

Verify Kubernetes:

```bash
kubectl version --client
```

Output:

```
Client Version: v1.32.3
Kustomize Version: v5.5.0
```

Check cluster:

```bash
kubectl get nodes
```

Output:

```
NAME                   STATUS   ROLES                  AGE   VERSION
lima-rancher-desktop   Ready    control-plane,master   14m   v1.32.3+k3s1
```

**Note**: If `nerdctl` or `kubectl` commands aren’t found, restart your terminal or ensure PATH is updated (`$HOME/.rd/bin`).

- If kubectl get nodes command fails then you will have to check and configure context to racher desktop. I faced this issue as a user switching from Docker.

```bash
kubectl config current-context
kubectl config get-contexts
kubectl config use-context rancher-desktop
kubectl config current-context
kubectl get nodes
```

---

## Step 6: Practical Example 1 – Running a Simple Container

Let’s run a container to learn container basics, using Rancher Desktop’s `containerd` engine and `nerdctl` CLI.

### Step 6.1: Run an Nginx Container

1. **Pull Nginx Image**:

   ```bash
   nerdctl pull nginx:alpine
   ```

   - Uses lightweight `alpine` (5 MB, M2-friendly).

2. **Run Container**:

   ```bash
   nerdctl run -d -p 8080:80 --name my-nginx nginx:alpine
   ```

   - `-d`: Background mode.
   - `-p 8080:80`: Maps host port 8080 to container port 80.
   - `--name my-nginx`: Names the container.

   **Note**: With `containerd`, images are namespaced (e.g., `nginx:alpine` is in the `default` namespace), but `nerdctl` handles this transparently for most commands.

3. **Verify**:

   ```bash
   nerdctl ps
   ```

   Output:

   ```
   CONTAINER ID    IMAGE                             COMMAND                   CREATED           STATUS    PORTS                   NAMES
   6c73ef9cda7a    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    10 seconds ago    Up        0.0.0.0:8080->80/tcp    my-nginx
   ```

4. **Access**:

   - Open `http://localhost:8080` to see Nginx’s welcome page.

5. **Clean Up**:

   ```bash
   nerdctl stop my-nginx
   nerdctl rm my-nginx
   ```

---

## Step 7: Practical Example 2 – Building a DACA Agent Container

Let’s build a container for a DACA agent app (FastAPI with OpenAI Agents SDK), mimicking the Chat Service.

### Step 7.1: Create the App

#### Create a project:

```bash
uv init daca-agent
cd daca-agent
```

#### Setup Virtual Environment and install dependencies

On macOS/Linux:

```bash
uv venv
source .venv/bin/activate
```

On Windows:

```bash
uv venv
.venv\Scripts\activate
```

```bash
uv add "fastapi[standard]"
```

#### Create `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": f"Hello from DACA Agent!"}
```


### Step 7.2: Create Dockerfile

Create `Dockerfile`:

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

Create `.dockerignore` file:
```
.venv
.git
.gitignore
.env
__pycache__
```

### Step 7.3: Build and Run

Build:

```bash
nerdctl build -t daca-agent .
```

Check Image
```bash
nerdctl images
```

OUTPUT:
```bash
(daca-agent) (chat-service) mjs@Muhammads-MacBook-Pro-3 daca-agent % nerdctl images
REPOSITORY    TAG       IMAGE ID        CREATED           PLATFORM       SIZE       BLOB SIZE
daca-agent    latest    3ec4183b0331    21 seconds ago    linux/arm64    366.6MB    118MB
nginx         alpine    4ff102c5d78d    13 minutes ago    linux/arm64    53.72MB    21.67MB
```

Run:

```bash
nerdctl run -d -p 8000:8000 --name daca-agent  daca-agent
```

- **Note**: `containerd` uses namespaces, so the image `daca-agent` is in the `default` namespace (`default/daca-agent`).

Verify:

```bash
nerdctl ps
```

Access `http://localhost:8000`:

```
{"message": "Hello from DACA Agent!"}
```

Logs:

```bash
nerdctl logs daca-agent
```

Clean up:

```bash
nerdctl stop daca-agent
nerdctl rm daca-agent
```

---

## Step 8: Practical Example 3 – Deploying to Kubernetes

Let’s deploy the DACA agent app to Rancher Desktop’s k3s cluster, introducing Kubernetes.

### Step 8.1: Create Kubernetes Manifest

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

### Step 8.2: Build and Load Image

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


### Step 8.3: Deploy

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

### Step 8.4: Clean Up

```bash
kubectl delete -f agent-deployment.yaml
```

---

## Step 9: Using Rancher Desktop GUI

1. Open Rancher Desktop.
2. **Images**: See `default/daca-agent`, `nginx:alpine`.
3. **Containers**: Run `default/daca-agent` via GUI, map port 8000.
4. **Kubernetes**: View `daca` namespace, `agent-app` pod, and Service.
5. Stop/delete resources via GUI.

---

## Step 10: Key Commands

- **Container (nerdctl)**:
  - `nerdctl build -t <name> .`: Build image.
  - `nerdctl run -d -p <port> <namespace>/<image>`: Run container.
  - `nerdctl ps`: List running containers.
  - `nerdctl logs/stop/rm <container>`: Manage containers.
- **Kubernetes**:
  - `kubectl apply -f <file>`: Deploy resources.
  - `kubectl get pods/services -n <namespace>`: List resources.
  - `kubectl port-forward svc/<name> <port>`: Access Service.
  - `kubectl delete -f <file>`: Remove resources.

---

## Step 11: Why Containers and Kubernetes for DACA?

- **Consistency**: Containers ensure agent apps (e.g., Chat Service) run identically everywhere.
- **Scalability**: Kubernetes scales pods for DACA’s event-driven architecture.
- **Deployment**: Prepares for ACA/Kubernetes, avoiding Compose’s rework.
- **Resilience**: Kubernetes restarts failed pods, supporting CockroachDB state management.

Next, in **13_dapr_containerization**, we’ll add a Dapr sidecar to this agent app in Kubernetes, enabling state and pub/sub.

---

## Step 12: Next Steps

You’ve learned containers and Kubernetes with Rancher Desktop! Now install Lense - we will use it later
- [Download Lens - IDE for Kubernetes](https://k8slens.dev/download)

### Optional Exercises

1. Deploy a Redis pod in Kubernetes (`redis:alpine`).
2. Push `default/daca-agent` to Docker Hub (requires `nerdctl push`).
3. Explore `kubectl describe pod` for debugging.

---

## Conclusion

We’ve covered containerization (images, `Dockerfile`, containers) and Kubernetes (pods, Deployments, Services) using Rancher Desktop with the `containerd` engine. With hands-on DACA examples, you’re ready to containerize microservices with Dapr in Kubernetes, paving the way for scalable agentic AI.