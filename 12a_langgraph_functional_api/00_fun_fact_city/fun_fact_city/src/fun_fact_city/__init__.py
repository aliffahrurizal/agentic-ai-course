from fun_fact_city.workflow import run_workflow


def main():
    result = run_workflow.invoke(input="Pakistan")
    print("\n\n", "Generated fun fact: ", result, "\n\n")
    
def stream():
    for event in run_workflow.stream(input="Pakistan"):
        print(event)