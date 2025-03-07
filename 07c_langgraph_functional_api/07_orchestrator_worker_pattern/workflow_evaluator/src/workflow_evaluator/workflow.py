import os
import json
import logging
from typing import TypedDict, Dict, Any, List

from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.func import entrypoint, task
from langchain_groq import ChatGroq

# Setup logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Load environment variables
load_dotenv(find_dotenv())

# Initialize LLM instances
# Here, orchestrator_llm is used for planning/execution prompts.
orchestrator_llm = ChatGroq(
    model="llama-3.3-70b-versatile", api_key=os.environ["GROQ_API_KEY"])
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21")

# Input state for the evaluation workflow


class InputState(TypedDict):
    prompt_to_evaluate: str
    gold_standard: str
    persona_runs: int


# Define the structure for an individual step in the workflow.
class RoutineStep(BaseModel):
    name: str
    goal: str
    instructions: str


# Define the overall plan structure.
class RoutinePlan(BaseModel):
    steps: List[RoutineStep]
    overall_goal: str
    estimated_completion_time: str


@task
def generate_workflow_plan(input_state: InputState) -> Dict[str, Any]:
    """
    Dynamically generate a detailed evaluation plan using the orchestrator LLM.
    The plan includes an overall goal, estimated completion time, and an array of steps.
    Each step must include:
      - name: Unique identifier (e.g., "simulate_personas", "aggregate_report")
      - goal: What the step is meant to achieve.
      - instructions: Detailed instructions.
    """
    plan_prompt = f"""
    Create a detailed evaluation plan for this prompt:

    PROMPT TO EVALUATE: {input_state['prompt_to_evaluate']}
    GOLD STANDARD: {input_state['gold_standard']}
    NUMBER OF RUNS: {input_state['persona_runs']}

    Return a JSON plan with:
    1. overall_goal: The main objective of the evaluation.
    2. estimated_completion_time: Estimated time to complete all steps.
    3. steps: An array of evaluation steps. Each step must include:
       - name: A unique identifier for the step.
       - goal: What this step aims to achieve.
       - instructions: Detailed instructions for executing the step.

    Return a JSON plan that exactly matches this structure:
    {{
        "overall_goal": "Brief description of the evaluation goal",
        "estimated_completion_time": "Estimated time in minutes",
        "steps": [
            {{
                "name": "step_identifier",
                "goal": "What this step aims to achieve",
                "instructions": "Detailed instructions for execution"
            }},
            // Additional steps...
        ]
    }}

    Requirements for each step:
    - name: A unique identifier (string)
    - goal: Clear objective (string)
    - instructions: Detailed execution instructions (string)

    Ensure all fields are present and properly formatted.
    """
    try:
        response = orchestrator_llm.with_structured_output(
            RoutinePlan).invoke(plan_prompt)
        plan = response  # plan is a RoutinePlan instance
        logging.info("Workflow plan generated successfully.")
        return plan.model_dump()  # Dump as dict for downstream tasks
    except Exception as e:
        logging.error(f"Error generating workflow plan: {e}")
        fallback_step = RoutineStep(
            name="basic_evaluation",
            goal="Perform a basic evaluation of the prompt.",
            instructions="Analyze the prompt and generate a simple report."
        )
        fallback_plan = RoutinePlan(
            steps=[fallback_step],
            overall_goal="Basic prompt evaluation",
            estimated_completion_time="5 minutes"
        )
        return fallback_plan.model_dump()


@task
def execute_single_iteration(
    step: Dict[str, Any],
    input_state: InputState,
    iteration: int,
    previous_results: Dict[str, Any] | None
) -> Dict[str, Any]:
    """
    Execute a single iteration of a routine step.
    """
    try:
        execution_prompt = f"""
        Execute iteration {iteration} of step:

        STEP NAME: {step['name']}
        GOAL: {step['goal']}
        INSTRUCTIONS: {step['instructions']}

        CONTEXT:
        PROMPT TO EVALUATE: {input_state['prompt_to_evaluate']}
        GOLD STANDARD: {input_state['gold_standard']}
        PREVIOUS RESULTS: {json.dumps(previous_results, indent=2)}

        Provide a detailed response that meets the stated goal.
        Include observations, analysis, and recommendations.
        """
        response = model.invoke(execution_prompt)
        return {
            "iteration": iteration,
            "output": response.content
        }
    except Exception as e:
        logging.error(f"Error in iteration {iteration} of step {step['name']}: {e}")
        return {
            "iteration": iteration,
            "error": str(e)
        }


@task
def execute_routine_step(
    step: Dict[str, Any],
    input_state: InputState,
    previous_results: Dict[str, Any] | None
) -> Dict[str, Any]:
    """
    Execute a routine step with a single iteration.
    """
    try:
        iteration_results = [
            execute_single_iteration(
                step, input_state, 1, previous_results).result()
        ]
        logging.info(f"Step '{step['name']}' completed.")
        return {
            "step_name": step["name"],
            "goal_achieved": step["goal"],
            "iterations": iteration_results
        }
    except Exception as e:
        logging.error(f"Error executing step {step['name']}: {e}")
        return {
            "step_name": step["name"],
            "error": str(e)
        }


@task
def synthesize_results(plan: Dict[str, Any], results: Dict[str, Any]) -> str:
    """
    Synthesize the final evaluation report from all step outputs.
    Format as a Markdown report with sections for:
    1. Executive Summary
    2. Detailed Findings (organized by step, including iteration outputs)
    3. Key Recommendations
    """
    synthesis_prompt = f"""
    Create a comprehensive evaluation report based on the following inputs:

    OVERALL GOAL: {plan['overall_goal']}
    ESTIMATED COMPLETION TIME: {plan['estimated_completion_time']}

    RESULTS FROM EACH STEP:
    {json.dumps(results, indent=2)}

    Format the report in Markdown with the following sections:
    1. Executive Summary (including if the overall goal was achieved)
    2. Detailed Findings (organized by step, with iteration details)
    3. Key Recommendations
    """
    try:
        response = model.invoke(synthesis_prompt)
        logging.info("Results synthesized into final report.")
        return response.content
    except Exception as e:
        logging.error(f"Error synthesizing results: {e}")
        return f"Error generating final report: {str(e)}"


@entrypoint()
def evaluate_prompt(input_state: InputState) -> Dict[str, Any]:
    """
    Parallel orchestrator workflow that:
      1. Generates a structured evaluation plan
      2. Executes all steps in parallel
      3. Synthesizes all step outputs into a final report
    """
    # Generate the workflow plan
    plan = generate_workflow_plan(input_state).result()

    print("PLAN", plan)

    # Execute all steps in parallel
    step_futures = [execute_routine_step(
        step, input_state, {}) for step in plan["steps"]]
    results = [future.result() for future in step_futures]

    # Convert results list to dictionary for synthesis
    results_dict = {result["step_name"]: result for result in results}

    # Synthesize the final report from all step results
    final_report = synthesize_results(plan, results_dict).result()

    # Save the final report
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    final_md_path = os.path.join(output_dir, "evaluation_report.md")
    with open(final_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(final_report)

    logging.info(f"Final report saved to {final_md_path}")

    return {
        "final_report": final_report,
        "report_path": final_md_path,
        "plan": plan,
        "step_results": results_dict
    }

