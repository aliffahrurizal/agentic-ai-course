import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")


# 1. Define the structured output schema for the plan structure.
class PlanSection(BaseModel):
    title: str = Field(
        description="Title of the plan section (e.g., 'Workout Plan', 'Nutrition Plan')."
    )
    description: str = Field(
        default="No description provided.",
        description="Brief description outlining what this section should cover."
    )

class PersonalizedPlan(BaseModel):
    sections: List[PlanSection] = Field(
        description="A list of sections for the personalized health and fitness plan."
    )

# Augment the LLM with the schema for structured output.
plan_generator = llm.with_structured_output(PersonalizedPlan)

# 2. Orchestrator Task: Generate a tailored plan structure based on user profile.
@task
def orchestrator(user_profile: str) -> List[PlanSection]:
    """
    Uses an LLM to generate a plan structure from the user's profile and goals.
    """
    messages = [
        SystemMessage(content="You are a top-tier health and fitness expert."),
        HumanMessage(content=(
            f"User Profile and Goals:\n{user_profile}\n\n"
            "Generate a JSON output with a key 'sections' that is a list of objects. "
            "Each object must have a 'title' and a 'description'. "
            "Please create exactly three sections with the following criteria:\n\n"
            "1. **Workout Plan**: The description should focus exclusively on exercise routines, training schedules, and progression strategies. Do not include nutrition or lifestyle advice.\n\n"
            "2. **Nutrition Plan**: The description should focus exclusively on meal planning, calorie and macronutrient calculations, and food choices. Do not include exercise or lifestyle advice.\n\n"
            "3. **Lifestyle Tips**: The description should focus exclusively on daily habits, recovery strategies, sleep, and stress management. Do not include exercise or nutrition details.\n\n"
            "Ensure that each section’s description is unique and does not overlap with the others."
        ))
    ]
    plan = plan_generator.invoke(messages)
    return plan.sections



# 3. Worker Task: Generate detailed content for a specific plan section.
@task
def worker_generate_section(section: PlanSection, user_profile: str) -> str:
    """
    Generates content for a given section using the section details and the user profile.
    """
    print(f"\n\n Section Plan for {section}")

    # Customize instructions based on section title.
    instructions = ""
    if section.title.lower() == "workout plan":
        instructions = "Focus exclusively on detailed exercise routines, training schedules, and progression strategies. Do not include any nutrition or lifestyle advice."
    elif section.title.lower() == "nutrition plan":
        instructions = "Focus exclusively on meal planning, calorie calculations, macronutrient breakdown, and food choices. Do not include any exercise or lifestyle advice."
    elif section.title.lower() == "lifestyle tips":
        instructions = "Focus exclusively on daily habits, recovery strategies, sleep, stress management, and additional lifestyle advice. Do not include any exercise or nutrition details."


    messages = [
        SystemMessage(content="You are a knowledgeable health and fitness advisor."),
        HumanMessage(content=(
            f"User Profile and Goals:\n{user_profile}\n\n"
            f"Generate detailed content for the section titled '{section.title}'.\n"
            f"Section Description: {section.description}\n\n"
            f"Instructions: {instructions}\n\n"
            "Make sure your output is unique, actionable, and does not repeat common advice from other sections."
        ))
    ]
    result = llm.invoke(messages)
    return result.content


# 4. Synthesizer Task: Combine all sections into a final, cohesive plan.
@task
def synthesizer(sections_content: List[str]) -> str:
    """
    Aggregates the content from all sections into a single comprehensive health and fitness plan.
    """
    final_plan = "\n\n===\n\n".join(sections_content)
    return final_plan

@task
def write_to_file(response: str):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    response_file_path = os.path.join(output_dir, "orchestrator-worker.txt")
    with open(response_file_path, "w", encoding="utf-8") as response_file:
        response_file.write(response)

# 5. Orchestrator-Workers Workflow Entry Point.
@entrypoint()
def personalized_fitness_plan(user_profile: str) -> str:
    # Step 1: Generate the plan structure.
    sections = orchestrator(user_profile).result()
    
    # Step 2: In parallel, generate content for each section.
    section_futures = [worker_generate_section(section, user_profile) for section in sections]
    sections_content = [future.result() for future in section_futures]
    
    # Step 3: Synthesize the final plan.
    final_plan = synthesizer(sections_content).result()
    
    # Step 4: Save the final plan to a text file.
    write_to_file(final_plan)
    return final_plan