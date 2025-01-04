# Agentia User Preference Project

Below is a **second project** in your learning path for **Agentia**, building on the “Hello World” foundation. In this second project, you’ll move beyond simple greetings to introduce **basic state management** and **multi-turn conversation**. You will add a **User Preference Agent** that stores and retrieves user-specific data (e.g., the user’s name, password, etc.). The **Front-End Orchestration Agent** will now coordinate between the Greeting Agent (from the first project) and the new User Preference Agent to demonstrate more robust agent collaboration.

---

## Project Overview

1. **Goal**  
   - Enhance the system to handle **basic conversation context** and **user preferences**.  
   - Demonstrate multi-turn dialogue: the user can introduce themselves (“My name is Zia”) and immediately ask a password, then later request that information (“What is my name?”). If the user didnot tell than ask the name and password (signup) and later signin when required.

2. **Key Components**  
   1. **Front-End Orchestration Agent**:  
      - Continues to receive user inputs and determine which specialized agent(s) should handle the request.  
      - Maintains conversation flow and delegates to the Greeting Agent or the User Preference Agent.  
   2. **Greeting Agent** *(From the first project)*:  
      - Still responsible for greeting-related interactions.  
      - No major change; can be reused from the “Hello World” setup.  
   3. **User Preference Agent** *(New)*:  
      - Stores and retrieves user-specific data (e.g., the user’s name, password, etc.).  
      - Exposes a simple interface for saving or retrieving user information using natural language.

3. **Value Proposition**  
   - By adding **state management**, you’ll learn how to handle conversation context and store user data in a minimal (yet flexible) way.  
   - This lays the groundwork for more advanced features like personalized recommendations, persistent user sessions, and multi-agent synergy.

4. **Data Storage**  
   - The **User Preference Agent** needs to store data. Options include:
     - **In-Memory Storage**: A simple dictionary or in-memory cache for quick prototyping.  
     - **Neon Serverless Postgres**: A serverless relational database for more persistence and reliability.  
   - A minimal schema for storing user preferences might include:
     - **user_id** (unique identifier for the user)  
     - **name** (the user’s name)  
     - **additional_attributes** (e.g., password, location, preferences, etc.)

## User Preference Agent

### Core Responsibilities

1. **Store User Data**: For example, “My name is John.” The agent should parse and save `name = John`.  
2. **Retrieve User Data**: For example, “What is my name?” The agent should look up the user’s stored name and return it.


## Front-End Orchestration Agent: Extended Logic

### Conversation Flow

1. **Receive User Message**:  
   - Check for greeting intent (delegate to **Greeting Agent**).  
   - If not a greeting, check if the user is providing or requesting personal info (delegate to **User Preference Agent**).  
   - Otherwise, fallback to: “I can handle greetings or your name for now.”


## Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent**  
   - **Greeting Agent** replies: “Hello there! How can I help you today?”  
   - **Front-End** passes that response to the user.

2. **User**: “My name is John”  
   - **Front-End** determines this is a “store name” intent.  
   - **Front-End** → **User Preference Agent** (stores `name = John` for `user_id = 1234`).  
   - **User Preference Agent** replies: “Got it! I’ll remember that your name is John.”

3. **User**: “What is my name?”  
   - **Front-End** identifies “retrieve name” intent.  
   - **Front-End** → **User Preference Agent** fetches name for `user_id = 1234`.  
   - **User Preference Agent** returns: “Your name is John.”  
   - **Front-End** passes the answer to the user.

At this point, you have demonstrated **multi-turn conversation** and **basic personalization** with minimal additional logic.

---

## Required Enhancements

1. **Context Preservation**  
   - Implement a conversation state in the Front-End Agent to handle references like “Call me John from now on.” or “Remember that I live in London.”  

2. **Authentication and Authorization**  
   - If you want to handle multiple users securely, add an authentication layer so each user has a unique token or session.

3. **Extended User Preferences**  
   - Expand from just “name” to other attributes: location, interests, or personal preferences.  
   - The system can become more “personal assistant”-like.

4. **Integration with Other Agents**  
   - Once user preferences are stored, you can create new agents (e.g., Weather Agent) that tailor responses using user location.  
   - The Front-End Agent can pass user context to the Weather Agent (“John is in New York; fetch local weather.”).

5. **Database**  
   - For production readiness a persistent database so data isn’t lost on restart.

---

## Conclusion

This second project evolves the “Hello World” demo into a **multi-turn, stateful conversation** by introducing a **User Preference Agent**. You’ll practice:

- **Intent detection** beyond simple greetings.  
- **Data storage** and retrieval (in-memory or a simple database).  
- **Orchestration** across multiple agents in a single conversation thread.  

By completing this project, you’ll further solidify the **Agentia** paradigm: loosely coupled, natural language-based agents that can be independently developed, scaled, and reused—opening the door to increasingly powerful AI ecosystems.

You have a choice of building these Agents for the Agentia World in CrewAI, LangGraph, Microsoft AutoGen version 0.4 and above, and AG2. You may develop anyone of these or develop multiple projects using all of these.