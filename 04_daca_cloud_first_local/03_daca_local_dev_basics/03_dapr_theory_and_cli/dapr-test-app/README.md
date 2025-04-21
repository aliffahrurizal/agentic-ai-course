# Installing the Dapr CLI And Run with FastAPI Hello World

The **Dapr CLI** is the primary tool for interacting with Dapr, allowing you to initialize Dapr, run applications with Dapr sidecars, manage components, and more. Let’s install and set up the Dapr CLI.

### [Install the Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/)

#### On macOS/Linux

```bash
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
```

#### On Windows (PowerShell)

```powershell
powershell -Command "iwr -useb https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 | iex"
```

#### Verify Installation

Check the Dapr CLI version:

```bash
dapr --version
```

Output:

```
CLI version: 1.15.0
Runtime version: n/a
```

### Install the Dapr Runtime

The Dapr CLI requires the Dapr runtime to be installed on your system. This includes the Dapr sidecar and its dependencies (e.g., Redis for default components).

#### [Initialize Dapr](https://docs.dapr.io/getting-started/install-dapr-selfhost/)

Run the following command to initialize Dapr:

```bash
dapr init
```

This command:

- Downloads and installs the Dapr runtime binaries.
- Sets up a default Redis container for state and pub/sub components.
- Configures default component files in `~/.dapr/components/`.

Output:

```
⌚  Making the jump to hyperspace...
ℹ  Installing runtime version 1.13.1
⬇  Downloading binaries and setting up components...
✅  Success! Dapr has been installed to /usr/local/bin. To get started, please visit https://docs.dapr.io/getting-started/
ℹ  Container images for Dapr have been pulled to your local machine
ℹ  Dapr control plane has been initialized in your local environment
ℹ  Note: To verify that Dapr has been installed properly, restart your terminal session
```

#### Verify Dapr Runtime

Check the Dapr runtime version:

```bash
dapr --version
```

Output:

```
CLI version: 1.13.1
Runtime version: 1.13.1
```

Check that the Dapr Redis container is running:

```bash
nerdctl ps
```

You should see a container named `dapr_redis` running on port `6379`.

### 3. `dapr run`

- **Purpose**: Runs an application with a Dapr sidecar.
- **Usage**:
  ```bash
  dapr run --app-id <app-id> --app-port <port> --dapr-http-port <dapr-port> -- <command>
  ```
- **Options**:
  - `--app-id`: A unique identifier for your application.
  - `--app-port`: The port your app listens on.
  - `--dapr-http-port`: The port for the Dapr sidecar’s HTTP API.
  - `<command>`: The command to run your app (e.g., `uvicorn main:app`).

Run the app with Dapr:

```bash
dapr run --app-id test-app --app-port 8000 --dapr-http-port 3500 -- uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

- `test-app` is the app ID.
- `8000` is the app port.
- `3500` is the Dapr sidecar port (default for Dapr’s HTTP API).

Output:

```
== APP == INFO:     Started server process [12345]
== APP == INFO:     Waiting for application startup.
== APP == INFO:     Application startup complete.
== APP == INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
ℹ  Starting Dapr with id test-app. HTTP Port: 3500  gRPC Port: 50001
✅  You're up and running! Both Dapr and your app logs will appear here.
```

Visit `http://localhost:8000/` to confirm the app is running:

```json
{ "message": "Hello from Dapr Test App!" }
```

---

### 4. `dapr dashboard`

- **Purpose**: Opens the Dapr dashboard, a web UI for monitoring Dapr applications.
- **Usage**:
  ```bash
  dapr dashboard
  ```
- **What It Does**:
  - Starts a web server (default port `8080`).
  - Provides a UI to view running Dapr apps, components, and logs.

#### Example: Open the Dapr Dashboard

While the test app is running, open a new terminal and run:

```bash
dapr dashboard
```

Output:

```
ℹ  Starting Dapr Dashboard on http://localhost:8080
```

Visit `http://localhost:8080` in your browser. You’ll see:

- The `test-app` application with its Dapr sidecar.
- Configured components (e.g., Redis for state and pub/sub).
- Logs and health status.

---
