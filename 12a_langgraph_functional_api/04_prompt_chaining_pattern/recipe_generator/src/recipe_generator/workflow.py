import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.func import entrypoint, task

load_dotenv() 

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Task 1: Ingredient Analysis
@task
def analyze_ingredients(ingredients: str):
    """
    Sends the list of ingredients to the LLM using the Ingredient Analysis Prompt.
    The LLM returns analysis such as flavor profiles, common pairings, or hints at possible dishes.
    """
    response = llm.invoke(
        f"Ingredient Analysis Prompt: Analyze the following list of ingredients and provide detailed insights including flavor profiles, textures, and any interesting pairing ideas:\n\n{ingredients}"
    )
    print(f"Ingredient Analysis: {response.content}")

    return response.content

# Task 2: Cuisine Suggestion
@task
def suggest_cuisine(analysis: str):
    """
    Uses the ingredient analysis to prompt the LLM with the Cuisine Suggestion Prompt.
    The LLM returns a suggested cuisine that best matches the analyzed ingredients.
    """
    response = llm.invoke(
        f"Cuisine Suggestion Prompt: Based on the following ingredient analysis, suggest a cuisine style that would best complement these ingredients:\n\n{analysis}"
    )
    print(f"Suggested Cuisine: {response.content}")
    return response.content

# Task 3: Recipe Generation
@task
def generate_recipe(ingredients: str, cuisine: str):
    """
    Prompts the LLM with the Recipe Generation Prompt, incorporating both the original ingredients and the suggested cuisine,
    to generate a complete recipe including instructions and serving suggestions.
    """
    response = llm.invoke(
        f"Recipe Generation Prompt: Generate a detailed recipe that uses the following ingredients: {ingredients}. "
        f"The recipe should be inspired by {cuisine} cuisine. Please include a list of ingredients, step-by-step instructions, and any serving tips."

    )
    print(f"Generated Recipe: {response.content}")
    return response.content

@task
def save_recipe(recipe: str) -> str:
    """Save the recipe to a file in a correct directory to avoid path errors."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(output_dir, "recipe.md")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(recipe)
    
    print(f"Recipe is being saved in {output_dir} directory...")

    return f"recipe saved successfully at {file_path}"


# Entrypoint: Recipe Generation Agent Workflow
@entrypoint()
def recipe_generation_agent(ingredients: str):
    # Step 1: Analyze the ingredients
    analysis = analyze_ingredients(ingredients).result()
    
    # Step 2: Suggest a cuisine based on the analysis
    cuisine = suggest_cuisine(analysis).result()
    
    # Step 3: Generate a recipe using the original ingredients and the suggested cuisine
    recipe = generate_recipe(ingredients, cuisine).result()

    save_status = save_recipe(recipe).result()
    
    final_recipe = {
        "ingredient_analysis":analysis,
        "suggested_cuisine":cuisine,
        "generated_recipe":recipe,
        "save_status":save_status
    }
    
    return final_recipe


# available_ingredients = "tomatoes, basil, mozzarella, olive oil, garlic"
# for step in recipe_generation_agent.stream(available_ingredients, stream_mode="updates"):
#     print(step)
#     print("\n")
