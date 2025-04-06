# Introduction to Docker Compose

Welcome to the fourteenth tutorial in our **Dapr Agentic Cloud Ascent (DACA)** series! In this tutorial, we’ll explore **Docker Compose**, a tool for defining and running multi-container Docker applications using YAML files. We’ll set aside our DACA example for now and focus solely on understanding Docker Compose through explanations, concepts, and a practical example. We’ll build a simple FastAPI web application that connects to a PostgreSQL database, demonstrating how Docker Compose simplifies managing multi-container applications. This will prepare us for the next tutorial (**15_dapr_docker_compose**), where we’ll apply Docker Compose to our DACA microservices with Dapr. Let’s dive in!

---

## What You’ll Learn
- What Docker Compose is and why it’s used for multi-container applications.
- The core concepts of Docker Compose (e.g., services, networks, volumes, `docker-compose.yml`).
- How to define a multi-container application using a `docker-compose.yml` file.
- Practical example of using Docker Compose to run a FastAPI web application with a PostgreSQL database.
- Key Docker Compose commands and workflows.

## Prerequisites
- Completion of **12_docker_and_desktop** (understanding of Docker, Docker Desktop, and containerization concepts).
- Docker and Docker Desktop installed (from **12_docker_and_desktop**).
- Basic familiarity with the command line (e.g., terminal on macOS/Linux, Command Prompt/PowerShell on Windows).
- No prior Docker Compose experience is required—we’ll start from the basics!

---

## Step 1: What is Docker Compose?
**Docker Compose** is a tool for defining and running multi-container Docker applications using YAML files. It allows you to define all the components of your application (e.g., services, networks, volumes) in a single `docker-compose.yml` file and manage them with simple commands like `docker-compose up` and `docker-compose down`.

### Why Use Docker Compose?
Docker Compose simplifies the process of managing multi-container applications by:
- **Centralized Configuration**: Define all services, networks, and volumes in one YAML file, making it easy to understand and manage the application’s architecture.
- **Simplified Commands**: Start, stop, and manage all containers with a single command (e.g., `docker-compose up`), instead of running multiple `docker run` commands.
- **Dependency Management**: Automatically handles dependencies between containers (e.g., starting a database before a web app that depends on it).
- **Networking**: Creates a default network for your services, allowing them to communicate with each other using service names as hostnames.
- **Development Efficiency**: Ideal for local development and testing, as it provides a reproducible environment for multi-container applications.

### Docker Compose vs. Docker
- **Docker**: Manages individual containers (e.g., `docker run`, `docker build`).
- **Docker Compose**: Manages multiple containers as a single application (e.g., `docker-compose up`).

**Analogy**: Think of Docker as a chef preparing individual dishes (containers). Docker Compose is like a restaurant manager who coordinates multiple dishes (services) to serve a complete meal (application).

---

## Step 2: Core Concepts of Docker Compose
Docker Compose revolves around a few key concepts:

### 2.1 Services
A **service** represents a containerized application component defined in the `docker-compose.yml` file. Each service typically corresponds to a container and is configured with:
- An image (e.g., `nginx`, `postgres`).
- Ports to expose.
- Environment variables.
- Volumes for persistent data.
- Dependencies on other services.

Example: A web application might have two services: a `web` service (e.g., a FastAPI app) and a `db` service (e.g., PostgreSQL).

### 2.2 Networks
Docker Compose automatically creates a default **network** for your application, allowing services to communicate with each other using their service names as hostnames. For example, a `web` service can connect to a `db` service by using the hostname `db`.

You can also define custom networks in the `docker-compose.yml` file if needed.

### 2.3 Volumes
**Volumes** provide persistent storage for containers. Docker Compose allows you to define volumes to persist data (e.g., database data) across container restarts. Volumes can be:
- **Named Volumes**: Managed by Docker (e.g., `myapp-data`).
- **Bind Mounts**: Map a host directory to a container directory (e.g., for sharing code during development).

### 2.4 The `docker-compose.yml` File
The `docker-compose.yml` file is the heart of Docker Compose. It defines:
- The services (containers) in your application.
- The networks they use.
- The volumes for persistent storage.
- Other configurations (e.g., environment variables, port mappings).

