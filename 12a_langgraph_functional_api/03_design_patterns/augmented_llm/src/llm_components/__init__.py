from llm_components.structured_output import get_structured_output
from llm_components.tool_usage import get_tools_output
from llm_components.memory import workflow, review_workflow_memories

def understand_tools():
    result = get_tools_output()
    print("\n\n", "Tool Call Output: ", "\n\n", result, "\n\n")


def understand_structured_output():
    result = get_structured_output()
    print("\n\n", "Structured Output: ", "\n\n", result.model_dump(), "\n\n")

def lt_memory_feed():
    # ✅ **Example Usage: Testing Bob-Agent’s Learning & Memory**
    config1 = {"configurable": {"thread_id": "1", "user_id": "user_123"}}
    input_message1 = {"role": "user", "content": "LangGraph and CrewAI are great Agentic Framrworks."}

    for chunk in workflow.stream([input_message1], config1, stream_mode="values"):
        chunk.pretty_print()
        
def lt_memory_review():
    return review_workflow_memories()
    