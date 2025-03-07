from assistant_selector.workflow import run_workflow


def main():
    result = run_workflow.invoke(input={"question": "Implement React Agent Pattern in Python"})
    print("\n\n", "Result: ", "\n\n", result, "\n\n")


def stream():
    for event in run_workflow.stream(input={"question": "Share Agentic Design Patterns best suited in Sales Vertical"}):
        print("\n")
        print(event)
        print("\n")
