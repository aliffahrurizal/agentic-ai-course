# Agentia Smart Home (IoT) Project

Below is a suggested **tenth project** in your **Agentia** learning path. This time, you will create a **Smart Home Orchestrator**, a multi-agent system that integrates with IoT devices (thermostats, lights, security cameras, etc.), uses an **LLM** for interpreting user requests in natural language, references user preferences and a knowledge graph for context, and maintains a **human-in-the-loop** approach for sensitive operations.

---

## Project Overview

1. **Goal**  
   - Develop a **Smart Home Orchestrator Agent** that can connect to various IoT devices and services to automate home management tasks (e.g., setting the thermostat, turning lights on/off, checking security cameras).  
   - Use **LLM-based function calling** to parse complex commands (e.g., “Dim the lights to 50% when I start watching a movie”) and integrate existing preferences (e.g., preferred temperature, device usage schedules) or knowledge graph data (e.g., device locations, user routines).  
   - Implement a **human-in-the-loop** step for critical actions (e.g., unlocking doors, disabling alarms).

2. **Key Components**  
   1. **Front-End Orchestration Agent** (existing)  
      - Continues to be the single point of contact for user interactions.  
   2. **Greeting Agent** (existing)  
      - Handles trivial greetings or small talk.  
   3. **User Preference Agent** (existing)  
      - Stores user-defined defaults (e.g., preferred room temperature, typical bedtime, do-not-disturb schedules).  
   4. **Knowledge Graph Agent** (existing, optional)  
      - Manages structured relationships between rooms, devices, user routines (e.g., “Living Room has a Smart Light,” “Alice’s bedtime is 10 PM,” “Lights can be set at 50% brightness”).  
   5. **Smart Home Orchestrator Agent** **(New)**  
      - Integrates with IoT devices/services (e.g., via **MQTT**, **Zigbee**, or **cloud APIs** from manufacturers).  
      - Uses an **LLM** to interpret user commands and call “control” tools (e.g., `SetThermostat`, `SwitchLights`, `LockDoor`, etc.) in structured form.  
      - Enforces **human approval** before executing sensitive actions (like unlocking doors or turning off security systems).

3. **Value Proposition**  
   - Demonstrates how multi-agent architecture can orchestrate **real-world device control** through **natural language**, bridging user preferences, knowledge graph data, and IoT APIs.  
   - Reinforces the importance of **human oversight** for critical or irreversible commands.

---

## 1. Plan the Architecture

1. **Service Layout**  
   - The **Smart Home Orchestrator Agent** is a new service that:  
     - Communicates with IoT devices or IoT hub(s).  
     - Leverages an LLM for command interpretation and tool-calling.  
   - The existing **Front-End**, **Greeting**, **User Preference**, and optional **Knowledge Graph** Agents continue to run in separate containers/processes.  

2. **Communication Mechanism**  
   - The Orchestrator Agent can either:  
     - Directly call local device APIs (e.g., `http://192.168.0.10/thermostat`) if your devices expose endpoints on the LAN.  
     - Use a message broker (e.g., **MQTT** on a Raspberry Pi), or a cloud-based IoT platform (e.g., AWS IoT, Google Cloud IoT) if your devices are integrated there.  
   - The LLM function-calling approach should define “tools” for each controllable action, for example:  
     - **SetThermostat**(temperature, room)  
     - **SwitchLights**(room, brightness_level, on_off)  
     - **LockDoor**(door_id, action)

3. **Human-in-the-Loop Approval**  
   - For potentially risky actions—like unlocking front doors, disabling alarms, or granting remote access—the Orchestrator returns a **draft** (“Proposed action: unlock the front door—do you approve?”).  
   - The user must confirm via the **Front-End Orchestration Agent** before the Smart Home Orchestrator Agent actually executes the command.

---

## 2. Smart Home Orchestrator Agent

### 2.1 Responsibilities

1. **Parse User Commands**  
   - Receive user requests like “Set the living room lights to 30% brightness after 9 PM” or “Lock all doors.”  
   - Use the LLM to interpret the request and decide which “tool” or combination of tools to invoke.  
   - Incorporate existing user preferences (e.g., brightness preference for evenings) or knowledge graph data (e.g., device IDs, location references).

2. **Orchestrate IoT Control**  
   - For each recognized action, call the appropriate device API.  
   - Return a success or error message (e.g., “Living room lights set to 30% brightness”).  
   - If the action is sensitive (unlocking a door, disabling a security camera), produce a draft that requires user confirmation.

3. **Condition-Based Automation**  
   - Handle conditional or scheduled logic. For example, “If the temperature goes below 68°F at night, set the thermostat to 72°F.”  
   - The Orchestrator Agent could internally track or subscribe to device status events and apply user rules.

