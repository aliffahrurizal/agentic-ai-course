# Agentic Long Term Memory in OpenAI Agentic 

[Different Types of Memories in Agentic Framework](https://www.linkedin.com/pulse/different-types-memories-agentic-framework-gourav-g--shdxc/)

Let's clarify and refine the understanding of memory types within the context of agentic frameworks, specifically with an eye towards how they might be implemented using tools like the OpenAI Agents SDK.

Here's a breakdown of the memory types and how they relate to agentic workflows:

**1. Memory Types in Agentic Frameworks:**

* **Episodic Memory:**
    * This stores specific, personal experiences or "episodes" of the agent's interaction with the environment or users.
    * Think of it as a log of what the agent has done and observed.
    * In an OpenAI Agents SDK context, this could involve storing:
        * User inputs and agent responses.
        * API call results.
        * Observations from tools the agent used.
        * Timestamps associated with each event.
    * Example: "At 2:30 PM, the user asked for the weather in London, and I called the weather API, which returned 15 degrees Celsius."

* **Semantic Memory:**
    * This stores general knowledge and facts about the world.
    * It's about understanding concepts, relationships, and meanings.
    * In the Agents SDK, this could be:
        * Pre-trained knowledge embedded in the language model.
        * Knowledge retrieved from external knowledge bases (e.g., databases, APIs).
        * Information extracted and stored from previous interactions.
    * Example: "London is the capital of the United Kingdom." or "The capital of France is Paris."

* **Procedural Memory:**
    * This stores knowledge about how to do things, or "procedures."
    * It's about skills, habits, and learned behaviors.
    * In the Agents SDK, this could involve:
        * Storing sequences of actions or tool calls that have been successful in the past.
        * Learning and refining strategies for achieving specific goals.
        * Storing the result of function calls, and the proper way to call those functions.
    * Example: "To get the weather, first, call the weather API with the city name, then parse the temperature from the response."

* **Temporal Memory:**
    * This is related to the agents ability to track and understand the passage of time, and the order of events.
    * This is often tightly coupled with episodic memory, but can also be considered it's own type.
    * In the Agents SDK, this would include.
        * Timestamps on all events.
        * The ability to understand "before" and "after" relationships.
        * The ability to understand time based context for actions.
    * Example: "The user asked about the weather, then 5 minutes later, asked about restaurants."

**2. Memory Mechanisms:**

* **Hot Path (Immediate/Short-Term) Memory:**
    * This refers to the agent's immediate working memory.
    * It's used for processing the current task and keeping track of recent interactions.
    * In the Agents SDK, this would involve:
        * The context window of the language model.
        * Variables and data structures used during the execution of a function call.
        * The current conversation history.
    * This is the memory that the agent uses to create it's next response.

* **Background (Long-Term) Memory:**
    * This refers to the agent's persistent memory, which is stored and retrieved over longer periods.
    * In the Agents SDK, this would involve:
        * External databases or vector stores.
        * File storage.
        * Knowledge graphs.
    * This is the memory that the agent uses to inform it's actions over multiple conversations.

**Applying this to OpenAI Agents SDK:**

* The Agents SDK provides the tools to build agents that can interact with external resources.
* You can use these tools to implement the different memory types.
* For example:
    * You could use a vector database (like Pinecone or Weaviate) to store episodic and semantic memory.
    * You could use function calling to implement procedural memory, by storing the results of function calls, and the proper way to call those functions.
    * You can use the conversation history that is managed by the SDK as the hot path memory.
* The choice of memory implementation will depend on the specific needs of your agent.

By understanding these memory types and mechanisms, you can design more sophisticated and capable agents that can learn, adapt, and reason effectively.


References:

We may also understand the theory from this course[Long-Term Agentic Memory with LangGraph](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/)
