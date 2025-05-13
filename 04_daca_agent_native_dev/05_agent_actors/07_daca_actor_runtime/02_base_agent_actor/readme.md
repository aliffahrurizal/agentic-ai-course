# BaseActor Implementation Plan

- The `BaseActor` will inherit from `dapr.actor.Actor` and `dapr.actor.Remindable`.
- It will make extensive use of Python's `asyncio` for non-blocking, concurrent operations.
- Comprehensive type hinting will be used for clarity, maintainability, and improved tooling.
- Structured logging will be integrated using Python's `logging` module, accessible via `self.logger`, and designed to be compatible with Dapr's observability features.
- A `DaprClient` instance may be used for direct interaction with Dapr building blocks (e.g., publishing events directly, invoking other services/actors, managing secrets or configuration).
- The design will be mindful of future extensibility, allowing for integration with other specialized frameworks or protocols as the DACA ecosystem evolves (e.g., potential hooks for ROS 2 interactions for physical agents).

This `BaseActor` will serve as the superclass for more specialized actors like `ChatActor`, `MemoryActor`, `TriageAgent`, etc., within the multi-agent system, providing them with a rich set of DACA-aligned capabilities out-of-the-box.

### Step 1: Setup Foundation Code

The `01_foundation_actor` have Base Code and a Guide to implement it from scratch.

Follow the guide or just clone and run the code. At end you will have the following services

- Tilt UI: http://localhost:1035
- Dapr Dashboard: http://localhost:8080
- Ambient Actor Interface: http://localhost:30080/docs
- Metrics Tracing Interface: http://localhost:9090
- Jaegur UI Interface: http://localhost:16686/

Now in step 2, 3, 4, 5, 6 we will create the base actor - the final code is present in 02_base_actor.

### Step 2: Create Base Actor Interface

### Step 3: Implemet Base Actor

### Step 4: Add Advanced Actor Config Learnings to Base Actor

### Step 5: Add Bindings, PubSub and State Invocation Components

### Step 6: Add Timers, Remineders and Jobs API for Actors Self Management.

