# Timers and Reminders

**Objective:** Explore advanced Dapr Virtual Actor features to enhance agent behavior and reliability. Learn how to use Dapr Actor timers and reminders for scheduling tasks and ensuring reliable execution, even after actor deactivation.

**Key Concepts Covered:**
- Reminders: Durable scheduling for periodic tasks.
- Timers: Temporary periodic tasks.
- Reentrancy: Concurrent message handling.
- Fault tolerance: Error handling and retries.

**Sub-Steps**:
1. **Reminders**:
   - Add a reminder to the `ChatAgent` to clear conversation history after a set period (e.g., 10 minutes).
   - Activities: Configure a reminder, implement a cleanup method, verify state reset.
   - Validation: Send messages, wait for the reminder to trigger, and confirm history is cleared.

2. **Timers**:
   - Implement a timer in `ChatAgent` to log the number of messages every 5 seconds.
   - Activities: Register a timer, log status to console, stop the timer after a condition.
   - Validation: Monitor logs to confirm periodic updates.

3. **Reentrancy**:
   - Enable reentrancy to allow the `ChatAgent` to handle follow-up messages concurrently.
   - Activities: Modify the actor to make a self-call after processing a message, test concurrent behavior.
   - Validation: Send a message and verify multiple responses are processed correctly.

4. **Fault Tolerance**:
   - Simulate errors in `ChatAgent` (e.g., state store failure) and implement retry logic.
   - Activities: Add try-catch blocks, configure Dapr retry policies, test recovery.
   - Validation: Trigger an error and confirm the actor retries and recovers.

**Ties to README**:
- “Fault Tolerance”
- “Turn-Based Concurrency” (reentrancy)
- “Dapr’s Implementation” (reminders, timers)