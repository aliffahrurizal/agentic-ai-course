from poemflow.workflow import run_workflow


def main():
    result = run_workflow.invoke(input={"topic": "Vertical AI Agents"})
    print("\n\n", "Generated Poem: ", "\n\n", result.get("poem"), "\n\n")


def stream():
    for event in run_workflow.stream(input={"topic": "AI Agent Design Patterns"}):
        print("\n")
        print(event)
        print("\n")
