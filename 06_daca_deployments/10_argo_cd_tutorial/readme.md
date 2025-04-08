# Tutorial: Getting Started with Argo CD on Kubernetes

Below is a detailed tutorial on **Argo CD**, a declarative, GitOps continuous delivery (CD) tool for Kubernetes. This tutorial covers installation, configuration, deploying an application, monitoring, and managing it using Argo CD. I’ll provide step-by-step instructions with examples, assuming a beginner-to-intermediate audience familiar with Kubernetes basics.

---

## What is Argo CD?

Argo CD is an open-source tool that automates the deployment and management of applications on Kubernetes using the GitOps methodology. In GitOps, your Git repository serves as the single source of truth for your application’s desired state, and Argo CD ensures your Kubernetes cluster matches that state by continuously reconciling differences.

### Key Features
- **Declarative Configuration**: Define your application state in Git using YAML, Helm, or Kustomize.
- **Automated Syncing**: Automatically applies changes from Git to your cluster.
- **Drift Detection**: Monitors and corrects deviations between the live cluster state and Git.
- **Web UI and CLI**: Offers both a graphical interface and command-line tools.
- **Multi-Cluster Support**: Manages applications across multiple Kubernetes clusters.

This tutorial will guide you through setting up Argo CD, deploying a sample application, and exploring its core functionalities.

---

## Prerequisites

- A Kubernetes cluster (e.g., Minikube, Kind, or a cloud provider like GKE/EKS). For this tutorial, I’ll use Minikube.
- `kubectl` installed and configured to access your cluster.
- Helm 3 installed (optional, for Helm-based installation).
- Git installed locally and access to a Git repository (e.g., GitHub).
- Basic understanding of Kubernetes resources (pods, deployments, services).

---

## Step 1: Install Argo CD

Argo CD can be installed using raw YAML manifests or Helm. We’ll use the YAML method for simplicity, then explore Helm later.

### Install Argo CD with YAML
1. **Create a Namespace**:
   Argo CD runs in its own namespace, typically `argocd`.
   ```bash
   kubectl create namespace argocd
   ```

2. **Apply the Installation Manifest**:
   Download and apply the official manifests from the Argo CD GitHub repository:
   ```bash
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
   This deploys:
   - The Argo CD API server.
   - Application controller.
   - Repository server.
   - Redis for caching.
   - RBAC and CRDs.

3. **Verify Installation**:
   Check the pods in the `argocd` namespace:
   ```bash
   kubectl get pods -n argocd
   ```
   You should see pods like:
   - `argocd-server-xxxxx`
   - `argocd-application-controller-xxxxx`
   - `argocd-repo-server-xxxxx`
   - `argocd-redis-xxxxx`

### Install the Argo CD CLI
The CLI enhances interaction with Argo CD. Install it based on your OS:
- **macOS (via Homebrew)**:
  ```bash
  brew install argocd
  ```
- **Linux/Windows**:
  Download the binary from the [releases page](https://github.com/argoproj/argo-cd/releases) and add it to your PATH:
  ```bash
  curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
  chmod +x argocd
  sudo mv argocd /usr/local/bin/
  ```

Verify:
```bash
argocd version --client
```

---

## Step 2: Access the Argo CD Web UI

By default, the Argo CD API server isn’t exposed externally. Use port-forwarding to access it locally.

1. **Port-Forward the Server**:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```

2. **Get the Admin Password**:
   Argo CD generates an initial admin password stored in a secret:
   ```bash
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   ```
   Copy the output (e.g., `abcd1234`).

3. **Log In to the Web UI**:
   Open your browser to `https://localhost:8080`. Accept the self-signed certificate warning (it’s safe for local use).
   - Username: `admin`
   - Password: The value from the previous step.

   You’ll see the Argo CD dashboard, which is empty until we add applications.

4. **Log In via CLI** (Optional):
   ```bash
   argocd login localhost:8080 --username admin --password <your-password> --insecure
   ```

---

## Step 3: Deploy a Sample Application

We’ll deploy a simple Nginx application from a Git repository using Argo CD.

### Prepare the Git Repository
1. **Create a Repository**:
   Use an existing GitHub repository or create a new one. For this tutorial, we’ll use a public example repo: `https://github.com/argoproj/argocd-example-apps.git`.

   The `guestbook` directory in this repo contains a basic Nginx deployment:
   - `deployment.yaml`
   - `service.yaml`

