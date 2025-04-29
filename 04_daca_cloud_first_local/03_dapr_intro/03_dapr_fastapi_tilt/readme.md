# Add Hot Reloading for Cloud-Native Local Development (using Tilt)

### What’s Happening?

We have deployed the Dapr infrastructure (Control Plane, Dashboard, Redis, Components) in our Kubernetes cluster (Rancher Desktop) using Helm and `kubectl apply` (from Document 01). We have also set up our FastAPI project with the application code, Dockerfile, and Kubernetes manifests (from Document 02).

Now, we need an efficient way to develop our FastAPI application with rapid iteration and hot-reloading, while keeping the application running within Kubernetes alongside its Dapr sidecar and components. 

The standard cloud-native approach for this kind of rapid development loop in Kubernetes is to use a tool that watches your local filesystem and syncs code changes into the running container. We will use **Tilt** to achieve this. Tilt will automate building the development image, deploying your application to Kubernetes, and crucially, syncing your local code changes into the running pod to trigger FastAPI's hot-reloading (via Uvicorn's `--reload` flag).

This setup aligns with the DACA principle of developing within a production-like (containerized, Kubernetes-based) environment from Stage 1.

### Prerequisites

*   You have completed all steps in Document 01 (Dapr Control Plane, Dashboard, Redis, Dapr Components deployed in Kubernetes).
*   You have completed Steps 1 and 2 in Document 02 (Project setup, `main.py`, `Dockerfile`, `.dockerignore`, `kubernetes/deployment.yaml`, `kubernetes/service.yaml` created).
*   Your Kubernetes cluster (Rancher Desktop) is running.
*   Ensure you are in the root directory of your `hello_dapr_fastapi` project.

### 1. Install Tilt

Tilt is a command-line tool and a local server with a UI. Install it on your local machine.

*   **macOS (Homebrew):**
    ```bash
    brew install tilt
    ```
*   **Windows (Chocolatey):**
    ```bash
    choco install tilt
    ```
*   **Linux:**
    ```bash
    curl -fsSL https://run.tilt.dev/install.sh | bash
    ```
