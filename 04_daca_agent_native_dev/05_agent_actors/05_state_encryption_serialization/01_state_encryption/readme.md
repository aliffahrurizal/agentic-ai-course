# Step 1: State Encryption

In this step, you’ll enhance the `ChatAgent` actor from **Agent Actors Step 2** by configuring Dapr state encryption to secure conversation history stored in Redis. This ensures user data privacy, aligning with DACA’s goal of building secure, privacy-conscious AI agents.

## Overview

The **state_encryption** step configures the `ChatAgent` to:
- Enable Dapr state encryption using a secret store (Kubernetes secrets) and an encryption key.
- Update the Redis state store configuration to encrypt conversation history.
- Test encryption by verifying that Redis stores unreadable (encrypted) data.
- Preserve the existing `process_message` and `get_conversation_history` functionality from **Step 2**.

State encryption protects sensitive user data (e.g., conversation history) in the state store, critical for production-grade AI agents.

### Learning Objectives
- Configure Dapr state encryption with a secret store.
- Secure conversation history in Redis.
- Validate encrypted state data.
- Maintain lightweight changes with no actor code modifications.

### Ties to DACA
- **Security**: Encryption protects user data, ensuring privacy.
- **Reliability**: Secure state management maintains data integrity.
- **Production-Readiness**: Encryption supports compliance for AI agents handling sensitive information.

## Key Concepts

### Dapr State Encryption
Dapr supports state encryption for state stores (e.g., Redis) by:
- Using a symmetric encryption key (e.g., AES-256) stored in a secret store.
- Encrypting state data before saving to the store and decrypting on retrieval.
- Integrating with secret stores like Kubernetes secrets or cloud providers (e.g., AWS Secrets Manager).

In this step, you’ll configure Dapr to encrypt `ChatAgent`’s conversation history using a Kubernetes secret and AES-256 encryption, ensuring Redis stores encrypted data.

### Lightweight Configuration
State encryption is added with minimal changes:
- A new Dapr secret store component (`secretstore.yaml`) using Kubernetes secrets.
- A Kubernetes secret containing an encryption key.
- An updated `statestore.yaml` to enable encryption with the secret store.
- No changes to the `ChatAgent` code, as encryption is handled by Dapr’s state management.
- Minimal dependencies (Kubernetes secrets), keeping the setup lightweight.

### Interaction Patterns
The `ChatAgent` supports:
- **Request/Response**: FastAPI endpoints (`/chat/{actor_id}`, `/chat/{actor_id}/history`) with encrypted state operations.
- **Event-Driven**: Pub/sub events via `/subscribe` for `ConversationUpdated`.
- **Secure Storage**: Conversation history is encrypted in Redis, transparent to the actor.

## Hands-On Dapr Virtual Actor

### 0. Setup Code
Use the [00_lab_starter_code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code) from **Step 2**. Ensure **Step 2** is complete and you have a Kubernetes cluster (e.g., `minikube`).

Verify dependencies:
```bash
uv add dapr dapr-ext-fastapi pydantic
```

### 1. Configure Dapr Components
Update the **Step 2** components to enable state encryption. Keep `daca-pubsub.yaml` and `message-subscription.yaml` unchanged (see **Step 4.1** README). Add a secret store and update the state store configuration.

**File**: `components/secretstore.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

**File**: `components/statestore.yaml`
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: default
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: redis-master.default.svc.cluster.local:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
  - name: primaryEncryptionKey
    secretKeyRef:
      name: encryption-key
      key: key
```

Create a Kubernetes secret for the encryption key (use a secure key in production):
```bash
kubectl create secret generic encryption-key --from-literal=key='my-secure-key-32-bytes-long12345' -n default
```

**Note**: The key must be 32 bytes for AES-256. The example key is for demonstration; generate a secure key using a tool like `openssl rand -base64 32`.

### 2. Use the Step 2 ChatAgent Code
No changes are needed to the **Step 2** `ChatAgent` code, as state encryption is handled by Dapr’s state management. Use the **Step 2** `main.py` as-is (see **Step 4.5** README).

### 3. Test the App
Port-forward the `ChatAgent` service to test:
```bash
kubectl port-forward svc/chat-agent 8000:8000 -n default
```