Example `docker-compose.yml`:
```yaml
version: "3.9"
services:
  web:
    image: my-web-app
    ports:
      - "5000:5000"
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

### 2.5 Docker Compose CLI
The `docker-compose` command-line tool is used to manage the application defined in the `docker-compose.yml` file. Common commands include:
- `docker-compose up`: Starts all services defined in the YAML file.
- `docker-compose down`: Stops and removes all services, networks, and volumes.
- `docker-compose ps`: Lists the running services.
- `docker-compose logs`: Views logs from all services.

---

## Step 3: Practical Example – Running a FastAPI App with a Database
Let’s create a simple multi-container application using Docker Compose: a FastAPI web app that connects to a PostgreSQL database. This example will demonstrate how Docker Compose simplifies running and managing multiple containers.

### Step 3.1: Set Up the Project
Create a directory for the example:
```bash
mkdir fastapi-postgres-app
cd fastapi-postgres-app
```

### Step 3.2: Create the FastAPI App
Create a file `app.py` for the FastAPI app:
```python
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import HTMLResponse

app = FastAPI()

# Database connection configuration
def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # Service name of the PostgreSQL container
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    return conn

# Initialize the database with a table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, content TEXT);")
    conn.commit()
    cur.close()
    conn.close()

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def index():
    # Add a sample message to the database
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO messages (content) VALUES (%s) RETURNING id;", ("Hello from FastAPI!",))
    message = cur.fetchone()
    message_id = message["id"]
    conn.commit()

    # Retrieve all messages
    cur.execute("SELECT content FROM messages;")
    messages = cur.fetchall()
    cur.close()
    conn.close()

    # Format the response as HTML
    messages_list = ", ".join(msg["content"] for msg in messages)
    return f"<h1>Message ID {message_id} added.</h1><p>All messages: {messages_list}</p>"
```

#### Explanation of the FastAPI App
- We use **FastAPI** to create a simple web application.
- The app connects to a PostgreSQL database using `psycopg2`.
- On startup (`@app.on_event("startup")`), it initializes the database by creating a `messages` table.
- The `/` endpoint:
  - Inserts a new message ("Hello from FastAPI!") into the database.
  - Retrieves all messages and displays them in an HTML response.
- We use `RealDictCursor` to get query results as dictionaries for easier access to column names.

Create a `requirements.txt` file:
```
fastapi==0.110.0
uvicorn==0.29.0
psycopg2-binary==2.9.6
```

#### Explanation of Dependencies
- `fastapi==0.110.0`: The FastAPI framework (version 0.110.0 as of April 2025; adjust if needed).
- `uvicorn==0.29.0`: An ASGI server to run the FastAPI app (version 0.29.0 as of April 2025).
- `psycopg2-binary==2.9.6`: A PostgreSQL adapter for Python.

### Step 3.3: Create a Dockerfile for the FastAPI App
Create a `Dockerfile` in the `fastapi-postgres-app` directory:
```dockerfile
# Use a base image with Python 3.9
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 5000

# Define the command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

#### Explanation of the Dockerfile
- `FROM python:3.9-slim`: Uses a lightweight Python 3.9 image.
- `WORKDIR /app`: Sets the working directory to `/app`.
- `COPY requirements.txt .`: Copies the `requirements.txt` file.
- `RUN pip install --no-cache-dir -r requirements.txt`: Installs the dependencies.
- `COPY . .`: Copies the application code (e.g., `app.py`).
- `EXPOSE 5000`: Documents that the app runs on port `5000`.
- `CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]`: Runs the FastAPI app using Uvicorn.

### Step 3.4: Create the `docker-compose.yml` File
Create a `docker-compose.yml` file in the `fastapi-postgres-app` directory:
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - PYTHONUNBUFFERED=1
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
volumes:
  db-data:
```

#### Explanation of the `docker-compose.yml`
- `version: "3.9"`: Specifies the Docker Compose file format version.
- `services`:
  - `web`:
    - `build: .`: Builds the image from the `Dockerfile` in the current directory.
    - `ports: - "5000:5000"`: Maps port `5000` on the host to port `5000` in the container.
    - `depends_on: - db`: Ensures the `db` service starts before the `web` service.
    - `environment: - PYTHONUNBUFFERED=1`: Ensures Python output is unbuffered for better logging.
  - `db`:
    - `image: postgres:13`: Uses the official PostgreSQL 13 image.
    - `environment`: Sets PostgreSQL configuration (username, password, database name).
    - `volumes: - db-data:/var/lib/postgresql/data`: Persists PostgreSQL data in a named volume.
    - `ports: - "5432:5432"`: Exposes the PostgreSQL port for external access (e.g., for debugging).
- `volumes`:
  - `db-data`: Defines a named volume to persist the database data.

### Step 3.5: Run the Application with Docker Compose
Start the application:
```bash
docker-compose up -d
```
- `-d`: Runs the containers in detached mode (in the background).

Output:
```
Creating network "fastapi-postgres-app_default" with the default driver
Creating volume "fastapi-postgres-app_db-data" with default driver
Building web
Step 1/6 : FROM python:3.9-slim
 ---> abc123def456
