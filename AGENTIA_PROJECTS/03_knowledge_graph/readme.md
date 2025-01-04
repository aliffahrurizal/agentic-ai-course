# Agentia Knowledge Graph Project

This is the **third project** in your learning path for **Agentia**. This project builds on the previous two—multi-turn conversation and a user preference store—by incorporating a **graph database** (such as **Neo4j/FalkorDB**) to handle more complex, relationship-centric queries. You will develop a **Knowledge Graph Agent** that manages entities and their relationships (e.g., users, friends, places, interests), enabling you to retrieve structured insights and respond in natural language.

---

## Project Overview

1. **Goal**  
   - Introduce a **Knowledge Graph Agent** that uses Neo4j/FalkorDB to store and retrieve relationships between entities.  
   - Demonstrate how the Front-End Orchestration Agent coordinates with the Greeting Agent, the User Preference Agent, and now the Knowledge Graph Agent.

2. **Key Components**  
   1. **Front-End Orchestration Agent** *(Existing)*  
      - Continues to be the single entry point for user requests.  
      - Determines whether to delegate requests to the Greeting Agent, User Preference Agent, or the Knowledge Graph Agent.  
   2. **Greeting Agent** *(Existing)*  
      - Handles simple greeting interactions.  
   3. **User Preference Agent** *(Existing)*  
      - Stores and retrieves user-specific information (e.g., names).  
   4. **Knowledge Graph Agent** *(New)*  
      - Maintains a Neo4j/FalkorDB graph database of entities (e.g., people, places, objects, concepts) and their relationships.  
      - Responds to queries about how these entities are related (e.g., “Who are my friends?” or “Is John connected to London?”).

3. **Value Proposition**  
   - By adding a graph database, you gain the ability to represent and traverse complex relationships, enabling more sophisticated queries and context-aware dialogues.  
   - This project moves Agentia closer to functioning as an intelligent assistant capable of relational reasoning.

---

## Plan the Architecture

**Service Layout**  
   - You now have four services (or containers):
     1. **Front-End Agent**  
     2. **Greeting Agent**  
     3. **User Preference Agent**  
     4. **Knowledge Graph Agent** (backed by Neo4j/FalkorDB)


## Knowledge Graph Agent

### Responsibilities

1. **Ingest New Relationships**  
   - Receive natural language instructions (e.g., “I am friends with Jane”) to create relationships in the graph.  
   - Map user input to a Neo4j/FalkorDB query that updates or merges nodes/relationships.

2. **Query Existing Relationships**  
   - Understand queries like “Who are my friends?” or “Where do I live?”  
   - Execute the appropriate Cypher queries to retrieve relationships.  
   - Return the information in a user-friendly format.


## Front-End Orchestration Agent: Extended Logic

1. **Identify Knowledge Graph Requests**  
   - If the user’s query references relationships or knowledge retrieval (e.g., “Am I friends with Jane?”), it delegates to the Knowledge Graph Agent.  
2. **Coordinate with Existing Agents**  
   - If the user’s query is still a greeting or a request to store a name, direct it to the existing Greeting Agent or User Preference Agent.  
3. **Session/Context Handling**  
   - The Front-End Agent might need to pass along both the user’s unique ID and recognized entities (e.g., “Jane” is a friend) so the Knowledge Graph Agent can run the correct Cypher queries.

---

## Demonstration Scenario

1. **User**: “Hello!”  
   - **Front-End** → **Greeting Agent** → Returns: “Hi there! How can I help you?”  

2. **User**: “My name is John.”  
   - **Front-End** → **User Preference Agent** → Stores name in a simple preferences store.

3. **User**: “I am friends with Jane.”  
   - **Front-End** detects the “create friend relationship” intent.  
   - **Front-End** → **Knowledge Graph Agent** → The agent merges or updates the `User(user_id=1234)` node and creates a `FRIEND_OF` relationship to `User(name="Jane")` in Neo4j/FalkorDB.  
   - **Knowledge Graph Agent** returns: “I’ve noted that you’re friends with Jane.”

4. **User**: “Who are my friends?”  
   - **Front-End** detects the “retrieve friend relationships” intent.  
   - **Front-End** → **Knowledge Graph Agent** → The agent runs a Cypher query, returns a list of friends.  
   - **Knowledge Graph Agent** returns: “Your friends are: Jane.”

5. **User**: “What is my name?”  
   - **Front-End** → **User Preference Agent** → Returns: “Your name is John.”

This sequence shows the interplay of three specialized agents plus the front-end orchestrator, each addressing different parts of the user’s request.

---

**Logs and Monitoring**  
   - **Knowledge Graph Agent**: Log all Cypher queries for debugging.  
   - **Front-End Agent**: Log the routing decisions—why it decided to call the Knowledge Graph Agent vs. others.

**Error Handling**  
   - If the graph is unavailable, the Knowledge Graph Agent should return an appropriate error message.  
   - Handle malformed queries or unexpected relationship formats gracefully (e.g., “I can’t process that relationship.”).

---

## Additional Enhancements

1. **Expanding the Schema**  
   - Add more node types (e.g., `City`, `Interest`) and relationships (`:LIVES_IN`, `:INTERESTED_IN`).  
   - Let users store more complex data (“I live in New York,” “I like soccer,” etc.).

2. **Full-Text Search Integration**  
   - Use Neo4j’s (FalkorDB) [Full-Text Indexing](https://neo4j.com/docs/cypher-manual/current/schema/index/#cypher-schema-index-fulltext-search) to handle queries that mention entity names or partial matches.

3. **Recommendation Logic**  
   - Implement simple graph-based recommendations—for example, “Suggest friends of my friends” or “Show me top interests among my friends.”

4. **User Authentication**  
   - Secure the system with user tokens so that user 1234 can only see or modify their own data.  
   - The Front-End Agent can validate tokens before delegating queries.

5. **Parallel Queries**  
   - If the user asks a question that touches user preferences (e.g., name) and knowledge relationships (e.g., city relationships) at once, the Front-End Agent might query the User Preference Agent and the Knowledge Graph Agent in parallel, then consolidate responses.

---

## Conclusion

This **third project** showcases how to integrate a **Neo4j/FalkorDB-based Knowledge Graph Agent** into your evolving **Agentia** ecosystem. You will learn to:

- Represent and manage relationships in a graph database.  
- Query and update these relationships in response to natural language requests.  
- Orchestrate interactions among four different agents (Front-End, Greeting, User Preference, and Knowledge Graph).

By taking this step, you’ll explore **graph-driven reasoning** and build a more **context-aware, relationship-centric** AI platform, setting the stage for even more sophisticated multi-agent solutions in the future.