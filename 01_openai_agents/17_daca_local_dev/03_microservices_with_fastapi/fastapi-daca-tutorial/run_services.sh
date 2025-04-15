#!/bin/bash

# Navigate to the agent_memory_service directory and start the service
(
  cd agent_memory_service || exit
  uv run fastapi dev
) &

# Navigate to the chat-service directory and start the service
(
  cd chat-service || exit
  uv run fastapi dev
) &

# Wait for both background processes to finish
wait
