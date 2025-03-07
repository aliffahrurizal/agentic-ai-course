from langgraph.func import entrypoint, task

@task
def first_step(input_text: str) -> str:
    """First step in the chain that processes the input."""
    print(f"Processing first step with input: {input_text}")
    return f"First step processed: {input_text}"

@task
def second_step(processed_text: str) -> str:
    """Second step in the chain that further processes the input."""
    print(f"Processing second step with input: {processed_text}")
    return f"Second step processed: {processed_text}"

@entrypoint()
def main_workflow(input_text: str) -> dict:
    """The main workflow that processes text through multiple steps."""
    # Process through first step
    first_result = first_step(input_text).result()
    
    # Process through second step
    final_result = second_step(first_result).result()
    
    return {
        "input": input_text,
        "output": final_result
    }
    
main_workflow.name = "main_workflow"

# def run_workflow():
#     """Function to run the workflow with a sample input."""
#     sample_input = "Hello, LangGraph!"
#     result = main_workflow.invoke(sample_input)
#     # print(f"\nWorkflow Result: {result}")
#     return result 