---

## 3. Front-End Orchestration Agent: Extended Logic

1. **Identify Smart Home Commands**  
   - If the user’s input references controlling devices, it delegates to the **Smart Home Orchestrator Agent**.  
   - Other requests (greetings, travel, email) remain handled by the existing specialized agents.

2. **Draft Confirmation**  
   - If the Orchestrator returns a `draft: true`, the Front-End Agent displays the proposed action(s).  
   - On user approval, the Front-End calls a finalization endpoint (e.g., `POST /smart_home_orchestrator/finalize`) so the Orchestrator executes the action.

3. **Fallback**  
   - If the Orchestrator encounters unknown devices or unclear commands, it may prompt the user for clarification (e.g., “I don’t see a device named ‘pool light’. Please confirm the device name.”).

---

## 4. Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent** → Returns a standard greeting.  
2. **User**: “When I say ‘movie time,’ dim the living room lights to 30% and set the AC to 70 degrees.”  
   - **Front-End** → **Smart Home Orchestrator Agent**  
   - The Orchestrator:  
     - Interprets user’s intention for a custom routine (“movie time”).  
     - Possibly stores a routine in the knowledge graph or preference store.  
     - Replies with a success message: “Noted. I’ll dim lights to 30% and set AC to 70°F when you say ‘movie time.’”  
3. **User**: “Movie time.”  
   - **Front-End** → **Smart Home Orchestrator Agent** → The agent sets lights to 30%, sets AC to 70°.  
   - If user or system flags these actions as safe, no further approval is needed, so the Orchestrator finalizes immediately.  
4. **User**: “I’m heading out. Lock all doors.”  
   - **Front-End** → **Smart Home Orchestrator Agent** → The agent returns a draft with “Lock front door, Lock back door, Lock garage door” for approval.  
   - The user approves. The agent executes the commands and confirms.

---

## 5. Deployment and Testing

1. **Local or Cloud Setup**  
   - Continue with containerization for each agent.  
   - For IoT device integration, either:  
     - Use **simulated** devices or a local IoT test environment (e.g., **Home Assistant** with demo devices).  
     - Connect to **real** devices if you have them, ensuring you manage authentication and local network access.

2. **LLM Function-Calling**  
   - Define tools like `LockDoor(door_id)`, `SetThermostat(temp, room)`, `SwitchLights(room, brightness, on_off)`.  
   - The LLM dispatches user requests to the correct tool, returning a structured plan (draft) or final execution note.

3. **Observability**  
   - **Smart Home Orchestrator Agent**: Log each command, device response, and user confirmation.  
   - **Front-End Agent**: Log user acceptance or modification.  
   - Optionally integrate a dashboard (e.g., Grafana, Home Assistant) to visualize the state of devices in real time.

4. **Error Handling**  
   - If a device is offline or unreachable, the agent should return a graceful error (“Couldn’t reach the living room thermostat—please try again later.”).

---

## 6. Possible Enhancements

1. **Machine Learning for Home Automation**  
   - Predict user behavior (e.g., user typically turns lights down at 10 PM) and preemptively propose automations.  
   - Incorporate data from sensors (temperature, humidity, occupancy) to optimize energy usage.

2. **Multi-User Permissions**  
   - If there are multiple household members, the system might require specific permissions for certain commands (e.g., only the homeowner can unlock the front door remotely).

3. **Security and Auth**  
   - Implement robust authentication and encryption for commands.  
   - Possibly integrate with device tokens (like HomeKit or OAuth tokens for cloud-based devices) so only authorized requests are processed.

4. **Scheduled Routines**  
   - Let the user define or modify schedules (“Every weekday at 7 AM, turn on the coffee machine and set lights to 70% brightness in the kitchen.”).

5. **Integration with Other Agents**  
   - Combine with the **Mail Processing Agent** to confirm “Door unlocked” events via email if user is away.  
   - Link with the **Knowledge Graph Agent** for advanced device relationships or usage analytics (e.g., “Which rooms have the most energy consumption?”).

6. **Voice Interface**  
   - Optionally add a speech-to-text or text-to-speech interface for a more natural, hands-free user experience.

---

## Conclusion

This **tenth project** evolves your **Agentia** ecosystem into a **Smart Home Orchestrator**, leveraging:

- **LLM-based** natural language commands and tool-calling to control IoT devices.  
- A **human-in-the-loop** mechanism to ensure security and user confirmation for sensitive actions.  
- The **multi-agent** design that integrates existing capabilities (user preferences, knowledge graphs, possibly email notifications).

By implementing a real or simulated home automation environment, you demonstrate how **Agentia** can extend beyond purely digital tasks into the **physical realm**, orchestrating devices and systems seamlessly under robust user oversight.