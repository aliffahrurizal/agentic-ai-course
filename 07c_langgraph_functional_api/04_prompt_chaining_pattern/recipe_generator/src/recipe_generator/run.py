from recipe_generator.workflow import recipe_generation_agent

ingredients = ("tomatoes, basil, mozzarella, olive oil, garlic")

def main_run():
    result = recipe_generation_agent.invoke(ingredients)
    print("\n\n", "Final Recipe: ", result, "\n\n")

def stream_run():
    for step in recipe_generation_agent.stream(ingredients):
        print(step)
        print("\n")