*   **Other methods:** See the [official Tilt installation guide](https://docs.tilt.dev/install.html).

Verify installation:
```bash
tilt version
```

### 2. Modify Dockerfile for Development

For hot-reloading to work inside the container using Uvicorn, the `CMD` instruction must include the `--reload` flag.

Open your `Dockerfile` (created in Document 02) and modify the `CMD` line:

```dockerfile
# ... other layers from Document 02 Dockerfile
EXPOSE 8000
# Original: CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Modified for Development Hot-reloading:
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Note:** This `Dockerfile` with `--reload` is optimized for your *development* workflow with Tilt. When you move to subsequent DACA deployment stages (prototyping, production), you will typically use a `Dockerfile` *without* the `--reload` flag for stability and performance in non-development environments. Tilt builds a *development image* based on this modified Dockerfile.

### 3. Create the Tiltfile

The `Tiltfile` tells Tilt how to build, deploy, and manage your application for development. Create a file named `Tiltfile` in the root of your `hello_dapr_fastapi` project directory.

Add the following content to `Tiltfile`:

```python
# Tiltfile for Dapr FastAPI Hot-reloading Development

# Build the Docker image for development.
# Tilt will automatically watch local files (like the Dockerfile)
# and trigger rebuilds/redeployments if the build context changes.
# The `docker_build` command uses the Dockerfile in the current directory '.'
# and tags the image as 'dapr-fastapi-hello:latest'.
# Tilt caches layers efficiently.
docker_build('dapr-fastapi-hello', '.',
             dockerfile='Dockerfile')

# Deploy the Kubernetes resources defined in your manifests.
# Tilt will apply these manifests to your connected Kubernetes cluster (Rancher Desktop).
# It expects that Dapr and its components (Redis, statestore, pubsub, subscriptions)
# have already been deployed via Helm and kubectl apply (Document 01).
# Tilt focuses on deploying and managing *your* application and its sidecar.
k8s_resource('dapr-fastapi-hello',
             file=['kubernetes/deployment.yaml', 'kubernetes/service.yaml'])

# Configure live updates for code changes.
# This is the core of hot-reloading with Tilt.
# It tells Tilt to watch the local directory '.' and sync changes
# into the container named 'app' inside the pod to the path '/code'.
# When files in '.' change, Tilt will sync them to '/code' in the container.
# Uvicorn, running with '--reload' from the Dockerfile CMD, will detect
# these changes in '/code' and automatically restart the FastAPI application.
# This provides the hot-reloading experience.
live_update('dapr-fastapi-hello', # This references the k8s_resource defined above
            sync = ['.:/code'], # Sync local directory '.' to container path '/code'
            # Uncomment below if Uvicorn isn't detecting changes automatically
            # or you want Tilt to force a restart regardless of --reload flag.
            # restart_container = 'app' # Restart the 'app' container on sync
           )

# Configure port-forwarding for easy access to the application.
# This forwards local port 8000 to the service/deployment port 8000.
# Tilt's UI will show you the port-forwarding status and give you a link.
k8s_forward('dapr-fastapi-hello', 8000, 8000)

# Optional: Set resource dependencies if your app depends on others.
# In this case, our app needs the Dapr sidecar, which is deployed
# implicitly by the Dapr annotation on our deployment, and the Dapr components
# which are assumed to be running from Document 01.
# No explicit dependencies needed in this simple case.

# Define resource health checks (optional but good practice)
# For FastAPI, checking the root endpoint is a simple start.
# Tilt will report the health status in the UI.
# k8s_resource('dapr-fastapi-hello', ...) # Add this check inside the k8s_resource definition
# health_check = {"http": {"path": "/", "port": 8000}} # This should be part of the deployment or ingress, but Tilt can also define checks

# Let's simplify health check for Tiltfile:
# k8s_resource('dapr-fastapi-hello',
#              file=['kubernetes/deployment.yaml', 'kubernetes/service.yaml'],
#              extra_pod_selectors=['app=dapr-fastapi-hello'], # Ensure Tilt finds the right pod
#              probe_liveness = http_probe("http://localhost:8000/"), # Simple HTTP check for Tilt UI
#              probe_ready = http_probe("http://localhost:8000/")
#             )
# NOTE: The probe definition can get complex. For simplicity in this intro,
# we'll rely on K8s readiness/liveness probes if defined in the manifest,
# or just let Tilt show pod status. The above probes are Tiltfile-specific.
# Let's keep the k8s_resource definition simple as just file= for this tutorial.

```

**Explanation of the `Tiltfile`:**

*   `docker_build('dapr-fastapi-hello', '.', dockerfile='Dockerfile')`: Tells Tilt how to build a Docker image named `dapr-fastapi-hello` for development, using the `Dockerfile` in the current directory (`.`). Tilt is smart and will only rebuild if necessary.
*   `k8s_resource('dapr-fastapi-hello', file=['kubernetes/deployment.yaml', 'kubernetes/service.yaml'])`: Tells Tilt to deploy your application to Kubernetes using the specified manifest files. It assumes Dapr and its components are already there.
*   `live_update('dapr-fastapi-hello', sync = ['.:/code'])`: This is the key part! It configures Tilt to watch your local project directory (`.`) and automatically sync any file changes into the running container named `app` (as defined in your deployment.yaml) to the path `/code`. Since Uvicorn in your container is running with `--reload` and watching `/code`, it will pick up these changes and restart your FastAPI app.
*   `k8s_forward('dapr-fastapi-hello', 8000, 8000)`: Sets up port-forwarding automatically so you can access your app at `http://localhost:8000`.

### 4. Run Tilt

Now, start Tilt from your project root directory:

```bash
tilt up
```

Tilt will:
1.  Start its UI in your browser (usually at `http://localhost:10350`).
2.  Read your `Tiltfile`.
3.  Build your Docker image (or use a cached one).
4.  Deploy your Kubernetes manifests (`deployment.yaml`, `service.yaml`) to Rancher Desktop. This will create your app pod with the Dapr sidecar injected.
5.  Start watching your local filesystem for changes.
6.  Set up the port-forwarding.

Watch the Tilt UI. You should see your `dapr-fastapi-hello` resource, its logs (including the Dapr sidecar starting and your FastAPI app starting via Uvicorn), and the port-forwarding status. Wait until the resource is green (healthy).

### 5. Verify Hot Reloading

Now that Tilt is running and managing your application in Kubernetes:

1.  **Test the application:** Use `curl` exactly as described in Step 4 of your Document 02, but you don't need to run `kubectl port-forward` manually anymore; Tilt is handling it.
    ```bash
    curl http://localhost:8000/
    curl -X POST "http://localhost:8000/messages?user_id=testuser&message=hello" -H "Content-Type: application/json"
    curl http://localhost:8000/messages/testuser
    ```
    Check the logs in the Tilt UI for your application container (`app`). You should see Uvicorn logs and the Pub/Sub `Received event` log when you store a message.

2.  **Test Hot Reloading:**
    *   Open your `main.py` file in your code editor.
    *   Modify the root endpoint slightly, e.g., change the message:
        ```python
        @app.get("/")
        async def root():
            return {"message": "Hello from Dapr FastAPI - UPDATED!"} # Added - UPDATED!
        ```
    *   Save the `main.py` file.
    *   Immediately look at the Tilt UI logs for your `dapr-fastapi-hello` resource, specifically the `app` container. You should see logs indicating that Tilt detected a file change, synced it, and Uvicorn restarted the application process.
    *   Test the root endpoint again:
        ```bash
        curl http://localhost:8000/
        ```
    *   Expected: `{"message": "Hello from Dapr FastAPI - UPDATED!"}`.

If you see Uvicorn restarting and the message change reflected, hot reloading is working correctly! Tilt is successfully syncing your local changes to the pod in Kubernetes, and Uvicorn is detecting them.

### 6. Stop and Clean Up Tilt Development Session

When you are finished with your development session:

1.  Go back to the terminal where you ran `tilt up`.
2.  Press `Ctrl+C`. Tilt will stop the process.
3.  To remove the resources Tilt deployed to Kubernetes:
    ```bash
    tilt down
    ```
    This will delete the deployment and service that Tilt created.

This completes the setup for cloud-native local development with hot-reloading using Tilt, fitting into your DACA Stage 1 workflow. You can now iterate rapidly on your FastAPI application while it runs in the ta