Step 2/6 : WORKDIR /app
 ---> Using cache
 ---> 123abc456def
Step 3/6 : COPY requirements.txt .
 ---> 456def789xyz
Step 4/6 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in def123abc456
Collecting fastapi==0.110.0
  Downloading fastapi-0.110.0-py3-none-any.whl (92 kB)
Collecting uvicorn==0.29.0
  Downloading uvicorn-0.29.0-py3-none-any.whl (60 kB)
Collecting psycopg2-binary==2.9.6
  Downloading psycopg2_binary-2.9.6-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
...
Successfully installed fastapi-0.110.0 uvicorn-0.29.0 psycopg2-binary-2.9.6 ...
 ---> 789xyz123abc
Step 5/6 : COPY . .
 ---> 123xyz456abc
Step 6/6 : EXPOSE 5000
 ---> Running in 456abc789def
 ---> def123abc789
Step 7/7 : CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
 ---> Running in abc123xyz456
 ---> 456xyz789def
Successfully built 456xyz789def
Successfully tagged fastapi-postgres-app_web:latest
Creating fastapi-postgres-app_db_1 ... done
Creating fastapi-postgres-app_web_1 ... done
```

### Step 3.6: Verify the Application is Running
List the running containers:
```bash
docker-compose ps
```
Output:
```
         Name                        Command               State           Ports         
---------------------------------------------------------------------------------------
fastapi-postgres-app_db_1    docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp
fastapi-postgres-app_web_1   uvicorn app:app --host 0.0. ...  Up      0.0.0.0:5000->5000/tcp
```

Access the FastAPI app at `http://localhost:5000`. You should see:
```html
<h1>Message ID 1 added.</h1><p>All messages: Hello from FastAPI!</p>
```

Refresh the page a few times, and the output will update:
```html
<h1>Message ID 2 added.</h1><p>All messages: Hello from FastAPI!, Hello from FastAPI!</p>
```

#### What Happened?
- `docker-compose up`:
  - Built the `web` service image from the `Dockerfile`.
  - Pulled the `postgres:13` image for the `db` service.
  - Created a default network (`fastapi-postgres-app_default`) for the services to communicate.
  - Created a named volume (`fastapi-postgres-app_db-data`) for the database.
  - Started both containers (`web` and `db`).
- The `web` service connected to the `db` service using the hostname `db` (the service name).
- The FastAPI app created a table, inserted messages, and retrieved them from the database.

### Step 3.7: View Logs
Check the logs for both services:
```bash
docker-compose logs
```
Output:
```
fastapi-postgres-app_db_1   | 2025-04-06 04:01:00.123 UTC [1] LOG:  starting PostgreSQL 13.3 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 10.2.1 20210110, 64-bit
fastapi-postgres-app_db_1   | 2025-04-06 04:01:00.123 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
fastapi-postgres-app_db_1   | 2025-04-06 04:01:00.456 UTC [1] LOG:  database system is ready to accept connections
fastapi-postgres-app_web_1  | INFO:     Started server process [1]
fastapi-postgres-app_web_1  | INFO:     Waiting for application startup.
fastapi-postgres-app_web_1  | INFO:     Application startup complete.
fastapi-postgres-app_web_1  | INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
fastapi-postgres-app_web_1  | INFO:     172.18.0.1:12345 - "GET / HTTP/1.1" 200 OK
```

### Step 3.8: Stop and Clean Up
Stop and remove the containers, networks, and volumes:
```bash
docker-compose down -v
```
- `-v`: Removes the named volumes (e.g., `db-data`).

Output:
```
Stopping fastapi-postgres-app_web_1 ... done
Stopping fastapi-postgres-app_db_1  ... done
Removing fastapi-postgres-app_web_1 ... done
Removing fastapi-postgres-app_db_1  ... done
Removing network fastapi-postgres-app_default
Removing volume fastapi-postgres-app_db-data
```

