import uuid

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage
from langgraph.store.memory import InMemoryStore, BaseStore
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages

_: bool = load_dotenv(find_dotenv())

# ✅ **Initialize LLM**
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# ✅ **Initialize Memory Store for Bob-Agent**
in_memory_store = InMemoryStore(
    index={
        "embed": GoogleGenerativeAIEmbeddings(model="models/embedding-001"),  # Ensure correct model
        "dims": 768,  # Ensure embedding dimensions match
    }
)


# ✅ **Task: Bob-Agent Retrieves Its Own Memory**
@task
def call_model(messages: list[BaseMessage], memory_store: BaseStore):
    """Retrieves Bob-Agent's context from memory and responds accordingly."""

    namespace = ("memories", "bob_agent")

    # 🔥 **Retrieve stored memories**
    stored_memories = memory_store.search(namespace, query="Bob AI Agent persona and improvements")
    stored_info = "\n".join([d.value["data"] for d in stored_memories]) if stored_memories else ""
    print("Existing Memories", stored_info, "\n\n")

    # ✅ **Adjust system prompt dynamically**
    if stored_info:
        system_msg = f"You are Bob, a helpful AI assistant. Your current persona and improvements:\n{stored_info}"
    else:
        system_msg = "You are Bob, a helpful AI assistant. No specific improvements or persona data is available yet."

    # ✅ **Invoke the model with memory-augmented context**
    response = model.invoke([{"role": "system", "content": system_msg}] + messages)

    return response


# ✅ **Task: Bob-Agent Learns from User Interactions**
@task
def learn_from_user(messages: list[BaseMessage], memory_store: BaseStore):
    """Stores learnings from a user interaction in memory."""

    namespace = ("memories", "bob_agent")

    # 🔥 **Extract key learnings using LLM**
    learnings_response = model.invoke([
        {"role": "system", "content": "Analyze the user chat and extract key improvements for yourself. Focus on persona refinement, response tone, and knowledge gaps. Do not store anything related to user."}
    ] + messages)

    # ✅ **Store learnings in Bob-Agent’s memory**
    new_learning = f"Bob-Agent learned: {learnings_response.content}"
    memory_store.put(namespace, str(uuid.uuid4()), {"data": new_learning})

    return new_learning

@task
def review_workflow_memories():
    namespace = ("memories", "bob_agent")
    stored_memories = in_memory_store.search(namespace, query=str("bob"))
    stored_info = "\n".join([d.value["data"] for d in stored_memories]) if stored_memories else ""
    
    print("\n\n", " 🔥 NEW SELF-LEARNING" ,stored_info  ,"\n\n")



# ✅ **Workflow EntryPoint: Handles Bob-Agent's Persistent Memory**
@entrypoint(checkpointer=MemorySaver(), store=in_memory_store)
def workflow(
    inputs: list[BaseMessage],
    *,
    previous: list[BaseMessage],
    config: RunnableConfig,
    store: BaseStore,
):
    """Handles Bob-Agent's conversation flow and learning."""
    
    previous = previous or []
    inputs = add_messages(previous, inputs)

    print("\n\n🔥 **Retrieve response based on Bob-Agent's memory**\n")
    response = call_model(inputs, store).result()
    print("\n\n🔥 **Bob-Agent response**\n", response)

    print("\n\n🔥 **Bob-Agent is now learning from the interaction**\n")
    learn_from_user(inputs, store).result()
    
    print("🔥 **See what Bob have learned from the interaction**\n")
    review_workflow_memories().result()

    return entrypoint.final(value=response, save=add_messages(inputs, response))


    