from recipe_generator.workflow import recipe_generation_agent

def main():
    result = recipe_generation_agent.invoke(input="tomatoes, basil, mozzarella, olive oil, garlic")
    print("\n\n", "Final Recipe: ", result, "\n\n")

def stream():
    for event in recipe_generation_agent.stream(input="tomatoes, basil, mozzarella, olive oil, garlic"):
        print(event)