#### Verify Cleanup
```bash
docker-compose ps
```
Output:
```
Name   Command   State   Ports
-------------------------------
```
No containers should be running.

---

## Step 4: Key Docker Compose Commands
Here are some essential Docker Compose commands to know:

- **Starting and Stopping**:
  - `docker-compose up`: Starts all services (add `-d` for detached mode).
  - `docker-compose down`: Stops and removes all services, networks, and volumes (add `-v` to remove volumes).
  - `docker-compose start`: Starts existing containers.
  - `docker-compose stop`: Stops running containers without removing them.

- **Building and Managing**:
  - `docker-compose build`: Builds or rebuilds service images.
  - `docker-compose ps`: Lists running services.
  - `docker-compose logs`: Views logs from all services (add `--follow` to stream logs).

- **Interacting with Services**:
  - `docker-compose exec <service> <command>`: Runs a command in a running service container (e.g., `docker-compose exec web bash`).
  - `docker-compose run <service> <command>`: Runs a one-off command in a new container for the service (e.g., `docker-compose run web python --version`).

---

## Step 5: Why Docker Compose for DACA?
Docker Compose will be critical for our DACA project in the next tutorial because:
- **Multi-Container Management**: We have multiple components (Chat Service, Analytics Service, Dapr sidecars, Redis, Zipkin, Prometheus) that need to run together.
- **Simplified Development**: Docker Compose allows us to start all components with a single command, making local development and testing easier.
- **Networking**: Docker Compose’s default network enables seamless communication between services (e.g., Chat Service to Analytics Service via Dapr).
- **Reproducibility**: The `docker-compose.yml` file ensures the application can be consistently reproduced across environments.

In the next tutorial (**15_dapr_docker_compose**), we’ll use Docker Compose to define and run our DACA microservices with Dapr, building on the concepts we’ve learned here.

---

## Step 6: Next Steps
You’ve gained a foundational understanding of Docker Compose and how to use it to manage multi-container applications! In the next tutorial (**15_dapr_docker_compose**), we’ll return to our DACA example and use Docker Compose to define and run the Chat Service, Analytics Service, Dapr sidecars, and supporting services (Redis, Zipkin, Prometheus).

### Exercises for Students
1. Add a third service to the `docker-compose.yml` file (e.g., a Redis cache) and modify the FastAPI app to use it.
2. Use `docker-compose exec` to connect to the PostgreSQL container and inspect the database (e.g., `docker-compose exec db psql -U myuser -d mydb`).
3. Define a custom network in the `docker-compose.yml` file and assign services to it.

---

## Conclusion
In this tutorial, we introduced Docker Compose, explored its core concepts, and walked through a practical example of running a FastAPI web app with a PostgreSQL database. You now have the knowledge needed to apply Docker Compose to our DACA microservices in the next tutorial. We’re ready to move on to **15_dapr_docker_compose**!

---

### Final Code for `fastapi-postgres-app/app.py`
```python
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.responses import HTMLResponse

app = FastAPI()

# Database connection configuration
def get_db_connection():
    conn = psycopg2.connect(
        host="db",  # Service name of the PostgreSQL container
        database="mydb",
        user="myuser",
        password="mypassword"
    )
    return conn

# Initialize the database with a table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, content TEXT);")
    conn.commit()
    cur.close()
    conn.close()

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def index():
    # Add a sample message to the database
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO messages (content) VALUES (%s) RETURNING id;", ("Hello from FastAPI!",))
    message = cur.fetchone()
    message_id = message["id"]
    conn.commit()

    # Retrieve all messages
    cur.execute("SELECT content FROM messages;")
    messages = cur.fetchall()
    cur.close()
    conn.close()

    # Format the response as HTML
    messages_list = ", ".join(msg["content"] for msg in messages)
    return f"<h1>Message ID {message_id} added.</h1><p>All messages: {messages_list}</p>"
```

### Final Code for `fastapi-postgres-app/requirements.txt`
```
fastapi==0.110.0
uvicorn==0.29.0
psycopg2-binary==2.9.6
```

### Final Code for `fastapi-postgres-app/Dockerfile`
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Final Code for `fastapi-postgres-app/docker-compose.yml`
```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - PYTHONUNBUFFERED=1
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
volumes:
  db-data:
```

---

