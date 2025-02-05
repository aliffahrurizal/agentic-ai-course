import os
from typing import TypedDict, List, Dict
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

@task
def extract_issues(customer_email: str) -> str:
    """
    First LLM call: Extract the main issues from the customer's email.
    """
    prompt = f"Extract the main issues and concerns from the following customer email:\n\n{customer_email}"
    msg = llm.invoke(prompt)
    return msg.content

@task
def generate_draft_response(issues: str) -> str:
    """
    Second LLM call: Draft a response addressing the extracted issues.
    """
    prompt = f"Draft a response email addressing the following customer issues: {issues}\n" \
             f"Ensure the response is clear, professional, and empathetic."
    msg = llm.invoke(prompt)
    return msg.content

def check_tone(response: str) -> str:
    """
    Gate function: Check if the draft response includes empathetic language.
    A simple check could look for words like 'sorry' or 'apologize'.
    """
    if "sorry" in response.lower() or "apologize" in response.lower():
        return "Pass"
    return "Fail"

@task
def improve_response_tone(response: str) -> str:
    """
    Third LLM call: Improve the tone of the response to be more empathetic if necessary.
    """
    prompt = f"The following response needs a warmer, more empathetic tone:\n\n{response}\n\n" \
             f"Rewrite it to better express understanding and concern for the customer's situation."
    msg = llm.invoke(prompt)
    return msg.content


@task
def polish_response(response: str) -> str:
    """
    Fourth LLM call: Polish the response for clarity and professionalism.
    """
    prompt = f"Polish and finalize the following customer support response for clarity and professionalism:\n\n{response}"
    msg = llm.invoke(prompt)
    return msg.content


@entrypoint()
def customer_support_response_workflow(customer_email: str):
    # Step 1: Extract key issues from the customer's email.
    issues = extract_issues(customer_email).result()

    # Step 2: Generate an initial draft response.
    draft_response = generate_draft_response(issues).result()

    # Step 3: Check if the draft has the right tone.
    if check_tone(draft_response) == "Pass":
        # If the tone is acceptable, finalize the response.
        return polish_response(draft_response).result()
    else:
        # If not, improve the tone first and then polish.
        improved_response = improve_response_tone(draft_response).result()
        return polish_response(improved_response).result()