2. **Inspect the Manifests** (Optional):
   Clone the repo locally to explore:
   ```bash
   git clone https://github.com/argoproj/argocd-example-apps.git
   cd argocd-example-apps/guestbook
   ```
   - `deployment.yaml`: Defines an Nginx deployment with 2 replicas.
   - `service.yaml`: Exposes Nginx on port 80.

### Define the Application in Argo CD
1. **Create an Application**:
   Use the CLI to define an application that syncs the `guestbook` manifests to your cluster:
   ```bash
   argocd app create guestbook \
     --repo https://github.com/argoproj/argocd-example-apps.git \
     --path guestbook \
     --dest-server https://kubernetes.default.svc \
     --dest-namespace default
   ```
   - `--repo`: Git repository URL.
   - `--path`: Directory containing manifests.
   - `--dest-server`: Kubernetes API server (default for the local cluster).
   - `--dest-namespace`: Target namespace.

2. **Sync the Application**:
   Manually trigger the sync to deploy the app:
   ```bash
   argocd app sync guestbook
   ```

3. **Verify Deployment**:
   Check the resources in the `default` namespace:
   ```bash
   kubectl get pods,svc -n default
   ```
   You’ll see an Nginx deployment and service running.

4. **View in the Web UI**:
   Refresh `https://localhost:8080`. The `guestbook` app appears as a tile. Click it to see a visual representation of the deployment and service, including sync status and health.

---

## Step 4: Automate Syncing and Self-Healing

Argo CD can automatically sync changes and correct drift.

### Enable Auto-Sync
1. **Update the Application**:
   Edit the `guestbook` app to enable auto-sync:
   ```bash
   argocd app set guestbook --sync-policy automated
   ```
   - `automated`: Syncs whenever Git changes are detected.
   Add pruning and self-healing:
   ```bash
   argocd app set guestbook --auto-prune --self-heal
   ```
   - `--auto-prune`: Deletes resources no longer in Git.
   - `--self-heal`: Reverts manual changes to match Git.

2. **Test Auto-Sync**:
   Fork the `argocd-example-apps` repo, modify `guestbook/deployment.yaml` (e.g., change `replicas: 2` to `replicas: 3`), and push the change. Update the app to use your fork:
   ```bash
   argocd app set guestbook --repo <your-fork-url>
   ```
   Wait a minute—Argo CD will detect the change and update the cluster automatically.

3. **Test Self-Healing**:
   Manually scale the deployment:
   ```bash
   kubectl scale deployment guestbook -n default --replicas=5
   ```
   Argo CD will revert it to 3 within moments due to self-healing.

---

## Step 5: Use Helm with Argo CD (Optional)

Argo CD supports Helm Charts for templated deployments.

1. **Create a Helm Chart**:
   Use the `helm-guestbook` example from the same repo:
   ```bash
   argocd app create helm-guestbook \
     --repo https://github.com/argoproj/argocd-example-apps.git \
     --path helm-guestbook \
     --dest-server https://kubernetes.default.svc \
     --dest-namespace default \
     --helm-set replicaCount=2
   ```

2. **Sync the Helm App**:
   ```bash
   argocd app sync helm-guestbook
   ```

3. **Verify**:
   ```bash
   kubectl get pods -n default -l app=helm-guestbook
   ```

---

## Step 6: Monitor and Manage

### Web UI Features
- **Sync Status**: Green (in sync) or yellow (out of sync).
- **History and Rollback**: Click “History and Rollback” to view past syncs and revert to a previous state.
- **Logs**: View pod logs directly in the UI.

### CLI Commands
- List apps:
  ```bash
  argocd app list
  ```
- Get app details:
  ```bash
  argocd app get guestbook
  ```
- Delete an app:
  ```bash
  argocd app delete guestbook
  ```

---

## Step 7: Clean Up

1. **Remove the Application**:
   ```bash
   argocd app delete guestbook
   argocd app delete helm-guestbook
   ```

2. **Uninstall Argo CD**:
   ```bash
   kubectl delete -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   kubectl delete namespace argocd
   ```

---

## Conclusion

In this tutorial, you’ve installed Argo CD, deployed a sample Nginx application using GitOps, enabled automation, and explored Helm integration. Argo CD simplifies Kubernetes deployments by keeping your cluster in sync with Git, offering visibility through its UI, and automating operational tasks. You can extend this setup by:
- Managing multiple clusters.
- Integrating with CI tools (e.g., GitHub Actions).
- Adding RBAC for team access.

