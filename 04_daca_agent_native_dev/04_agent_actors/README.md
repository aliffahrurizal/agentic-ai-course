# Agent Actors

In this module we will learn to build Agent as Actors following DACA.

**Dapr Actors** are lightweight, stateful entities based on the Actor Model (Hewitt, 1973), ideal for modeling AI agents in DACA. Each agent, implemented as a Dapr Actor, encapsulates its own state (e.g., task history, user context) and behavior, communicating asynchronously via A2A endpoints or Dapr pub/sub (e.g., RabbitMQ, Kafka). Actors enable concurrent task execution, dynamic agent creation (e.g., spawning child agents for subtasks), and fault isolation, storing state in Dapr-managed stores like Redis or CockroachDB. For example, in a content moderation system, a parent actor delegates post analysis to child actors, each processing a post concurrently and coordinating via A2A messages, ensuring scalability across DACA’s deployment pipeline.

## What Is the [Actor Model](https://www.geeksforgeeks.org/design-patterns-for-building-actor-based-systems/)?

Introduced by Carl Hewitt, Peter Bishop, and Richard Steiger in 1973, the **Actor Model** is a mathematical model of computation designed for concurrent and distributed systems. It treats **actors** as the universal primitives of computation, encapsulating state, behavior, and a mailbox for asynchronous message passing. Actors interact exclusively via messages, avoiding shared memory and locking, which simplifies concurrency and enhances scalability.

### Key Principles of the Actor Model

1. **Actors as the Fundamental Unit**:
   - An actor is a lightweight, isolated entity that:
     - Receives and processes messages.
     - Performs computations based on its internal state and behavior.
     - Sends messages to other actors.
     - Creates new actors dynamically.
   - Actors operate independently, processing one message at a time.

2. **Asynchronous Message Passing**:
   - Actors communicate by sending messages to each other’s mailboxes, decoupling senders and receivers for better scalability and resilience.

3. **No Shared State**:
   - Each actor maintains its own private state, eliminating race conditions, deadlocks, and other concurrency issues associated with shared memory.

4. **Concurrency by Default**:
   - Actors process messages sequentially, enabling safe concurrent execution without complex synchronization mechanisms.

5. **Fault Tolerance**:
   - Actors are isolated, so failures are contained locally. Supervisor strategies can restart or recover failed actors, ensuring system robustness.

## [Dapr’s Implementation of the Actor Model](https://docs.dapr.io/developing-applications/building-blocks/actors/)

**Dapr (Distributed Application Runtime)**, a core component of DACA, implements the Actor Model through its **Dapr Actors** framework, providing a robust abstraction for stateful, concurrent, and distributed agent interactions. Dapr Actors are **virtual actors**, meaning they are activated on-demand and can be garbage-collected when idle, optimizing resource usage. Key features of Dapr Actors in DACA include:

- **State Management**: Dapr persists actor state (e.g., agent context, task progress) in a configured store (e.g., Redis, CockroachDB), ensuring durability across activations.
- **Message Passing**: Actors communicate via asynchronous method calls or events, integrated with Dapr’s pub/sub messaging (e.g., RabbitMQ, Kafka).
- **Concurrency Control**: Dapr enforces single-threaded access to each actor, preventing concurrent modifications and simplifying state management.
- **Scalability**: Actors are distributed across a cluster (e.g., Kubernetes), with Dapr handling placement and load balancing.
- **Fault Tolerance**: Dapr retries failed actor operations and supports supervisor-like patterns for error handling.
- **Turn-Based Concurrency**: Dapr Actors process one message at a time, ensuring predictable behavior in high-concurrency scenarios.

In DACA, Dapr Actors are used alongside other Dapr building blocks (state management, pub/sub, workflows) to orchestrate AI agents, making the Actor Model a natural fit for its event-driven, microservices-based architecture.

### Reading and Learning Resources
- [Dapr Actors](https://docs.dapr.io/developing-applications/building-blocks/actors/)
- [Getting started with the Dapr actor Python SDK](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [Dapr Day Oct 2024 - The Dapr Actors Journey: From Understanding to Intuition](https://www.youtube.com/watch?v=xZyuO2dU9b0&t=303s)
- [Actor Based Design Patterns](https://www.geeksforgeeks.org/design-patterns-for-building-actor-based-systems/)
- [AutoGen Core - the building blocks for an event-driven agentic system where agents are developed using Actor Model.](https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/index.html)
- [Examples and Implementations of Actor Model](https://chatgpt.com/share/68134b71-baa0-8002-bb73-1db508dbf687)

- [Getting Started](https://docs.dapr.io/developing-applications/sdks/python/python-actor/)
- [Actors Overview](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-overview/)
- [Actor Lifetime](https://docs.dapr.io/developing-applications/building-blocks/actors/actors-features-concepts/#actor-lifetime)
- [Actors API Reference](https://docs.dapr.io/reference/api/actors_api/)
- [Dapr Python SDK FastAPI Integration](https://docs.dapr.io/developing-applications/sdks/python/python-fastapi/)