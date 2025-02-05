import os
import argparse
from typing import TypedDict, Dict, Any, List
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

# Setup logging for internal debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load environment variables securely (ensure your .env file is protected)
load_dotenv(find_dotenv())

# Initialize the LLM instances using your secure API key.
# 'model' is used for general tasks; 'judge_llm' is used for judge and research tasks.
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
judge_llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-thinking-exp-01-21")

# Define the input state structure.
# "prompt_to_evaluate" holds the system prompt instructions to evaluate.
# "gold_standard" provides the trusted expected outcome (a detailed, realistic expected response).
# "persona_runs" is the number of persona simulations (golden examples) to run.
class InputState(TypedDict):
    prompt_to_evaluate: str   # Detailed system prompt instructions to evaluate
    gold_standard: str        # Trusted expected outcome (gold standard) for evaluation
    persona_runs: int         # Number of persona simulations to run

###########################
# Task: Simulate Persona
###########################
@task
def simulate_persona(prompt_to_evaluate: str, gold_standard: str, persona_id: int) -> Dict[str, str]:
    """
    For a given system prompt, simulate a concise persona action.
    Uses the externally provided gold standard as the expected outcome and generates
    the actual outcome by using the sample input as a user query.
    
    Production enhancements:
      - Robust error handling with fallback values.
      - Clear separation between generating a sample input and generating the actual outcome.
    """
    try:
        # Generate a sample input that a typical user might ask.
        sample_input_prompt = (
            f"Provide a concise sample question that a user might ask based on the following system prompt instructions:\n\n"
            f"{prompt_to_evaluate}\n\n"
            f"Context: {gold_standard}"
        )
        sample_input_resp = model.invoke(sample_input_prompt)
        sample_input = sample_input_resp.content.strip() or "No sample input generated."
    except Exception as e:
        logging.error(f"Error generating sample input for persona {persona_id}: {e}")
        sample_input = "Error generating sample input."

    # Use the gold standard as the expected outcome.
    expected_output = gold_standard.strip()

    try:
        # Generate the actual outcome from the LLM using the sample input as the user query.
        actual_prompt = (
            f"Based on the following system prompt instructions:\n\n{prompt_to_evaluate}\n\n"
            f"Answer the user: {sample_input}"
        )
        actual_resp = model.invoke(actual_prompt)
        actual_output = actual_resp.content.strip() or "No actual outcome generated."
    except Exception as e:
        logging.error(f"Error generating actual outcome for persona {persona_id}: {e}")
        actual_output = "Error generating actual outcome."

    logging.info(f"Persona {persona_id} simulation complete.")
    return {
        "persona_id": str(persona_id),
        "sample_input": sample_input,
        "expected_output": expected_output,
        "actual_output": actual_output
    }

@task
def simulate_personas(prompt_to_evaluate: str, gold_standard: str, persona_runs: int) -> List[Dict[str, str]]:
    """
    Generate multiple persona simulations in parallel from the given system prompt,
    using the gold standard for expected outcomes.
    """
    return [simulate_persona(prompt_to_evaluate, gold_standard, i + 1).result() for i in range(persona_runs)]

###########################
# Task: Judge Evaluation
###########################
@task
def judge_prompt(simulations: List[Dict[str, str]]) -> str:
    """
    Review the persona simulation outputs (which include the gold standard as the expected outcome)
    and provide an overall evaluation of the system prompt instructions.
    Compares the ideal (gold standard) with the actual outcomes and includes actionable recommendations.
    """
    sim_details = ""
    for sim in simulations:
        sim_details += (
            f"**Persona {sim['persona_id']}**\n"
            f"- Input: {sim['sample_input']}\n"
            f"- Expected: {sim['expected_output']}\n"
            f"- Actual: {sim['actual_output']}\n\n"
        )
    
    judge_prompt_text = (
        f"You are an expert evaluator. Review the following persona simulation details derived from the system prompt instructions:\n\n"
        f"{sim_details}\n"
        "Provide an overall evaluation of the prompt instructions, discussing how well the actual outcomes align with the gold standard. "
        "Highlight strengths, weaknesses, and provide clear, actionable recommendations for improvement. "
        "Respond in a detailed, single paragraph."
    )
    response = judge_llm.invoke(judge_prompt_text)
    final_evaluation = response.content.strip()
    logging.info("Judge evaluation complete.")
    return final_evaluation

###########################
# Task: Research for Prompt Improvement
###########################
@task
def research_prompt_improvement(prompt_to_evaluate: str, judge_eval: str) -> str:
    """
    Conduct industry research using the system prompt instructions and the judge's evaluation as context,
    then provide supporting evidence and actionable recommendations to improve the prompt.
    """
    research_prompt = (
        f"Using the following system prompt instructions and the judge's evaluation, conduct industry research on best practices "
        f"for creating effective system prompts for AI agents. Provide supporting evidence and specific recommendations for improvement.\n\n"
        f"**System Prompt Instructions:**\n'{prompt_to_evaluate}'\n\n"
        f"**Judge Evaluation:**\n'{judge_eval}'\n\n"
        "Focus on clear, actionable improvements."
    )
    response = judge_llm.invoke(research_prompt)
    result = response.content.strip()
    logging.info("Industry research for prompt improvement complete.")
    return result

###########################
# Task: Aggregate Final Markdown Report
###########################
@task
def aggregate_final_report(prompt_instructions: str,
                           simulations: List[Dict[str, str]],
                           judge_eval: str,
                           research_eval: str) -> str:
    """
    Combine the system prompt instructions, persona simulation details, judge evaluation, 
    and industry research into a final comprehensive Markdown report.
    """
    report = f"# Final Evaluation Report for System Prompt Instructions\n\n"
    report += f"**System Prompt Instructions:**\n{prompt_instructions}\n\n"
    
    report += "## Persona Simulations\n"
    for sim in simulations:
        report += (
            f"### Persona {sim['persona_id']}\n"
            f"- **Input:** {sim['sample_input']}\n"
            f"- **Expected Outcome (Gold Standard):** {sim['expected_output']}\n"
            f"- **Actual Outcome:** {sim['actual_output']}\n\n"
        )
    
    report += "## Judge Evaluation\n"
    report += f"{judge_eval}\n\n"
    
    report += "## Industry Research & Recommendations\n"
    report += f"{research_eval}\n\n"
    
    return report

###########################
# Main Workflow
###########################
@entrypoint()
def evaluate_prompt(input_state: InputState) -> Dict[str, Any]:
    """
    Main workflow that:
      1. Simulates multiple persona tests using the system prompt instructions and an external gold standard.
      2. Runs a judge evaluation to provide an overall assessment.
      3. Conducts industry research (using the judge evaluation as context) for supporting recommendations.
      4. Aggregates all outputs into a professional Markdown report.
    """
    simulations = simulate_personas(input_state["prompt_to_evaluate"], input_state["gold_standard"], input_state["persona_runs"]).result()
    judge_eval = judge_prompt(simulations).result()
    research_eval = research_prompt_improvement(input_state["prompt_to_evaluate"], judge_eval).result()
    
    final_report = aggregate_final_report(input_state["prompt_to_evaluate"], simulations, judge_eval, research_eval).result()
    
    # Save the final Markdown document
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    final_md_path = os.path.join(output_dir, "final_evaluation_report.md")
    with open(final_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(final_report)
    
    logging.info(f"Final Markdown report saved to {final_md_path}")
    
    overall_output = {
        "final_markdown": final_report,
        "report_path": final_md_path,
    }
    return overall_output