Test the **default** route group:
- **POST /chat/{actor_id}**: Sends a user message.
- **GET /chat/{actor_id}/history**: Retrieves the conversation history.
- **POST /subscribe**: Handles `user-chat` topic events.

Use `curl` commands to generate state data:
```bash
curl -X POST http://localhost:8000/chat/user1 -H "Content-Type: application/json" -d '{"role": "user", "content": "Hi there"}'
curl http://localhost:8000/chat/user1/history
```

Check Redis to verify encrypted data:
```bash
redis-cli -h redis-master.default.svc.cluster.local -p 6379
GET history-user1
```

**Expected Output**:
- POST: `{"response": {"role": "assistant", "content": "Got your message: Hi there"}}`
- GET: `{"history": [{"role": "user", "content": "Hi there"}, {"role": "assistant", "content": "Got your message: Hi there"}]}`
- Redis GET: Unreadable binary data (e.g., `"\x8f\x9a..."`), indicating encryption, not plain JSON (`[{"role": "user", ...}]`).

### 4. Understand the Setup
Review the setup:
- **No Code Changes**: The **Step 2** `main.py` remains unchanged, as encryption is configured via Dapr.
- **Secret Store**: `secretstore.yaml` uses Kubernetes secrets to manage the encryption key.
- **State Store**: `statestore.yaml` enables encryption with `primaryEncryptionKey` referencing the secret.
- **Existing Functionality**: Preserves `process_message`, `get_conversation_history`, and pub/sub from **Step 2**.

State encryption ensures conversation history is stored securely in Redis, transparent to the `ChatAgent`.

### 5. Observe the Dapr Dashboard
Run:
```bash
dapr dashboard
```
Check the **Actors** tab for `ChatAgent` instances (e.g., `1` for `user1`). Use `redis-cli` to confirm encrypted state data, and check logs (`dapr logs -a chat-agent`) for normal operation without encryption-related errors.

## Validation
Verify state encryption functionality:
1. **Message Processing**: POST to `/chat/user1` succeeds and stores history.
2. **History Retrieval**: GET `/chat/user1/history` returns the correct, decrypted history.
3. **Encrypted State**: Use `redis-cli GET history-user1` to confirm the data is encrypted (unreadable binary, not plain JSON).
4. **State Consistency**: Send multiple POSTs and verify GET returns consistent history, indicating proper decryption.
5. **Logs**: Check `dapr logs -a chat-agent` for no encryption-related errors (e.g., missing key).

## Troubleshooting
- **Encryption Not Applied**:
  - Verify `statestore.yaml` has `primaryEncryptionKey` with `secretKeyRef`.
  - Check `secretstore.yaml` is loaded and uses `secretstores.kubernetes`.
  - Ensure the Kubernetes secret exists (`kubectl get secret encryption-key`).
- **State Not Accessible**:
  - Confirm Redis is running (`kubectl get pods`).
  - Check logs for encryption key errors (`dapr logs -a chat-agent`).
- **Plain Text in Redis**:
  - Verify `GET history-user1` shows binary data, not JSON.
  - Recreate the secret with a valid 32-byte key.

## Key Takeaways
- **State Encryption**: Secures conversation history in Redis, protecting user data.
- **Lightweight Configuration**: Dapr’s state encryption requires only component files and a secret.
- **Privacy**: Ensures compliance for AI agents handling sensitive information.
- **DACA Alignment**: Supports secure, privacy-conscious systems for conversational AI.

## Next Steps
- Proceed to **Step 7: Middleware** to add authentication/authorization.
- Experiment with different encryption keys or secret stores (e.g., AWS Secrets Manager).
- Test encryption with larger conversation histories to verify performance.

## Resources
- [Dapr State Encryption](https://docs.dapr.io/developing-applications/building-blocks/state-management/state-management-encryption/)
- [Dapr Secret Stores](https://docs.dapr.io/developing-applications/building-blocks/secrets/secrets-overview/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Labs Starter Code](https://github.com/panaversity/learn-agentic-ai/tree/main/04_daca_agent_native_dev/05_agent_actors/00_lab_starter_code)