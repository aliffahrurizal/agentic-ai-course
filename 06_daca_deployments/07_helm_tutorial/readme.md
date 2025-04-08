# Helm Tutorial

Below is a detailed tutorial on Helm, the package manager for Kubernetes. This tutorial will cover what Helm is, why it’s useful, how to install it, and how to use it to deploy applications on a Kubernetes cluster. We have broken it down into clear sections for beginners and intermediate users alike.

---

### What is Helm?

Helm is a tool that simplifies the deployment and management of applications on Kubernetes. Think of it as a "package manager" for Kubernetes, similar to how `apt` works for Ubuntu or `npm` for Node.js. Helm uses pre-configured packages called **charts**, which are collections of Kubernetes resource manifests (e.g., Deployments, Services, ConfigMaps) bundled together with customizable variables.

#### Key Concepts
1. **Chart**: A Helm package that contains all the resource definitions needed to run an application, along with a `values.yaml` file for configuration.
2. **Release**: An instance of a chart deployed to a Kubernetes cluster.
3. **Repository**: A place where charts are stored and shared (e.g., Artifact Hub).
4. **Tiller**: The server-side component of Helm (used in Helm 2 but removed in Helm 3 in favor of a client-only architecture).

Helm 3 (the current version) is widely adopted due to its simplicity and improved security over Helm 2.

---

### Why Use Helm?

- **Simplifies Deployment**: Instead of manually applying dozens of YAML files, Helm lets you deploy an app with a single command.
- **Reusability**: Charts can be templated and reused across environments (e.g., dev, staging, prod).
- **Versioning**: Helm tracks releases, allowing you to roll back or upgrade applications easily.
- **Community Support**: Thousands of pre-built charts are available for popular software (e.g., Nginx, MySQL, Prometheus).

---

### Prerequisites

Before starting, ensure you have:
1. A Kubernetes cluster (e.g., Minikube for local testing or a cloud provider like GKE, EKS, or AKS).
2. `kubectl` installed and configured to communicate with your cluster.
3. Basic familiarity with Kubernetes concepts (Pods, Deployments, Services).

---

### Step 1: Install Helm

#### On macOS (using Homebrew)
```bash
brew install helm
```

#### On Linux (using a script)
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh
```

#### On Windows (using Chocolatey)
```powershell
choco install kubernetes-helm
```

#### Verify Installation
Run the following to check the Helm version:
```bash
helm version
```
Output should look like: `version.BuildInfo{Version:"v3.x.x", ...}`.

---

### Step 2: Set Up a Kubernetes Cluster (Optional)

If you don’t have a cluster, use Minikube for local testing:
```bash
minikube start
```
Verify `kubectl` is working:
```bash
kubectl get nodes
```

---

### Step 3: Explore Helm Commands

Here are some basic Helm commands to get started:
- `helm search hub <keyword>`: Search for charts in Artifact Hub.
- `helm repo add <name> <url>`: Add a chart repository.
- `helm install <release-name> <chart>`: Deploy a chart.
- `helm list`: List all releases in the current namespace.
- `helm upgrade <release-name> <chart>`: Update a release.
- `helm rollback <release-name> <revision>`: Roll back to a previous release.
- `helm uninstall <release-name>`: Delete a release.

---

### Step 4: Deploy Your First Application

Let’s deploy a simple Nginx web server using a Helm chart.

#### 1. Add a Chart Repository
Add the Bitnami repository, which hosts many popular charts:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

#### 2. Search for the Nginx Chart
```bash
helm search repo nginx
```
Look for `bitnami/nginx` in the output.

#### 3. Install the Nginx Chart
Deploy Nginx with the release name `my-nginx`:
```bash
helm install my-nginx bitnami/nginx
```
Helm will output details about the deployment, including how to access it.

#### 4. Verify the Deployment
Check the pods:
```bash
kubectl get pods
```
You should see a pod like `my-nginx-xxxxx`.

#### 5. Access Nginx
The chart creates a Service. Expose it locally with Minikube:
```bash
minikube service my-nginx
```
This opens your browser to the Nginx welcome page.

---

### Step 5: Customize a Chart

Charts are customizable via the `values.yaml` file or command-line overrides.

#### Example: Customize Nginx
1. Inspect the default values:
```bash
helm show values bitnami/nginx
```
2. Create a custom `my-values.yaml` file:
```yaml
replicaCount: 2
service:
  type: LoadBalancer
```
3. Install with custom values:
```bash
helm install my-nginx -f my-values.yaml bitnami/nginx
```
This deploys Nginx with 2 replicas and a LoadBalancer service.

#### Alternative: Inline Overrides
```bash
helm install my-nginx bitnami/nginx --set replicaCount=2,service.type=LoadBalancer
```

---

### Step 6: Manage Releases

#### List Releases
```bash
helm list
```

#### Upgrade a Release
If the chart or values change:
```bash
helm upgrade my-nginx bitnami/nginx --set replicaCount=3
```

#### Roll Back a Release
Check revision history:
```bash
helm history my-nginx
```
Roll back to revision 1:
```bash
helm rollback my-nginx 1
```

#### Uninstall a Release
```bash
helm uninstall my-nginx
```

---

### Step 7: Create Your Own Helm Chart

#### 1. Generate a Chart
```bash
helm create my-chart
```
This creates a directory `my-chart/` with:
- `Chart.yaml`: Metadata about the chart.
- `values.yaml`: Default configuration values.
- `templates/`: Kubernetes manifests with templating.

#### 2. Edit the Chart
Modify `values.yaml`:
```yaml
replicaCount: 1
image:
  repository: nginx
  tag: "latest"
```
Update `templates/deployment.yaml` to use these values (it’s pre-populated with Helm templating).

#### 3. Test the Chart
Dry-run to preview the rendered YAML:
```bash
helm install my-release ./my-chart --dry-run --debug
```

#### 4. Install the Chart
```bash
helm install my-release ./my-chart
```

---

### Step 8: Best Practices

- **Version Control**: Store charts in Git for collaboration.
- **Namespace Management**: Use `--namespace <name>` to isolate releases.
- **Secrets**: Avoid hardcoding sensitive data; integrate with tools like Kubernetes Secrets or external secret managers.
- **Lint Charts**: Run `helm lint ./my-chart` to catch errors.

---

### Troubleshooting

- **Pods Not Starting**: Check logs with `kubectl logs <pod-name>`.
- **Chart Not Found**: Ensure `helm repo update` is run.
- **Permission Issues**: Verify `kubectl` context and RBAC settings.

---

### Next Steps

- Explore advanced templating with Helm’s Go-based syntax.
- Package and share your chart on a repository like Artifact Hub.
- Integrate Helm with CI/CD pipelines (e.g., GitHub Actions).

---

That’s it! You now have a solid foundation for using Helm to manage Kubernetes applications. 