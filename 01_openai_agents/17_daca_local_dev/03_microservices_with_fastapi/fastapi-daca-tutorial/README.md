# 🧠 FastAPI DACA Microservices

This project comprises two FastAPI microservices:

- [agent_memory_service](./agent_memory_service/)
- [chat-service](./chat-service/)

Each service is managed using the `uv` Python package manager for efficient dependency management and execution.

## 🚀 Running the Services

### Prerequisites

- Ensure that [uv](https://docs.astral.sh/uv/) is installed on your system.
- Navigate to the `fastapi-daca-tutorial` directory, which contains both microservices.

### For Linux/macOS Users

1. **Make the script executable**:

   ```bash
   chmod +x run_services.sh
   ``


2. **Run the script**:

   ```bash
   ./run_services.sh
   ``


   This script will start both microservices concurrently in the background.

### For Windows Users

1. **Run the batch file**:

   Double-click on `run_services.bat` or execute it via the Command Prompt:

   ```cmd
   run_services.bat
   ``


   This will open two separate Command Prompt windows, each running one of the microservices.

## 📝 Notes
- Both scripts utilize `uv run fastapi dev` to start the FastAPI applications in development moe.- Ensure that each microservice directory contains a valid `pyproject.toml` file with the necessary configuratios.- If you encounter issues with dependencies, consider running `uv sync` in each microservice directory to synchronize dependencies as specified in the `pyproject.toml` fils.

